from datetime import datetime
import importlib
import os
import sys

import abjad
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO

class LitchiServer:
	def __init__(self, path):
		self.app = Flask(__name__)
		self.socketio = SocketIO(self.app)

		self.path = path
		self.main_file = path.project_main_file
		self.watched_files = [self.main_file]
		self.reload_modules = ['material', 'segment']

		self.current_time = datetime.now().strftime("%H:%M:%S")
		self.html_template = 'index-pdf_frame.html'
		self.last_mtimes = {file: os.path.getmtime(file) for file in self.watched_files}
		self.shared_main = self.default_shared_main

		self.setup_routes()

	def default_shared_main(self):
		"""Default function to generate a PDF (in case the user doesn't have one)."""
		staff = abjad.Staff([abjad.Note("c'4")])
		abjad.persist.as_pdf(staff, self.path.build_pdf)

	def reload_main_module(self):
		try:
			module_name = os.path.splitext(os.path.basename(self.main_file))[0]

			if module_name in sys.modules:
				del sys.modules[module_name]
			spec = importlib.util.spec_from_file_location(module_name, self.main_file)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			self.main_module = module
		except Exception as e:
			raise RuntimeError(f"Error reloading main module: {module_name}: {e}")

	def reload_lib(self):
		try:
			for module_name in self.reload_modules:
				file_path = os.path.join(os.path.dirname(self.main_file), module_name, '__init__.py')
				spec = importlib.util.spec_from_file_location(module_name, file_path)
				module = importlib.util.module_from_spec(spec)
				sys.modules[module_name] = module
				spec.loader.exec_module(module)
		except Exception as e:
			raise RuntimeError(f"Error reloading library: {module_name}: {e}")

	def reload(self):
		try:
			self.reload_lib()
			self.reload_main_module()
			self.shared_main = self.main_module.shared_main
		except Exception as e:
			raise RuntimeError(f"Error reloading module: {e}")

	def setup_routes(self):
		@self.app.route('/')
		def display_pdf():
			"""Serve the main page with PDF view."""
			self.shared_main()  # Call the shared_main function to regenerate the PDF
			return render_template(self.html_template,
								   current_time=self.current_time,
								   pdf_file=self.path.build_pdf,
								   title="Dynamic PDF Score")

		@self.app.route(f'/{self.path.build_pdf}')
		def serve_pdf():
			"""Serve the dynamically generated PDF."""
			return send_file(self.path.build_pdf, mimetype='application/pdf')

		@self.socketio.on('connect')
		def handle_connect():
			print("Client connected")

	def watch_files(self):
		for file_path in self.watched_files:
			print(f"Watching file: {file_path}")

		while True:
			for file_path in self.watched_files:
				current_mtime = os.path.getmtime(file_path)
				if current_mtime != self.last_mtimes[file_path]:
					self.last_mtimes[file_path] = current_mtime
					print(f"File {file_path} changed at {datetime.now()}")
					try:
						self.reload()
						self.shared_main()
						self.socketio.emit('file_changed')
						break
					except Exception as e:
						raise RuntimeError(f"Error reloading {file_path}: {e}")

			self.socketio.sleep(1)

	def run(self):
		"""Start the Flask application with socketIO."""
		self.socketio.start_background_task(self.watch_files)
		self.socketio.run(self.app, port=3000)
