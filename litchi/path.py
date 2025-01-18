import os

class LitchiPath:
	def __init__(self):
		self.project_main_file = __file__
		self.project_main_dir = os.path.dirname(self.project_main_file)
		self.project_name = os.path.basename(self.project_main_dir)
		self.build_dir = self.find_build()
		self.csound_dir = self.find_csound()
		self.stylesheet_dir = self.find_stylesheet()
		self.generate_build_paths()

	def find_build(self):
		build_dir = os.path.join(self.project_main_dir, 'build')
		if not os.path.exists(build_dir):
			os.makedirs(build_dir)
		return build_dir

	def find_csound(self):
		current_dir = self.project_main_dir
		for _ in range(2):
			current_dir = os.path.dirname(current_dir)
			if os.path.basename(current_dir) == 'csound':
				return current_dir
		raise ValueError('Csound directory not found')

	def find_stylesheet(self):
		stylesheet_dir = os.path.join(self.project_main_dir, 'stylesheet')
		if not os.path.exists(stylesheet_dir):
			raise ResourceWarning('.ily stylesheet not found')
		return stylesheet_dir

	def generate_build_paths(self):
		extensions = ['pdf', 'ly', 'sco', 'orc', 'wav']
		for ext in extensions:
			setattr(self, f'build_{ext}', os.path.join(self.build_dir, f'{self.project_name}.{ext}'))

	def generate_working_paths(self):
		dirs = ['material', 'segment']
		for d in dirs:
			setattr(self, f'{d}_dir', os.path.join(self.build_dir, d))