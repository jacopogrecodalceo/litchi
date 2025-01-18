import abjad
import random
import re

import litchi.lib.engraving as engraving
from litchi.lib.const import METRIC_STAFF_SPACE_DIV

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

def add_jitter_metronome(score, probability=.95, bpm_range=(40, 120), at_least=5/4):
	for staff in score:
		dur = 0
		if staff.name == 'MetricStaff':
			for leaf in abjad.select.leaves(staff):
				if random.random() > probability and dur > float(at_least):
					metronome_mark = abjad.MetronomeMark(
						abjad.Duration(1, 4),
						random.randint(*bpm_range)
					)
					abjad.attach(metronome_mark, leaf)
					dur = 0
				dur += leaf.written_duration

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

def attach_meta_info(partial, leaf, show_ratio=True, show_cent=False, show_interval_name=False):
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
		abjad.attach(abjad.Markup(rf'\markup \teeny \bold "{string}"'), leaf, direction=abjad.UP)
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
	
def set_staff_info(staff_info):
	staff = abjad.Staff()
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