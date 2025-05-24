from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import os

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # ✅ CORS enabled
        self.end_headers()

        # Load JSON data
        json_path = os.path.join(os.path.dirname(__file__), '../students.json')
        with open(json_path, 'r') as f:
            marks_data = json.load(f)

        # Get ?name=... parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])
        result = [marks_data.get(name, None) for name in names]

        # Return JSON response
        self.wfile.write(json.dumps({ "marks": result }).encode())
