import re
import abjad
from fractions import Fraction

import litchi.lib.const as const
from litchi.lib.engraving import *
from litchi.lib.utils import *
from litchi.lib.utils_abjad import *

preamble = r"""
#(set-global-staff-size 15)

\paper {
	print-page-number = ##f
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
"""

def process_notes(notes, origin_pitch_class, data):
	result = []
	for note in notes:
		interval = abs(abjad.NamedIntervalClass.from_pitch_carriers(origin_pitch_class, abjad.NamedPitch(note).pitch_class))
		result.append(f"{note}, as {interval.name} - with {len(data[note])} ratio")
	return result

def find_notes_with_most_partials(data, origin_pitch_class):
	max_keys = [key for key in data if len(data[key]) == max(len(data[k]) for k in data)]
	result = process_notes(max_keys, origin_pitch_class, data)
	return result

def find_notes_with_least_partials(data, origin_pitch_class):
	min_keys = [key for key in data if len(data[key]) == min(len(data[k]) for k in data)]
	result = process_notes(min_keys, origin_pitch_class, data)
	return result


def analyse_chromatic_dict(origin, data):
	insights = {}

	origin_pitch_class = abjad.NamedPitch.from_hertz(origin).pitch_class.name
	insights["origin"] = f"{origin}, as {origin_pitch_class}"	

	insights["Partial with MOST different elements"] = find_notes_with_most_partials(data, origin_pitch_class)
	insights["Partial with LEAST different elements"] = find_notes_with_least_partials(data, origin_pitch_class)

	return insights



def calc_harmonic_series(limit=64):
	j = 1
	harmonic_series = []
	for i in range(1, limit):
		while j < i / 2:
			j *= 2
		ratio = Fraction(i, j).limit_denominator()
		harmonic_series.append(ratio)
	
	sorted_harmonic_series = sorted(set(harmonic_series))[:-1]
	return sorted_harmonic_series

def get_info(origin, harmonic_series, chromatic_dict):

	blocks = []

	insights = analyse_chromatic_dict(origin, chromatic_dict)
	for key, value in insights.items():
		#print(f"{key}: {value}")
		blocks.append(abjad.Markup(rf'\markup "{key}: {value}"'))
	
	for each in harmonic_series:
		blocks.append(abjad.Markup(rf'\markup "{each}={float(each)}"'))

	blocks.append('\pageBreak')
	origin_pitch_class = abjad.NamedPitch.from_hertz(origin).pitch_class
	origin_pitch_class = remove_quarter_tones(origin_pitch_class)
	index = 0
	for note, partials in iterate_from_key(origin_pitch_class.name, chromatic_dict):
		#print('-'*128)
		#print(note)

		pitch = abjad.NamedPitch(note).transpose(12)
		staff = abjad.Staff()
		note = abjad.Note(pitch, (1, 4))
		markups = []
		for partial in partials:
			attachs = {}
			#print('.'*32)
			# Get all the names defined in the class
			names = dir(partial)

			for name in names:
				if not name.startswith('__') and name != 'ratio':  # Skip special methods
					attr = getattr(partial, name)  # Get the attribute or method
					attributes = f"{name:<20}: {attr:<20}"
					#print(attributes)

					if name == 'string':
						attachs['ratio'] = rf'\bold "{attr}"'

					if name == 'freq':
						reference = pitch.hertz
						cent_diff = round(freq2cent(attr, reference), 2)
						while abs(cent_diff) > 100:
							attr *= 2
							cent_diff = round(freq2cent(attr, reference), 2)
						#print(cent_diff)
						string = cent_diff if cent_diff < 0 else f'+{cent_diff}'
						attachs['cent'] = rf'"{string}¢"'

					if name == 'interval_name':
						attachs['name'] = rf'\italic "{attr}"'

					if name == 'position':
						string = f'{ordinal_suffix(attr - 1)} partial' if attr != 1 else 'fundamental'
						attachs['pos'] = rf'"{string}  // {ordinal_suffix(attr)} harmonic"'

			markups.append(attachs)
			staff.append(note)

		sorted_markups = sorted(
			markups,
			key=lambda x: int(re.search(r'\d+', x['pos']).group())
		)
		
		text = [r"\line {" + '***' + r"}"]
		for attachs in sorted_markups:
			order = ['name', 'pos', 'ratio', 'cent']
			order_list = [attachs[k] for k in order] + ['***']
			for e in order_list:
				text.append(r"\line {" + e + r"}")

		#markup = abjad.Markup(r"\markup \override #'(baseline-skip . 4) \column {" + '\n'.join(text) + r"}")
		score = abjad.Score([staff], simultaneous=False)

		#print('-'*128)
		

		score_inside = abjad.Block(r"score", items=[score])
		line = abjad.Block(r"line", items=[score_inside])
		interval_line = abjad.Block(r"line", items=[rf'\huge \bold "{abjad.NamedInterval(index).name}"']) 
		override = abjad.Block(r"override #'(baseline-skip . 3.5) \center-column", items=[interval_line] + [line] + text)
		fill_line = abjad.Block(r"markup \fill-line", items=[override])
		blocks.append(fill_line)
		blocks.append('\pageBreak')
		
		index += 1

	""" blocks.insert(0, preamble)
	blocks.insert(0, make_preamble(info))
	lilypond_file = abjad.LilyPondFile(blocks)
	abjad.persist.as_pdf(lilypond_file, path.build_ji) """

def calc_chromatic_partials(origin, limit=64):

	harmonic_series = calc_harmonic_series(limit=limit)

	chromatic_dict = {
		'c': [],
		'cs': [],
		'd': [],
		'ef': [],
		'e': [],
		'f': [],
		'fs': [],
		'g': [],
		'af': [],
		'a': [],
		'bf': [],
		'b': []
	}

	for partial_ratio in harmonic_series:
		
		partial_freq = origin * partial_ratio
		partial_freq = adjust_to_reference_octave(partial_freq)

		partial_pitch_class = abjad.NamedPitch.from_hertz(partial_freq).pitch_class
		partial_pitch_class = remove_quarter_tones(partial_pitch_class)

		partial_name = partial_pitch_class.name
		
		if partial_name in chromatic_dict:
			partial = const.Partial()
			partial.freq = float(partial_freq)
			partial.ratio = partial_ratio
			partial.string = f"{partial_ratio.numerator}/{partial_ratio.denominator}"
			partial.pitch_name = partial_name
			partial.position = partial_ratio.numerator

			bpm = partial.freq * 60
			while bpm > 150:
				bpm /= 2
			partial.bpm = bpm

			for interval_name, values in const.INTERVAL_NAMEs.items():
				if values.get("ratio") == partial.string:
					partial.interval_name = interval_name
					break
				else:
					partial.interval_name = 'unknown?'

			assert hasattr(partial, 'interval_name'), f'No interval name for {partial.ratio}'
			chromatic_dict[partial_name].append(partial)
		else:
			raise ValueError(f"Invalid pitch class name: {partial_name}.")

	assert len(chromatic_dict.keys()) == 12, "It seems that chromatic dictonary is more than 12."
	for key, value in chromatic_dict.items():
		assert value is not None, f"Value for key {key} is None."

	get_info(origin, harmonic_series, chromatic_dict)

	return chromatic_dict

if __name__ == "__main__":
	calc_chromatic_partials(31.5, limit=64)
