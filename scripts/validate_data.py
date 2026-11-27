#!/usr/bin/env python3
"""Validate profile data before rendering or publishing."""
from datetime import date
from urllib.parse import urlparse
from common import load_yaml

ALLOWED_VISIBILITY = {"featured", "other", "draft"}
ALLOWED_MODULES = {"about", "focus", "github_activity", "featured_projects", "other_projects", "contributions", "highlights", "milestones", "tech_stack", "activity_archive"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def valid_url(value):
    if value is None:
        return True
    parsed = urlparse(str(value))
    return parsed.scheme in {"https", "http"} and bool(parsed.netloc)

def valid_hex_color(value):
    value = str(value or "")
    return len(value) == 6 and all(c in "0123456789abcdefABCDEF" for c in value)

def main():
    identity = load_yaml("profile/identity.yml").get("identity", {})
    require(identity.get("username") == "zshebjtzs", "Unexpected profile username.")
    require(bool(identity.get("bio")), "Identity bio must not be empty.")
    for name, url in (identity.get("links") or {}).items():
        require(valid_url(url), f"Invalid social link: {name}")
    projects = load_yaml("profile/projects.yml").get("projects", [])
    ids = set()
    for p in projects:
        require(p.get("id") not in ids, f"Duplicate project id: {p.get('id')}")
        ids.add(p.get("id"))
        require(p.get("visibility") in ALLOWED_VISIBILITY, f"Invalid visibility for {p.get('id')}")
        require(valid_url(p.get("repository")), f"Invalid repository URL for {p.get('id')}")
        require(valid_url(p.get("demo")), f"Invalid demo URL for {p.get('id')}")
    module_config = load_yaml("profile/modules.yml")
    modules = module_config.get("modules", [])
    module_ids = [m.get("id") for m in modules]
    require(len(module_ids) == len(set(module_ids)), "Duplicate presentation module id.")
    for module in modules:
        require(module.get("id") in ALLOWED_MODULES, f"Unknown presentation module: {module.get('id')}")
        require(isinstance(module.get("enabled", True), bool), f"Invalid enabled flag for module: {module.get('id')}")
    presentation = module_config.get("presentation", {})
    require(1 <= int(presentation.get("project_columns", 2)) <= 3, "project_columns must be between 1 and 3.")
    for key in ("stats_provider", "contribution_provider"):
        require(valid_url(presentation.get(key)), f"Invalid presentation provider URL: {key}")
    for key in ("accent", "secondary_accent", "title_color", "text_color", "panel_color", "border_color", "badge_color", "badge_text_color"):
        require(valid_hex_color(presentation.get(key)), f"Invalid presentation color token: {key}")
    records = load_yaml("activity/records.yml").get("activities", [])
    activity_ids = set()
    for a in records:
        require(a.get("id") not in activity_ids, f"Duplicate activity id: {a.get('id')}")
        activity_ids.add(a.get("id"))
        require(a.get("review_status") in {"verified", "featured", "archived"},
                f"Unreviewed activity cannot be published: {a.get('id')}")
    milestones = load_yaml("profile/milestones.yml").get("milestones", [])
    milestone_ids = set()
    for m in milestones:
        require(m.get("id") not in milestone_ids, f"Duplicate milestone id: {m.get('id')}")
        milestone_ids.add(m.get("id"))
        date.fromisoformat(str(m.get("date")))
        require(valid_url(m.get("evidence")), f"Invalid milestone evidence URL: {m.get('id')}")
    print(f"Validation passed: {len(projects)} projects, {len(records)} reviewed activities, {len(milestones)} milestones.")

if __name__ == "__main__":
    main()
