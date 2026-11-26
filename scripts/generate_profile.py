#!/usr/bin/env python3
"""Generate README.md and activity/ACTIVITY.md from reviewed source data."""
from common import ROOT, load_yaml

def md_link(label, url):
    return f"[{label}]({url})" if url else label

def bullets(items):
    return "\n".join(f"- {x}" for x in items) if items else "- 暂无已确认内容。"

def render_project(p):
    line = f"### {md_link(p['name'], p['repository'])}"
    if p.get("demo"):
        line += f" · {md_link('在线体验', p['demo'])}"
    line += f"\n\n{p.get('description', '')}"
    line += f"\n\n`{p.get('development_status', 'Unknown')}` · {p.get('project_type', 'Project')}"
    if p.get("highlights"):
        line += "\n\n" + "\n".join(f"- {x}" for x in p["highlights"])
    return line

def main():
    identity = load_yaml("profile/identity.yml")["identity"]
    focus = load_yaml("profile/current-focus.yml")
    projects = load_yaml("profile/projects.yml").get("projects", [])
    records = load_yaml("activity/records.yml").get("activities", [])
    milestones = load_yaml("profile/milestones.yml").get("milestones", [])
    template = (ROOT / "templates/README.template.md").read_text(encoding="utf-8")
    featured = [p for p in projects if p.get("visibility") == "featured"]
    others = [p for p in projects if p.get("visibility") == "other"]
    featured.sort(key=lambda p: p.get("order", 999))
    others.sort(key=lambda p: p.get("order", 999))
    links = identity.get("links", {})
    social = " · ".join(
        md_link(label, links.get(key))
        for label, key in [("GitHub", "github"), ("Luogu", "luogu"), ("Bilibili", "bilibili"), ("X", "x")]
        if links.get(key)
    )
    primary = bullets(focus.get("primary_focus", []))
    secondary = bullets(focus.get("secondary_interests", []))
    long_term = bullets(focus.get("long_term_interests", []))
    focus_md = f"**Primary**\n{primary}\n\n**Secondary**\n{secondary}\n\n**Long-term**\n{long_term}"
    method = identity.get("engineering_method", {})
    method_md = f"**{method.get('title', 'Engineering Method')}** — {method.get('description', '')}"
    featured_md = "\n\n".join(render_project(p) for p in featured) or "暂无精选项目。"
    others_md = "\n\n".join(render_project(p) for p in others) or "暂无其他公开项目。"
    contributions = [a for a in records if a.get("type") in {"pull_request", "issue", "review"}]
    contributions_md = "\n".join(
        f"- [{a.get('title', 'Contribution')}]({a.get('url', '#')}) · {a.get('repository', '')}"
        for a in contributions[:8]
    ) or "贡献记录采用自动收集、人工审核机制；目前暂无已审核发布的记录。"
    highlights = [a for a in records if a.get("review_status") == "featured"]
    highlights.sort(key=lambda a: a.get("date") or a.get("updated_at") or "", reverse=True)
    highlights_md = "\n".join(
        f"- **{a.get('date', (a.get('updated_at') or '')[:10])}** — [{a.get('title', 'Activity')}]({a.get('url', '#')})"
        for a in highlights[:5]
    ) or "暂无已审核精选动态。"
    milestone_md = "\n".join(
        f"- **{m['date']}** — [{m['title']}]({m['evidence']})：{m.get('description', '')}"
        for m in sorted(milestones, key=lambda x: x.get("date", ""), reverse=True)
    ) or "里程碑仅在日期、证据与长期意义确认后归档。"
    stack = load_yaml("profile/settings.yml").get("tech_stack", {})
    if not stack:
        stack = {
            "Experienced": ["JavaScript", "C++", "Git", "GitHub"],
            "Familiar": ["TypeScript", "Vue 3", "Node.js", "MySQL", "HTML", "CSS", "Vite"],
            "Exploring": [],
        }
    stack_md = "\n".join(
        f"- **{level}:** {', '.join(values) if values else '—'}"
        for level, values in stack.items()
    )
    replacements = {
        "{{display_name}}": identity.get("display_name", identity["username"]),
        "{{title}}": identity.get("title", ""),
        "{{domains}}": " · ".join(identity.get("domains", [])),
        "{{bio}}": identity.get("bio", ""),
        "{{social_links}}": social,
        "{{summary}}": identity.get("summary", ""),
        "{{engineering_method}}": method_md,
        "{{current_focus}}": focus_md,
        "{{featured_projects}}": featured_md,
        "{{other_projects}}": others_md,
        "{{open_source_contributions}}": contributions_md,
        "{{recent_highlights}}": highlights_md,
        "{{milestones}}": milestone_md,
        "{{tech_stack}}": stack_md,
    }
    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)
    (ROOT / "README.md").write_text(output, encoding="utf-8")
    archive = ["# Activity Archive", "", "Only reviewed records are included.", ""]
    ordered = sorted(records, key=lambda a: a.get("date") or a.get("updated_at") or "", reverse=True)
    if not ordered:
        archive.append("No reviewed activity records have been published yet.")
    for a in ordered:
        d = a.get("date") or (a.get("updated_at") or "")[:10] or "Undated"
        archive.append(f"## {d} — {md_link(a.get('title', 'Activity'), a.get('url'))}")
        if a.get("repository"):
            archive.append(f"\n**Repository:** {a['repository']}")
        if a.get("description"):
            archive.append(f"\n{a['description']}")
        if a.get("review_note"):
            archive.append(f"\n> {a['review_note']}")
        archive.append("")
    (ROOT / "activity/ACTIVITY.md").write_text("\n".join(archive).rstrip() + "\n", encoding="utf-8")
    print("Generated README.md and activity/ACTIVITY.md.")

if __name__ == "__main__":
    main()
