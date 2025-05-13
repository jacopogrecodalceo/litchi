import os
import abjad
import cairosvg
import io
from bezmerizing import Polyline
from matplotlib import colors
import shoebot


# Function Definitions
def draw_open_polyline(b, polyline, stroke_width=3):
	b.stroke(*colors.to_rgb('black'))
	b.fill(None)
	b.strokewidth(stroke_width)
	pts = polyline.vertices
	for i in range(len(pts) - 1):  # Do not connect start/end
		b.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])

def draw_pitches(b, polyline, index, pitches, events_space_y):

	pts = polyline.vertices
	b.fontsize(32)  # Adjust font size as needed
	b.fill(*colors.to_rgb('black'))  # Text color
	
	for pitch, (x, y) in zip(pitches, pts):
		# Draw a small circle at the point
		b.stroke(None)
		b.fill(*colors.to_rgb('purple'))  # Point color
		b.circle(x, y, 15)  # Point radius
		
		# Draw the index text next to the point
		b.fill(*colors.to_rgb('black'))
		b.text(str(pitch), x, y - 15)  # Offset the text slightly from the point
	b.text(f'{index}, {len(pitches) = }', 135, 95+events_space_y*index)  # Offset the text slightly from the point

def draw_cubic_interpolation(b, polyline):
	b.stroke(*colors.to_rgb('black'))
	b.fill(None)
	b.strokewidth(2)
	pts = polyline.vertices
	if len(pts) < 4:
		return

	b.beginpath(pts[0][0], pts[0][1])
	for i in range(1, len(pts) - 2, 1):
		x0, y0 = pts[i]
		x1, y1 = pts[i + 1]
		cx = (x0 + x1) / 2
		cy = (y0 + y1) / 2
		b.curveto(x0, y0, cx, cy, x1, y1)
	b.endpath()


def draw_catmull_rom(b, polyline, alpha=0.5):
	from math import pow, sqrt

	def tj(ti, pi, pj):
		d = sqrt((pj[0] - pi[0]) ** 2 + (pj[1] - pi[1]) ** 2)
		return pow(d, alpha) + ti

	def catmull_rom_to_bezier(p0, p1, p2, p3):
		return [
			p1,
			(
				p1[0] + (p2[0] - p0[0]) / 6,
				p1[1] + (p2[1] - p0[1]) / 6
			),
			(
				p2[0] - (p3[0] - p1[0]) / 6,
				p2[1] - (p3[1] - p1[1]) / 6
			),
			p2
		]

	b.stroke(*colors.to_rgb('black'))
	b.fill(None)
	b.strokewidth(2)
	pts = polyline.vertices
	if len(pts) < 4:
		return

	for i in range(len(pts) - 3):
		p0, p1, p2, p3 = pts[i:i + 4]
		cps = catmull_rom_to_bezier(p0, p1, p2, p3)
		b.beginpath(cps[0][0], cps[0][1])
		b.curveto(cps[1][0], cps[1][1], cps[2][0], cps[2][1], cps[3][0], cps[3][1])
		b.moveto(pts[-1][0], pts[-1][1])
		b.endpath()


def draw_quadratic_bezier_chain(b, polyline):
	b.stroke(*colors.to_rgb('black'))
	b.fill(None)
	b.strokewidth(2)
	pts = polyline.vertices
	if len(pts) < 3:
		return

	b.beginpath(pts[0][0], pts[0][1])
	for i in range(1, len(pts) - 1):
		p0 = pts[i]
		p1 = pts[i + 1]
		mid_x = (p0[0] + p1[0]) / 2
		mid_y = (p0[1] + p1[1]) / 2
		b.curveto(p0[0], p0[1], mid_x, mid_y, p1[0], p1[1])

	b.moveto(pts[-1][0], pts[-1][1])
		
	b.endpath()


def draw_smooth_bezier(b, polyline, stroke_width=3):
	b.stroke(*colors.to_rgb('black'))
	b.fill(None)
	b.strokewidth(stroke_width)
	pts = polyline.vertices
	if len(pts) < 3:
		return

	# Start drawing from the first point
	b.beginpath(pts[0][0], pts[0][1])

	# Draw Bézier curves for each point except the last one
	for i in range(1, len(pts) - 1):  # Stop before the last point
		x0, y0 = pts[i]
		x1, y1 = pts[i + 1]
		# Control points for smooth transition
		ctrl1 = ((x0 + x1) / 2, y0)
		ctrl2 = ((x0 + x1) / 2, y1)
		b.curveto(ctrl1[0], ctrl1[1], ctrl2[0], ctrl2[1], x1, y1)
	b.moveto(pts[-1][0], pts[-1][1])

	# End the path
	b.endpath()

# drawing params
width = 297 * 10
height = 210 * 10
margin = 95
usable_width = width - 2 * margin
usable_height = height - 2 * margin


def draw_from_nodes(node_events_raw, output_path):

	node_events = []
	for events in node_events_raw:
		node_events.append(sorted(events, key=lambda event: event.onset))

	events_space_y = usable_height / len(node_events)
	# find max onset and freq
	max_onset = max(event.onset + event.dur for group in node_events for event in group)
	max_freq = max(event.freq for group in node_events for event in group)

	# build polylines
	polys = []
	for index_events, events in enumerate(node_events):
		pitches = []
		points = []
		for event in events:
			x = margin + (event.onset / max_onset * usable_width)
			y = margin + (index_events * events_space_y) + ((max_freq - event.freq) / max_freq * events_space_y)
			coord = (x, y)
			points.append(coord)

			pitch = abjad.NamedPitch.from_hertz(float(event.freq)).name
			pitches.append(pitch)

		polys.append((pitches, Polyline(points)))
	#exit()
	# SVG buffer
	svg_data = io.BytesIO()
	b = shoebot.create_bot(buff=svg_data, format='svg')
	b.size(width, height)
	b.background(*colors.to_rgba('white'))
	# draw polylines
	for index, (pitches, poly) in enumerate(polys):
		assert len(pitches) == len(poly) // 2, f'{len(pitches) = }, {len(poly) =}'
		draw_open_polyline(b, poly)
		draw_pitches(b, poly, index, pitches, events_space_y)
		draw_smooth_bezier(b, poly)
		
	b.finish()
	svg_data.seek(0)
	svg_output = svg_data.read()

	# export PNG
	cairosvg.svg2png(bytestring=svg_output, write_to=output_path)


def draw_from_csound_score(csound_score_path, output_path):

	if not os.path.exists(csound_score_path):
		raise 'No score'
	
	score = []
	with open(csound_score_path, 'r') as f:
		lines = f.readlines()
		all_i_lines = [line for line in lines if line.startswith('i')]
		while lines:
			line = lines.pop(0)
			if line.startswith('staff index'):
				staff = []
				while lines:
					peek = lines[0]
					if peek.startswith('staff index'):
						break
					line = lines.pop(0)
					if line.startswith('i'):
						staff.append(line)
				score.append(staff)

	assert sum([len(staff) for staff in score]) == len(all_i_lines), 'u missing smthig'
	

	for staff in score:
		for line_index, line in enumerate(staff):
			parts = line.strip().split()
			converted = []
			for p in parts:
				if p.replace('.', '', 1).isdigit():  # handles floats
					converted.append(float(p))
				else:
					converted.append(p)
			staff[line_index] = converted
	#i "rod" 8.5 2.0 0.5303030303030303 0 317.77777777777777 1.002



	events_space_y = usable_height / len(score)

	# find max onset and freq
	# onset is #2
	# dur is #3
	# freq is #6
	max_onset = max(p[2] + p[3] for line in score for p in line)
	max_freq = max(p[6] for line in score for p in line)

	# build polylines
	polys = []
	for index_staff, line in enumerate(score):
		pitches = []
		points = []
		for p in line:
			onset = p[2]
			freq = p[6]
			x = margin + (onset / max_onset * usable_width)
			y = margin + (index_staff * events_space_y) + ((max_freq - freq) / max_freq * events_space_y)
			coord = (x, y)
			points.append(coord)

			pitch = abjad.NamedPitch.from_hertz(freq).name
			pitches.append(pitch)

		polys.append((pitches, Polyline(points)))
	#exit()
	# SVG buffer
	svg_data = io.BytesIO()
	b = shoebot.create_bot(buff=svg_data, format='svg')
	b.size(width, height)
	b.background(*colors.to_rgba('white'))
	# draw polylines
	for index, (pitches, poly) in enumerate(polys):
		assert len(pitches) == len(poly) // 2, f'{len(pitches) = }, {len(poly) =}'
		draw_open_polyline(b, poly)
		draw_pitches(b, poly, index, pitches, events_space_y)
		draw_smooth_bezier(b, poly)
		
	b.finish()
	svg_data.seek(0)
	svg_output = svg_data.read()

	# export PNG
	cairosvg.svg2png(bytestring=svg_output, write_to=output_path)

def draw(node_events_raw, path):
	draw_from_nodes(node_events_raw, f'{path.build}-from_nodes.png')
	draw_from_csound_score(path.build_sco, f'{path.build}-from_orc.png')