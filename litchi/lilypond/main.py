import quickly
from quickly.dom import lily
from quickly.dom.scope import Scope

import litchi.lilypond.processor.node as node
import litchi.lilypond.processor.param as param
import litchi.lilypond.processor.articulation as articulation

class LitchiLilyPond:
	def __init__(self, ):
		pass

	def load(self, file_path: str, language: str = 'english', log_path: str = None):
		self.file_path = file_path
		self.language = language

		d = quickly.load(self.file_path)
		self.scope = Scope(d)
		self.tree = d.get_transform(True)
		if log_path:
			with open(log_path, 'w') as f:
				self.tree.dump(file=f)
		self.replace_includes()

	def replace_includes(self):
		for identifier in self.tree // lily.IdentifierRef:
			identifier.replace_with(identifier.get_value(self.scope))

	def find_staves(self):
		self.instrument_staves = []

		for context in self.tree // lily.Context:
			for token in context.descendants():
				if isinstance(token, lily.String) and token.head == 'MetricStaff':
					self.metric_staff = context
					break
				elif isinstance(token, lily.Symbol):
					if token.head == 'Score':
						break
					elif token.head in ('Staff', 'PianoStaff', 'StaffGroup'):
						self.instrument_staves.append(context)
						break

	def apply_processors(self, processor_classes):
		for processor_class in processor_classes:
			processor = processor_class(self.instrument_events)
			processor.process()

	def analyse(self):

		self.find_staves()

		# Nodes separation
		self.tempi = node.TempoStaff(self.metric_staff).process()
		self.instrument_events = node.InstrumentStaff(self.instrument_staves).process()
		self.apply_processors(
			[
				param.Duration,
				param.Dynamic,
				param.Frequency
			])

		self.apply_processors(
			[
				articulation.Tie,
				articulation.Glissando,
			])
		
		for events in self.instrument_events:
			for event in events:
				for p in ['name', 'dur', 'dyn', 'env', 'freq']:
					assert p in event.__dict__ and getattr(event, p) is not None, f'No {p} in event: {event.name} at {event.onset}'

		for tempo in self.tempi:
			tempo.onset *= 4
			tempo.bpm *= 4*tempo.div
		for events in self.instrument_events:
			for event in events:
				event.onset *= 4
				event.dur *= 4

		return self.instrument_events, self.tempi