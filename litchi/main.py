import importlib
import inspect

from litchi.lilypond.main import LitchiLilyPond
from litchi.csound.main import LitchiCsound

class Litchi:
	def __init__(self):
		self.csound = LitchiCsound()
		self.lilypond = LitchiLilyPond()
		# Dynamically import the module
		module = importlib.import_module('litchi.csound.score.operator')

		# Get all functions from the module
		functions = inspect.getmembers(module, inspect.isfunction)
		for name, func in functions:
			setattr(self, name, func)

