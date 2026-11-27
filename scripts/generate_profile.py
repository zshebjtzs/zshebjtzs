#!/usr/bin/env python3
"""Generate Chinese-default and English profile pages from reviewed source data."""
from common import ROOT, load_yaml
from html import escape
from urllib.parse import quote
import hashlib
ASSET_DIR = ROOT / "assets" / "badges"

TECH_BRANDS = {
    "C++": ("00599C", "C++"),
    "JavaScript": ("F7DF1E", "JS"),
    "TypeScript": ("3178C6", "TS"),
    "Python": ("3776AB", "Py"),
    "Kotlin": ("7F52FF", "K"),
    "Rust": ("CE422B", "R"),
    "LaTeX": ("008080", "TEX"),
    "Git": ("F05032", "Git"),
    "GitHub": ("24292F", "GH"),
    "Vue 3": ("42B883", "V"),
    "Node.js": ("339933", "N"),
    "MySQL": ("4479A1", "SQL"),
    "HTML": ("E34F26", "5"),
    "HTML5": ("E34F26", "5"),
    "CSS": ("1572B6", "3"),
    "CSS3": ("1572B6", "3"),
    "Vite": ("646CFF", "V"),
    "Naive UI": ("18A058", "N"),
    "Neutralinojs": ("20232A", "N"),
    "Express": ("444444", "Ex"),
    "JWT": ("6B5B95", "JWT"),
    "VitePress": ("5C73E7", "VP"),
    "GitHub Actions": ("2088FF", "A"),
    "GitHub Pages": ("222222", "GH"),
    "Canvas 2D": ("E76F51", "C"),
    "d3-delaunay": ("F9A03C", "d3"),
}
TECH_LOGOS = {
    "C++": "M22.394 6c-.167-.29-.398-.543-.652-.69L12.926.22c-.509-.294-1.34-.294-1.848 0L2.26 5.31c-.508.293-.923 1.013-.923 1.6v10.18c0 .294.104.62.271.91.167.29.398.543.652.69l8.816 5.09c.508.293 1.34.293 1.848 0l8.816-5.09c.254-.147.485-.4.652-.69.167-.29.27-.616.27-.91V6.91c.003-.294-.1-.62-.268-.91zM12 19.11c-3.92 0-7.109-3.19-7.109-7.11 0-3.92 3.19-7.11 7.11-7.11a7.133 7.133 0 016.156 3.553l-3.076 1.78a3.567 3.567 0 00-3.08-1.78A3.56 3.56 0 008.444 12 3.56 3.56 0 0012 15.555a3.57 3.57 0 003.08-1.778l3.078 1.78A7.135 7.135 0 0112 19.11zm7.11-6.715h-.79v.79h-.79v-.79h-.79v-.79h.79v-.79h.79v.79h.79zm2.962 0h-.79v.79h-.79v-.79h-.79v-.79h.79v-.79h.79v.79h.79z",
    "TypeScript": "M1.125 0C.502 0 0 .502 0 1.125v21.75C0 23.498.502 24 1.125 24h21.75c.623 0 1.125-.502 1.125-1.125V1.125C24 .502 23.498 0 22.875 0zm17.363 9.75c.612 0 1.154.037 1.627.111a6.38 6.38 0 011.306.34v2.458a3.95 3.95 0 00-.643-.361 5.093 5.093 0 00-.717-.26 5.453 5.453 0 00-1.426-.2c-.3 0-.573.028-.819.086a2.1 2.1 0 00-.623.242c-.17.104-.3.229-.393.374a.888.888 0 00-.14.49c0 .196.053.373.156.529.104.156.252.304.443.444s.423.276.696.41c.273.135.582.274.926.416.47.197.892.407 1.266.628.374.222.695.473.963.753.268.279.472.598.614.957.142.359.214.776.214 1.253 0 .657-.125 1.21-.373 1.656a3.033 3.033 0 01-1.012 1.085 4.38 4.38 0 01-1.487.596c-.566.12-1.163.18-1.79.18a9.916 9.916 0 01-1.84-.164 5.544 5.544 0 01-1.512-.493v-2.63a5.033 5.033 0 003.237 1.2c.333 0 .624-.03.872-.09.249-.06.456-.144.623-.25.166-.108.29-.234.373-.38a1.023 1.023 0 00-.074-1.089 2.12 2.12 0 00-.537-.5 5.597 5.597 0 00-.807-.444 27.72 27.72 0 00-1.007-.436c-.918-.383-1.602-.852-2.053-1.405-.45-.553-.676-1.222-.676-2.005 0-.614.123-1.141.369-1.582.246-.441.58-.804 1.004-1.089a4.494 4.494 0 011.47-.629 7.536 7.536 0 011.77-.201zm-15.113.188h9.563v2.166H9.506v9.646H6.789v-9.646H3.375z",
    "JavaScript": "M0 0h24v24H0V0zm22.034 18.276c-.175-1.095-.888-2.015-3.003-2.873-.736-.345-1.554-.585-1.797-1.14-.091-.33-.105-.51-.046-.705.15-.646.915-.84 1.515-.66.39.12.75.42.976.9l1.755-1.125c-.27-.42-.404-.601-.586-.78-.63-.705-1.469-1.065-2.834-1.034l-.705.089c-.676.165-1.32.525-1.71 1.005-1.14 1.291-.811 3.541.569 4.471 1.365 1.02 3.361 1.244 3.616 2.205.24 1.17-.87 1.545-1.966 1.41-.811-.18-1.26-.586-1.755-1.336l-1.83 1.051c.21.48.45.689.81 1.109 1.74 1.756 6.09 1.666 6.871-1.004.029-.09.24-.705.074-1.65z",
    "Git": "M13.09 23.549a1.54 1.54 0 0 1-2.18 0L.451 13.089a1.54 1.54 0 0 1 0-2.179l7.191-7.19 2.733 2.733a1.85 1.85 0 0 0 .964 2.326v6.66a1.849 1.849 0 1 0 1.54 0V8.957l2.508 2.508a1.85 1.85 0 1 0 1.09-1.09l-2.634-2.634a1.85 1.85 0 0 0-2.378-2.377L8.73 2.63 10.91.451a1.54 1.54 0 0 1 2.179 0l10.459 10.46a1.54 1.54 0 0 1 0 2.179z",
    "GitHub": "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 0 0 3.285-1.552 3.285-1.23 0 0 .645 1.653.12 3.176.765.84 1.235 1.91 1.235 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
}
def tech_badge(name):
    """Render a brand-colored, self-hosted technology badge with a logo mark."""
    brand, mark = TECH_BRANDS.get(name, ("496579", name[:2].upper()))
    fg = "17212B" if name == "JavaScript" else "FFFFFF"
    path = TECH_LOGOS.get(name)
    icon = (f'<path d="{path}" fill="{fg}"/>' if path else
            f'<text x="12" y="17" text-anchor="middle" font-size="10" font-weight="700" fill="{fg}">{escape(mark)}</text>')
    width = max(72, 34 + len(name) * 7)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="26" viewBox="0 0 {width} 26" role="img" aria-label="{escape(name)}">'
        f'<rect width="{width}" height="26" rx="2" fill="#{brand}"/>'
        f'<svg x="6" y="5" width="16" height="16" viewBox="0 0 24 24">{icon}</svg>'
        f'<text x="28" y="17" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="{fg}">{escape(name)}</text>'
        f'</svg>'
    )
    digest = hashlib.sha1(f"tech|{name}|{brand}|{path or mark}".encode("utf-8")).hexdigest()[:12]
    filename = f"tech-{digest}.svg"
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    (ASSET_DIR / filename).write_text(svg + "\n", encoding="utf-8")
    return f'<img src="./assets/badges/{filename}" alt="{escape(name)}" height="26"/>'


def md_link(label, url):
    return f"[{label}]({url})" if url else label

def bullets(items, empty):
    return "\n".join(f"- {x}" for x in items) if items else f"- {empty}"

def localized(item, key, lang, fallback=None):
    return item.get(f"{key}_{lang}") or item.get(key) or fallback or ""

def render_project(p, lang):
    line = f"### {md_link(p['name'], p['repository'])}"
    demo_label = "在线体验" if lang == "zh" else "Live Demo"
    if p.get("demo"):
        line += f" · {md_link(demo_label, p['demo'])}"
    line += f"\n\n{localized(p, 'description', lang)}"
    status = p.get("development_status", "Unknown")
    status_map = {
        "Maintained": "持续维护中" if lang == "zh" else "Maintained",
        "In Development": "开发中" if lang == "zh" else "In Development",
        "Needs Review": "待确认" if lang == "zh" else "Needs Review",
        "Early Stage": "早期阶段" if lang == "zh" else "Early Stage",
    }
    kind = p.get("project_type", "Project")
    kind_map = {
        "Personal Project": "个人项目" if lang == "zh" else "Personal Project",
        "Collaboration": "协作项目" if lang == "zh" else "Collaboration",
    }
    line += f"\n\n`{status_map.get(status, status)}` · {kind_map.get(kind, kind)}"
    highlights = p.get(f"highlights_{lang}") or p.get("highlights", [])
    if highlights:
        line += "\n\n" + "\n".join(f"- {x}" for x in highlights)
    return line

def badge(label, color, presentation):
    """Create a repository-hosted SVG badge and return its relative image tag."""
    label_text = str(label)
    bg = str(color).lstrip("#")
    fg = str(presentation.get("badge_text_color", "C9D1D9")).lstrip("#")
    accent = str(presentation.get("accent", "79C0FF")).lstrip("#")
    digest = hashlib.sha1(f"{label_text}|{bg}|{fg}|{accent}".encode("utf-8")).hexdigest()[:12]
    filename = f"badge-{digest}.svg"
    width = max(54, 18 + len(label_text) * 8)
    height = 22
    safe_label = escape(label_text)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{safe_label}">'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="5" '
        f'fill="#{bg}" stroke="#{accent}" stroke-opacity=".42"/>'
        f'<text x="{width / 2}" y="15" text-anchor="middle" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="600" '
        f'fill="#{fg}">{safe_label}</text></svg>'
    )
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    (ASSET_DIR / filename).write_text(svg + "\n", encoding="utf-8")
    return f'<img src="./assets/badges/{filename}" alt="{escape(label_text)}" height="{height}"/>'

def render_project_cards(items, lang, columns=2, presentation=None):
    """Render a compact project grid with consistent editorial card rhythm."""
    presentation = presentation or {}
    border = presentation.get("border_color", "2B4052")
    panel = presentation.get("panel_color", "102235")
    accent = presentation.get("accent", "79D7D0")
    status_map = {
        "Maintained": "持续维护" if lang == "zh" else "Maintained",
        "In Development": "开发中" if lang == "zh" else "In Development",
        "Needs Review": "待确认" if lang == "zh" else "Needs Review",
        "Early Stage": "早期阶段" if lang == "zh" else "Early Stage",
    }
    cards = []
    for p in items:
        name = escape(p.get("name", p["id"]))
        repo = escape(p.get("repository", ""))
        desc = escape(localized(p, "description", lang))
        status = status_map.get(p.get("development_status", "Unknown"), p.get("development_status", "Unknown"))
        kind = ("个人项目" if lang == "zh" else "Personal") if p.get("project_type") == "Personal Project" else (
            ("协作项目" if lang == "zh" else "Collaboration") if p.get("project_type") == "Collaboration" else p.get("project_type", "Project")
        )
        tech = " ".join(tech_badge(t) for t in p.get("technologies", [])[:5])
        demo = p.get("demo")
        demo_label = "在线体验 ↗" if lang == "zh" else "Live Demo ↗"
        demo_html = f'<a href="{escape(demo)}">{demo_label}</a>' if demo else ""
        meta = f'<p><sub><font color="#{accent}">{escape(status)}</font> · {escape(kind)}</sub></p>'
        cards.append(
            f'<td width="{100 // columns}%" valign="top" style="border:1px solid #{border};padding:16px;background:#{panel}">'
            f'<p><strong><a href="{repo}">{name} ↗</a></strong></p>'
            f'<p>{desc}</p>{meta}<p>{tech}</p><p>{demo_html}</p></td>'
        )
    rows = []
    for i in range(0, len(cards), columns):
        row = cards[i:i + columns]
        if len(row) < columns:
            row.append(f'<td width="{100 // columns}%" style="border:0;background:transparent"></td>')
        rows.append("<tr>" + "".join(row) + "</tr>")
    return '<table><tbody>' + "".join(rows) + '</tbody></table>' if rows else ("暂无项目。" if lang == "zh" else "No projects yet.")
def render_github_activity(lang, presentation=None):
    """Render stats cards with the same palette as the profile's other components."""
    presentation = presentation or {}
    username = presentation.get("username", "zshebjtzs")
    theme = presentation.get("theme", "transparent")
    accent = presentation.get("accent", "79D7D0")
    title = presentation.get("title_color", accent)
    text_color = presentation.get("text_color", "C9D1D9")
    bg = presentation.get("panel_color", "0D1117")
    border = presentation.get("border_color", "30363D")
    stats_base = presentation.get("stats_provider", "https://github-readme-stats.vercel.app")
    chart_base = presentation.get("contribution_provider", "https://ghchart.rshah.org")
    common = (
        f"&bg_color={bg}&title_color={title}&text_color={text_color}"
        f"&icon_color={accent}&border_color={border}&hide_border=false"
    )
    stats = f"{stats_base}/api?username={username}&show_icons=true&include_all_commits=true&rank_icon=github{common}"
    langs = f"{stats_base}/api/top-langs/?username={username}&layout=compact&langs_count=8{common}"
    chart = f"{chart_base}/{accent}/{username}"
    alt_stats = "GitHub statistics" if lang == "en" else "GitHub 统计数据"
    alt_langs = "Most used languages" if lang == "en" else "主要编程语言"
    alt_chart = "GitHub contribution graph" if lang == "en" else "GitHub 贡献热力图"
    note = ("Live cards are served by external providers; the rest of this profile is generated locally."
            if lang == "en" else "统计图由第三方服务提供；主页其他内容由本仓库独立生成。")
    return (
        '<table><tbody><tr>'
        f'<td width="50%" valign="top"><img src="{stats}" alt="{alt_stats}" width="100%"/></td>'
        f'<td width="50%" valign="top"><img src="{langs}" alt="{alt_langs}" width="100%"/></td>'
        '</tr></tbody></table>'
        f'<p align="center"><img src="{chart}" alt="{alt_chart}" width="100%"/></p>'
        f'<p align="center"><sub>{note}</sub></p>'
    )

def render_about(summary, method_title, method_desc, lang, presentation):
    """Render an editorial introduction without a heavy enclosing card."""
    accent = presentation.get("accent", "79D7D0")
    label = "工程方法 / ENGINEERING APPROACH" if lang == "zh" else "ENGINEERING APPROACH"
    return (
        f'<p><strong>{escape(summary)}</strong></p>'
        f'<p><sub>{label}</sub></p>'
        f'<p><strong><font color="#{accent}">{escape(method_title)}</font></strong></p>'
        f'<p>{escape(method_desc)}</p>'
    )
def render_focus_cards(groups, lang, presentation):
    """Render three balanced focus columns with restrained separators."""
    labels = {
        "primary": ("主要方向", "PRIMARY"),
        "secondary": ("次要方向", "SECONDARY"),
        "long_term": ("长期兴趣", "LONG-TERM"),
    }
    cells = []
    for key in ("primary", "secondary", "long_term"):
        title = labels[key][0] if lang == "zh" else labels[key][1]
        values = groups.get(key, [])
        body = "<br/>".join(escape(str(v)) for v in values) if values else "—"
        cells.append(
            f'<td width="33%" valign="top" style="padding:12px 16px;border-left:2px solid #{presentation.get("border_color", "2B4052")}">'
            f'<sub><b>{title}</b></sub><p>{body}</p></td>'
        )
    return '<table><tbody><tr>' + "".join(cells) + '</tr></tbody></table>'
def render_link_cards(items, lang, presentation, limit=8):
    if not items:
        return "暂无记录。" if lang == "zh" else "No records yet."
    border = presentation.get("border_color", "30363D")
    rows = []
    for item in items[:limit]:
        title = escape(localized(item, "title", lang, "活动" if lang == "zh" else "Activity"))
        url = escape(item.get("url", "#"))
        date_text = escape(item.get("date") or (item.get("updated_at") or "")[:10])
        repo = escape(item.get("repository", ""))
        rows.append(
            f'<tr><td style="border-bottom:1px solid #{border};padding:10px 8px" width="76%">'
            f'<a href="{url}">{title} ↗</a><br/><sub>{repo}</sub></td>'
            f'<td align="right" style="border-bottom:1px solid #{border};padding:10px 8px"><sub>{date_text}</sub></td></tr>'
        )
    return '<table><tbody>' + "".join(rows) + '</tbody></table>'

def render_stack(stack, lang, presentation):
    """Render technology groups using compact brand-colored local SVG badges."""
    labels = {
        "Experienced": "熟悉" if lang == "zh" else "Experienced",
        "Familiar": "使用过" if lang == "zh" else "Familiar",
        "Exploring": "正在探索" if lang == "zh" else "Exploring",
    }
    rows = []
    for level in ("Experienced", "Familiar", "Exploring"):
        values = stack.get(level, [])
        if not values:
            continue
        badges = " ".join(tech_badge(v) for v in values)
        rows.append(
            f'<p><sub><b>{labels.get(level, level)}</b></sub><br/>{badges}</p>'
        )
    return "\n".join(rows)
def build_page(lang, identity, focus, projects, records, milestones, stack, template):
    zh = lang == "zh"
    module_config = load_yaml("profile/modules.yml")
    presentation = module_config.get("presentation", {})
    project_columns = max(1, min(3, int(presentation.get("project_columns", 2))))
    labels = {
        "about_heading": "关于我" if zh else "About",
        "focus_heading": "当前关注" if zh else "Current Focus",
        "featured_heading": "精选项目" if zh else "Featured Projects",
        "other_heading": "其他项目" if zh else "Other Projects",
        "contributions_heading": "开源贡献" if zh else "Open-Source Contributions",
        "highlights_heading": "近期动态" if zh else "Recent Highlights",
        "milestones_heading": "里程碑" if zh else "Milestones",
        "stack_heading": "技术栈" if zh else "Tech Stack",
        "archive_heading": "活动档案" if zh else "Activity Archive",
        "footer": "动态开发者主页 · 自动追踪事实，人工审核与精选。" if zh else "Living Developer Profile · Facts are collected automatically and published after human review.",
    }
    primary = focus.get("primary_focus_zh" if zh else "primary_focus", focus.get("primary_focus", []))
    secondary = focus.get("secondary_interests_zh" if zh else "secondary_interests", focus.get("secondary_interests", []))
    long_term = focus.get("long_term_interests_zh" if zh else "long_term_interests", focus.get("long_term_interests", []))
    focus_md = render_focus_cards({
        "primary": primary, "secondary": secondary, "long_term": long_term
    }, lang, presentation)
    method = identity.get("engineering_method", {})
    method_title = method.get("title_zh" if zh else "title_en") or method.get("title", "工程方法" if zh else "Engineering Method")
    method_desc = method.get("description_zh" if zh else "description_en") or method.get("description", "")
    method_md = f"**{method_title}** — {method_desc}"
    featured = sorted([p for p in projects if p.get("visibility") == "featured"], key=lambda p: p.get("order", 999))
    others = sorted([p for p in projects if p.get("visibility") == "other"], key=lambda p: p.get("order", 999))
    featured_md = render_project_cards(featured, lang, columns=project_columns, presentation=presentation)
    others_md = render_project_cards(others, lang, columns=1, presentation=presentation)
    contributions = [a for a in records if a.get("type") in {"pull_request", "issue", "review"}]
    contributions_md = render_link_cards(contributions, lang, presentation, limit=8)
    highlights = [a for a in records if a.get("review_status") == "featured"]
    highlights.sort(key=lambda a: a.get("date") or a.get("updated_at") or "", reverse=True)
    highlights_md = render_link_cards(highlights, lang, presentation, limit=5)
    milestone_md = "\n".join(
        f"- **{m['date']}** — [{localized(m, 'title', lang)}]({m['evidence']})：{localized(m, 'description', lang)}"
        if zh else f"- **{m['date']}** — [{localized(m, 'title', lang)}]({m['evidence']}): {localized(m, 'description', lang)}"
        for m in sorted(milestones, key=lambda x: x.get("date", ""), reverse=True)
    ) or ("里程碑仅在日期、证据与长期意义确认后归档。" if zh else "Milestones are archived only after their date, evidence, and long-term significance are verified.")
    stack_md = render_stack(stack, lang, presentation)
    links = identity.get("links", {})
    social_badges = []
    for label, key, logo in [
        ("GitHub", "github", "github"), ("Luogu", "luogu", ""),
        ("Bilibili", "bilibili", "bilibili"), ("X", "x", "x")
    ]:
        url = links.get(key)
        if url:
            color = presentation.get("badge_color", "21262D")
            social_badges.append(f'<a href="{escape(url)}">{badge(label, color, presentation)}</a>')
    social = " &nbsp; ".join(social_badges)
    archive_link = "[activity/ACTIVITY.md](./activity/ACTIVITY.md)" if zh else "[activity/ACTIVITY.en.md](./activity/ACTIVITY.en.md)"
    archive_sentence = "完整的已审核活动记录见" if zh else "Browse the complete reviewed activity archive:"
    module_titles = {
        "about": labels["about_heading"], "focus": labels["focus_heading"],
        "github_activity": "GitHub 活动" if zh else "GitHub Activity",
        "featured_projects": labels["featured_heading"], "other_projects": labels["other_heading"],
        "contributions": labels["contributions_heading"], "highlights": labels["highlights_heading"],
        "milestones": labels["milestones_heading"], "tech_stack": labels["stack_heading"],
        "activity_archive": labels["archive_heading"],
    }
    module_bodies = {
        "about": render_about(
            identity.get("summary_zh" if zh else "summary_en") or identity.get("summary", ""),
            method_title, method_desc, lang, presentation
        ),
        "focus": focus_md, "github_activity": render_github_activity(lang, presentation),
        "featured_projects": featured_md, "other_projects": others_md,
        "contributions": contributions_md, "highlights": highlights_md,
        "milestones": milestone_md, "tech_stack": stack_md,
        "activity_archive": f"{archive_sentence} {archive_link}。" if zh else f"{archive_sentence} {archive_link}.",
    }
    module_config = module_config.get("modules", [])
    enabled_modules = [m for m in module_config if m.get("enabled", True)]
    modules_md = "\n\n<hr/>\n\n".join(
        f"## {module_titles[m['id']]}\n\n{module_bodies[m['id']]}"
        for m in enabled_modules if m.get("id") in module_titles
    )
    replacements = {
        "{{display_name}}": identity.get("display_name", identity["username"]),
        "{{title}}": identity.get("title_zh" if zh else "title_en") or identity.get("title", ""),
        "{{domains}}": " · ".join(identity.get("domains_zh" if zh else "domains_en") or identity.get("domains", [])),
        "{{bio}}": identity.get("bio", "") if zh else identity.get("bio_en", identity.get("bio", "")),
        "{{social_links}}": social,
        "{{language_switch}}": (
            f'<a href="./README.md">{badge("简体中文", presentation.get("accent", "79C0FF"), presentation)}</a> &nbsp; <a href="./README.en.md">{badge("English", presentation.get("badge_color", "21262D"), presentation)}</a>'
        ) if zh else (
            f'<a href="./README.md">{badge("简体中文", presentation.get("badge_color", "21262D"), presentation)}</a> &nbsp; <a href="./README.en.md">{badge("English", presentation.get("accent", "79C0FF"), presentation)}</a>'
        ),
        "{{modules}}": modules_md,
        "{{about_heading}}": labels["about_heading"],
        "{{focus_heading}}": labels["focus_heading"],
        "{{featured_heading}}": labels["featured_heading"],
        "{{other_heading}}": labels["other_heading"],
        "{{contributions_heading}}": labels["contributions_heading"],
        "{{highlights_heading}}": labels["highlights_heading"],
        "{{milestones_heading}}": labels["milestones_heading"],
        "{{stack_heading}}": labels["stack_heading"],
        "{{archive_heading}}": labels["archive_heading"],
        "{{footer}}": labels["footer"],
        "{{summary}}": identity.get("summary_zh" if zh else "summary_en") or identity.get("summary", ""),
        "{{engineering_method}}": method_md,
        "{{current_focus}}": focus_md,
        "{{featured_projects}}": featured_md,
        "{{other_projects}}": others_md,
        "{{open_source_contributions}}": contributions_md,
        "{{recent_highlights}}": highlights_md,
        "{{milestones}}": milestone_md,
        "{{tech_stack}}": stack_md,
        "{{archive_link}}": f"{archive_sentence} {archive_link}。" if zh else f"{archive_sentence} {archive_link}.",
    }
    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)
    return output

def build_archive(records, lang):
    zh = lang == "zh"
    lines = ["# 活动档案" if zh else "# Activity Archive", "", "仅收录已审核记录。" if zh else "Only reviewed records are included.", ""]
    ordered = sorted(records, key=lambda a: a.get("date") or a.get("updated_at") or "", reverse=True)
    if not ordered:
        lines.append("目前暂无已审核发布的活动记录。" if zh else "No reviewed activity records have been published yet.")
    for a in ordered:
        d = a.get("date") or (a.get("updated_at") or "")[:10] or ("未注明日期" if zh else "Undated")
        lines.append(f"## {d} — {md_link(localized(a, 'title', lang, '活动' if zh else 'Activity'), a.get('url'))}")
        if a.get("repository"):
            lines.append(f"\n**仓库：** {a['repository']}" if zh else f"\n**Repository:** {a['repository']}")
        desc = localized(a, "description", lang)
        if desc:
            lines.append(f"\n{desc}")
        note = localized(a, "review_note", lang)
        if note:
            lines.append(f"\n> {note}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def main():
    identity = load_yaml("profile/identity.yml")["identity"]
    focus = load_yaml("profile/current-focus.yml")
    projects = load_yaml("profile/projects.yml").get("projects", [])
    records = load_yaml("activity/records.yml").get("activities", [])
    milestones = load_yaml("profile/milestones.yml").get("milestones", [])
    stack = load_yaml("profile/settings.yml").get("tech_stack", {})
    if not stack:
        stack = {
            "Experienced": ["JavaScript", "C++", "Git", "GitHub"],
            "Familiar": ["TypeScript", "Vue 3", "Node.js", "MySQL", "HTML", "CSS", "Vite"],
            "Exploring": [],
        }
    template = (ROOT / "templates/README.template.md").read_text(encoding="utf-8")
    (ROOT / "README.md").write_text(build_page("zh", identity, focus, projects, records, milestones, stack, template), encoding="utf-8")
    (ROOT / "README.en.md").write_text(build_page("en", identity, focus, projects, records, milestones, stack, template), encoding="utf-8")
    (ROOT / "activity/ACTIVITY.md").write_text(build_archive(records, "zh"), encoding="utf-8")
    (ROOT / "activity/ACTIVITY.en.md").write_text(build_archive(records, "en"), encoding="utf-8")
    print("Generated Chinese-default and English profile pages and activity archives.")

if __name__ == "__main__":
    main()
