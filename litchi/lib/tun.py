import abjad
from fractions import Fraction

from litchi.lib import const
from litchi.lib.engraving import *
from litchi.lib.utils import *
from litchi.lib.utils_abjad import *

def load_tuning(origin, tuning_name):

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

	tuning_values = const.SCALA[tuning_name]['tuning_values'].split(',')
	for index_value, value in enumerate(tuning_values):

		freq = float(Fraction(value)) * origin

		partial_freq = adjust_to_reference_octave(freq)

		partial_pitch_class = abjad.NamedPitch.from_hertz(partial_freq).pitch_class
		partial_pitch_class = remove_quarter_tones(partial_pitch_class)

		partial_name = partial_pitch_class.name
		
		if partial_name in chromatic_dict:
			partial = const.Partial()
			partial.freq = float(partial_freq)
			partial.ratio = float(Fraction(value)) if float(Fraction(value)) < 2 else float(Fraction(value))/2
			partial.string = partial.ratio
			partial.pitch_name = partial_name
			partial.position = index_value

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

	sorted_chromatic_dict = {}
	for name, partials in chromatic_dict.items():
		sorted_chromatic_dict[name] = sorted(partials, key=lambda partial: partial.ratio)

	return sorted_chromatic_dict

if __name__ == "__main__":
	print(load_tuning(440, 'edo31'))
