from numpy.random import normal

def humanize(node_events, depth: float):
	for events in node_events:
		for event in events:
			if not isinstance(event.onset, str):
				onset = event.onset
				onset += normal(loc=0.0, scale=1 / 48) * depth
				onset = max(0, abs(onset))
				event.onset = float(onset)

			if not isinstance(event.dur, str):
				dur = event.dur
				sign = 1 if dur > 0 else -1

				dur += normal(loc=0.0, scale=1 / 48) * depth
				dur = abs(dur) if sign == 1 else -abs(dur)

				event.dur = float(dur)

	return events