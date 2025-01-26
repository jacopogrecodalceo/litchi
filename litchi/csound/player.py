import ctcsound
import logging

class CsoundPlayer:
	def __init__(self, flags, orc, export_orchestra=False, dyn_factor=1, export_wav=False, export_stems=False):
		self.flags = flags
		self.orc = orc
		self.export_orchestra = export_orchestra
		self.dyn_factor = dyn_factor
		self.export_wav = export_wav
		self.export_stems = export_stems

	def init(self):
		logging.info("Initializing Csound")
		ctcsound.csoundInitialize(ctcsound.CSOUNDINIT_NO_ATEXIT | ctcsound.CSOUNDINIT_NO_SIGNAL_HANDLER)
		cs = ctcsound.Csound()
		self.set_csound_options(cs)
		return cs

	def set_csound_options(self, cs):
		logging.info("Setting Csound options")
		for flag in self.flags:
			cs.setOption(flag)
		cs.setOption('--limiter')

	def prepare_orchestra(self, cs):
		logging.info("Preparing orchestra")
		orc_prefix = f'giDYN init 1/{self.dyn_factor}\n'
		orc = orc_prefix + self.orc
		retval = cs.evalCode(orc)
		if retval != retval:  # NaN is not equal to itself
			raise ValueError('Error in orchestra')
		if self.export_orchestra:
			with open(self.export_orchestra, 'w') as f:
				f.write(orc)
		
		cs.compileOrc(orc)

	def play(self, csound_score):
		logging.info("Starting Csound playback")
		
		cs = self.init()

		if self.export_wav:
			print("Do you want to continue with the MAIN .wav export? (y/n)")
			user_input = input().strip().lower()
			if user_input != 'y':
				logging.info(f"Setting export option: {self.export_wav}")
				cs.setOption(f'-o{self.export_wav}')
			else:
				return
		
		if self.export_stems:
			print("Do you want to continue with the STEMs .wav export? (y/n)")
			user_input = input().strip().lower()
			if user_input != 'y':
				logging.info(f"Setting export option: {self.export_wav}")
				cs.setOption(f'-o{self.export_wav}')

				retval = cs.evalCode(orc)
				if retval != retval:  # NaN is not equal to itself
					raise ValueError('Error in orchestra')

				cs.readScore(csound_score)
				result = cs.start()
				if result == 0:
					self.perform_csound(cs)
				cs.cleanup()
				del cs
				return

			else:
				return


		self.prepare_orchestra(cs)
		cs.readScore(csound_score)
		result = cs.start()
		if result == 0:
			self.perform_csound(cs)
		cs.cleanup()
		del cs

	def perform_csound(self, cs):
		logging.info("Performing Csound")
		while cs.performKsmps() == 0:
			pass
