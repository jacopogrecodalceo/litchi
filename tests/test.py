import os
import threading
import abjad
import random
from litchi import Litchi

OUTPUT_PDF = os.path.join(os.path.dirname(__file__), 'output.pdf')
OUTPUT_LY = os.path.join(os.path.dirname(__file__), 'output.ly')
OUTPUT_SCO = os.path.join(os.path.dirname(__file__), 'output.sco')

ORC_FILE = '/Users/j/Desktop/main.orc'

def create_metric_staff():
	staff_name = 'MetricStaff'
	# ▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃
	staff = abjad.Staff(lilypond_type='Devnull')
	staff.name = staff_name
	# ▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃
	TEMPO = 135
	staff.append(f's1')
	metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), TEMPO)
	abjad.attach(metronome_mark, staff[0])
	return staff

def create_ariel_lpf():
	staff_info = {
		'csound_instrument': 'ariel_lpf',
		'staff_name_id': 'ariel_lpf',
		'staff_name_shown': 'ariel_lpf',
		'channels': 1,
	}
	staff = abjad.Staff()
	staff.name = staff_info['staff_name_id']
	staff.with_commands.extend([
		f'instrumentName = "{staff_info["staff_name_shown"]}"',
		f'shortInstrumentName = "{staff_info["staff_name_shown"][:2]}."'
	])
	staff.with_commands.extend([
		'%{',
		'---CSOUND INFO---',
		f'Instrument = {staff_info["csound_instrument"]}',
		f'Channels = {staff_info["channels"]}',
		'%}',
	])

	for _ in range(256):
		note = abjad.Note(random.randint(0, 36), (1, 16))
		abjad.attach(abjad.Dynamic(random.choice(['p', 'fff', 'mf'])), note)
		if random.random()>.5:
			abjad.attach(abjad.Glissando(), note)
		staff.append(note)
	return staff


def create_ariel_1():
	staff_info = {
		'csound_instrument': 'ariel',
		'staff_name_id': 'ariel_1',
		'staff_name_shown': 'ariel',
		'channels': 2,
	}
	staff = abjad.Staff()
	staff.name = staff_info['staff_name_id']
	staff.with_commands.extend([
		f'instrumentName = "{staff_info["staff_name_shown"]}"',
		f'shortInstrumentName = "{staff_info["staff_name_shown"][:2]}."'
	])
	staff.with_commands.extend([
		'%{',
		'---CSOUND INFO---',
		f'Instrument = {staff_info["csound_instrument"]}',
		f'Channels = {staff_info["channels"]}',
		'%}',
	])

	for _ in range(64):
		note = abjad.Note(random.randint(-32, 0), (1, 4))
		abjad.attach(abjad.Dynamic(random.choice(['p', 'fff', 'mf'])), note)
		if random.random()>.5:
			abjad.attach(abjad.Glissando(), note)
		staff.append(note)

	abjad.attach(abjad.Clef('bass'), abjad.select.leaf(staff, 0))

	return staff

def create_ariel_2():
	staff_info = {
		'csound_instrument': 'ariel',
		'staff_name_id': 'ariel_2',
		'staff_name_shown': 'ariel',
		'channels': 2,
	}
	staff = abjad.Staff()
	staff.name = staff_info['staff_name_id']
	staff.with_commands.extend([
		f'instrumentName = "{staff_info["staff_name_shown"]}"',
		f'shortInstrumentName = "{staff_info["staff_name_shown"][:2]}."'
	])
	staff.with_commands.extend([
		'%{',
		'---CSOUND INFO---',
		f'Instrument = {staff_info["csound_instrument"]}',
		f'Channels = {staff_info["channels"]}',
		'%}',
	])

	for _ in range(32):
		note = abjad.Note(random.randint(-32, 0), (1, 2))
		abjad.attach(abjad.Dynamic(random.choice(['p', 'fff', 'mf'])), note)
		if random.random()>.5:
			abjad.attach(abjad.Glissando(), note)
		staff.append(note)

	abjad.attach(abjad.Clef('bass'), abjad.select.leaf(staff, 0))

	return staff

def craft():

	SCORE = abjad.Score()
	SCORE.extend([
			create_metric_staff(),
			create_ariel_lpf(),
			create_ariel_1(),
			create_ariel_2(),
		])
	abjad.persist.as_pdf(SCORE, OUTPUT_PDF)


def run_litchi():
	litchi = Litchi()
  
  # load a lilypond file
	litchi.lilypond.load(file_path=OUTPUT_LY)
  
	# here litchi analyse nodes
	node_events, node_tempi = litchi.lilypond.analyse()

	# load a file or a directory for csound orchestra
	litchi.csound.load(ORC_FILE)
  
 	# here it will play
	litchi.csound.process_events(node_events, node_tempi)
	litchi.csound.play(export_score=OUTPUT_SCO)

def main():
	craft()
	thread = threading.Thread(target=run_litchi)
	thread.start()

main()