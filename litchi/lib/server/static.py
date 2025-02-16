from flask import Flask, send_file, render_template_string
from flask_socketio import SocketIO, emit
import threading
import os

class LitchiStaticServer:
    def __init__(self, path):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)  # Initialize SocketIO
        self.path = path
        self.server_started = False
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def display_pdf():
            """Serve the main page with PDF view and auto-refresh."""
            pdf_filename = os.path.basename(self.path.build_pdf)
            return render_template_string(f'''
            <html>
            <head>
                <title>PDF Viewer</title>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
                <script type="text/javascript">
                    document.addEventListener("DOMContentLoaded", function() {{
                        var socket = io.connect('http://' + document.domain + ':' + location.port);
                        socket.on('refresh_page', function() {{
                            window.location.reload();
                        }});
                    }});
                </script>
            </head>
            <body>
                <iframe src="/pdf" width="100%" height="100%"></iframe>
            </body>
            </html>
            ''')

        @self.app.route('/pdf')
        def serve_pdf():
            """Serve the PDF file."""
            return send_file(self.path.build_pdf, mimetype='application/pdf')

    def run(self):
        """Run the Flask application in a separate thread."""
        def run_server():
            self.server_started = True

            # Emit the refresh event once when the server starts
            @self.socketio.on('connect')
            def handle_connect():
                if self.server_started:
                    emit('refresh_page')
                    self.server_started = False  # Ensure the event is emitted only once

            self.socketio.run(self.app, port=3000, debug=False, use_reloader=False)

        # Start the server in a daemon thread
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True  # Daemonize the thread so it stops when the main program exits
        server_thread.start()
