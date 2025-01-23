from datetime import datetime
import importlib
import os
import sys

import abjad
from flask import Flask, render_template, send_file
from flask_socketio import SocketIO
import logging

class LitchiServer:
    def __init__(self, path):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.path = path
        self.watched_main_file = path.project_main_file
        self.watched_files = [self.watched_main_file]
        self.reload_modules = ['material', 'segment']
        self.current_time = datetime.now().strftime("%H:%M:%S")
        self.html_template = 'index-pdf_frame.html'
        self.last_mtimes = {file: os.path.getmtime(file) for file in self.watched_files}
        self.shared_main = self.default_shared_main

        self.logger = logging.getLogger(__name__)

        self.setup_routes()

    def default_shared_main(self):
        """Default function to generate a PDF (in case the user doesn't have one)."""
        staff = abjad.Staff([abjad.Note("c'4")])
        abjad.persist.as_pdf(staff, self.path.build_pdf)

    def reload_module(self, module_name, file_path):
        try:
            if module_name in sys.modules:
                del sys.modules[module_name]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.logger.info(f"Reloaded module: {module_name}")
            return module
        except Exception as e:
            self.logger.error(f"Error reloading module: {module_name}: {e}")
            raise RuntimeError(f"Error reloading module: {module_name}: {e}")

    def reload_lib(self):
        try:
            for module_name in self.reload_modules:
                module = importlib.import_module(module_name)
                importlib.reload(module)
                self.logger.info(f"Reloaded module: {module_name}")
        except Exception as e:
            self.logger.error(f"Error reloading library: {e}")
            raise RuntimeError(f"Error reloading library: {module_name}: {e}")

    def reload(self):
        module_name = os.path.splitext(os.path.basename(self.watched_main_file))[0]
        try:
            self.reload_lib()
            main_module = self.reload_module(module_name, self.watched_main_file)
            self.shared_main = main_module.shared_main
        except Exception as e:
            print(f"Error reloading module: {e}")

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

    def watch_files(self, file_paths):
        print(f"Watching files: {file_paths}")
        while True:
            for file_path in file_paths:
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
                        print(f"Error reloading {file_path}: {e}")

            self.socketio.sleep(1)

    def run(self):
        """Start the Flask application with socketIO."""
        self.socketio.start_background_task(self.watch_files, self.watched_files)
        self.socketio.run(self.app, port=3000)

