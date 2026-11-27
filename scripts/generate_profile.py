#!/usr/bin/env python3
"""Generate Chinese-default and English profile pages from reviewed source data."""
from common import ROOT, load_yaml
from html import escape

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

def render_project_cards(items, lang, columns=2):
    """Render responsive-ish GitHub README project cards from project data."""
    cards = []
    for p in items:
        name = escape(p.get("name", p["id"]))
        repo = escape(p.get("repository", ""))
        desc = escape(localized(p, "description", lang))
        status = p.get("development_status", "Unknown")
        kind = p.get("project_type", "Project")
        status_map = {
            "Maintained": "持续维护中" if lang == "zh" else "Maintained",
            "In Development": "开发中" if lang == "zh" else "In Development",
            "Needs Review": "待确认" if lang == "zh" else "Needs Review",
            "Early Stage": "早期阶段" if lang == "zh" else "Early Stage",
        }
        technologies = p.get("technologies", [])[:4]
        tech = " · ".join(escape(x) for x in technologies)
        demo = p.get("demo")
        demo_link = f' · <a href="{escape(demo)}">{"在线体验" if lang == "zh" else "Live Demo"}</a>' if demo else ""
        stars = f'<img src="https://img.shields.io/github/stars/{escape(p["repository"].split("github.com/")[-1])}?style=flat-square&label=Stars" alt="GitHub stars"/>' if "github.com/" in p.get("repository", "") else ""
        cards.append(
            '<td width="50%" valign="top"><h3><a href="' + repo + '">' + name + '</a></h3>'
            '<p>' + desc + '</p><p><sub>' + escape(status_map.get(status, status)) + ' · ' + escape(kind) + '</sub></p>'
            '<p><sub>' + tech + '</sub></p><p>' + stars + demo_link + '</p></td>'
        )
    rows = []
    for i in range(0, len(cards), columns):
        row = cards[i:i + columns]
        if len(row) < columns:
            row += ['<td width="50%"></td>'] * (columns - len(row))
        rows.append("<tr>" + "".join(row) + "</tr>")
    return '<table>\n' + "\n".join(rows) + '\n</table>' if rows else ("暂无项目。" if lang == "zh" else "No projects yet.")

def render_github_activity(lang, presentation=None):
    """Third-party SVG cards are optional visual enhancements, not data dependencies."""
    presentation = presentation or {}
    username = presentation.get("username", "zshebjtzs")
    theme = presentation.get("theme", "transparent")
    accent = presentation.get("accent", "6B9FE8")
    stats_base = presentation.get("stats_provider", "https://github-readme-stats.vercel.app")
    chart_base = presentation.get("contribution_provider", "https://ghchart.rshah.org")
    stats = f"{stats_base}/api?username={username}&show_icons=true&hide_border=true&theme={theme}&include_all_commits=true"
    langs = f"{stats_base}/api/top-langs/?username={username}&layout=compact&hide_border=true&theme={theme}&langs_count=8"
    chart = f"{chart_base}/{accent}/{username}"
    alt_stats = "GitHub statistics" if lang == "en" else "GitHub 统计数据"
    alt_langs = "Most used languages" if lang == "en" else "主要编程语言"
    alt_chart = "GitHub contribution graph" if lang == "en" else "GitHub 贡献热力图"
    return (
        '<table><tr><td width="50%" valign="top"><img src="' + stats + '" alt="' + alt_stats + '" width="100%"/></td>'
        '<td width="50%" valign="top"><img src="' + langs + '" alt="' + alt_langs + '" width="100%"/></td></tr></table>\n'
        '<p align="center"><img src="' + chart + '" alt="' + alt_chart + '" width="100%"/></p>'
        '<sub>' + ("Statistics are provided by external services and may be temporarily unavailable." if lang == "en" else "统计图由第三方服务提供，可能存在短暂不可用或数据延迟；不影响主页其他内容。") + '</sub>'
    )

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
    focus_md = (
        f"**{('主要方向' if zh else 'Primary')}**\n{bullets(primary, '暂无已确认内容。' if zh else 'No confirmed items yet.')}\n\n"
        f"**{('次要方向' if zh else 'Secondary')}**\n{bullets(secondary, '暂无已确认内容。' if zh else 'No confirmed items yet.')}\n\n"
        f"**{('长期兴趣' if zh else 'Long-term')}**\n{bullets(long_term, '暂无已确认内容。' if zh else 'No confirmed items yet.')}"
    )
    method = identity.get("engineering_method", {})
    method_title = method.get("title_zh" if zh else "title_en") or method.get("title", "工程方法" if zh else "Engineering Method")
    method_desc = method.get("description_zh" if zh else "description_en") or method.get("description", "")
    method_md = f"**{method_title}** — {method_desc}"
    featured = sorted([p for p in projects if p.get("visibility") == "featured"], key=lambda p: p.get("order", 999))
    others = sorted([p for p in projects if p.get("visibility") == "other"], key=lambda p: p.get("order", 999))
    featured_md = render_project_cards(featured, lang, columns=project_columns)
    others_md = render_project_cards(others, lang, columns=project_columns)
    contributions = [a for a in records if a.get("type") in {"pull_request", "issue", "review"}]
    contributions_md = "\n".join(
        f"- [{localized(a, 'title', lang, 'Contribution')}]({a.get('url', '#')}) · {a.get('repository', '')}"
        for a in contributions[:8]
    ) or ("贡献记录采用自动收集、人工审核机制；目前暂无已审核发布的记录。" if zh else "Contributions are collected automatically and published after review; no reviewed records have been published yet.")
    highlights = [a for a in records if a.get("review_status") == "featured"]
    highlights.sort(key=lambda a: a.get("date") or a.get("updated_at") or "", reverse=True)
    highlights_md = "\n".join(
        f"- **{a.get('date', (a.get('updated_at') or '')[:10])}** — [{localized(a, 'title', lang, 'Activity')}]({a.get('url', '#')})"
        for a in highlights[:5]
    ) or ("暂无已审核精选动态。" if zh else "No reviewed highlights yet.")
    milestone_md = "\n".join(
        f"- **{m['date']}** — [{localized(m, 'title', lang)}]({m['evidence']})：{localized(m, 'description', lang)}"
        if zh else f"- **{m['date']}** — [{localized(m, 'title', lang)}]({m['evidence']}): {localized(m, 'description', lang)}"
        for m in sorted(milestones, key=lambda x: x.get("date", ""), reverse=True)
    ) or ("里程碑仅在日期、证据与长期意义确认后归档。" if zh else "Milestones are archived only after their date, evidence, and long-term significance are verified.")
    stack_labels = {
        "Experienced": "熟悉" if zh else "Experienced",
        "Familiar": "使用过" if zh else "Familiar",
        "Exploring": "正在探索" if zh else "Exploring",
    }
    stack_md = "\n".join(
        f"- **{stack_labels.get(level, level)}:** {', '.join(values) if values else '—'}"
        for level, values in stack.items()
    )
    links = identity.get("links", {})
    social = " · ".join(
        md_link(label, links.get(key))
        for label, key in [("GitHub", "github"), ("Luogu", "luogu"), ("Bilibili", "bilibili"), ("X", "x")]
        if links.get(key)
    )
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
        "about": f"{identity.get('summary_zh' if zh else 'summary_en') or identity.get('summary', '')}\n\n{method_md}",
        "focus": focus_md, "github_activity": render_github_activity(lang, presentation),
        "featured_projects": featured_md, "other_projects": others_md,
        "contributions": contributions_md, "highlights": highlights_md,
        "milestones": milestone_md, "tech_stack": stack_md,
        "activity_archive": f"{archive_sentence} {archive_link}。" if zh else f"{archive_sentence} {archive_link}.",
    }
    module_config = module_config.get("modules", [])
    enabled_modules = [m for m in module_config if m.get("enabled", True)]
    modules_md = "\n\n".join(
        f"## {module_titles[m['id']]}\n\n{module_bodies[m['id']]}"
        for m in enabled_modules if m.get("id") in module_titles
    )
    replacements = {
        "{{display_name}}": identity.get("display_name", identity["username"]),
        "{{title}}": identity.get("title_zh" if zh else "title_en") or identity.get("title", ""),
        "{{domains}}": " · ".join(identity.get("domains_zh" if zh else "domains_en") or identity.get("domains", [])),
        "{{bio}}": identity.get("bio", "") if zh else identity.get("bio_en", identity.get("bio", "")),
        "{{social_links}}": social,
        "{{language_switch}}": "**简体中文** · [English](./README.en.md)" if zh else "[简体中文](./README.md) · **English**",
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
