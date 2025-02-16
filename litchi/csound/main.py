import logging
from pathlib import Path
from litchi.csound.score.builder import CsoundScoreBuilder
from litchi.csound.player import CsoundPlayer

logging.basicConfig(level=logging.INFO)

class LitchiCsound:
	def __init__(self):
		self.orc_files = []
		self.csound_flags = []
		self.csound_orc: str = None
		self.flag_path = None

	# LOAD
	def load(self, path):
		path = Path(path)
		self.flag_path = path.parent / '_flags' if path.is_file() else path / '_flags'
		if path.is_dir():
			self.load_directory(path)
		elif path.is_file() and path.suffix == '.orc':
			self.load_file(path)

		self.read()

	def load_directory(self, path: Path):
		self.orc_files.extend(file for file in path.rglob('*.orc') if file.is_file())
		logging.info(f"Loaded ORC files from directory: {path}")

	def load_file(self, path: Path):
		self.orc_files.append(path)
		logging.info(f"Loaded ORC file: {path}")

	# BUILD
	def read(self):
		self.read_flag()
		self.read_orc()

	def read_flag(self):
		if self.flag_path and self.flag_path.exists():
			with self.flag_path.open('r') as f:
				self.csound_flags = [line.strip() for line in f if line.strip() and not line.startswith(';')]
			logging.info(f"Loaded flags from: {self.flag_path}")
		else:
			raise FileNotFoundError(f"Flag file not found: {self.flag_path}")

	def read_orc(self):
		orc_parts = ['; BEGINNING THE CONSTRUCTION OF THE ORCHESTRA\n']
		for orc in self.orc_files:
			if orc.exists():
				with orc.open('r') as f:
					orc_parts.append(f.read())
			else:
				raise FileNotFoundError(f"ORC file not found: {orc}")
		self.csound_orc = ''.join(orc_parts)
		logging.info("Read and concatenated ORC files")

	def process_events(self, node_events, node_tempi):
		self.dynamic_factor = len(node_events)
		builder = CsoundScoreBuilder(node_events, node_tempi)
		self.csound_score_dict = builder.create_score_as_dict()
		logging.info("Processed events and created score")

	def play(self, export_orchestra=None, export_wav=None, apply_dynamic_factor=True, export_score=None, export_stems=None):

		if apply_dynamic_factor:
			dyn_factor=self.dynamic_factor
		else:
			dyn_factor=1

		self.player = CsoundPlayer(
			csound_flags=self.csound_flags,
			csound_orchestra=self.csound_orc,
			csound_score_dict=self.csound_score_dict,
			export_orchestra=export_orchestra,
			dyn_factor=dyn_factor,
			export_wav=export_wav,
			export_stems=export_stems,
			export_score=export_score,
		)

		self.player.play()

		logging.info("Played Csound score")
