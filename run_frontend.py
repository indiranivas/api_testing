#!/usr/bin/env python3
"""
Frontend HTTP Server for Telemetry System

Serves static HTML files with CORS headers enabled.
Used for Render.com two-service deployment.

Run locally:
    python run_frontend.py

Run on Render:
    PORT=8000 python run_frontend.py
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Get port from environment or use default
PORT = int(os.getenv('PORT', 8000))

# Get the directory where this script is located
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

print(f"📁 Serving files from: {DIRECTORY}")
print(f"🔗 Frontend will be available at:")
print(f"   http://localhost:{PORT}/")
print(f"   http://localhost:{PORT}/test.html")
print(f"   http://localhost:{PORT}/dashboard.html")
print(f"\n✅ Frontend server started on port {PORT}")
print(f"Press Ctrl+C to stop\n")


class FrontendHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that:
    1. Serves files from the current directory
    2. Adds CORS headers for API calls
    3. Handles 404s by serving index.html (SPA support)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        """Add CORS headers to all responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        """Handle GET requests"""
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'

        try:
            return super().do_GET()
        except Exception as e:
            print(f"Error serving {self.path}: {e}")
            self.send_error(500, "Internal Server Error")

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Customize log output"""
        # Only log important messages
        if isinstance(args[0], str) and ('HTTP' in str(args[0]) or 'GET' in str(args[0]) or 'POST' in str(args[0])):
            print(f"[{self.log_date_time_string()}] {format % args}")


def run_frontend_server():
    """Start the frontend HTTP server"""
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), FrontendHTTPRequestHandler) as httpd:
            print(f"🚀 Server is running! Access at: http://localhost:{PORT}/\n")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48 or e.errno == 98:  # Port already in use
            print(f"❌ Error: Port {PORT} is already in use!")
            print(f"Try: lsof -i :{PORT}")
            sys.exit(1)
        raise
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    # Verify required files exist
    required_files = ['index.html', 'test.html', 'dashboard.html']
    missing_files = []

    for file in required_files:
        file_path = Path(DIRECTORY) / file
        if not file_path.exists():
            missing_files.append(file)

    if missing_files:
        print(f"⚠️  Warning: Missing files: {', '.join(missing_files)}")
        print(f"   These should be in: {DIRECTORY}")
        print(f"   Creating them is required before deployment.\n")

    # Start server
    run_frontend_server()
