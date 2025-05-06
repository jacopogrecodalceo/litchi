import math
import abjad
import abjadext.rmakers as rmakers
import random
import re
from fractions import Fraction
from litchi.lib.scala import Interval

from decimal import Decimal, getcontext

import litchi.lib.engraving as engraving
from litchi.lib.const import METRIC_STAFF_SPACE_DIV

def split_at_first_integer(s):
    for i, char in enumerate(s):
        if char.isdigit():
            return s[:i], s[i:]
    return s, ''

def attach_interval_markup(note: abjad.Leaf, interval: Interval):
	markup_freq = abjad.Markup(rf'\markup \teeny "FREQ: {interval.freq}Hz"')
	markup_pitch_freq = abjad.Markup(rf'\markup \teeny "REAL FREQ: {round(abjad.NamedPitch(interval.pitch).hertz, 2)}"')
	markup_cent = abjad.Markup(rf'\markup \teeny "{interval.cents}"')

	abjad.attach(markup_cent, note, direction=abjad.UP)
	abjad.attach(markup_pitch_freq, note, direction=abjad.UP, tag=abjad.Tag('REAL_FREQ'), deactivate=True)
	abjad.attach(markup_freq, note, direction=abjad.UP, tag=abjad.Tag("FREQ"), deactivate=True)

def make_dummy_staff():
	staff = abjad.Staff([abjad.Note("b''''1")])
	abjad.attach(abjad.Clef('treble^22'), staff[0])
	return staff

def add_coding_markup(param: str, string, leaf, deactivate=True):
	abjad.attach(abjad.Markup(rf'\markup "{param}{string}"'), leaf, tag=abjad.Tag(param.upper()), deactivate=deactivate)


def attach_ji_chord_markup(chord, container, n=0):
	origin, ji_nums = chord
	ji_nums_string = ':'.join(re.search(r'\d+', x).group(0) for x in ji_nums)
	abjad.attach(abjad.Markup(rf'\markup \box "{origin}, {ji_nums_string}"'), abjad.select.leaf(container, n), direction=abjad.UP)

def adjust_to_reference_octave(frequency, octave_reference=0):
	
	named_pitch = abjad.NamedPitch.from_hertz(frequency)
	
	named_pitch = remove_quarter_tones(named_pitch)
	while named_pitch.octave.number != octave_reference:
		if named_pitch.octave.number < octave_reference:
			frequency *= 2
		elif named_pitch.octave.number > octave_reference:
			frequency /= 2
		named_pitch = abjad.NamedPitch.from_hertz(frequency)
	assert named_pitch.octave.number == 0
	#print(named_pitch.name, frequency)
	return frequency

def has_not_dynamic(pitched_leaf):
	indicators = abjad.get.indicators(pitched_leaf)
	return indicators and not any(isinstance(indicator, abjad.Dynamic) for indicator in indicators)

def remove_quarter_tones(pitch_class):
		if 'qf' in pitch_class.name:
			pitch_class = pitch_class.transpose(.5)
		if 'qs' in pitch_class.name:
			pitch_class = pitch_class.transpose(-.5)
		return pitch_class

def set_init_dyn(score, dyn='mf'):
	for staff in score:
		if staff.name != 'MetricStaff':
			leaf = abjad.select.leaf(staff, 0, pitched=True)
			if has_not_dynamic(leaf):
				abjad.attach(abjad.Dynamic(dyn), leaf)

def set_init_time_sig(score, time_sig=(4, 4)):
	for staff in score:
		if staff.name != 'MetricStaff':
			leaf = abjad.select.leaf(staff, 0)
			abjad.attach(abjad.TimeSignature(time_sig), leaf)

def add_jitter_dyn(score, dyn_range=(-5, 4)):
	for staff in score:
		if staff.name != 'MetricStaff':
			leaves = abjad.select.logical_ties(staff, pitched=True)
			for leaf in leaves:
				if has_not_dynamic(leaf[0]) and random.random()> .65:
					jitter_dyn = random.choice([x for x in range(*dyn_range) if x != 0])
					dyn = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(jitter_dyn)
					abjad.attach(abjad.Dynamic(dyn), leaf[0])

def create_tie(score):
	for staff in score:
		if staff.name != 'MetricStaff':
			# cannot use pitched=True because we need to check for Rest, too
			runs = abjad.select.runs(staff)
			for notes in runs:
				for note, next_note in zip(notes[:-1], notes[1:]):
					if note.written_pitch == next_note.written_pitch:
						# check if has markup with FREQ:
						for markup in abjad.get.markup(note):
							match = re.search(r'([\d.]+)Hz', markup.string)
							if match and abjad.get.markup(note) == abjad.get.markup(next_note):
								abjad.attach(abjad.Tie(), note)

def create_gliss(score, threshold=.5):
	for staff in score:
		if 'lins' in abjad.lilypond(staff) or '_gliss' in abjad.lilypond(staff):
			ties = abjad.select.logical_ties(staff)
			for tie, next_tie in zip(ties[:-1], ties[1:]):
				if random.random() > threshold and not isinstance(next_tie[0], abjad.Rest):
					abjad.attach(abjad.Glissando(), tie[-1])

def extract_shuffled_motif(source, length=2, repeat=2):

	if length > len(source):
		length = len(source)
	
	start = random.randint(0, len(source) - length)
	motif = source[start:start + length]
	return motif * random.randint(repeat, repeat + 1)

def get_respelled_pitch_class(pitch_class: str, dict_to_check: dict) -> str:
	if pitch_class in dict_to_check:
		return pitch_class

	for accidental in ['flats', 'sharps']:
		new_pitch_name = abjad.NamedPitch(pitch_class).respell(accidental=accidental)
		new_pitch_class = new_pitch_name.pitch_class
		new_pitch_class = remove_quarter_tones(new_pitch_class)
		new_pitch_class = new_pitch_class.name
		if new_pitch_class in dict_to_check:
			return new_pitch_class

	raise ValueError(f"No matching pitch class found for {pitch_class}.")

def persist_as_pdf(score, path, info):
	#layout_block = abjad.Block('layout')
	#score_block = abjad.Block('score', [score, layout_block])
	preamble = engraving.make_preamble(path, info)
	
	lilypond_file = abjad.LilyPondFile([preamble, score])
	abjad.persist.as_pdf(lilypond_file, path.build_pdf)

def add_jitter_metronome(container, duration=(1, 4), probability=.95, bpm_range=(40, 120), minimum_duration=5/4):
		dur = 0
		for leaf in abjad.select.leaves(container):
			if random.random() < probability and dur > float(minimum_duration):
				metronome_mark = abjad.MetronomeMark(
					abjad.Duration(duration),
					random.randint(*bpm_range)
				)
				abjad.attach(metronome_mark, leaf)
				dur = 0
			dur += leaf.written_duration

def add_rallentando_ending(staff, tempo, duration=(1, 4), start_pos=-8, end_pos=-1):

	metronome_mark = abjad.MetronomeMark(
		abjad.Duration(duration),
		random.randint(tempo-1, tempo+1)
	)
	abjad.attach(metronome_mark, abjad.select.leaf(staff, start_pos))

	metronome_mark = abjad.MetronomeMark(
		abjad.Duration(duration),
		random.randint(tempo//12, tempo//8)
	)
	abjad.attach(metronome_mark, abjad.select.leaf(staff, end_pos))

def create_metric_staff(staves, tempo=60, diff=1):
	"""
	for:
		- REHEARSAL MARKs
		- METRONOME
		- \break
	"""
	metric_staff = abjad.Staff(lilypond_type='Devnull', name='MetricStaff')
	staff_dur = 0
	metric_staff_dur = 0
	index = 0
	for leaf in abjad.select.leaves(staves[-1]):
		if metric_staff_dur <= staff_dur:
			metric_staff.append(f's{METRIC_STAFF_SPACE_DIV}')
			metric_staff_dur += 1/METRIC_STAFF_SPACE_DIV
			index += 1
		staff_dur += float(leaf.written_duration)

	metronome_mark = abjad.MetronomeMark(
		abjad.Duration(1, 4),
		random.randint(tempo-diff, tempo+diff)
	)
	abjad.attach(metronome_mark, metric_staff[0])

	staves.insert(0, metric_staff)

def create_staves(instruments):
	staves = []

	for i, instr_name in enumerate(instruments):
		block = [
			f'instrumentName = "{instr_name}"',
			f'shortInstrumentName = "{instr_name[:2]}."'
		]
		staff_block = abjad.Block("with", items=block)
		staff = abjad.Staff(lilypond_type=f"Staff {abjad.lilypond(staff_block)}")
		staves.append(staff)

	""" for i, instr_name in enumerate(instruments):
		staff = abjad.Staff()
		abjad.override(staff).InstrumentName = instr_name
		abjad.override(staff).ShortInstrumentName = instr_name[:2]
		staves.append(staff) """
	return staves

def attach_meta_info(partial, leaf, show_ratio=True, ratio_direction='horizontal', show_cent=False, show_interval_name=False):
	""" attach meta info to leaf"""
	if show_cent and partial.cent_diff != 0:
		cent_diff = partial.cent_diff
		string = cent_diff if cent_diff < 0 else f'+{cent_diff}'
		abjad.attach(abjad.Markup(rf'\markup \teeny "{string}¢"'), leaf, direction=abjad.UP)
	if show_ratio and partial.ratio != 1:
		string = partial.ratio
		if isinstance(string, str) and len(string) > 5:
			string = string[:5]
		elif isinstance(string, float):
			string = round(string, 2)
		if ratio_direction.lower() == 'horizontal':
			abjad.attach(abjad.Markup(rf'\markup \teeny \bold "{string}"'), leaf, direction=abjad.UP)
		elif ratio_direction.lower() == 'vertical' and hasattr(partial.ratio, 'numerator'):
			abjad.attach(abjad.Markup(rf'\markup \teeny \bold \fraction {partial.ratio.numerator} {partial.ratio.denominator}'), leaf, direction=abjad.UP)

	if show_interval_name:
		abjad.attach(abjad.Markup(rf'\markup \teeny \italic "{partial.interval_name}"'), leaf, direction=abjad.UP)

def validate_frequency_match(freq: float, written_pitch: abjad.NamedPitch, threshold: float = 250) -> None:
	difference = abs(freq - written_pitch.hertz)
	if difference >= threshold:
		raise ValueError(
			f"Frequency mismatch: {freq:.2f} Hz and {written_pitch.hertz:.2f} Hz differ by "
			f"{difference:.2f} Hz, exceeding the threshold of {threshold} Hz. "
			f"Written pitch: {written_pitch}"
		)

def set_short_instrument_name(name):
	if '_' in name:
		parts = name.split('_')
		return f'{parts[0][:2]}_{parts[1]}'
	else:
		return name[:2]
	
def set_staff_info(staff, staff_info):
	staff.name = staff_info['staff_name_id']
	staff.with_commands.extend([
		f'instrumentName = "{staff_info["staff_name_shown"]}"',
		f'shortInstrumentName = "{set_short_instrument_name(staff_info["staff_name_shown"])}."'
	])
	staff.with_commands.extend([
		'%{',
		'---CSOUND INFO---',
		f'Instrument = {staff_info["csound_instrument"]}',
		f'Channels = {staff_info["channels"]}',
		'%}',
	])
	return staff

def repeat_each_leaf(original_list: list, n: int) -> list:
	return [e for e in original_list for _ in range(n)]

def add_glissandos(container, min_duration=0, each=1):
	logical_ties = abjad.select.logical_ties(container)
	for index, (tie, next_tie) in enumerate(zip(logical_ties, logical_ties[1:])):
		if (
			not isinstance(tie[0], abjad.Rest)
			and not isinstance(next_tie[0], abjad.Rest)
			and tie[-1].written_duration > min_duration
			and index % each == each-1
			# and not next_tie[0].written_pitch == tie[0].written_pitch
		):
			abjad.attach(abjad.Glissando(), tie[-1])

def create_talea(talea: list, denominator: int, time_signatures: list, start: int = None, end:int = None, preamble=[], show=True, rewrite=True, extra_counts=[], trivial=False):
	durations = [abjad.Duration(_) for _ in time_signatures][start:end]
	tuplets = rmakers.talea(durations, talea, denominator, preamble=preamble, extra_counts=extra_counts)

	voice = rmakers.wrap_in_time_signature_staff(tuplets, time_signatures[start:end])
	if not trivial:
		rmakers.extract_trivial(voice)
	if rewrite:
		rmakers.rewrite_meter(voice)
	components = abjad.mutate.eject_contents(voice)

	if show and len(talea) > 3:
		leaves = abjad.select.leaves(components)
		talea_durations = [abjad.Duration(1, denominator)*abs(_) for _ in talea if _ ]
		partition = abjad.select.partition_by_durations(
			leaves,
			talea_durations,
			cyclic=True,
			fill=abjad.MORE,
		)
		for i, leaves in enumerate(partition):
			try:
				selected = abjad.select.leaf(leaves, 0, pitched=True)
				abjad.attach(abjad.Markup(rf'\markup \huge \bold "{talea[i%len(talea)]}"'), selected)
			except:
				pass

	return components

def create_accent_pattern(accent_indices: list, length: int, accent_dynamic='f', non_accent_dynamic='p'):
	# Initialize a list of the specified length filled with None
	result = [None] * length

	# Iterate through the accents list
	for accent in accent_indices:
		accent = accent-1
		# Ensure the accent is within the valid range
		if 0 <= accent < length:
			result[accent] = accent_dynamic
			# Insert 'p' just after 'f' if it's within the valid range
			if accent + 1 < length:
				result[accent + 1] = non_accent_dynamic

	return result

def create_pattern(accent_indices: list, length: int):
	# Initialize a list of the specified length filled with None
	result = [None] * length

	# Iterate through the accents list
	for accent in accent_indices:
		accent = accent-1
		# Ensure the accent is within the valid range
		if 0 <= accent < length:
			result[accent] = 1

	return result

def count_8va(string: str):
	index = string.find("'")
	ji_num = string[:index]
	symbols = string[index:]
	return int(ji_num), 2**(len(symbols))

def count_8vb(string: str):
	index = string.find(",")
	ji_num = string[:index]
	symbols = string[index:]
	return int(ji_num), 1/(2**len(symbols))

def set_pitch_and_markup(this_pitch, ties, transpose=0, log=False):
	origin, ji_num_string = this_pitch

	assert ji_num_string[0].isdigit()
	if "'" in ji_num_string:
		ji_num, octave = count_8va(ji_num_string)
	elif "," in ji_num_string:
		ji_num, octave = count_8vb(ji_num_string)
	else:
		ji_num = int(ji_num_string)
		octave = 1
		
	origin_pitch = abjad.NamedPitch(origin).transpose(transpose)
	ji_ratio = Fraction(ji_num, 2 ** math.floor(math.log2(ji_num)))
	freq = origin_pitch.hertz * ji_ratio
	freq *= octave
	written_pitch = abjad.NamedPitch.from_hertz(freq)
	if log:
		print(f"Origin: {origin_pitch.get_name()}, JI Ratio: {ji_ratio}, Frequency: {origin_pitch.hertz * ji_ratio}Hz, written_pitch: {written_pitch.get_name()}")

	cent = round(1200 * math.log2(abs(freq) / abjad.NamedPitch.from_hertz(freq).hertz))
	cent_string = f"{cent:+}¢"

	if ji_ratio != 1:
		#markup_ratio = abjad.Markup(rf'\markup \teeny \bold \fraction {ji_ratio.numerator} {ji_ratio.denominator}')
		markup_ratio = abjad.Markup(
   			rf'\markup \teeny \concat {{ \bold \fraction {ji_ratio.numerator} {ji_ratio.denominator} \hspace #0.15 "{origin_pitch.pitch_class.name}" }}',
		)
		markup_freq = abjad.Markup(rf'\markup \teeny "FREQ: {freq}Hz"')
		markup_pitch_freq = abjad.Markup(rf'\markup \teeny "REAL FREQ: {round(abjad.NamedPitch.from_hertz(freq).hertz, 2)}"')
		markup_cent = abjad.Markup(rf'\markup \teeny "{cent_string}"')

		abjad.attach(markup_cent, ties[0], direction=abjad.UP)
		abjad.attach(markup_ratio, ties[0], direction=abjad.UP)
		abjad.attach(markup_pitch_freq, ties[0], direction=abjad.UP, tag=abjad.Tag('REAL_FREQ'), deactivate=True)
		abjad.attach(markup_freq, ties[0], direction=abjad.UP, tag=abjad.Tag('FREQ'), deactivate=True)

	for note in ties:
		note.note_head.written_pitch = written_pitch

class MetricStaff:
	def __init__(self, time_signatures, tempo=65, duration=(1, 4), tempo_diff=1, measures=None):
		self.tempo = tempo
		self.duration = duration
		self.tempo_diff = tempo_diff
		self.time_signatures = time_signatures
		self.measures = measures

	def create_time_signatures(self, staff):
		durations = [ts.duration for ts in self.time_signatures]
		leaves = abjad.select.leaves(staff)
		parts = abjad.select.partition_by_durations(leaves, durations)
		
		assert len(parts) == len(self.time_signatures), f'{len(parts)} == {len(self.time_signatures)}, {staff}'
		
		previous_time_signature = None
		for time_signature, part in zip(self.time_signatures, parts):
			if time_signature != previous_time_signature:
				abjad.attach(time_signature, abjad.select.leaf(part, 0))
			previous_time_signature = time_signature

	def make(self, staff_index):
		staff_name = 'MetricStaff'
		staff = abjad.Staff(lilypond_type='Devnull')
		staff.name = staff_name

		voice = abjad.Voice()
		voice.extend(create_talea([-1], 8, self.time_signatures, rewrite=False))
		self.create_time_signatures(voice)

		metronome_mark = abjad.MetronomeMark(
			abjad.Duration(self.duration),
			random.randint(self.tempo - self.tempo_diff, self.tempo + self.tempo_diff)
		)
		abjad.attach(metronome_mark, abjad.select.leaf(voice, 0))
		#add_jitter_metronome(voice, probability=.25)
		if self.measures:
			measures_count = abjad.select.group_by_measure(voice)
			for (measure_number, tempo) in self.measures:
				metronome_mark = abjad.MetronomeMark(
					abjad.Duration(self.duration),
					random.randint(tempo - self.tempo_diff, tempo + self.tempo_diff)
				)
				abjad.attach(metronome_mark, abjad.select.leaf(measures_count[measure_number], 0))


		staff.extend(voice)
		return staff

class LitchiStaff:
	def __init__(
		self,
		csound_instrument: str,
		staves: list,
		channels: int = 2,
		staff_name_visible: str = None,
		lilypond_type: str = 'Staff'
	):
		self.staves = staves
		self.channels = channels
		self.csound_instrument = csound_instrument
		self.staff_name_visible = staff_name_visible or csound_instrument
		self.lilypond_type = lilypond_type

	def make(self, staff_index):
		staff = abjad.Staff(lilypond_type=self.lilypond_type)
		staff_id = f'staff_{staff_index}'
		staff.name = staff_id

		staff.with_commands.extend([
			f'instrumentName = "{self.staff_name_visible}"',
			f'shortInstrumentName = "{set_short_instrument_name(self.staff_name_visible)}."'
		])

		staff.with_commands.extend([
			'%{',
			'---CSOUND INFO---',
			f'Instrument = {self.csound_instrument}',
			f'Channels = {self.channels}',
			'%}',
		])
		for s in self.staves:
			staff.extend(s)
		return staff

def create_score_with_order(order):
	score = abjad.Score()
	for index, staff in enumerate(order):
		staff_index = 0 if isinstance(staff, MetricStaff) else len(order) - index
		score.append(staff.make(staff_index))
	return score

def make_rests(time_signatures): 
	durations = [abjad.Duration(_) for _ in time_signatures]
	tuplets = rmakers.talea(durations, [-1], 1)
	voice = rmakers.wrap_in_time_signature_staff(tuplets, time_signatures)
	rmakers.rewrite_meter(voice)
	rmakers.extract_trivial(voice)
	return abjad.mutate.eject_contents(voice)