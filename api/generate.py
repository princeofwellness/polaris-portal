"""Vercel Serverless — POLARIS Portal Generator. GET /generate?name=...&date=...&time=...&lat=...&lon=...&tz=..."""

import sys, os, json, urllib.parse
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_ephemeris():
    bundled = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "de421.bsp")
    if os.path.exists(bundled): return bundled
    for p in ["/tmp/de421.bsp", "/tmp/hd-research/de421.bsp"]:
        if os.path.exists(p): return p
    return bundled

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/generate" and params:
            self._generate(params)
        else:
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

    def _generate(self, params):
        try:
            name = params.get("name", [""])[0]
            date = params.get("date", [""])[0]
            time_str = params.get("time", ["12:00"])[0]
            lat = float(params.get("lat", ["48.1486"])[0])
            lon = float(params.get("lon", ["17.1077"])[0])
            tz = params.get("tz", ["+00:00"])[0]
            
            if "/" in tz and not tz.startswith("+"):
                try:
                    import zoneinfo
                    from datetime import datetime as dt_mod
                    tz_info = zoneinfo.ZoneInfo(tz)
                    now = dt_mod.now(tz_info)
                    secs = now.utcoffset().total_seconds()
                    h = int(secs / 3600); m = int(abs(secs) % 3600 / 60)
                    sign = "+" if h >= 0 else "-"
                    tz = f"{sign}{abs(h):02d}:{m:02d}"
                except: tz = "+00:00"
            
            birth_dt = f"{date}T{time_str}:00{tz}"
            os.environ["COSMOS_EPHEMERIS"] = ensure_ephemeris()
            
            from main import build_portal
            html = build_portal(name, birth_dt, lat, lon)
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h2>Error</h2><pre>{traceback.format_exc()[-800:]}</pre><a href='/'>Back</a>".encode())
