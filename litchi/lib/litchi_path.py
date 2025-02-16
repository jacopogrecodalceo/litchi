import os

class LitchiPath:
	def __init__(self, file, csound_dir=None, stylesheet_dir=None):
		self.project_main_file = file
		self.project_main_dir = os.path.dirname(self.project_main_file)
		self.project_name = os.path.basename(self.project_main_dir)
		
		self.find_build()
		
		self.generate_build()

		self.csound_dir = csound_dir
		if not self.csound_dir:
			self.csound_dir = self.find_dir('csound')
		
		self.stylesheet_dir = stylesheet_dir
		if not self.stylesheet_dir:
			self.stylesheet_dir = self.find_dir('stylesheet')


	def find_build(self):
		build_dir = os.path.join(self.project_main_dir, 'build')
		if not os.path.exists(build_dir):
			os.makedirs(build_dir)
		self.build_dir = build_dir

	def find_dir(self, string):
		current_dir = self.project_main_dir

		# Loop to search up to 3 levels up from the current directory
		for _ in range(5):
			# Scan the current directory
			try:
				with os.scandir(current_dir) as entries:
					for entry in entries:
						if entry.is_dir() and string in entry.name:
							# Exit the method once the directory is found
							return  entry.path
			except OSError as e:
				# Handle potential errors during directory scanning
				print(f"Error scanning directory {current_dir}: {e}")

			# Move up one directory level
			current_dir = os.path.dirname(current_dir)

		# Raise an error if the directory is not found after 3 levels
		raise ValueError('Directory not found')
	
	def generate_build(self):
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