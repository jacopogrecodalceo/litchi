import abjad

def messa_di_voce(container, each=4, dynamic_cycle=[-5, -4, -3, -2, -1, 1, -2, -3, -4], offset=0):
	
	# Select pitched leaves (notes) from the container
	notes = abjad.select.logical_ties(container, pitched=True)

	length_cycle = len(dynamic_cycle)
	length_notes = len(notes)

	index = offset
	index_cycle = 0
	while index < length_notes:
		note = notes[index][0]
		# Get the current dynamic based on the cycle
		current_dynamic = abjad.Dynamic.dynamic_ordinal_to_dynamic_name(dynamic_cycle[index_cycle % length_cycle])
		abjad.attach(abjad.Dynamic(current_dynamic), note)

		if index + each >= length_notes:
			break
		# Determine direction for the hairpin
		direction = '<' if dynamic_cycle[index_cycle % length_cycle] < dynamic_cycle[(index_cycle + 1) % length_cycle] else '>'

		# Attach the hairpin
		hairpin = abjad.StartHairpin(direction)
		abjad.attach(hairpin, note)

		# Increment the index for the cycle
		index += each
		index_cycle += 1
	
