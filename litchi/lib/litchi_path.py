import os

class LitchiPath:
	def __init__(self, file):
		self.project_main_file = file
		self.project_main_dir = os.path.dirname(self.project_main_file)
		self.project_name = os.path.basename(self.project_main_dir)
		
		self.find_build()
		self.find_csound()
		self.find_stylesheet()

		self.generate_build_paths()

	def find_build(self):
		build_dir = os.path.join(self.project_main_dir, 'build')
		if not os.path.exists(build_dir):
			os.makedirs(build_dir)
		self.build_dir = build_dir

	def find_csound(self):
		current_dir = self.project_main_dir

		# Loop to search up to 3 levels up from the current directory
		for _ in range(3):
			# Scan the current directory
			with os.scandir(current_dir) as entries:
				for entry in entries:
					if entry.is_dir() and 'csound' in entry.name:
						self.csound_dir = entry.path
						return  # Exit the method once the directory is found

			# Move up one directory level
			current_dir = os.path.dirname(current_dir)

		# Raise an error if the directory is not found after 3 levels
		raise ValueError('Csound directory not found')
	
	def find_stylesheet(self):
		stylesheet_dir = os.path.join(self.project_main_dir, 'stylesheet')
		if not os.path.exists(stylesheet_dir):
			raise ResourceWarning('.ily stylesheet not found')
		self.stylesheet_dir = stylesheet_dir

	def generate_build_paths(self):
		extensions = ['pdf', 'ly', 'sco', 'orc', 'wav', 'log']
		for ext in extensions:
			setattr(self, f'build_{ext}', os.path.join(self.build_dir, f'{self.project_name}.{ext}'))

	def generate_working_paths(self):
		dirs = ['material', 'segment']
		for d in dirs:
			setattr(self, f'{d}_dir', os.path.join(self.build_dir, d))

	def show(self):
		for attribute in dir(self):
			if not attribute.startswith('__'):
				print(f'{attribute}: {getattr(self, attribute)}')