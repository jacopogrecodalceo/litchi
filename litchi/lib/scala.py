import re
import os
import abjad
import math
from dataclasses import dataclass, field
from fractions import Fraction
from decimal import Decimal

from litchi.lib.const import INTERVAL_NAMEs, SCALA

from litchi.lib.scala_exporter import export_scala

"""
AT THE MOMENT I AM NOT SURE IT DOES SUPPORT TRITAVES or NOT OCTAVED SYSTEMs
"""

# Constants
EDO12_LOG2 = Decimal(1200 / math.log10(2))
CHROMATIC_PITCH_CLASS_NAMEs = {  
	'c': [], 'cs': [], 'd': [], 'ef': [], 'e': [], 'f': [],
	'fs': [], 'g': [], 'af': [], 'a': [], 'bf': [], 'b': []
}

CHROMATIC_PITCH_CLASS_NUMs = {num: [] for num in range(13)}

@dataclass
class Interval:
    value: float
    denominator_limit: int

    name: str | None = field(init=False, default=None)
    cents: str | None = field(init=False, default=None)

    tolerance: int = 6

    def process(self):
        log_value = Decimal(math.log10(float(self.value)))
        self.abs_cents = log_value * EDO12_LOG2
        self.semitones = self.abs_cents / 100
        self.assign_interval_name()

    def assign_interval_name(self):
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

    def __repr__(self):
        attributes = {
            "value": self.value,
            "denominator_limit": self.denominator_limit,
            "name": self.name,
            "cents": self.cents,
            "tolerance": self.tolerance,
            "abs_cents": getattr(self, 'abs_cents', None),
            "semitones": getattr(self, 'semitones', None),
            "ratio": getattr(self, 'ratio', None),
            "interval_name_ratio": getattr(self, 'interval_name_ratio', None)
        }

        attr_strings = [f"    {name:<20} = {value}" for name, value in attributes.items()]
        attr_strings_str = ",\n".join(attr_strings)

        return f"Interval(\n{attr_strings_str}\n)"

@dataclass
class Scala:
	origin_value: str | int | float
	quarter_tones: bool = False

	name: str | None = field(init=False, default=None)
	values: list[float] = field(default_factory=list)
	chromatic_intervals: dict = field(default_factory=lambda: {num: [] for num in range(13)})
	#chromatic_intervals: dict = field(default_factory=lambda: CHROMATIC_PITCH_CLASS_NAMES.copy())


	denominator_limit: int = 1e5 		# Closest Fraction to self with denominator at most max_denominator.
	tolerance: int = 6					# this is the exponent for 1e^...

	def __post_init__(self):
		if isinstance(self.origin_value, str) and self.origin_value[0].isalpha():
			#self.origin_numbered_pitch = abjad.NamedPitch(self.origin_value)
			self.origin_numbered_pitch = abjad.NumberedPitch(self.origin_value)
			self.origin_decimal_value = self.origin_numbered_pitch.hertz
		elif isinstance(self.origin_value, (int, float)):
			self.origin_numbered_pitch = abjad.NumberedPitch.from_hertz(self.origin_value)			
			self.origin_decimal_value = self.origin_value


	def edo(self, n: int):
		"""Generates an equal division of the octave (EDO) scale."""
		self.values = [Decimal(2) ** (Decimal(step) / Decimal(n)) for step in range(n)]
		self.name = f'edo{n}'
		print(f'Calculating edo{n}..')
		return self.values
	
	def edolin(self, n: int):
		"""Generates a linear division of the octave (EDO) scale."""
		self.values = [Decimal(1) + (Decimal(step) / Decimal(n)) for step in range(n)]
		self.name = f'harm{n}-edolin'
		print(f'Calculating harmonic{n}..')
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
		print(f"Loading scala: {scala_name}")
		self.name = scala_name
		self.values = [Decimal(x) if not '/' in x else float(Fraction(x)) for x in SCALA[scala_name]['tuning_values'].strip().split(',')]
		self.values.insert(0, 1)
		if self.values[-1] == 2:
			self.values.pop(-1)

	@staticmethod
	def ajust_unison_values(interval):
		"""
		This happens for exemple when in edo31 there's a seventh that is more an octave:
		e.g.
			5 septatones or septatonic diminished octave, 32768/16807
			with 1e05 limited denominator | 1e2 tolerance
			21582
			11035 1.96
			11.61 st | 1161.29 abs cents	
		this function simply check this.	
		"""
		interval.value /= 2
		return interval



	def make(self):
		"""Computes pitch class values from the scale values."""
		assert self.values[0] == 1, "WARNING: First value is not 1."
		for value in self.values:
			interval = Interval(value, denominator_limit=self.denominator_limit)
			interval.process()

			decimal_part, integer_part = math.modf(float(interval.semitones))
			pitch = self.origin_numbered_pitch.number + int(integer_part)
			cents_from_written_pitch = round(decimal_part * 100)

			if abs(cents_from_written_pitch) > 50:
				pitch += 1 if cents_from_written_pitch > 0 else -1
				cents_from_written_pitch = (
					cents_from_written_pitch - 100 if cents_from_written_pitch > 0
					else cents_from_written_pitch + 100
				)

			if self.quarter_tones and abs(cents_from_written_pitch) > 25:
				pitch += .5 if cents_from_written_pitch > 0 else -.5
				cents_from_written_pitch = (
					cents_from_written_pitch - 50 if cents_from_written_pitch > 0
					else cents_from_written_pitch + 50
				)

			if cents_from_written_pitch != 0:
				interval.cents = f"{cents_from_written_pitch:+}¢"
			else:
				interval.cents = None

			interval.pitch_class_name = abjad.NamedPitch(int(pitch)).pitch_class.name
			interval.pitch_class_num = abjad.NamedPitch(int(pitch)).pitch_class.number
			if pitch > 11.5:
				interval = self.ajust_unison_values(interval)
			self.chromatic_intervals[interval.pitch_class_num].append(interval)

		assert self.values

	@staticmethod
	def calculate_harmonics(freq, n=32):
		"""
		even if it depents from sound
		"""
		return [freq * i for i in range(n)]

	@staticmethod
	def find_nearest_harmonics(harmonics1, harmonics2):
		"""
		Optimized function to find the nearest harmonic between two lists of harmonics.

		Parameters:
			harmonics1 (list): First list of harmonic frequencies.
			harmonics2 (list): Second list of harmonic frequencies.

		Returns:
			tuple: A tuple containing:
				- The nearest harmonic from harmonics1.
				- The nearest harmonic from harmonics2.
				- The absolute difference between them.
		"""
		# Sort both lists
		harmonics1.sort()
		harmonics2.sort()

		min_diff = float('inf')
		nearest_pair = (None, None)

		# Initialize pointers for both lists
		i, j = 1, 1

		# Traverse both lists using two pointers
		while i < len(harmonics1) and j < len(harmonics2):
			diff = abs(Decimal(harmonics1[i]) - harmonics2[j])
			if diff < min_diff:
				min_diff = diff
				nearest_pair = (i, harmonics1[i], harmonics2[j])

			# Move the pointer with the smaller value
			if harmonics1[i] < harmonics2[j]:
				i += 1
			else:
				j += 1

		return nearest_pair, min_diff

	def get_interval(self, string: str, transpose=0, print_modulo=True):

		def split_string_from_number(string):
			"""
			This will get a string in a lilypond format, but the last number will always be
			the chosen interval in the temperament.
			e.g.
			a'40 - it means a', duration 1/4, first a in scala
			"""
			# Use regex to find the first occurrence of a number
			match = re.search(r'(\d+)', string)
			if match:
				# Split the text at the position of the first number
				position = match.start()
				return [string[:position], int(string[position:])]
			else:
				# If no number is found, return the original text as a single element
				return [string, 0]

		lilypond_pitch_string, selected_interval_number = split_string_from_number(string)
		selected_pitch = abjad.NumberedPitch(lilypond_pitch_string).transpose(transpose)
		
		length_interval_numbers = len(self.chromatic_intervals[selected_pitch.pitch_class.number])
		selected_inverval = self.chromatic_intervals[selected_pitch.pitch_class.number][selected_interval_number%length_interval_numbers]

		if selected_interval_number > length_interval_numbers and print_modulo:
			print('NO VALUE, MODULO ENABLED!')

		selected_inverval.pitch = selected_pitch
		selected_inverval.freq = Decimal(self.origin_decimal_value) * Decimal(selected_inverval.value)
		
		""" print(
			choosen_interval.pitch,
			self.find_nearest_harmonics(
			self.calculate_harmonics(self.origin_value),
			self.calculate_harmonics(choosen_interval.freq)
			)
		) """

		octave_diff = selected_pitch.octave.number - self.origin_numbered_pitch.octave.number
		
		factor = Decimal(2) ** Decimal(octave_diff)
		selected_inverval.freq *= factor


		difference = abs(Decimal(selected_pitch.hertz) - selected_inverval.freq)
		threshold = min(selected_inverval.freq, selected_pitch.hertz)

		if difference >= threshold:
			print(f"Warning: Frequency difference exceeds threshold:")
			print(f"Difference: {difference}")
			print(f"Threshold: {threshold}")
			print(f"{selected_inverval.freq=}")
			print(f"{selected_pitch.hertz=}")
			print(f"Selected interval: {selected_inverval}")
			response = input("Continue anyway? (y/n): ").lower().strip()
			if response != 'y':
				print("Aborting execution")
				exit(1)

		return selected_inverval

	def __repr__(self):
		# Define the attributes to include in the representation
		attributes = {
			"name": self.name,
			"origin_value": self.origin_value,
			"origin_numbered_pitch": self.origin_numbered_pitch.name,
			"denominator_limit": self.denominator_limit,
			"tolerance": self.tolerance,
		}

		# Format the attributes into a string
		attr_strings = [f"    {name:<20} = {value}" for name, value in attributes.items()]
		attr_strings_str = ",\n".join(attr_strings)

		return f"Scala(\n{attr_strings_str}\n)"

	def export(self, output_dir: str):
		export_scala(self, output_dir)


if __name__ == "__main__":
	origin = 440
	scala = Scala(origin)
	scala.evoke('edo31')
	scala.make()
	scala.export('/Users/j/Downloads/scala-3.pdf')
	imagined_melody = ["a,0", "a,1", "a,2","c'", "e'"]

	for p in imagined_melody:
		interval = scala.get_interval(p)
		print(interval.freq)
		print(interval.name)
		print(interval.cents)
		print('-'*32)
	