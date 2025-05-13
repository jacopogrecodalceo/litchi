import abjad
import cairosvg
import io
from bezmerizing import Polyline
from matplotlib import colors
import shoebot


# Function Definitions
def draw_open_polyline(b, polyline):
	b.stroke(*colors.to_rgb('black'))
	b.fill(None)
	b.strokewidth(3)
	pts = polyline.vertices
	for i in range(len(pts) - 1):  # Do not connect start/end
		b.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])


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


def draw_smooth_bezier(b, pitches, polyline, stroke_width=3):
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

	# Draw point indices
	if hasattr(b, 'fontnames'):
		b.fontnames = ['Andale Mono', 'Courier', 'monospace']  # Try available monospace fonts
	b.fontsize(32)  # Adjust font size as needed
	b.fill(*colors.to_rgb('black'))  # Text color
	for pitch, (x, y) in zip(pitches, pts):
		# Draw a small circle at the point
		b.stroke(None)
		b.fill(*colors.to_rgb('purple'))  # Point color
		b.circle(x, y-stroke_width, 15)  # Point radius
		
		# Draw the index text next to the point
		b.fill(*colors.to_rgb('black'))
		b.text(str(pitch), x, y - 15)  # Offset the text slightly from the point


def draw(node_events_raw):

	node_events = []
	for events in node_events_raw:
		node_events.append(sorted(events, key=lambda event: event.onset))

	# drawing params
	width = 297 * 10
	height = 210 * 10
	margin = 95

	usable_width = width - 2 * margin
	usable_height = height - 2 * margin
	events_space_y = usable_height / len(node_events)

	# find max onset and freq
	max_onset = max(event.onset for group in node_events for event in group)
	max_freq = max(event.freq for group in node_events for event in group)

	# build polylines
	polys = []
	for index_events, events in enumerate(node_events):
		pitches = []
		points = []
		for event in events:
			x = margin + (event.onset / max_onset * usable_width)
			y = margin + (index_events * events_space_y) + ((max_freq - event.freq) / max_freq * events_space_y)
			print(event.pitch)
			print(event.onset)
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
	for pitches, poly in polys:
		assert len(pitches) == len(poly) // 2, f'{len(pitches) = }, {len(poly) =}'
		draw_open_polyline(b, poly)
		draw_smooth_bezier(b, pitches, poly)
		
	b.finish()
	svg_data.seek(0)
	svg_output = svg_data.read()

	# export PNG
	cairosvg.svg2png(bytestring=svg_output, write_to="output.png")
