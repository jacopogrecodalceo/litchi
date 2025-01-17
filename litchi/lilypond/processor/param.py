import re
import ast
import logging
from typing import List

import abjad
from quickly.dom import lily

from litchi.lilypond.classes import Event, Processor
from litchi.lilypond.const import DYNs, LILYPOND_OCTAVE_ADJUST
from litchi.lilypond.utils import db2amp

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Duration(Processor):
	def process(self):
		for events in self.nodes:
			for event in events:
				self._process_written_duration(event)

	def _process_written_duration(self, event: Event):
		for articulation in event.articulations:
			if isinstance(articulation, (lily.SinglelineComment, lily.String)):
				match = re.search(r'dur.*', articulation.head)
				if match:
					try:
						event.dur = ast.literal_eval(match.group(0))
					except (SyntaxError, ValueError) as e:
						logger.error(f"Failed to evaluate duration: {match.group(0)}. Error: {e}")

class Dynamic(Processor):
	def process(self):
		self.process_dynamics()
		self.interpolate_dynamics()        

	def process_dynamics(self):
		for events in self.nodes:
			last_dyn = 'mf'  # Default dynamic level
			for event in events:
				dynamics = self._find_dynamics(event)
				if not dynamics:
					event.dyn = db2amp(DYNs[last_dyn])
					continue
				assert len(dynamics) == 1, '2 or more dynamics are associated to the same'
				dyn = dynamics[0]
				if dyn.head in DYNs:
					event.dyn = db2amp(DYNs[dyn.head])
					last_dyn = dyn.head

	def interpolate_dynamics(self):
		for events in self.nodes:
			index = 0
			while index < len(events):
				start_event = events[index]
				dynamics = self._find_dynamics(start_event)
				for dyn in dynamics:
					if dyn.head in ('<', '>'):
						direction = 1 if dyn.head == '<' else -1
						index = self._interpolate_dyn(index, start_event, events, direction)
						break
				index += 1

	def _find_dynamics(self, event: Event) -> List[lily.Dynamic]:
		return [dyn for dyn in event.articulations if isinstance(dyn, lily.Dynamic)]

	def _interpolate_dyn(self, index: int, event: Event, events: List[Event], direction: int) -> int:
		start_dyn = event.dyn
		end_dyn, count = self._find_next_dynamic(index, events)

		if end_dyn is not None and count > 0:
			step = direction * (end_dyn - start_dyn) / (count + 1)
			interpolated_values = [start_dyn + direction * step * i for i in range(1, count + 1)]
			for value in interpolated_values:
				index += 1
				events[index].dyn = value
			return index + count
		else:
			logger.error(f"Failed to find the end dynamic for interpolation. Index: {index}, Start Dyn: {start_dyn}, End Dyn: {end_dyn}, Count: {count}, Direction: {direction}")
			raise ValueError('Failed to find the end dynamic for interpolation.')

	def _find_next_dynamic(self, index: int, events: List[Event]):
		end_dyn = None
		count = 0
		for next_event in events[index + 1:]:
			next_dynamics = self._find_dynamics(next_event)
			if next_dynamics and any(d.head in DYNs or d.head == '!' for d in next_dynamics):
				end_dyn = next_event.dyn
				break
			count += 1
		return end_dyn, count

class Frequency(Processor):
	def process(self):
		for events in self.nodes:
			for event in events:
				self.process_note_frequency(event)
				self.process_markup_frequency(event)

	def process_note_frequency(self, event):
		event.freq = abjad.NamedPitch(event.pitch, octave=event.octave + LILYPOND_OCTAVE_ADJUST).hertz

	def process_markup_frequency(self, event: Event):
		for articulation in event.articulations:
			if isinstance(articulation, (lily.SinglelineComment, lily.String)):
				match = re.search(r'([\d.]+)Hz', articulation.head)
				if match:
					event.freq = float(match.group(1))
