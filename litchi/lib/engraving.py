import os
import abjad

TITLE_FONT_NAME = "Longinus"
TITLE_FONT_SIZE = 16

def make_title(title='canvas'):
	string = rf"""\markup {{
		\override #'(font-name . "{TITLE_FONT_NAME}")
		\fontsize #{TITLE_FONT_SIZE}
		"{title.upper()}"
	}}"""
	return string

def make_preamble(path, info):

	header_lines = [
		'\header {',
		rf'title = {make_title(title=info["title"])}',
		rf'composer = "{info["composer"]}"',
		rf'tagline = "{info["composer"]}"',
		rf'date = "{info["date"]}"',
		'}'
	]

	header = '\n'.join(header_lines)

	PREAMBLEs = [header]

	for f in [file for file in os.listdir(path.stylesheet_dir) if file.endswith('.ily')]:
		PREAMBLEs.append(f'\include "{os.path.join(path.stylesheet_dir, f)}"')

	return '\n'.join(PREAMBLEs)

def adjust_clefs(score):
	for staff in score:
		index = 0
		temp_leaf = None
		for leaf in abjad.select.leaves(staff, pitched=True):
			if leaf.written_pitch <= abjad.Note('c'):
				index += 1
				if not temp_leaf:
					temp_leaf = leaf
			else:
				index = 0
				temp_leaf = None

			if index > 2:
				if not isinstance(abjad.get.indicator(temp_leaf, abjad.Clef), abjad.Clef):
					abjad.attach(abjad.Clef('bass'), temp_leaf)
				index = 0

def format_measures(score):
	for staff in score:
		time_sig = abjad.TimeSignature((4, 4))
		if staff.name != 'MetricStaff':
			leaves = abjad.select.leaves(staff)
			for measure in abjad.select.group_by_measure(leaves):
				for leaf in measure:
					for indicator in abjad.get.indicators(leaf):
						if isinstance(indicator, abjad.TimeSignature):
							time_sig = indicator
				beams = abjad.select.partition_by_durations(measure, [abjad.Duration(1, time_sig.denominator)], cyclic=True, fill=abjad.EXACT)
				for beam in beams:
					abjad.mutate.fuse(abjad.select.rests(beam))