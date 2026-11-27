#!/usr/bin/env python3
"""Generate Chinese-default and English profile pages from reviewed source data."""
from common import ROOT, load_yaml
from html import escape
from urllib.parse import quote
import hashlib
import re
from pathlib import Path

ASSET_DIR = ROOT / "assets" / "badges"

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
    (ASSET_DIR / filename).write_text(svg + "\\n", encoding="utf-8")
    return f'<img src="./assets/badges/{filename}" alt="{escape(label_text)}" height="{height}"/>'

def render_project_cards(items, lang, columns=2, presentation=None):
    """Render consistent project cards from reviewed project data."""
    presentation = presentation or {}
    border = presentation.get("border_color", "30363D")
    panel = presentation.get("panel_color", "0D1117")
    accent = presentation.get("accent", "79C0FF")
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
        kind = "个人项目" if lang == "zh" and p.get("project_type") == "Personal Project" else (
            "协作项目" if lang == "zh" and p.get("project_type") == "Collaboration" else p.get("project_type", "Project")
        )
        tech = " ".join(
            badge(t, presentation.get("badge_color", "21262D"), presentation)
            for t in p.get("technologies", [])[:5]
        )
        demo = p.get("demo")
        demo_label = "在线体验 ↗" if lang == "zh" else "Live Demo ↗"
        demo_html = f'<a href="{escape(demo)}">{demo_label}</a>' if demo else ""
        meta = f'<p>{badge(status, accent, presentation)} &nbsp; {badge(kind, presentation.get("badge_color", "21262D"), presentation)}</p>'
        footer = demo_html
        cards.append(
            f'<td width="{100 // columns}%" valign="top" style="border:1px solid #{border};border-radius:10px;padding:18px;background:#{panel}">'
            f'<h3 style="margin-top:0"><a href="{repo}">{name} ↗</a></h3>'
            f'<p>{desc}</p>{meta}<p>{tech}</p><p>{footer}</p></td>'
        )
    rows = []
    for i in range(0, len(cards), columns):
        row = cards[i:i + columns]
        if len(row) < columns:
            row.append(f'<td width="{100 // columns}%" style="border:0"></td>')
        rows.append("<tr>" + "".join(row) + "</tr>")
    return '<table><tbody>' + "".join(rows) + '</tbody></table>' if rows else ("暂无项目。" if lang == "zh" else "No projects yet.")

def render_github_activity(lang, presentation=None):
    """Render stats cards with the same palette as the profile's other components."""
    presentation = presentation or {}
    username = presentation.get("username", "zshebjtzs")
    theme = presentation.get("theme", "transparent")
    accent = presentation.get("accent", "79C0FF")
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
    border = presentation.get("border_color", "30363D")
    accent = presentation.get("accent", "79C0FF")
    label = "工程方法" if lang == "zh" else "ENGINEERING METHOD"
    return (
        f'<table><tbody><tr><td style="border:1px solid #{border};padding:18px">'
        f'<p>{escape(summary)}</p><p><sub>{label}</sub></p>'
        f'<p><b><font color="#{accent}">{escape(method_title)}</font></b></p>'
        f'<p>{escape(method_desc)}</p></td></tr></tbody></table>'
    )

def render_focus_cards(groups, lang, presentation):
    labels = (
        [("主要方向", "Primary"), ("次要方向", "Secondary"), ("长期兴趣", "Long-term")]
        if lang == "zh" else
        [("主要方向", "Primary"), ("次要方向", "Secondary"), ("长期兴趣", "Long-term")]
    )
    keys = ["primary", "secondary", "long_term"]
    cells = []
    for key, (zh_label, en_label) in zip(keys, labels):
        title = zh_label if lang == "zh" else en_label
        values = groups.get(key, [])
        body = "<br/>".join(escape(str(v)) for v in values) if values else "—"
        cells.append(
            f'<td width="33%" valign="top" style="border:1px solid #{presentation.get("border_color", "30363D")};border-radius:8px;padding:14px">'
            f'<sub>{title.upper() if lang == "en" else title}</sub><p>{body}</p></td>'
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
    labels = {
        "Experienced": "熟悉" if lang == "zh" else "Experienced",
        "Familiar": "使用过" if lang == "zh" else "Familiar",
        "Exploring": "正在探索" if lang == "zh" else "Exploring",
    }
    colors = {
        "Experienced": presentation.get("accent", "79C0FF"),
        "Familiar": presentation.get("badge_color", "21262D"),
        "Exploring": presentation.get("secondary_accent", "D29922"),
    }
    rows = []
    for level, values in stack.items():
        if not values:
            continue
        badges = " ".join(badge(v, colors.get(level, "21262D"), presentation) for v in values)
        rows.append(
            f'<tr><td width="18%" valign="top"><sub><b>{labels.get(level, level)}</b></sub></td>'
            f'<td>{badges}</td></tr>'
        )
    return '<table><tbody>' + "".join(rows) + '</tbody></table>'

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
    others_md = render_project_cards(others, lang, columns=project_columns, presentation=presentation)
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
