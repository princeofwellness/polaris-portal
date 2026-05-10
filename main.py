"""
POLARIS Portal — FastAPI Backend
Generates four-system synthesis portals. Deploy to Railway.
"""

import sys, os
from pathlib import Path

# Ensure cosmos module is importable
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from cosmos.synthesis import SynthesisProfile
from cosmos.constants import SIGNS, ELEMENTS


app = FastAPI(title="POLARIS Portal", version="1.0.0")

# Load template
TEMPLATE = (ROOT / "portal_template.html").read_text()


def _sign_name(lon: float) -> str:
    s = SIGNS[int(lon / 30) + 1] if int(lon / 30) + 1 <= 12 else SIGNS[12]
    return s["name"]


def _sign_deg_min(lon: float) -> str:
    d = int(lon % 30)
    m = int((lon % 30 - d) * 60)
    return f"{d}°{m:02d}'"


def _aspect_symbol(name: str) -> str:
    symbols = {
        "conjunction": "☌", "opposition": "☍", "trine": "△", "square": "□",
        "sextile": "⚹", "quincunx": "⚻", "semisextile": "⚺",
        "semisquare": "∠", "sesquiquadrate": "⚼", "quintile": "Q", "biquintile": "bQ",
    }
    return symbols.get(name, name)


def build_portal(name: str, birth_dt: str, lat: float, lon: float) -> str:
    """Generate complete portal HTML from birth data."""
    profile = SynthesisProfile(name=name, birth_dt=birth_dt, lat=lat, lon=lon)
    a = profile.astrology.to_dict()
    n = profile.numerology.to_dict()
    cz = profile.chinese_zodiac.to_dict()

    # === ASTROLOGY ===
    asc_lon = a["angles"]["ascendant"]
    mc_lon = a["angles"]["midheaven"]
    sun = a["planets"]["SUN"]
    moon = a["planets"]["MOON"]
    sun_sign = sun["sign_info"]["sign_name"]
    moon_sign = moon["sign_info"]["sign_name"]
    asc_sign = _sign_name(asc_lon)

    subtitle = f"{sun_sign} Sun · {moon_sign} Moon · {asc_sign} Rising"

    planet_order = ["SUN","MOON","MERCURY","VENUS","MARS","JUPITER","SATURN","URANUS","NEPTUNE","PLUTO"]
    planet_table = ""
    for pn in planet_order:
        p = a["planets"].get(pn, {})
        si = p.get("sign_info", {})
        sd = int(si.get("degree", 0))
        sm = int((si.get("degree", 0) - sd) * 60)
        h = p.get("house", "?")
        planet_table += f'<tr><td class="planet-name">{pn}</td><td>{si.get("sign_name","")} {sd}°{sm:02d}\'</td><td>House {h}</td></tr>'

    house_table = ""
    for h in range(1, 13):
        lon = a["houses"]["cusps"].get(str(h), 0)
        sn = _sign_name(lon)
        sd = int(lon % 30)
        sm = int((lon % 30 - sd) * 60)
        label = ""
        if h == 1: label = " ASC"
        elif h == 4: label = " IC"
        elif h == 7: label = " DSC"
        elif h == 10: label = " MC"
        house_table += f'<tr><td>House {h}{label}</td><td>{sn} {sd}°{sm:02d}\'</td></tr>'

    elements_html = " ".join(
        f'<span class="elem-{e.lower()}">{e}: {a["elements"][e]}</span>' for e in ELEMENTS
    )

    aspects_html = ""
    for asp in a.get("aspects", [])[:12]:
        sym = _aspect_symbol(asp["aspect"])
        aspects_html += f'<div class="aspect-item"><span class="asp-sym">{sym}</span> {asp["planet1"]} — {asp["planet2"]} <span class="asp-orb">{asp["deviation"]:.2f}°</span></div>'

    # === HUMAN DESIGN ===
    gates_html = ""
    for pn in planet_order + ["CHIRON","NORTH_NODE","SOUTH_NODE"]:
        g = a.get("hd_gates", {}).get(pn, {})
        if g:
            gates_html += f'<div class="gate-chip"><span class="gate-num">Gate {g["gate"]}</span><span class="gate-line">.{g["line"]}</span></div>'

    # === NUMEROLOGY ===
    nc = n["core"]
    num_grid = ""
    for key in ["life_path", "destiny", "soul_urge", "personality", "maturity", "balance"]:
        d = nc[key]
        meaning_short = d.get("meaning", "")[:70]
        num_grid += f'<div class="num-card"><div class="num-value">{d["number"]}</div><div class="num-label">{key.replace("_"," ").title()}</div><div class="num-desc">{meaning_short}...</div></div>'

    karmic_html = ""
    if n.get("karmic_debts"):
        kd_list = ", ".join(f"Karmic Debt {k['number']} ({k['source']})" for k in n["karmic_debts"])
        karmic_html = f'<div class="card card-num" style="margin-top:12px;"><div class="card-label">Karmic Debts</div><p style="font-size:11px; color:var(--magenta);">{kd_list}</p></div>'

    # === CHINESE ZODIAC ===
    animal = cz["animal"]
    pillars = cz["four_pillars"]
    pillar_grid = ""
    for pname, pdata in pillars.items():
        pillar_grid += f'<div class="pillar-cell"><div class="p-label">{pname}</div><div class="p-stem">{pdata["stem"]}{pdata["branch"]}</div><div class="p-elem">{pdata["stem_element"]}/{pdata["branch_element"]}</div></div>'

    dm = cz["day_master"]
    eb = cz["element_balance"]
    element_bars = ""
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = eb["counts"].get(elem, 0)
        pct = count / 8 * 100
        element_bars += f'<div class="elem-bar"><span class="e-name">{elem}</span><span class="e-fill" style="width:{pct}%"></span><span class="e-count">{count}</span></div>'

    subs = {
        "{$name}": name,
        "{$subtitle}": subtitle,
        "{$planet_table}": planet_table,
        "{$house_table}": house_table,
        "{$elements_html}": elements_html,
        "{$dominant_elem}": a["dominant"]["element"],
        "{$dominant_mod}": a["dominant"]["modality"],
        "{$aspects_html}": aspects_html,
        "{$gates_html}": gates_html,
        "{$num_grid}": num_grid,
        "{$karmic_html}": karmic_html,
        "{$animal_chinese}": animal["chinese"],
        "{$animal_name}": animal["name"],
        "{$animal_element}": animal["element"],
        "{$animal_traits}": animal["traits"][:150],
        "{$pillar_grid}": pillar_grid,
        "{$day_master_stem}": dm["stem"],
        "{$day_master_elem}": dm["element"],
        "{$day_master_pol}": dm["polarity"],
        "{$element_bars}": element_bars,
        "{$lucky_elements}": ", ".join(eb["lucky"]),
        "{$astro_summary}": f"{sun_sign} {int(sun['sign_degree'])}° · {moon_sign} {int(moon['sign_degree'])}° · {asc_sign} {int(asc_lon%30)}° ASC",
        "{$life_path}": str(nc["life_path"]["number"]),
    }

    html = TEMPLATE
    for key, val in subs.items():
        html = html.replace(key, str(val))

    return html


@app.get("/", response_class=HTMLResponse)
async def index():
    return (ROOT / "index.html").read_text()


@app.post("/generate", response_class=HTMLResponse)
async def generate(
    name: str = Form(...),
    date: str = Form(...),
    time: str = Form("12:00"),
    lat: float = Form(48.1486),
    lon: float = Form(17.1077),
    tz: str = Form("+00:00"),
):
    birth_dt = f"{date}T{time}:00{tz}"
    try:
        html = build_portal(name, birth_dt, lat, lon)
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(
            content=f"<html><body style='background:#05050a;color:#ff2d95;font-family:sans-serif;padding:40px;'>"
                    f"<h2>Portal Error</h2><p>{e}</p><a href='/' style='color:#00e5ff;'>← Return</a></body></html>",
            status_code=500
        )


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "cosmos-engine"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
