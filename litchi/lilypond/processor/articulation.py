import logging
from typing import List, Tuple, Set, Type
from quickly.dom import lily
from lilypond.classes import Event, Processor
from lilypond.const import ONSET_GLISSANDO_OFFSET

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Tie(Processor):
	def process(self):
		for events in self.nodes:
			i = 0
			tied_events = []

			while i < len(events) - 1:
				current_event = events[i]
				current_articulations = {type(a) for a in current_event.articulations}

				# Check if current event has a Tie
				if lily.Tie in current_articulations:
					j = i + 1
					while j < len(events):
						next_event = events[j]
						next_articulations = {type(a) for a in next_event.articulations}

						if lily.Glissando in next_articulations:
							# Stop if there's a glissando: update pitch/freq and exit the tie sequence
							# This to be sure frequency is the same (if markup frequency)
							next_event.freq = current_event.freq
							next_event.pitch = current_event.pitch
							i = j  # Process the Glissando next
							break
						elif lily.Tie in next_articulations:
							# Merge tied event into the current one
							current_event.dur += next_event.dur
							current_event.articulations += next_event.articulations
							tied_events.append(next_event)  # Mark for deletion
							j += 1
						else:
							# Stop tie sequence if no further articulation
							current_event.dur += next_event.dur
							current_event.articulations += next_event.articulations
							tied_events.append(next_event)  # Mark for deletion

							current_event.articulations = [a for a in current_event.articulations if not isinstance(a, lily.Tie)]

							i = j  # Move to next event after processing
							break
					else:
						# If the loop completes without a break, set `i` to `j`
						i = j
				else:
					# No Tie: move to the next event
					i += 1

			# Remove all tied events in reverse order to preserve indices
			for event in tied_events:
				events.remove(event)


class Glissando(Processor):
	def process(self):
		for events in self.nodes:
			grace_events = []
			i = 0
			while i < len(events) - 1:
				head_event = events[i]
				next_head_event = events[i + 1]
				articulations = {type(a) for a in head_event.articulations}  # Set of articulation types for current event
				
				if lily.Glissando in articulations:

					# TODO precise articulations in grace event
					grace_event = Event()
					grace_event.name = head_event.name
					grace_event.comment_name = f'{head_event.name}-grace'
					grace_event.onset = head_event.onset + ONSET_GLISSANDO_OFFSET
					grace_event.dur = -head_event.dur
					grace_event.dyn = head_event.dyn
					grace_event.freq = next_head_event.freq
					grace_event.pitch = next_head_event.pitch
					grace_events.append((i + 1, grace_event))

					head_event.dur = -ONSET_GLISSANDO_OFFSET

					j = i + 1
					while j < len(events) - 1:
						mid_event = events[j]
						next_mid_event = events[j + 1]
						mid_articulations = {type(a) for a in mid_event.articulations}
						if lily.Glissando in mid_articulations:
							mid_event.dur *= -1
							mid_event.freq = next_mid_event.freq
							mid_event.pitch = next_mid_event.pitch
							j += 1
						elif lily.Tie in mid_articulations:
							mid_event.dur *= -1
							j += 1
						else:
							# stop at tail event
							break
					i = j

				elif lily.Tie in articulations:

					head_event.dur *= -1

					j = i + 1
					while j < len(events) - 1:
						mid_event = events[j]
						next_mid_event = events[j + 1]
						mid_articulations = {type(a) for a in mid_event.articulations}
						if lily.Glissando in mid_articulations:
							mid_event.dur *= -1
							mid_event.freq = next_mid_event.freq
							mid_event.pitch = next_mid_event.pitch
							j += 1
						elif lily.Tie in mid_articulations:
							mid_event.dur *= -1
							j += 1
						else:
							# stop at tail event
							break
					i = j
				else:
					i += 1

			for index, ghost_event in reversed(grace_events):
				events.insert(index, ghost_event)

