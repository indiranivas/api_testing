#!/usr/bin/env python3
"""
Telemetry System Web Server
Serves the dashboard and testing interface
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler that serves index.html for root requests"""

    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def log_message(self, format, *args):
        """Suppress verbose logging"""
        return

def main():
    print("=" * 70)
    print("TELEMETRY SYSTEM - WEB SERVER")
    print("=" * 70)

    # Get current directory
    current_dir = Path(__file__).parent

    # Check required files
    required_files = ["index.html", "dashboard.html", "test.html"]
    missing = []
    for file in required_files:
        if not (current_dir / file).exists():
            missing.append(file)

    if missing:
        print(f"\n✗ Error: Missing files: {', '.join(missing)}")
        print(f"   Directory: {current_dir}")
        sys.exit(1)

    print(f"\n📁 Directory: {current_dir}")
    print(f"✓ index.html (Landing page)")
    print(f"✓ test.html (Testing interface)")
    print(f"✓ dashboard.html (Monitoring dashboard)")

    # Start Python web server
    PORT = 8001
    print(f"\n🚀 Starting web server on http://localhost:{PORT}")
    print("   Press Ctrl+C to stop\n")

    try:
        # Change to the directory
        os.chdir(current_dir)

        # Create and start server
        server = HTTPServer(("127.0.0.1", PORT), MyHTTPRequestHandler)

        # Wait a moment then open browser
        time.sleep(0.5)

        # Open in browser
        home_url = f"http://localhost:{PORT}/"
        print(f"📱 Opening in your browser...")
        print(f"   🏠 Home:       {home_url}")
        print(f"   🧪 Testing:    {home_url}test.html")
        print(f"   📊 Dashboard:  {home_url}dashboard.html\n")

        webbrowser.open(home_url)

        # Keep running
        print("✓ Web server is running!")
        print("✓ Make sure FastAPI backend is running on port 8000:")
        print("  $ uvicorn main:app --reload\n")
        print("Press Ctrl+C to stop the server...\n")

        server.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✓ Shutting down...")
        server.shutdown()
        print("✓ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
