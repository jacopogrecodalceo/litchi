from numpy.random import normal

def humanize(events, value):
	for event in events:
		if not isinstance(event.onset, str):
			onset = event.onset * 4 + (normal(loc=0.0, scale=1/48) * value if event.onset > 0 else 0)
			event.onset = max(0, onset)
		if not isinstance(event.dur, str):
			dur = event.dur * 4 + normal(loc=0.0, scale=1/48) * humanize
			event.dur = dur
	return events