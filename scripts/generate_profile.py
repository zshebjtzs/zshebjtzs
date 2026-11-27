#!/usr/bin/env python3
"""Generate bilingual, data-driven developer profile pages."""
from common import ROOT, load_yaml
from html import escape
import hashlib
import json

BADGE_MAP_PATH = ROOT / "data" / "tech-badges.json"
BADGE_DIR = ROOT / "assets" / "badges"


def localized(item, key, lang, fallback=None):
    return item.get(f"{key}_{lang}") or item.get(key) or fallback or ""


def image(path, alt, width="100%"):
    return f'<p align="center"><img src="./{path}" alt="{escape(alt)}" width="{width}"/></p>'


def tech_badge(name):
    mapping = {}
    if BADGE_MAP_PATH.exists():
        mapping = json.loads(BADGE_MAP_PATH.read_text(encoding="utf-8"))
    filename = mapping.get(name)
    if not filename:
        digest = hashlib.sha1(f"shields-flat|{name}".encode()).hexdigest()[:12]
        filename = f"tech-{digest}.svg"
    return f'<img src="./assets/badges/{escape(filename)}" alt="{escape(name)}" height="28"/>'


def render_project_cards(items, lang, columns=2, presentation=None):
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
    kind_map = {
        "Personal Project": "个人项目" if lang == "zh" else "Personal Project",
        "Collaboration": "协作项目" if lang == "zh" else "Collaboration",
    }
    cards = []
    for index, project in enumerate(items, 1):
        name = escape(project.get("name", project["id"]))
        repo = escape(project.get("repository", ""))
        desc = escape(localized(project, "description", lang))
        status = status_map.get(project.get("development_status", "Unknown"), project.get("development_status", "Unknown"))
        kind = kind_map.get(project.get("project_type", "Project"), project.get("project_type", "Project"))
        technologies = " ".join(tech_badge(t) for t in project.get("technologies", [])[:6])
        demo = project.get("demo")
        demo_label = "在线体验 ↗" if lang == "zh" else "Live Demo ↗"
        demo_html = f'<a href="{escape(demo)}">{demo_label}</a>' if demo else ""
        cards.append(
            f'<td width="{100 // columns}%" valign="top" style="border:1px solid #{border};padding:16px;background:#{panel}">'
            f'<p><sub><font color="#{accent}">PROJECT {index:02d}</font> · {escape(status)}</sub></p>'
            f'<p><strong><a href="{repo}">{name} ↗</a></strong></p>'
            f'<p>{desc}</p>'
            f'<p><sub>{escape(kind)}</sub></p>'
            f'<p>{technologies}</p>'
            f'<p>{demo_html}</p></td>'
        )
    rows = []
    for start in range(0, len(cards), columns):
        row = cards[start:start + columns]
        while len(row) < columns:
            row.append(f'<td width="{100 // columns}%" style="border:0;background:transparent"></td>')
        rows.append("<tr>" + "".join(row) + "</tr>")
    return '<table><tbody>' + "".join(rows) + '</tbody></table>' if rows else ("暂无项目。" if lang == "zh" else "No projects yet.")


def render_github_activity(lang):
    stats_path = ROOT / "data" / "stats.json"
    stats = json.loads(stats_path.read_text(encoding="utf-8")) if stats_path.exists() else {}
    updated = (stats.get("generated_at") or "")[:10]
    if lang == "zh":
        overview_alt = "GitHub 公开活动统计：提交、仓库、Stars 和 Pull Requests"
        language_alt = "按代码体积分布的主要编程语言"
        contribution_alt = "最近 365 天 GitHub 贡献热力图"
        note = f"数据来自 GitHub REST / GraphQL API，定期缓存；提交数使用 GitHub 公开 Commit Search 统计。更新于 {updated or '暂无'}。"
    else:
        overview_alt = "GitHub public activity: commits, repositories, stars and pull requests"
        language_alt = "Most used languages by source-code bytes"
        contribution_alt = "GitHub contribution activity during the last 365 days"
        note = f"Public data is cached from GitHub REST / GraphQL APIs. Commit count uses GitHub public commit search. Updated {updated or 'not yet synced'}."
    return (
        image("assets/stats/overview.svg", overview_alt)
        + image("assets/stats/languages.svg", language_alt)
        + image("assets/stats/contributions.svg", contribution_alt)
        + f'<p align="center"><sub>{note}</sub></p>'
    )


def render_about(identity, lang):
    summary = escape(localized(identity, "summary", lang))
    method = identity.get("engineering_method", {})
    title = escape(method.get("title_zh" if lang == "zh" else "title_en") or method.get("title", ""))
    desc = escape(method.get("description_zh" if lang == "zh" else "description", ""))
    heading = "ENGINEERING APPROACH" if lang == "en" else "工程方法 / ENGINEERING APPROACH"
    diagram = "assets/profile/about.en.svg" if lang == "en" else "assets/profile/about.zh.svg"
    alt = "Software engineering workflow: requirements, architecture, implementation, testing and delivery"
    return (
        f'<p><strong>{summary}</strong></p>'
        f'<p><sub>{heading}</sub></p>'
        f'<p><strong><font color="#79D7D0">{title}</font></strong></p>'
        f'<p>{desc}</p>'
        + image(diagram, alt)
    )


def render_focus(lang):
    path = "assets/profile/focus.en.svg" if lang == "en" else "assets/profile/focus.zh.svg"
    alt = "Three focus areas: primary direction, current practice and long-term interests"
    return image(path, alt)


def render_link_cards(items, lang, presentation, limit=8):
    if not items:
        return "暂无记录。" if lang == "zh" else "No records yet."
    border = presentation.get("border_color", "2B4052")
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


def render_stack(stack, lang):
    labels = {
        "Languages": ("语言", "LANGUAGES"),
        "Frameworks & Runtime": ("框架与运行时", "FRAMEWORKS & RUNTIME"),
        "Tools & Infrastructure": ("工具与基础设施", "TOOLS & INFRASTRUCTURE"),
        "Graphics & Data": ("图形与数据", "GRAPHICS & DATA"),
    }
    rows = []
    for group, values in stack.items():
        if not values:
            continue
        title = labels.get(group, (group, group))[0 if lang == "zh" else 1]
        badges = " ".join(tech_badge(name) for name in values)
        rows.append(
            f'<p><sub><b>{escape(title)}</b></sub><br/>{badges}</p>'
        )
    return "\n".join(rows)


def build_page(lang, identity, focus, projects, records, milestones, stack, template):
    zh = lang == "zh"
    config = load_yaml("profile/modules.yml")
    presentation = config.get("presentation", {})
    project_columns = max(1, min(3, int(presentation.get("project_columns", 3))))
    labels = {
        "about": "关于我" if zh else "About",
        "focus": "当前关注" if zh else "Current Focus",
        "github_activity": "GitHub 活动" if zh else "GitHub Activity",
        "featured_projects": "精选项目" if zh else "Featured Projects",
        "other_projects": "其他项目" if zh else "Other Projects",
        "contributions": "开源贡献" if zh else "Open-Source Contributions",
        "highlights": "近期动态" if zh else "Recent Highlights",
        "milestones": "里程碑" if zh else "Milestones",
        "tech_stack": "技术栈" if zh else "Technology Stack",
        "activity_archive": "活动档案" if zh else "Activity Archive",
    }
    featured = sorted([p for p in projects if p.get("visibility") == "featured"], key=lambda p: p.get("order", 999))
    others = sorted([p for p in projects if p.get("visibility") == "other"], key=lambda p: p.get("order", 999))
    contributions = [a for a in records if a.get("type") in {"pull_request", "issue", "review"}]
    highlights = [a for a in records if a.get("review_status") == "featured"]
    highlights.sort(key=lambda a: a.get("date") or a.get("updated_at") or "", reverse=True)
    milestone_items = sorted(milestones, key=lambda x: x.get("date", ""), reverse=True)
    if milestone_items:
        milestone_body = "\n".join(
            f"- **{m['date']}** — [{localized(m, 'title', lang)}]({m['evidence']})：{localized(m, 'description', lang)}"
            if zh else f"- **{m['date']}** — [{localized(m, 'title', lang)}]({m['evidence']}): {localized(m, 'description', lang)}"
            for m in milestone_items
        )
    else:
        milestone_body = "里程碑仅在日期、证据与长期意义确认后归档。" if zh else "Milestones are archived only after their date, evidence, and significance are verified."
    archive_link = "[activity/ACTIVITY.md](./activity/ACTIVITY.md)" if zh else "[activity/ACTIVITY.en.md](./activity/ACTIVITY.en.md)"
    archive_sentence = "完整的已审核活动记录见" if zh else "Browse the complete reviewed activity archive:"
    bodies = {
        "about": render_about(identity, lang),
        "focus": render_focus(lang),
        "github_activity": render_github_activity(lang),
        "featured_projects": render_project_cards(featured, lang, project_columns, presentation),
        "other_projects": render_project_cards(others, lang, 1, presentation),
        "contributions": render_link_cards(contributions, lang, presentation, 8),
        "highlights": render_link_cards(highlights, lang, presentation, 5),
        "milestones": milestone_body,
        "tech_stack": render_stack(stack, lang),
        "activity_archive": f"{archive_sentence} {archive_link}。" if zh else f"{archive_sentence} {archive_link}.",
    }
    enabled = [m for m in config.get("modules", []) if m.get("enabled", True)]
    modules_md = "\n\n<hr/>\n\n".join(
        f"## {labels[m['id']]}\n\n{bodies[m['id']]}"
        for m in enabled if m.get("id") in labels
    )
    links = identity.get("links", {})
    social = []
    for label, key in [("GitHub", "github"), ("Luogu", "luogu"), ("Bilibili", "bilibili"), ("X", "x")]:
        if links.get(key):
            social.append(f'<a href="{escape(links[key])}">{label}</a>')
    bio = escape(identity.get("bio", "") if zh else identity.get("bio_en", identity.get("bio", "")))
    domains = " · ".join(identity.get("domains_zh" if zh else "domains_en") or identity.get("domains", []))
    replacements = {
        "{{display_name}}": escape(identity.get("display_name", identity["username"])),
        "{{title}}": escape(identity.get("title_zh" if zh else "title_en") or identity.get("title", "")),
        "{{domains}}": escape(domains),
        "{{bio}}": bio,
        "{{social_links}}": " &nbsp;·&nbsp; ".join(social),
        "{{language_switch}}": (
            '<a href="./README.md">简体中文</a> &nbsp;·&nbsp; <a href="./README.en.md">English</a>'
            if zh else
            '<a href="./README.md">简体中文</a> &nbsp;·&nbsp; <a href="./README.en.md">English</a>'
        ),
        "{{modules}}": modules_md,
        "{{footer}}": "动态开发者主页 · 自动追踪事实，人工审核与精选。" if zh else "Living Developer Profile · Facts are collected automatically and published after human review.",
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
    for activity in ordered:
        day = activity.get("date") or (activity.get("updated_at") or "")[:10] or ("未注明日期" if zh else "Undated")
        lines.append(f"## {day} — {localized(activity, 'title', lang, '活动' if zh else 'Activity')}")
        if activity.get("url"):
            lines[-1] = f"## {day} — [{localized(activity, 'title', lang, '活动' if zh else 'Activity')}]({activity['url']})"
        if activity.get("repository"):
            lines.append(f"\n**仓库：** {activity['repository']}" if zh else f"\n**Repository:** {activity['repository']}")
        description = localized(activity, "description", lang)
        if description:
            lines.append(f"\n{description}")
        note = localized(activity, "review_note", lang)
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
    settings = load_yaml("profile/settings.yml")
    stack = settings.get("tech_stack", {})
    template = (ROOT / "templates/README.template.md").read_text(encoding="utf-8")
    (ROOT / "README.md").write_text(build_page("zh", identity, focus, projects, records, milestones, stack, template), encoding="utf-8")
    (ROOT / "README.en.md").write_text(build_page("en", identity, focus, projects, records, milestones, stack, template), encoding="utf-8")
    (ROOT / "activity/ACTIVITY.md").write_text(build_archive(records, "zh"), encoding="utf-8")
    (ROOT / "activity/ACTIVITY.en.md").write_text(build_archive(records, "en"), encoding="utf-8")
    print("Generated bilingual profile pages and reviewed activity archives.")


if __name__ == "__main__":
    main()
