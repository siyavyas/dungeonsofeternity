#!/usr/bin/env python3

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent.absolute()

# Define the port to run the server on
PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(script_dir), **kwargs)

    def end_headers(self):
        # Add CORS headers to allow loading resources
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Change to the script's directory
os.chdir(script_dir)

# Create and start the HTTP server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    print(f"Open your browser and navigate to http://localhost:{PORT}/standalone/game.html")
    
    # Automatically open the game in the default web browser
    webbrowser.open(f"http://localhost:{PORT}/standalone/game.html")
    
    # Keep the server running
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.") 