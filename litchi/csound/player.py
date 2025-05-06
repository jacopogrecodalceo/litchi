import ctcsound
import os
import shutil
import logging
from litchi.lib.const import SKIP_RENDER_IF_IN_NAME

class CsoundPlayer:
	def __init__(
		self,
		csound_flags,
		csound_orchestra,
		csound_score_dict,
		dyn_factor=1,
		message=True,
		export_orchestra=None,
		export_wav=None,
		export_stems=None,
		export_score=None,
	):
		
		self.csound_score_dict = csound_score_dict
		self.csound_flags = csound_flags
		self.csound_orchestra = csound_orchestra
		self.export_orchestra = export_orchestra
		self.message = message
		self.dyn_factor = dyn_factor
		self.export_wav = export_wav
		self.export_stems = export_stems
		self.export_score = export_score

	def init(self):
		logging.info("Initializing Csound")
		ctcsound.csoundInitialize(ctcsound.CSOUNDINIT_NO_ATEXIT | ctcsound.CSOUNDINIT_NO_SIGNAL_HANDLER)
		cs = ctcsound.Csound()
		if not self.message:
			cs.createMessageBuffer(self.message)
		self.set_csound_options(cs)
		return cs

	def set_csound_options(self, cs):
		logging.info("Setting Csound options")
		for flag in self.csound_flags:
			cs.setOption(flag)
		cs.setOption('--limiter')

	def prepare_main_score(self):
		"""
		convert from a dict to a multiline string
		"""
		csound_score_list = [self.csound_score_dict['t_statement']]

		for _, i_lines in self.csound_score_dict['i_statements'].items():
			csound_score_list.extend(i_lines)

		self.csound_score = '\n'.join(map(str, csound_score_list))
		if self.export_score:
			with open(self.export_score, 'w') as f:
				f.write(self.csound_score)

	""" def add_tempo_instrument(self) -> str:
		t_values = self.csound_score_dict['t_statement'].split()

		string = f'''
gktempo init {t_values[2]}		
	instr tempo_counter

gktempo linseg {", ".join(t_values[2:])}
printk2 floor(gktempo)
	endin
	alwayson("tempo_counter")

'''
		return string """

	def prepare_orchestra(self, cs):
		logging.info("Preparing orchestra")
		orc_prefix = f'giDYN init 1/{self.dyn_factor}\n'
		#orc_prefix += self.add_tempo_instrument()
		orc = orc_prefix + self.csound_orchestra
		retval = cs.evalCode(orc)
		if retval != retval:  # NaN is not equal to itself
			raise ValueError('Error in orchestra')
		if self.export_orchestra:
			with open(self.export_orchestra, 'w') as f:
				f.write(orc)
		
		cs.compileOrc(orc)

	def perform_csound(self, cs):
		logging.info("Performing Csound")
		while cs.performKsmps() == 0:
			pass

	def handle_wav_export(self):
		if self.confirm_export("MAIN .wav export"):
			cs = self.init()
			logging.info(f"Setting export option: {self.export_wav}")
			cs.setOption(f'-o{self.export_wav}')

			self.prepare_orchestra(cs)
			self.prepare_main_score()
			cs.readScore(self.csound_score)
			result = cs.start()
			if result == 0:
				self.perform_csound(cs)
			cs.cleanup()
			del cs
		else:
			cs.cleanup()
			del cs
			return False
		return True

	def handle_stems_export(self):
		if self.confirm_export("STEMs .wav export"):
			self.export_stems_wav()
		else:
			return True
		return False

	def confirm_export(self, export_type):
		user_input = input(f"Do you want to continue with the {export_type}? (y/n)").strip().lower()
		return user_input == 'y'

	def export_stems_wav(self):
		orc_prefix = f'giDYN init 1\n'
		csound_orchestra = orc_prefix + self.csound_orchestra
		assert os.path.isdir(self.export_stems), "Export stems is not a directory"
		build_dir = os.path.join(self.export_stems, 'stems')
		self.create_or_clear_directory(build_dir)

		for instrument_name_with_number, i_lines in self.csound_score_dict['i_statements'].items():
			instrument_name = instrument_name_with_number[3:]
			if any(string in instrument_name for string in SKIP_RENDER_IF_IN_NAME):
				continue

			instrument_directory = os.path.join(build_dir, instrument_name_with_number)
			os.mkdir(instrument_directory)

			csound_score_list = [self.csound_score_dict['t_statement']]
			csound_score_list.extend(i_lines)

			for another_instrument_name_with_number in self.csound_score_dict['i_statements'].keys():
				another_instrument_name = another_instrument_name_with_number[3:]
				if any(string in another_instrument_name for string in SKIP_RENDER_IF_IN_NAME) and instrument_name in another_instrument_name:
					csound_score_list.extend(self.csound_score_dict['i_statements'][another_instrument_name_with_number])

			csound_score = '\n'.join(map(str, csound_score_list))
			score_path = os.path.join(instrument_directory, f'{instrument_name_with_number}.sco')
			with open(score_path, 'w') as f:
				f.write(csound_score)

			wav_path = os.path.join(instrument_directory, f'{instrument_name_with_number}.wav')

			cs = self.init()
			cs.setOption(f'-o{wav_path}')

			cs.compileOrc(csound_orchestra)
			cs.readScore(csound_score)
			result = cs.start()
			if result == 0:
				self.perform_csound(cs)
			cs.reset()
		cs.cleanup()
		del cs

	def create_or_clear_directory(self, directory):
		if not os.path.exists(directory):
			os.mkdir(directory)
		else:
			shutil.rmtree(directory)
			os.mkdir(directory)

	def play(self):
		logging.info("Starting Csound playback")

		if self.export_wav:
			self.handle_wav_export()
			return

		if self.export_stems:
			self.handle_stems_export()
			return

		cs = self.init()
		self.prepare_orchestra(cs)
		self.prepare_main_score()
		cs.readScore(self.csound_score)
		result = cs.start()
		if result == 0:
			self.perform_csound(cs)
		cs.cleanup()
		del cs
