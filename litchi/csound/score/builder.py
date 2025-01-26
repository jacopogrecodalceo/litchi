from litchi.lilypond.const import DYNs_amp
from litchi.lilypond.utils import find_nearest

class CsoundScoreBuilder:
	def __init__(self, node_events, node_tempi):
		self.node_events = node_events
		self.node_tempi = node_tempi

	def create_score(self):
		csound_score_list = []

		t_statement_string = self._create_t_statement()
		csound_score_list.append(t_statement_string)
		
		i_statements = self._create_i_statement()
		csound_score_list.extend(i_statements)
		return '\n'.join(map(str, csound_score_list))

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

	def _create_i_statement(self):
		i_statements = []
		for index_staff, events in enumerate(self.node_events):
			self._add_header(i_statements, events[0].name)
			self._add_prefix(i_statements)
			for e in events:
				comment_name = getattr(e, 'comment_name', e.name)
				onset, onset_comment = self._calculate_onset(e)
				dyn = e.dyn
				dur, dur_comment = self._calculate_duration(e)
				i_statement = [';', f'"{comment_name}"', onset_comment, dur_comment, DYNs_amp[find_nearest(dyn, DYNs_amp)], 'envelope', e.pitch]
				i_statements.append(' '.join(map(lambda x: f'{x:<25}', map(str, i_statement))))

				for ch in range(1, e.channels + 1):
					self._add_i_statement(i_statements, e, onset, dur, dyn, e.env, e.freq, ch, index_staff)
		return i_statements

	def _add_header(self, i_statements, name):
		header = ['/*', '▃' * 145, name, '▃' * 145, '*/']
		i_statements.extend(header)

	def _add_prefix(self, i_statements):
		prefix = [';', 'name', 'onset', 'dur', 'dyn', 'env', 'freq']
		i_statements.append(' '.join(map(lambda x: f'{x.upper():<25}', map(str, prefix))))

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

	def _add_i_statement(self, i_statements, e, onset, dur, dyn, env, freq, ch, index_staff):
		i_statement = ['i', f'"{e.name}"', onset, dur, dyn, env, freq]
		i_statements.append(' '.join(map(lambda x: f'{x:<25}', map(str, i_statement + [f'{ch}.00{index_staff}']))))

