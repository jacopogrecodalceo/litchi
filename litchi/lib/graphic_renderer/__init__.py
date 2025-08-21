from litchi.lib.graphic_renderer.classes import PolylineParser

# Drawing parameters
width = 297 * 10
height = 210 * 10
margin = 75

def draw(node_events, path):
	polyline = PolylineParser((width, height), margin)

	polyline.from_node_events(node_events)
	polyline.export_all(f'{path.build}-all-from_nodes')
	polyline.export_score(f'{path.build}-score-from_nodes')

	polyline.from_csound_score(path.build_sco)
	polyline.export_score(f'{path.build}-score-from_csound')

__all__ = ['draw']
