import re
import abjad
import math
from dataclasses import dataclass, field
from fractions import Fraction
from decimal import Decimal

from litchi.lib.const import INTERVAL_NAMEs, SCALA

"""
AT THE MOMENT I AM NOT SURE IT DOES SUPPORT TRITAVES or NOT OCTAVED SYSTEMs
"""

# Constants
LOG2_EDO12 = Decimal(1200) / Decimal(math.log10(2))  # 1200 / log10(2)
CHROMATIC_PITCH_CLASS_NAMES = {  
	'c': [], 'cs': [], 'd': [], 'ef': [], 'e': [], 'f': [],
	'fs': [], 'g': [], 'af': [], 'a': [], 'bf': [], 'b': []
}

@dataclass
class Interval:
	value: float
	denominator_limit: int
	
	name: str | None = field(init=False, default=None)
	cents: str | None = field(init=False, default=None)

	tolerance: int = 6

	def process(self):
		log_value = Decimal(math.log10(float(self.value)))
		self.abs_cents = log_value * LOG2_EDO12
		self.semitones = self.abs_cents / 100
		self.lookup_name()

	def lookup_name(self):
		self.ratio = Fraction(float(self.value)).limit_denominator(int(self.denominator_limit))

		for name, v in INTERVAL_NAMEs.items():
			if str(v['ratio']) == (str(self.ratio) if self.ratio != 1 else '1/1'):
				self.name = name
				self.interval_name_ratio = str(v['ratio'])
				return

		while not self.name and self.tolerance > 1:
			tolerance_value = Decimal(1) / (Decimal(10) ** self.tolerance)

			for name, v in INTERVAL_NAMEs.items():
				if abs(Fraction(v['ratio']) - self.ratio) < tolerance_value:
					self.name = name
					self.interval_name_ratio = str(v['ratio'])
					return

			self.tolerance -= 1

@dataclass
class Scala:
	origin_value: str | int | float
	quarter_tones: bool = False

	name: str | None = field(init=False, default=None)
	values: list[float] = field(default_factory=list)
	chromatic_intervals: dict = field(default_factory=lambda: CHROMATIC_PITCH_CLASS_NAMES.copy())

	denominator_limit: int = 1e5  # Closest Fraction to self with denominator at most max_denominator.
	tolerance: int = 6 # this is the exponent for 1e^...

	def __post_init__(self):
		if isinstance(self.origin_value, str) and self.origin_value[0].isalpha():
			self.origin_named_pitch = abjad.NamedPitch(self.value)
			self.origin_decimal_value = self.origin_named_pitch.hertz
		elif isinstance(self.origin_value, (int, float)):
			self.origin_named_pitch = abjad.NamedPitch.from_hertz(self.origin_value)
			self.origin_decimal_value = self.origin_value


	def edo(self, n: int):
		"""Generates an equal division of the octave (EDO) scale."""
		self.values = [Decimal(2) ** (Decimal(step) / Decimal(n)) for step in range(n)]
		self.name = f'edo{n}'
		return self.values
	
	def evoke(self, scala_name: str):
		"""
		Structure of a .scl File:
		Description Line: The first line is a description of the scale, often the name of the scale.

		Number of Notes: The second line specifies the number of notes in the scale.

		Note Definitions: The subsequent lines define the intervals for each note in the scale. These can be specified as:

		Ratios: Fractions like 5/4 (just intonation).

		Cents: Decimal values like 386.3137 (equal temperament or microtonal scales).

		Frequency: Direct frequency values (less common).
		"""
		self.name = scala_name
		self.values = [Decimal(x) if not '/' in x else float(Fraction(x)) for x in SCALA[scala_name]['tuning_values'].strip().split(',')]
		self.values.insert(0, 1)
		if self.values[-1] == 2:
			self.values.pop(-1)

	def make(self):
		"""Computes pitch class values from the scale values."""
		assert self.values[0] == 1, "WARNING: First value is not 1."
		for value in self.values:
			interval = Interval(value, denominator_limit=self.denominator_limit)
			interval.process()

			decimal_part, integer_part = math.modf(float(interval.semitones))
			pitch = self.origin_named_pitch.number + int(integer_part)
			cents_from_written_pitch = round(decimal_part * 100)

			if abs(cents_from_written_pitch) > 50:
				pitch += 1 if cents_from_written_pitch > 0 else -1
				cents_from_written_pitch = (
					cents_from_written_pitch - 100 if cents_from_written_pitch > 0
					else cents_from_written_pitch + 100
				)

			if self.quarter_tones and abs(cents_from_written_pitch) > 25:
				pitch += 0.5 if cents_from_written_pitch > 0 else -0.5
				cents_from_written_pitch = (
					cents_from_written_pitch - 50 if cents_from_written_pitch > 0
					else cents_from_written_pitch + 50
				)
				
			interval.cents = f"{cents_from_written_pitch:+}¢"
			interval.pitch_class_name = abjad.NamedPitch(int(pitch)).pitch_class.name
			self.chromatic_intervals[interval.pitch_class_name].append(interval)
		
		assert self.values

	def get_interval(self, string: str):

		def split_string_from_number(string):
			# Use regex to find the first occurrence of a number
			match = re.search(r'(\d+)', string)
			if match:
				# Split the text at the position of the first number
				position = match.start()
				return [string[:position], int(string[position:])]
			else:
				# If no number is found, return the original text as a single element
				return [string, 0]

		lilypond_pitch_string, choosen_value = split_string_from_number(string)

		choosen_pitch = abjad.NamedPitch(lilypond_pitch_string)
		choosen_interval = self.chromatic_intervals[choosen_pitch.pitch_class.name][choosen_value]

		choosen_interval.frequency = Decimal(self.origin_decimal_value) * Decimal(choosen_interval.value)

		choosen_pitch_octave = choosen_pitch.octave.number - self.origin_named_pitch.octave.number
		if choosen_pitch.pitch_class < self.origin_named_pitch.pitch_class:
			choosen_pitch_octave = choosen_pitch_octave - 1 # No shift
		else:
			choosen_pitch_octave = choosen_pitch_octave  # Shift for A-based origin

		factor = 2 ** choosen_pitch_octave
		choosen_interval.frequency *= Decimal(factor)

		return choosen_interval

	def __repr__(self):
		# Define the attributes to include in the representation
		attributes = {
			"name": self.name,
			"origin_value": self.origin_value,
			"origin_named_pitch": self.origin_named_pitch.name,
			"denominator_limit": self.denominator_limit,
			"tolerance": self.tolerance,
		}

		# Format the attributes into a string
		attr_strings = [f"    {name:<20} = {value}" for name, value in attributes.items()]
		attr_strings_str = ",\n".join(attr_strings)

		return f"Scala(\n{attr_strings_str}\n)"

	def export(self, output):

		preamble = r"""

\paper {
	#(set-global-staff-size 15)
	print-page-number = ##f
	#(set-paper-size "a4landscape")
}

\layout {
	\context {
		\Score
		\override BarLine.stencil = ##f
		%\override Clef.stencil = ##f
		\override SpacingSpanner.strict-spacing = ##t
		\override SystemStartBar.stencil = ##f
		\override Stem.stencil = ##f
		\override TextScript.staff-padding = 5
		\override TimeSignature.transparent = ##t
	}
}

\header {
	tagline = "jacqouemin"
}
"""

		key_to_start = self.origin_named_pitch.pitch_class.name

		# Find the index of the key to start from
		keys = list(self.chromatic_intervals.keys())
		start_index = keys.index(key_to_start)

		# Shift the dictionary starting from the key
		shifted_chromatic_intervals = {key: self.chromatic_intervals[key] for key in keys[start_index:] + keys[:start_index]}

		blocks = []

		# TITLE
		markup_string = rf"""
		\markup {{
			\column {{
				\vspace #5  % Adds vertical space
				\fill-line {{ \fontsize #15 "{self.name}" }}
				\vspace #2  % Adds vertical space
				\fill-line {{ \fontsize #9 "***" }}
				\fill-line {{ \fontsize #9 "origin: {self.origin_value}, {self.origin_named_pitch.name}" }}
				\vspace #.5  % Adds vertical space
				\fill-line {{ \italic "jacqouemin greco d'alceo" }}
			}}
		}}
		"""

		blocks.append(markup_string)
		blocks.append('\pageBreak')

		# FIRST PAGE
		for note, intervals in shifted_chromatic_intervals.items():
			blocks.append(abjad.Markup(rf'\markup "{note}"'))
			values = [f'{i}, {interval.value:.3f}, {interval.name}' for i, interval in enumerate(intervals)]
			for value in values:
				blocks.append(abjad.Markup(rf'\markup "\t\t\t{value}"'))
		
		blocks.append('\pageBreak')

		index = 0
		for note_name, intervals in shifted_chromatic_intervals.items():

			# Adjust note for view in staff
			pitch = abjad.NamedPitch(note_name).transpose(12)

			staff = abjad.Staff()
			note = abjad.Note(pitch, (1, 4))
			lines = []
			for interval in intervals:
				"""
				abs_cents : 270.9677419354839066588489396
				cents : -29¢
				denominator_limit : 1000.0
				name : Pythagorean double diminished fourth
				pitch_class_name : c
				ratio : 987/844
				semitones : 2.709677419354839066588489396
				tolerance : 3
				value : 1.169430765597687
				"""

				lines.append('***')
				lines.append(f'\italic "{interval.name}, {interval.interval_name_ratio}"')
				f_denominator_limit = f"{interval.denominator_limit:.0e}".replace("+", "").replace(".0", "")
				lines.append(f'with {f_denominator_limit} limited denominator | 1e{interval.tolerance} tolerance')
				if interval.ratio != 1:
					lines.append(rf'\italic \box {{ \fraction {interval.ratio.numerator} {interval.ratio.denominator} "{interval.value:.2f}"}}')

				lines.append(f'{interval.semitones:.2f} st | {interval.abs_cents:.2f} abs cents')
				lines.append(f'{interval.cents}')

				staff.append(note)

			text = []
			for line in lines:
				text.append(r"\line {" + line + r"}")

			score = abjad.Score([staff], simultaneous=False)			

			score_inside = abjad.Block(r"score", items=[score])
			line = abjad.Block(r"line", items=[score_inside])
			interval_line = abjad.Block(r"line", items=[rf'\huge \bold "{abjad.NamedInterval(index).name}"']) 
			override = abjad.Block(r"override #'(baseline-skip . 3.5) \center-column", items=[interval_line] + [line] + text)
			fill_line = abjad.Block(r"markup \fill-line", items=[override])
			blocks.append(fill_line)
			blocks.append('\pageBreak')
			
			index += 1

		blocks.insert(0, preamble)
		lilypond_file = abjad.LilyPondFile(blocks)
		abjad.persist.as_pdf(lilypond_file, output)


if __name__ == "__main__":
	origin = 440
	scala = Scala(origin)
	scala.evoke('edo31hex')
	scala.make()
	scala.export('/Users/j/Downloads/scala.pdf')
	imagined_melody = ["a,", "c'", "e'"]

	for p in imagined_melody:
		interval = scala.get_interval(p)
		print(interval.frequency)
		print(interval.name)
		print(interval.cents)
		print('-'*32)
	
	for i in range(24):
		print(abjad.NamedPitchClass(i/2).name)
