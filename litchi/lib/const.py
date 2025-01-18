import os
import json
from datetime import datetime 

DATE = datetime.today().strftime('%y%m%d-%H%M')

LILYPOND_OCTAVE_ADJUST = +3

METRIC_STAFF_SPACE_DIV = 8 # this means 1/8

ONSET_GLISSANDO_OFFSET = 1/64#.00125 #48 / 48000

with open(os.path.join(os.path.dirname(__file__), 'intervals.json'), 'r') as file:
    INTERVAL_NAMEs = json.load(file)

with open(os.path.join(os.path.dirname(__file__), 'scala.json'), 'r') as file:
    SCALA = json.load(file)

class Partial:
	def __init__(self):
		pass
