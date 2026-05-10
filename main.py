"""
POLARIS Portal v2 — Enhanced synthesis generator.
Oracle narrative, cross-system correlations, interpretive depth, sacred geometry, animations.
"""

import sys, os, math
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from cosmos.synthesis import SynthesisProfile
from cosmos.constants import SIGNS, ELEMENTS, PLANETS, ASPECTS

# === PLANET INTERPRETATIONS BY SIGN ===
PLANET_SIGN_MEANINGS = {
    ("SUN", "Aries"): "You lead with fire. Identity forged in action.",
    ("SUN", "Taurus"): "You build slowly and permanently. Worth is felt, not argued.",
    ("SUN", "Gemini"): "You think yourself into existence. Words are your mirror.",
    ("SUN", "Cancer"): "You feel the world before you name it. Home is the compass.",
    ("SUN", "Leo"): "You radiate. Your presence is the gift.",
    ("SUN", "Virgo"): "You refine. Precision is your love language.",
    ("SUN", "Libra"): "You balance. Relationship is the lens through which you see yourself.",
    ("SUN", "Scorpio"): "You transform. Depth is not optional — it's the only way in.",
    ("SUN", "Sagittarius"): "You quest. The horizon is home.",
    ("SUN", "Capricorn"): "You climb. Time is your ally, not your enemy.",
    ("SUN", "Aquarius"): "You see the future. Systems are your canvas.",
    ("SUN", "Pisces"): "You dissolve boundaries. The dream is as real as the flesh.",
    ("MOON", "Aries"): "Emotions are immediate, fiery, quick to rise and release.",
    ("MOON", "Taurus"): "Emotional security through stability. You need to feel safe to feel anything.",
    ("MOON", "Gemini"): "Emotions processed through words. You need to talk it out.",
    ("MOON", "Cancer"): "This is home. Cancer Moon feels everything — the gift and the weight.",
    ("MOON", "Leo"): "Emotions are dramatic, generous, meant to be expressed openly.",
    ("MOON", "Virgo"): "Emotional processing through analysis. You fix feelings by understanding them.",
    ("MOON", "Libra"): "Emotional equilibrium through relationship. You feel through others.",
    ("MOON", "Scorpio"): "Emotions run deep, intense, transformative. Nothing is surface.",
    ("MOON", "Sagittarius"): "Emotional freedom. Adventure heals. Optimism is the default.",
    ("MOON", "Capricorn"): "Emotions are private, earned. Vulnerability is built over time.",
    ("MOON", "Aquarius"): "Emotions processed through intellect. You care about everyone in theory.",
    ("MOON", "Pisces"): "Emotions are oceanic. You absorb the world's feelings as your own.",
}

# === RISING SIGN INTERPRETATIONS ===
RISING_MEANINGS = {
    "Aries": "The world meets a pioneer. You arrive first, figure it out later. Mars energy — direct, unapologetic, initiating. People feel your presence before you speak.",
    "Taurus": "The world meets solid ground. You arrive slowly, stay long. Venus energy — sensuous, steady, unmovable once decided. People feel calmed by your presence.",
    "Gemini": "The world meets a question. You arrive curious, leave with stories. Mercury energy — quick, witty, adaptable. People feel engaged, never bored, slightly breathless.",
    "Cancer": "The world meets a shell that holds an ocean. You arrive protecting something soft. Moon energy — nurturing, intuitive, defensive of what's precious. People feel mothered or guarded, sometimes both.",
    "Leo": "The world meets the sun. You arrive radiating. Solar energy — warm, generous, impossible to ignore. People feel seen, or they feel overshadowed. Both are true.",
    "Virgo": "The world meets precision. You arrive noticing what others missed. Mercury energy — discerning, helpful, quietly brilliant. People feel analyzed, then grateful.",
    "Libra": "The world meets grace. You arrive seeking equilibrium. Venus energy — diplomatic, aesthetic, relationship-oriented. People feel harmonized, or they feel the weight of your unspoken needs.",
    "Scorpio": "The world meets depth. You arrive reading what's beneath. Pluto energy — intense, perceptive, transformative. People feel naked, or they feel truly seen for the first time.",
    "Sagittarius": "The world meets a arrow in flight. You arrive already leaving. Jupiter energy — expansive, optimistic, truth-seeking. People feel inspired, or left behind. Neither is intentional.",
    "Capricorn": "The world meets competence. You arrive with a plan. Saturn energy — disciplined, ambitious, earned. People feel slightly intimidated, then impressed, then reliant.",
    "Aquarius": "The world meets the future. You arrive from somewhere else. Uranus energy — innovative, detached, visionary. People feel intrigued, sometimes confused, never bored.",
    "Pisces": "The world meets the dream. You arrive half-elsewhere. Neptune energy — compassionate, artistic, boundaryless. People feel understood without words, or they feel you slipping through their fingers.",
}

# === LIFE PATH + PLANET CORRELATION ===
LP_PLANET = {
    1: ("Sun", "The Leader's fire. You are here to initiate, to stand alone, to become the authority of your own life."),
    2: ("Moon", "The Diplomat's intuition. You are here to harmonize, to partner, to feel the invisible threads between people."),
    3: ("Jupiter", "The Creator's expansion. You are here to express, to communicate, to turn joy into form."),
    4: ("Saturn", "The Builder's foundation. You are here to construct, to discipline, to make something that outlasts you."),
    5: ("Mercury", "The Adventurer's freedom. You are here to change, to explore, to gather experiences like currency."),
    6: ("Venus", "The Nurturer's love. You are here to serve, to harmonize, to create beauty that heals."),
    7: ("Uranus", "The Seeker's vision. You are here to question, to analyze, to pierce through illusion to truth."),
    8: ("Pluto", "The Powerhouse's depth. You are here to master, to transform, to wield influence wisely."),
    9: ("Neptune", "The Humanitarian's compassion. You are here to complete, to release, to love universally."),
    11: ("Uranus+Neptune", "The Master Intuitive. You are here to channel — light, ideas, healing. The veil is thin for you."),
    22: ("Saturn+Jupiter", "The Master Builder. You are here to manifest at scale. What you dream, you can construct."),
    33: ("Neptune+Venus", "The Master Teacher. You are here to serve through love made visible."),
}

# === FIVE ELEMENT MEANINGS ===
ELEMENT_MEANING = {
    "Wood": "Growth, expansion, vision, flexibility. Wood types pioneer and push upward.",
    "Fire": "Passion, transformation, expression, warmth. Fire types ignite and inspire.",
    "Earth": "Stability, nourishment, grounding, patience. Earth types build and sustain.",
    "Metal": "Structure, precision, refinement, integrity. Metal types define and perfect.",
    "Water": "Wisdom, depth, adaptability, flow. Water types intuit and connect.",
}


def _sign_name(lon: float) -> str:
    s = SIGNS[int(lon / 30) + 1] if int(lon / 30) + 1 <= 12 else SIGNS[12]
    return s["name"]


def _sign_from_num(n: int) -> str:
    return SIGNS[n]["name"] if 1 <= n <= 12 else ""


def _deg_min(lon: float) -> str:
    d = int(lon % 30); m = int((lon % 30 - d) * 60)
    return f"{d}°{m:02d}'"


def _aspect_sym(name: str) -> str:
    return {"conjunction":"☌","opposition":"☍","trine":"△","square":"□","sextile":"⚹","quincunx":"⚻","semisextile":"⚺","semisquare":"∠","sesquiquadrate":"⚼","quintile":"Q","biquintile":"bQ"}.get(name, name)


def _planet_meaning(planet: str, sign_name: str) -> str:
    key = (planet, sign_name)
    if key in PLANET_SIGN_MEANINGS:
        return PLANET_SIGN_MEANINGS[key]
    # Generic fallbacks
    generic = {
        "MERCURY": f"Your mind operates through {sign_name} — {SIGNS[[s for s in SIGNS if SIGNS[s]['name']==sign_name][0]]['element']} thinking, {SIGNS[[s for s in SIGNS if SIGNS[s]['name']==sign_name][0]]['modality']} processing.",
        "VENUS": f"You value {sign_name} qualities — this is how you love, spend, and appreciate beauty.",
        "MARS": f"Your drive expresses through {sign_name} — this is how you fight, assert, and pursue.",
        "JUPITER": f"Your expansion follows {sign_name} patterns — this is how you grow and find meaning.",
        "SATURN": f"Your discipline is shaped by {sign_name} — this is how you structure, limit, and master.",
        "URANUS": f"Your revolution wears {sign_name} colors — this is how you break through and innovate.",
        "NEPTUNE": f"Your spirituality flows through {sign_name} — this is how you dissolve, dream, and transcend.",
        "PLUTO": f"Your transformation follows {sign_name} logic — this is how you destroy, rebirth, and empower.",
    }
    return generic.get(planet, f"{sign_name} energy shapes this planet's expression.")


def _generate_oracle(name: str, sun_sign: str, moon_sign: str, asc_sign: str, 
                      animal: dict, lp: int, lp_planet: str, day_master: dict,
                      asc_meaning: str, dominant_elem: str, saturn_pluto: bool) -> str:
    """Generate the Oracle synthesis paragraph."""
    lines = []
    lines.append(f"You came through the {animal['name']} gate — {animal['element']} soul, {animal['chinese']} spirit.")
    
    if sun_sign == "Pisces":
        lines.append(f"Your {sun_sign} Sun dissolves at the anaretic degree — already becoming the next thing while still being this one. Identity is not fixed; it is weather.")
    else:
        lines.append(f"Your {sun_sign} Sun shapes your core identity through the lens of {SIGNS[[s for s in SIGNS if SIGNS[s]['name']==sun_sign][0]]['element']} — {SIGNS[[s for s in SIGNS if SIGNS[s]['name']==sun_sign][0]]['modality']} and unwavering in its essence.")
    
    lines.append(f"The {moon_sign} Moon is your private truth — emotions that run deep, felt before they're named, processed in solitude before they're shared.")
    
    if asc_meaning:
        lines.append(asc_meaning.split(".")[0] + ".")
    
    lines.append(f"Life Path {lp} aligns with {lp_planet} energy. ")
    
    lp_meanings = {
        4: "You are not here for quick wins. You are here to build foundations — in yourself, in your work, in the people who find shelter in what you construct.",
        1: "You are here to lead. Not to follow, not to blend — to carve a path that only you can walk.",
        5: "Freedom is not a luxury for you; it is the only mode in which you can breathe.",
        3: "Expression is your medicine. Communication is your gift. Joy is your compass.",
        7: "You seek what others overlook. Truth is not given to you — it is excavated.",
        9: "Completion is your theme. You are here to finish things — cycles, patterns, karmic debts.",
        11: "The veil is thin for you. You receive what others cannot see. Your task is to trust the transmission.",
        22: "What you dream, you can build. The scale of your vision is not hubris — it is accurate.",
        33: "Your love is a teaching. Your presence is a healing. You serve by being fully who you are.",
    }
    if lp in lp_meanings:
        lines.append(lp_meanings[lp])
    
    dm_elem = day_master.get("element", "")
    dm_stem = day_master.get("stem", "")
    if dm_elem:
        elem_desc = ELEMENT_MEANING.get(dm_elem, "")
        lines.append(f"Your Day Master is {dm_stem} {dm_elem} — {elem_desc.split('.')[0].lower()}. In the Ba Zi, this is the core self: how you meet the world at the deepest level.")
    
    if dominant_elem == "Air":
        lines.append("Air dominates your Western chart — you think before you feel, you analyze before you act. But the Chinese pillars tell a different story: your elemental balance reveals what the astrology hides.")
    
    if saturn_pluto:
        lines.append("Saturn and Pluto are in perfect conversation — discipline and transformation are not enemies in your chart. They are the same motion. Every structure you build transforms you. Every death feeds a rebirth. The Phoenix is not your myth. It is your method.")
    
    return "\n\n".join(lines)


def _cross_element_analysis(astro_elements: dict, cz_elements: dict, cz_lucky: list, cz_missing: list) -> str:
    """Generate cross-system element analysis."""
    parts = []
    
    shared_strong = [e for e in astro_elements if astro_elements[e] >= 2 and cz_elements.get(e, 0) >= 2]
    shared_weak = [e for e in astro_elements if astro_elements[e] <= 1 and cz_elements.get(e, 0) <= 1]
    astro_strong_cz_weak = [e for e in astro_elements if astro_elements[e] >= 2 and cz_elements.get(e, 0) <= 1]
    
    if shared_strong:
        parts.append(f"Both systems agree: <strong>{', '.join(shared_strong)}</strong> is strong in your design. "
                     f"This element defines you across traditions — a rare convergence that amplifies its influence.")
    if astro_strong_cz_weak:
        parts.append(f"A tension exists: <strong>{', '.join(astro_strong_cz_weak)}</strong> dominates your Western chart but is weak or absent in your Chinese pillars. "
                     f"Your conscious personality expresses this element, but your deeper energetic structure lacks its grounding. This can create a feeling of being '{', '.join(astro_strong_cz_weak)}' on the surface but something else underneath.")
    if cz_missing:
        parts.append(f"Your Ba Zi reveals missing elements: <strong>{', '.join(cz_missing)}</strong>. "
                     f"{' '.join(ELEMENT_MEANING.get(e, '').split('.')[0] + '.' for e in cz_missing)} "
                     f"Your lucky elements — <strong>{', '.join(cz_lucky)}</strong> — are the energies to cultivate.")
    
    return "<br><br>".join(parts) if parts else ""


def build_portal(name: str, birth_dt: str, lat: float, lon: float) -> str:
    """Generate complete enhanced portal HTML."""
    profile = SynthesisProfile(name=name, birth_dt=birth_dt, lat=lat, lon=lon)
    a = profile.astrology.to_dict()
    n = profile.numerology.to_dict()
    cz = profile.chinese_zodiac.to_dict()
    
    # === QUICK REFS ===
    asc_lon = a["angles"]["ascendant"]
    asc_sign = _sign_name(asc_lon)
    sun = a["planets"]["SUN"]
    moon = a["planets"]["MOON"]
    sun_sign = sun["sign_info"]["sign_name"]
    moon_sign = moon["sign_info"]["sign_name"]
    
    # === ORACLE ===
    lp = n["core"]["life_path"]["number"]
    lp_data = LP_PLANET.get(lp, ("Unknown", ""))
    saturn_pluto_tight = False
    for asp in a.get("aspects", []):
        p1, p2 = asp.get("planet1",""), asp.get("planet2","")
        if (("SATURN" in p1 and "PLUTO" in p2) or ("SATURN" in p2 and "PLUTO" in p1)):
            if asp.get("deviation", 999) < 0.5:
                saturn_pluto_tight = True
                break
    
    animal = cz["animal"]
    dm = cz["day_master"]
    asc_meaning = RISING_MEANINGS.get(asc_sign, "")
    
    oracle_text = _generate_oracle(name, sun_sign, moon_sign, asc_sign, animal, lp, lp_data[0], dm, asc_meaning, a["dominant"]["element"], saturn_pluto_tight)
    
    # === PLANET TABLE ===
    planet_order = ["SUN","MOON","MERCURY","VENUS","MARS","JUPITER","SATURN","URANUS","NEPTUNE","PLUTO"]
    planet_rows = ""
    for pn in planet_order:
        p = a["planets"].get(pn, {})
        si = p.get("sign_info", {})
        sn = si.get("sign_name", "")
        sd = int(si.get("degree", 0))
        sm = int((si.get("degree", 0) - sd) * 60)
        h = p.get("house", "?")
        meaning = _planet_meaning(pn, sn)
        planet_rows += f"""<tr>
          <td class="planet-name">{pn}</td>
          <td>{sn} {sd}°{sm:02d}'</td>
          <td>House {h}</td>
          <td class="planet-meaning">{meaning}</td>
        </tr>"""
    
    # === HOUSE TABLE ===
    house_rows = ""
    for h in range(1, 13):
        lon = a["houses"]["cusps"].get(str(h), 0)
        sn = _sign_name(lon)
        sd = int(lon % 30); sm = int((lon % 30 - sd) * 60)
        label = {1:"ASC",4:"IC",7:"DSC",10:"MC"}.get(h,"")
        label_html = f'<span class="angle-tag">{label}</span>' if label else ""
        house_rows += f'<tr><td>{h}{label_html}</td><td>{sn} {sd}°{sm:02d}\'</td></tr>'
    
    # === ELEMENTS ===
    elements_html = " ".join(
        f'<span class="elem-tag elem-{e.lower()}">{e} {a["elements"][e]}</span>' for e in ELEMENTS
    )
    
    # === ASPECTS ===
    aspects_html = ""
    for asp in a.get("aspects", [])[:15]:
        cls = "aspect-tight" if asp["deviation"] < 1.0 else ""
        aspects_html += f'<div class="aspect-item {cls}"><span class="asp-sym">{_aspect_sym(asp["aspect"])}</span> {asp["planet1"]} – {asp["planet2"]} <span class="asp-orb">{asp["deviation"]:.2f}°</span></div>'
    
    # === HD GATES ===
    gate_meanings = {
        34: "Raw life force. Sacral power.", 55: "Spirit. Emotional depth. The Phoenix.",
        20: "Presence. The now. Contemplation.", 59: "Intimacy. Breaking barriers.",
        49: "Revolution. Reform. Principled change.", 41: "New cycles. Letting go to begin.",
        18: "Correction. Pattern recognition.", 28: "Meaning. Existential struggle.",
        60: "Limitation as doorway. Acceptance.", 5: "Fixed rhythms. Patience.",
        61: "Inner truth. Knowing the unknowable.",
    }
    # === HD GATES (sorted by zodiacal degree) ===
    # Build list of (planet, gate, line, longitude) tuples, sort by longitude
    gate_entries = []
    for pn in planet_order + ["CHIRON","NORTH_NODE","SOUTH_NODE"]:
        g = a.get("hd_gates", {}).get(pn, {})
        if g:
            p = a["planets"].get(pn, {})
            lon = p.get("longitude", 0)
            gm = gate_meanings.get(g["gate"], "")
            gate_entries.append((pn, g["gate"], g["line"], lon, gm))
    
    # Sort by zodiacal longitude (0° = Gate 41, Aries)
    gate_entries.sort(key=lambda x: x[3])
    
    gates_html = ""
    for pn, gate_num, gate_line, lon, gm in gate_entries:
        sign = _sign_name(lon)
        gates_html += f'<div class="gate-chip"><span class="gate-num">Gate {gate_num}</span><span class="gate-line">.{gate_line}</span><span class="gate-planet">{pn}</span><span class="gate-sign">{sign}</span><span class="gate-meaning">{gm}</span></div>'
    
    # === NUMEROLOGY ===
    nc = n["core"]
    num_cards = ""
    for key in ["life_path", "destiny", "soul_urge", "personality", "maturity"]:
        d = nc[key]
        label = key.replace("_", " ").title()
        meaning = d.get("meaning", "")
        # Shorten meaning for the card
        short = meaning.split("—")[0].strip() if "—" in meaning else meaning[:60]
        num_cards += f"""<div class="num-card">
          <div class="num-value">{d["number"]}</div>
          <div class="num-label">{label}</div>
          <div class="num-desc">{short}</div>
        </div>"""
    
    # Add personalized LP interpretation
    lp_interpretation = f"""<div class="card card-num" style="margin-top:12px;">
      <div class="card-label">Life Path {lp} — {lp_data[0]} Energy</div>
      <p class="card-text">{lp_data[1]}</p>
    </div>"""
    
    # Karmic debts
    karmic_html = ""
    if n.get("karmic_debts"):
        kd = n["karmic_debts"]
        kd_parts = [f"KD {k['number']} ({k['source']})" for k in kd]
        kd_str = " · ".join(kd_parts)
        karmic_html = f'<div class="card card-num" style="margin-top:8px;"><div class="card-label">Karmic Debts</div><p class="card-text" style="color:var(--magenta);">{kd_str}</p></div>'
    
    # === CHINESE ZODIAC ===
    pillars = cz["four_pillars"]
    pillar_grid = ""
    for pname in ["year", "month", "day", "hour"]:
        pdata = pillars[pname]
        pillar_grid += f"""<div class="pillar-cell">
          <div class="p-label">{pname}</div>
          <div class="p-stem">{pdata["stem"]}{pdata["branch"]}</div>
          <div class="p-elem">{pdata["stem_element"]} {pdata["stem_polarity"]} / {pdata["branch_element"]}</div>
        </div>"""
    
    # Element bars
    eb = cz["element_balance"]
    element_bars = ""
    elem_colors = {"Wood":"#76ff03","Fire":"#ff5252","Earth":"#ff9100","Metal":"#e0e0e0","Water":"#448aff"}
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = eb["counts"].get(elem, 0)
        pct = count / 8 * 100
        color = elem_colors.get(elem, "#fff")
        element_bars += f'<div class="elem-bar"><span class="e-name">{elem}</span><div class="e-track"><div class="e-fill" style="width:{pct}%;background:{color};"></div></div><span class="e-count">{count}/8</span></div>'
    
    # Cross-element analysis
    cross_elem = _cross_element_analysis(a["elements"], cz["element_balance"]["counts"], 
                                          cz["element_balance"]["lucky"], cz["element_balance"]["missing"])
    
    # === RISING SIGN DEEP DIVE ===
    rising_block = f"""<div class="card card-astro">
      <div class="card-label">Rising Sign — {asc_sign}</div>
      <p class="card-text">{asc_meaning}</p>
    </div>"""
    
    # === CHINESE ZODIAC ANIMAL DEEP ===
    cz_hero = f"""<div class="cz-hero">
      <div class="cz-animal-name">{animal['chinese']} {animal['name']}</div>
      <div class="cz-element-tag">{animal['element']}</div>
      <p class="cz-desc">{animal['traits']}</p>
      <p class="cz-meta">Trine: {animal['trine']} · Opposite: {animal['opposite']} · Season: {animal['season']}</p>
    </div>"""
    
    day_master_block = f"""<div class="card card-cz" style="text-align:center;margin-top:12px;">
      <div class="card-label">Day Master</div>
      <p style="font-size:18px;color:var(--amber);font-weight:300;">{dm['stem']} ({dm['element']} {dm['polarity']})</p>
      <p class="card-text" style="max-width:500px;margin:8px auto 0;">{ELEMENT_MEANING.get(dm['element'], '')}</p>
    </div>"""
    
    # === BUILD HTML ===
    subtitle = f"{sun_sign} Sun · {moon_sign} Moon · {asc_sign} Rising · {animal['name']} Spirit"
    
    # Read template and substitute
    template = (ROOT / "portal_template.html").read_text()
    
    subs = {
        "{$NAME}": name,
        "{$SUBTITLE}": subtitle,
        "{$ORACLE}": oracle_text.replace("\n", "<br>"),
        "{$PLANET_ROWS}": planet_rows,
        "{$HOUSE_ROWS}": house_rows,
        "{$ASC_SIGN}": asc_sign,
        "{$MC_SIGN}": _sign_name(a["angles"]["midheaven"]),
        "{$ASC_POS}": _deg_min(asc_lon),
        "{$MC_POS}": _deg_min(a["angles"]["midheaven"]),
        "{$RISING_BLOCK_TEXT}": asc_meaning,
        "{$ELEMENTS}": elements_html,
        "{$DOM_ELEM}": a["dominant"]["element"],
        "{$DOM_MOD}": a["dominant"]["modality"],
        "{$ASPECTS}": aspects_html,
        "{$GATES}": gates_html,
        "{$NUM_CARDS}": num_cards,
        "{$LP_INTERP}": lp_interpretation,
        "{$KARMIC}": karmic_html,
        "{$CZ_HERO}": cz_hero,
        "{$PILLARS}": pillar_grid,
        "{$DAY_MASTER_BLOCK}": day_master_block,
        "{$ELEMENT_BARS}": element_bars,
        "{$LUCKY}": ", ".join(eb["lucky"]),
        "{$CROSS_ELEMENTS_BLOCK}": f'<div class="card card-cz"><div class="card-label">Cross-System Element Analysis</div><div class="cross-element">{cross_elem}</div></div>' if cross_elem else "",
    }
    
    html = template
    for key, val in subs.items():
        html = html.replace(key, str(val))
    
    return html
