"""
Vercel Serverless Function — POLARIS Portal Generator
Takes POST form data, returns a full synthesis portal HTML page.
"""

import sys, os, json, urllib.parse
from http.server import BaseHTTPRequestHandler

# Add parent to path for cosmos module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cache the ephemeris path
EPHEMERIS_PATH = "/tmp/de421.bsp"

def ensure_ephemeris():
    """Find the JPL ephemeris file."""
    # Check bundled location first (included in Vercel deployment)
    bundled = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "de421.bsp")
    if os.path.exists(bundled):
        return bundled
    
    # Check /tmp 
    if os.path.exists("/tmp/de421.bsp"):
        return "/tmp/de421.bsp"
    
    # Check common paths
    for path in ["/tmp/hd-research/de421.bsp", "./de421.bsp"]:
        if os.path.exists(path):
            return path
    
    return bundled  # Will fail with clear error if not found


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Redirect to form."""
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_POST(self):
        """Handle portal generation."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            params = urllib.parse.parse_qs(body)

            name = params.get("name", [""])[0]
            date = params.get("date", [""])[0]
            time_str = params.get("time", ["12:00"])[0]
            lat = float(params.get("lat", ["48.1486"])[0])
            lon = float(params.get("lon", ["17.1077"])[0])
            tz = params.get("tz", ["+00:00"])[0]
            birth_dt = f"{date}T{time_str}:00{tz}"

            # Set ephemeris path
            os.environ["COSMOS_EPHEMERIS"] = ensure_ephemeris()

            from main import build_portal
            html = build_portal(name, birth_dt, lat, lon)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

        except Exception as e:
            import traceback
            err = traceback.format_exc()
            self.send_response(500)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"""<!DOCTYPE html>
<html><head><title>Error</title><style>
body{{background:#05050a;color:#ff2d95;font-family:sans-serif;padding:40px;}}
a{{color:#00e5ff;}}
</style></head><body>
<h2>Portal Generation Error</h2>
<pre style="font-size:11px;color:#6a6a80;">{err[-1000:]}</pre>
<p><a href="/">← Try again</a></p>
</body></html>""".encode())
