#!/usr/bin/env python3
"""Generate self-hosted SVG components for the Tech-Dawn profile system."""
from datetime import date
from html import escape
from pathlib import Path
import hashlib
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = ROOT / "assets" / "profile"
STATS_DIR = ROOT / "assets" / "stats"
BADGE_DIR = ROOT / "assets" / "badges"
PALETTE = {
    "bg": "#0B1724", "panel": "#102235", "panel2": "#142B40",
    "border": "#2B4052", "text": "#DCE5EC", "muted": "#91A4B5",
    "cyan": "#79D7D0", "orange": "#E8A56D", "white": "#FFFFFF",
}
# Official Simple Icons paths for frequently used technologies; other entries use a clean monogram.
LOGOS = {
    "C++": ("00599C", "M22.394 6c-.167-.29-.398-.543-.652-.69L12.926.22c-.509-.294-1.34-.294-1.848 0L2.26 5.31c-.508.293-.923 1.013-.923 1.6v10.18c0 .294.104.62.271.91.167.29.398.543.652.69l8.816 5.09c.508.293 1.34.293 1.848 0l8.816-5.09c.254-.147.485-.4.652-.69.167-.29.27-.616.27-.91V6.91c.003-.294-.1-.62-.268-.91zM12 19.11c-3.92 0-7.109-3.19-7.109-7.11 0-3.92 3.19-7.11 7.11-7.11a7.133 7.133 0 016.156 3.553l-3.076 1.78a3.567 3.567 0 00-3.08-1.78A3.56 3.56 0 008.444 12 3.56 3.56 0 0012 15.555a3.57 3.57 0 003.08-1.778l3.078 1.78A7.135 7.135 0 0112 19.11z"),
    "JavaScript": ("F7DF1E", "M0 0h24v24H0V0zm22.034 18.276c-.175-1.095-.888-2.015-3.003-2.873-.736-.345-1.554-.585-1.797-1.14-.091-.33-.105-.51-.046-.705.15-.646.915-.84 1.515-.66.39.12.75.42.976.9l1.755-1.125c-.27-.42-.404-.601-.586-.78-.63-.705-1.469-1.065-2.834-1.034l-.705.089c-.676.165-1.32.525-1.71 1.005-1.14 1.291-.811 3.541.569 4.471 1.365 1.02 3.361 1.244 3.616 2.205.24 1.17-.87 1.545-1.966 1.41-.811-.18-1.26-.586-1.755-1.336l-1.83 1.051c.21.48.45.689.81 1.109 1.74 1.756 6.09 1.666 6.871-1.004z"),
    "TypeScript": ("3178C6", "M1.125 0C.502 0 0 .502 0 1.125v21.75C0 23.498.502 24 1.125 24h21.75c.623 0 1.125-.502 1.125-1.125V1.125C24 .502 23.498 0 22.875 0zm17.363 9.75c.612 0 1.154.037 1.627.111v2.458a5.1 5.1 0 00-2.786-.821c-.3 0-.573.028-.819.086v-2.166h-9.563v2.166h3.414v9.646h2.717v-9.646h5.41z"),
    "Python": ("3776AB", "M11.858 0c-.978.005-1.913.088-2.736.234C6.7.662 6.26 1.558 6.26 3.21v2.182h5.725v.727H4.111c-1.664 0-3.121 1-3.577 2.903-.526 2.181-.549 3.542 0 5.82.407 1.694 1.379 2.902 3.043 2.902h1.969v-2.616c0-1.89 1.635-3.557 3.576-3.557h5.72c1.591 0 2.862-1.31 2.862-2.91v-5.45c0-1.553-1.309-2.718-2.863-2.977A18 18 0 0 0 11.858 0"),
    "Kotlin": ("7F52FF", "M24 24H0V0h24L12 12Z"),
    "Rust": ("CE422B", "M23.8346 11.7033l-1.0073-.6236a13.7268 13.7268 0 00-.0283-.2936l.8656-.8069a.3483.3483 0 00-.1154-.578l-1.1066-.414a8.4958 8.4958 0 00-.087-.2856l.6904-.9587a.3462.3462 0 00-.2257-.5446l-1.1663-.1894a9.3574 9.3574 0 00-.1407-.2622l.49-1.0761a.3437.3437 0 00-.0274-.3361.3486.3486 0 00-.3006-.154l-1.1845.0416a6.7444 6.7444 0 00-.1873-.2268l.2723-1.153a.3472.3472 0 00-.417-.4172l-1.1532.2724a14.0183 14.0183 0 00-.2278-.1873l.0415-1.1845a.3442.3442 0 00-.49-.328l-1.076.491c-.0872-.0476-.1742-.0952-.2623-.1407l-.1903-1.1673A.3483.3483 0 0016.256.955l-.9597.6905a8.4867 8.4867 0 00-.2855-.086l-.414-1.1066a.3483.3483 0 00-.5781-.1154l-.8069.8666a9.2936 9.2936 0 00-.2936-.0284L12.2946.1683a.3462.3462 0 00-.5892 0l-.6236 1.0073z"),
    "Git": ("F05032", "M13.09 23.549a1.54 1.54 0 01-2.18 0L.451 13.089a1.54 1.54 0 010-2.179l7.191-7.19 2.733 2.733a1.85 1.85 0 00.964 2.326v6.66a1.849 1.849 0 101.54 0V8.957l2.508 2.508a1.85 1.85 0 101.09-1.09l-2.634-2.634a1.85 1.85 0 00-2.378-2.377L8.73 2.63 10.91.451a1.54 1.54 0 012.179 0l10.459 10.46a1.54 1.54 0 010 2.179z"),
    "GitHub": ("24292F", "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998"),
}
BRANDS = {
    "HTML5":"E34F26","CSS3":"1572B6","Vue 3":"42B883","Node.js":"339933","MySQL":"4479A1",
    "Vite":"646CFF","Naive UI":"18A058","Neutralinojs":"20232A","Express":"444444",
    "JWT":"6B5B95","VitePress":"5C73E7","GitHub Actions":"2088FF","GitHub Pages":"222222",
    "Canvas 2D":"E76F51","d3-delaunay":"F9A03C","Vditor":"3A78F2","Web Worker":"496579",
}
def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")

def svg_start(width, height, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'

def generate_badges(stack):
    names = []
    for group in stack.values():
        names.extend(group or [])
    for name in dict.fromkeys(names):
        color, path = LOGOS.get(name, (BRANDS.get(name, "496579"), None))
        fg = "#17212B" if name == "JavaScript" else "#FFFFFF"
        icon = (f'<path d="{path}" fill="{fg}"/>' if path else
                f'<text x="12" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="{fg}">{escape(name[:2].upper())}</text>')
        label = escape(name)
        width = max(74, 34 + len(name) * 7)
        digest = hashlib.sha1(f"shields-flat|{name}|{color}|{path or ''}".encode()).hexdigest()[:12]
        svg = (svg_start(width, 28, name) +
               f'<rect width="{width}" height="28" rx="3" fill="#{color}"/>'
               f'<svg x="6" y="6" width="16" height="16" viewBox="0 0 24 24">{icon}</svg>'
               f'<text x="28" y="18.5" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11.5" font-weight="600" fill="{fg}">{label}</text>'
               '</svg>')
        write(BADGE_DIR / f"tech-{digest}.svg", svg)

def generate_hero():
    svg = svg_start(1200, 154, "Tech-Dawn developer profile identity banner")
    svg += f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{PALETTE["bg"]}"/><stop offset="1" stop-color="{PALETTE["panel2"]}"/></linearGradient><pattern id="p" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{PALETTE["border"]}" stroke-width=".65" opacity=".55"/></pattern></defs>'
    svg += '<rect width="1200" height="154" rx="8" fill="url(#g)"/><rect width="1200" height="154" rx="8" fill="url(#p)"/>'
    svg += f'<path d="M0 130H1200" stroke="{PALETTE["cyan"]}" stroke-opacity=".55"/><path d="M890 0L1200 0 1200 154 1030 154Z" fill="{PALETTE["cyan"]}" opacity=".045"/>'
    svg += f'<circle cx="1070" cy="75" r="43" fill="none" stroke="{PALETTE["cyan"]}" stroke-opacity=".32"/><circle cx="1070" cy="75" r="27" fill="none" stroke="{PALETTE["orange"]}" stroke-opacity=".55"/><circle cx="1070" cy="75" r="5" fill="{PALETTE["cyan"]}"/>'
    svg += f'<text x="42" y="48" font-family="Verdana,DejaVu Sans,sans-serif" font-size="13" letter-spacing="3" fill="{PALETTE["cyan"]}">INDEPENDENT DEVELOPER  /  OPEN SOURCE</text>'
    svg += f'<text x="42" y="91" font-family="Verdana,DejaVu Sans,sans-serif" font-size="32" font-weight="700" fill="{PALETTE["text"]}">SOFTWARE ENGINEERING</text>'
    svg += f'<text x="42" y="118" font-family="Verdana,DejaVu Sans,sans-serif" font-size="14" letter-spacing="1.2" fill="{PALETTE["muted"]}">BUILD · ITERATE · SHARE</text></svg>'
    write(PROFILE_DIR / "hero.svg", svg)

def generate_about():
    steps = [("01","需求分析","REQUIREMENTS"),("02","架构设计","ARCHITECTURE"),("03","工程实现","IMPLEMENTATION"),("04","调试测试","TESTING"),("05","交付维护","DELIVERY")]
    svg = svg_start(1100, 190, "AI-assisted software engineering workflow")
    svg += f'<rect width="1100" height="190" rx="8" fill="{PALETTE["bg"]}"/>'
    svg += f'<text x="24" y="29" font-family="Verdana,sans-serif" font-size="12" letter-spacing="2" fill="{PALETTE["cyan"]}">ENGINEERING WORKFLOW</text>'
    for i,(num,zh,en) in enumerate(steps):
        x=24+i*216
        svg += f'<rect x="{x}" y="52" width="190" height="106" rx="6" fill="{PALETTE["panel"]}" stroke="{PALETTE["border"]}"/>'
        svg += f'<text x="{x+14}" y="78" font-family="Verdana,sans-serif" font-size="12" fill="{PALETTE["orange"]}">{num}</text>'
        svg += f'<text x="{x+14}" y="108" font-family="Verdana,DejaVu Sans,sans-serif" font-size="17" font-weight="700" fill="{PALETTE["text"]}">{zh}</text>'
        svg += f'<text x="{x+14}" y="133" font-family="Verdana,sans-serif" font-size="10" letter-spacing=".6" fill="{PALETTE["muted"]}">{en}</text>'
        if i<4:
            svg += f'<path d="M{x+194} 105h12m-4 -4 4 4-4 4" fill="none" stroke="{PALETTE["cyan"]}" stroke-width="1.5"/>'
    svg += '</svg>'
    write(PROFILE_DIR / "about.svg", svg)

def generate_focus():
    groups = [
        ("01","CORE","核心方向","软件工程 · 开源开发"),
        ("02","PRACTICE","次要方向","开发者工具 · AI 辅助开发 · Web 与桌面应用"),
        ("03","EXPLORE","长期兴趣","算法 · 计算机科学"),
    ]
    svg=svg_start(1100,190,"Current focus areas")
    svg+=f'<rect width="1100" height="190" rx="8" fill="{PALETTE["bg"]}"/>'
    for i,(num,en,zh,body) in enumerate(groups):
        x=24+i*360
        svg+=f'<rect x="{x}" y="16" width="336" height="154" rx="7" fill="{PALETTE["panel"]}" stroke="{PALETTE["border"]}"/>'
        svg+=f'<rect x="{x}" y="16" width="3" height="154" rx="1.5" fill="{PALETTE["cyan"] if i<2 else PALETTE["orange"]}"/>'
        svg+=f'<text x="{x+18}" y="45" font-family="Verdana,sans-serif" font-size="11" letter-spacing="1.5" fill="{PALETTE["muted"]}">{num} / {en}</text>'
        svg+=f'<text x="{x+18}" y="82" font-family="Verdana,DejaVu Sans,sans-serif" font-size="20" font-weight="700" fill="{PALETTE["text"]}">{zh}</text>'
        svg+=f'<foreignObject x="{x+18}" y="98" width="300" height="58"><div xmlns="http://www.w3.org/1999/xhtml" style="font:13px Verdana,'DejaVu Sans',sans-serif;color:{PALETTE["muted"]};line-height:1.55">{escape(body)}</div></foreignObject>'
    svg+='</svg>'
    write(PROFILE_DIR / "focus.svg",svg)

def generate_stats(stats):
    metrics=stats.get("metrics",{})
    items=[
        ("COMMITS",metrics.get("total_commits"),"公开提交"),
        ("REPOSITORIES",metrics.get("public_repositories"),"公开仓库"),
        ("STARS",metrics.get("stars"),"获得 Stars"),
        ("PULL REQUESTS",metrics.get("total_pull_requests"),"公开 PR"),
    ]
    svg=svg_start(1100,154,"GitHub public activity overview")
    svg+=f'<rect width="1100" height="154" rx="8" fill="{PALETTE["bg"]}"/>'
    for i,(label,value,desc) in enumerate(items):
        x=18+i*272
        svg+=f'<rect x="{x}" y="12" width="258" height="128" rx="7" fill="{PALETTE["panel"]}" stroke="{PALETTE["border"]}"/>'
        svg+=f'<text x="{x+17}" y="39" font-family="Verdana,sans-serif" font-size="10" letter-spacing="1.1" fill="{PALETTE["muted"]}">{label}</text>'
        shown=f'{int(value):,}' if isinstance(value,(int,float)) else "—"
        svg+=f'<text x="{x+17}" y="91" font-family="Verdana,sans-serif" font-size="34" font-weight="700" fill="{PALETTE["text"]}">{shown}</text>'
        svg+=f'<text x="{x+17}" y="119" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11" fill="{PALETTE["cyan"]}">{desc}</text>'
    svg+='</svg>'
    write(STATS_DIR / "overview.svg",svg)

def generate_languages(stats):
    languages=stats.get("languages",{})
    top=list(languages.items())[:6]
    total=sum(max(0,int(v)) for _,v in top) or 1
    colors=["79D7D0","4E91C8","E8A56D","8E78C8","66A88C","71859B"]
    svg=svg_start(1100,220,"Programming language distribution by source bytes")
    svg+=f'<rect width="1100" height="220" rx="8" fill="{PALETTE["bg"]}"/>'
    svg+=f'<text x="24" y="31" font-family="Verdana,sans-serif" font-size="12" letter-spacing="1.5" fill="{PALETTE["cyan"]}">LANGUAGE FOOTPRINT</text>'
    if not top:
        svg+=f'<text x="24" y="100" font-family="Verdana,sans-serif" font-size="14" fill="{PALETTE["muted"]}">Statistics will appear after the first successful sync.</text>'
    for i,(name,value) in enumerate(top):
        y=62+i*25
        pct=int(value)/total
        svg+=f'<text x="24" y="{y+11}" font-family="Verdana,DejaVu Sans,sans-serif" font-size="12" fill="{PALETTE["text"]}">{escape(name)}</text>'
        svg+=f'<rect x="190" y="{y}" width="760" height="12" rx="6" fill="{PALETTE["border"]}"/>'
        svg+=f'<rect x="190" y="{y}" width="{max(3,760*pct):.1f}" height="12" rx="6" fill="#{colors[i%len(colors)]}"/>'
        svg+=f'<text x="975" y="{y+11}" font-family="Verdana,sans-serif" font-size="11" fill="{PALETTE["muted"]}">{pct*100:.1f}%</text>'
    svg+='</svg>'
    write(STATS_DIR / "languages.svg",svg)

def generate_contributions(stats):
    days=stats.get("contributions",{}).get("days",[])
    by_date={d.get("date"):int(d.get("count",0)) for d in days}
    if days:
        first=date.fromisoformat(min(by_date))
        monday=first.fromordinal(first.toordinal()-first.weekday())
    else:
        today=date.today()
        monday=today.fromordinal(today.toordinal()-today.weekday()-364)
    colors=["142536","1B4A55","267A7B","42AAA0","79D7D0"]
    svg=svg_start(1100,166,"GitHub contributions during the last 365 days")
    svg+=f'<rect width="1100" height="166" rx="8" fill="{PALETTE["bg"]}"/>'
    svg+=f'<text x="24" y="26" font-family="Verdana,sans-serif" font-size="11" letter-spacing="1.5" fill="{PALETTE["cyan"]}">CONTRIBUTION ACTIVITY · LAST 365 DAYS</text>'
    cell=11; gap=4; x0=24; y0=47
    for day_offset in range(371):
        d=monday.fromordinal(monday.toordinal()+day_offset)
        if d>date.today(): continue
        week=day_offset//7; dow=day_offset%7
        count=by_date.get(d.isoformat(),0)
        level=0 if count==0 else 1 if count<=2 else 2 if count<=5 else 3 if count<=9 else 4
        x=x0+week*(cell+gap); y=y0+dow*(cell+gap)
        svg+=f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="#{colors[level]}"><title>{d.isoformat()}: {count}</title></rect>'
    total=stats.get("metrics",{}).get("yearly_contributions",0)
    svg+=f'<text x="930" y="78" font-family="Verdana,sans-serif" font-size="26" font-weight="700" fill="{PALETTE["text"]}">{int(total):,}</text>'
    svg+=f'<text x="930" y="99" font-family="Verdana,sans-serif" font-size="10" fill="{PALETTE["muted"]}">CONTRIBUTIONS</text>'
    svg+='</svg>'
    write(STATS_DIR / "contributions.svg",svg)

def main():
    settings=yaml.safe_load((ROOT/"profile/settings.yml").read_text(encoding="utf-8")) or {}
    stack=settings.get("tech_stack",{})
    generate_badges(stack)
    generate_hero()
    generate_about()
    generate_focus()
    stats_path=ROOT/"data/stats.json"
    stats=json.loads(stats_path.read_text(encoding="utf-8")) if stats_path.exists() else {}
    generate_stats(stats)
    generate_languages(stats)
    generate_contributions(stats)
    print("Generated local profile visuals and Shields-style technology badges.")

if __name__=="__main__":
    main()
