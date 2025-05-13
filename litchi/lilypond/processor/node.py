import logging
import re
from typing import List

import abjad
from quickly.dom import lily

from litchi.lilypond.classes import Event, Rest, Processor, Tempo

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InstrumentStaff(Processor):
	def process(self) -> List[List[Event]]:
		nodes = []
		for node in self.nodes:
			events = self._process_node(node)
			nodes.append(events)
		return nodes

	def _process_node(self, node) -> List[Event]:
		self._find_csound_info(node)
		name = self._process_instrument_name()
		channels = self._process_instrument_channels()
		assert name, 'No instrument name'
		assert channels, 'No channels'

		events = []
		onset = 0
		event_for_comment = None
		for sub_node in node.descendants():
			if isinstance(sub_node, lily.Note):
				event = self._process_note(sub_node, onset)
				event.name = name
				event.channels = channels
				events.append(event)
				onset += event.dur
				event_for_comment = event
			elif isinstance(sub_node, lily.SinglelineComment) and event_for_comment:
				if sub_node not in event_for_comment.articulations:
					event_for_comment.articulations.append(sub_node)
			elif isinstance(sub_node, lily.Rest):
				onset, rest = self._process_rest(sub_node, onset)
				#events.append(rest) this can be long..

		if not events:
			print('WARNING: no events, probably only rests')

		return events

	def _find_csound_info(self, node):
		for e in node.descendants():
			if isinstance(e, lily.MultilineComment) and '---CSOUND INFO---' in e.head:
				self.csound_info = e.head

	def _process_instrument_name(self) -> str:
		match = re.search(r'Instrument\s*=\s*(.*)', self.csound_info, re.IGNORECASE)
		if match:
			return match.group(1)
		return None

	def _process_instrument_channels(self) -> int:
		match = re.search(r'Channels\s*=\s*(.*)', self.csound_info, re.IGNORECASE)
		if match:
			return int(match.group(1))
		return None


	def _process_note(self, node, onset: float) -> Event:
		multiplier = self._get_multiplier(node)
		event = Event()

		event.pitch = node.head
		event.onset = onset

		for p in node:
			if isinstance(p, lily.Duration):
				event.dur = float(p.head) * float(multiplier)
			elif isinstance(p, lily.Octave):
				event.octave = p.head
			elif isinstance(p, lily.Articulations):
				event.articulations.extend(list(p.descendants()))
			""" elif isinstance(p, lily.SinglelineComment):
				event.articulations.append(p) """

		return event

	def _process_rest(self, node: lily.Rest, onset: float) -> float:
		multiplier = self._get_multiplier(node)
		rest = Rest()

		for p in node:
			if isinstance(p, lily.Duration):
				rest.onset = float(p.head) * float(multiplier)
				onset += float(p.head) * float(multiplier)
		return onset, rest

	def _get_multiplier(self, node) -> float:
		multiplier = 1
		parent = node.parent.parent
		if isinstance(parent, lily.Times):
			multiplier = abjad.Duration([n for n in parent // lily.Fraction][0].head)
		return multiplier

class TempoStaff(Processor):
	def process(self) -> List[Tempo]:
		tempi = []
		onset = 0

		for music_list in self.nodes // lily.MusicList:
			for node in music_list:
				if isinstance(node, lily.Tempo):
					tempo = self._process_tempo_node(node, onset)
					tempi.append(tempo)
				else:
					onset = self._update_onset(node, onset)
		#exit()
		return tempi

	def _process_tempo_node(self, node: lily.Tempo, onset: float) -> Tempo:
		tempo = Tempo()
		tempo.onset = onset

		found = False
		for p in node.descendants():
			if isinstance(p, lily.Duration):
				tempo.div = p.head
			elif isinstance(p, lily.Int):
				tempo.bpm = p.head
				found = True
				break

		if not found:
			for p in node.forward():
				if isinstance(p, lily.Duration):
					tempo.div = p.head
				elif isinstance(p, lily.Int):
					tempo.bpm = p.head
					break

		if not hasattr(tempo, 'div') or tempo.div is None:
			tempo.div = self._find_div_in_parent(node)
			
		if not hasattr(tempo, 'bpm') or tempo.bpm is None:
			tempo.bpm = self._find_bpm_in_parent(node)


		return tempo

	def _find_bpm_in_parent(self, node: lily.Tempo) -> int:
		for p in node.parent.descendants():
			if isinstance(p, lily.Int):
				return p.head
		logger.error(f"BPM not found for tempo node: {node}")
		raise ValueError("BPM not found for tempo node")
	
	def _find_div_in_parent(self, node: lily.Duration):
		for p in node.parent.descendants():
			if isinstance(p, lily.Duration):
				return p.head
		logger.error(f"DIV not found for tempo node: {node}")
		raise ValueError("DIV not found for tempo node")

	def _update_onset(self, node, onset: float) -> float:
		for p in node:
			if isinstance(p, lily.Duration):
				onset += float(p.head)
		return onset
