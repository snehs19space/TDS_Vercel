from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
        self.end_headers()

        # Load the student marks from the JSON file
        json_path = os.path.join(os.path.dirname(__file__), '../students.json')
        with open(json_path, 'r') as f:
            marks_data = json.load(f)

        # Parse the query parameters
        query = parse_qs(urlparse(self.path).query)
        names = query.get('name', [])
        result = [marks_data.get(name, None) for name in names]

        # Send response
        self.wfile.write(json.dumps({ "marks": result }).encode())
