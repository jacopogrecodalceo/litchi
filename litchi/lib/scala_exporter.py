# scala_exporter.py

import os
import abjad

def export_scala(scala, output_dir: str):
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
	key_to_start = scala.origin_named_pitch.pitch_class.number
	keys = list(scala.chromatic_intervals.keys())
	start_index = keys.index(key_to_start)
	shifted_chromatic_intervals = {key: scala.chromatic_intervals[key] for key in keys[start_index:] + keys[:start_index]}

	blocks = []
	markup_string = rf"""
	\markup {{
		\column {{
			\vspace #5
			\fill-line {{ \fontsize #15 "{scala.name}" }}
			\vspace #2
			\fill-line {{ \fontsize #9 "***" }}
			\fill-line {{ \fontsize #9 "origin: {scala.origin_value}, {scala.origin_named_pitch.name}" }}
			\vspace #.5
			\fill-line {{ \italic "jacqouemin greco d'alceo" }}
		}}
	}}
	"""
	blocks.append(markup_string)
	blocks.append('\pageBreak')

	for note, intervals in shifted_chromatic_intervals.items():
		blocks.append(abjad.Markup(rf'\markup "{note}"'))
		values = [f'{i}, {interval.value:.3f}, {interval.name}' for i, interval in enumerate(intervals)]
		for value in values:
			blocks.append(abjad.Markup(rf'\markup "\t\t\t{value}"'))
	blocks.append('\pageBreak')

	index = 0
	for note_name, intervals in shifted_chromatic_intervals.items():
		pitch = abjad.NamedPitch(note_name).transpose(12)
		staff = abjad.Staff()
		note = abjad.Note(pitch, (1, 4))
		lines = []
		for interval in intervals:
			lines.append('***')
			lines.append(f'\italic "{interval.name}, {interval.interval_name_ratio}"')
			f_denom = f"{interval.denominator_limit:.0e}".replace("+", "").replace(".0", "")
			lines.append(f'with {f_denom} limited denominator | 1e{interval.tolerance} tolerance')
			if interval.ratio != 1:
				lines.append(rf'\italic \box {{ \fraction {interval.ratio.numerator} {interval.ratio.denominator} "{interval.value:.2f}"}}')
			lines.append(f'{interval.semitones:.2f} st | {interval.abs_cents:.2f} abs cents')
			lines.append(f'{interval.cents}')
			staff.append(note)

		text = [r"\line {" + line + r"}" for line in lines]
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
	output_path = os.path.join(output_dir, f'{scala.name}-{scala.origin_value}.pdf')
	if not os.path.exists(output_path):
		abjad.persist.as_pdf(lilypond_file, output_path)