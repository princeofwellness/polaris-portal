import sys, os, json, urllib.parse
from http.server import BaseHTTPRequestHandler

# Project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cosmos.synthesis import SynthesisProfile
from generate_portal import generate


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path in ("/", "/index.html", ""):
            self._serve_index()
        elif parsed.path in ("/generate", "/api/generate") and params:
            self._generate(params)
        else:
            self._serve_index()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = urllib.parse.parse_qs(body)
        self._generate(params)

    def _serve_index(self):
        html_path = os.path.join(ROOT, "index.html")
        html = open(html_path).read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _generate(self, params):
        try:
            name = params.get("name", [""])[0]
            date = params.get("date", [""])[0]
            time_str = params.get("time", ["12:00"])[0]
            lat = float(params.get("lat", ["48.1486"])[0])
            lon = float(params.get("lon", ["17.1077"])[0])
            tz = params.get("tz", ["+00:00"])[0]
            birth_dt = f"{date}T{time_str}:00{tz}"

            profile = SynthesisProfile(name=name, birth_dt=birth_dt, lat=lat, lon=lon)
            html = generate(profile)

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f"<h2>Error</h2><p>{e}</p><a href='/'>Back</a>".encode())
