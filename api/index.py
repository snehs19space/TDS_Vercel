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
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # ✅ Enable CORS
            self.end_headers()

            # Correct path to students.json file
            current_dir = os.path.dirname(__file__)
            json_path = os.path.join(current_dir, '..', 'students.json')

            with open(json_path, 'r') as f:
                marks_data = json.load(f)

            # Parse query parameters
            query = parse_qs(urlparse(self.path).query)
            names = query.get('name', [])
            result = [marks_data.get(name, None) for name in names]

            self.wfile.write(json.dumps({"marks": result}).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
