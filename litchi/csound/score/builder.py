from litchi.lilypond.const import DYNs_amp
from litchi.lilypond.utils import find_nearest

class CsoundScoreBuilder:
	def __init__(self, node_events, node_tempi):
		self.node_events = node_events
		self.node_tempi = node_tempi

	def create_score_as_dict(self) -> dict:
		t_statement_string = self._create_t_statement()
		i_statements_dict = self._create_i_statement()
		csound_score_dict = {
			't_statement': t_statement_string,
			'i_statements': i_statements_dict
		}

		#return '\n'.join(map(str, csound_score_list))
		return csound_score_dict

	def _create_t_statement(self):
		# create a string of t values
		# e.g.
		# t 0 60 12 120 ..
		t_list = ['t']
		self.node_tempi[0].onset = 0
		for tempo in self.node_tempi:
			t_list.append(tempo.onset)
			t_list.append(tempo.bpm)
		t_statement_string = '\t'.join(map(str, t_list))
		return t_statement_string if t_statement_string else 't 0 60'

	def _create_i_statement(self) -> dict:
		"""
		a dict of each line
		"""
		i_statements_dict = {}
		for index_staff, events in enumerate(self.node_events, start=1):
			if not events:
				print(f'No events found in staff #{index_staff}')
				continue
			instrument_name = events[0].name

			i_score_lines = []

			self._add_header(i_score_lines, instrument_name=instrument_name, index_staff=index_staff)
			self._add_prefix(i_score_lines)

			for e in events:
				comment_name = getattr(e, 'comment_name', e.name)
				onset, onset_comment = self._calculate_onset(e)
				dyn = e.dyn
				dur, dur_comment = self._calculate_duration(e)
				i_line = [';', f'"{comment_name}"', onset_comment, dur_comment, DYNs_amp[find_nearest(dyn, DYNs_amp)], 'envelope', e.pitch]
				i_score_lines.append(' '.join(map(lambda x: f'{x:<25}', map(str, i_line))))

				if hasattr(e, 'channel'):
					i_statement = ['i', f'"{e.name}"', onset, dur, dyn, e.env, e.freq]
					i_score_lines.append(' '.join(map(lambda x: f'{x:<25}', map(str, i_statement + [f'{e.channel+(index_staff/1000)}']))))
				else:
					for ch in range(1, e.channels + 1):
						i_statement = ['i', f'"{e.name}"', onset, dur, dyn, e.env, e.freq]
						i_score_lines.append(' '.join(map(lambda x: f'{x:<25}', map(str, i_statement + [f'{ch+(index_staff/1000)}']))))

			i_statements_dict[f'{index_staff:02}-{instrument_name}'] = i_score_lines

		return i_statements_dict

	def _add_header(self, lines, instrument_name: str, index_staff: int):
		header = ['/*', '▃' * 145, 
			f'staff index: {index_staff}',
			instrument_name,
		'▃' * 145, '*/']
		lines.extend(header)

	def _add_prefix(self, lines):
		prefix = [';', 'name', 'onset', 'dur', 'dyn', 'env', 'freq']
		lines.append(' '.join(map(lambda x: f'{x.upper():<25}', map(str, prefix))))

	def _calculate_onset(self, e):
		if isinstance(e.onset, str):
			return e.onset, e.onset
		else:
			return e.onset, round(e.onset, 2)

	def _calculate_duration(self, e):
		if isinstance(e.dur, str):
			return e.dur, e.dur
		else:
			return e.dur, round(e.dur, 2)


