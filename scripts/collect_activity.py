#!/usr/bin/env python3
"""Collect public GitHub activity into data/ only. Never publishes the profile."""
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from common import dump_json

API = "https://api.github.com"
USERNAME = os.environ.get("GITHUB_USERNAME", "zshebjtzs")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "living-developer-profile/1.0",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return __import__("json").loads(response.read().decode("utf-8"))

def paginate(url, max_pages=5):
    out = []
    for page in range(1, max_pages + 1):
        separator = "&" if "?" in url else "?"
        data = get_json(f"{url}{separator}per_page=100&page={page}")
        if not data:
            break
        out.extend(data)
        if len(data) < 100:
            break
    return out

def normalize_search_item(item, kind):
    repo = item.get("repository") or {}
    number = item.get("number")
    merged = bool(item.get("pull_request", {}).get("merged_at"))
    state = "merged" if kind == "pull_request" and merged else item.get("state", "unknown")
    return {
        "id": item.get("node_id") or item.get("html_url"),
        "source": "github",
        "repository": repo.get("full_name"),
        "url": item.get("html_url"),
        "type": kind,
        "title": item.get("title") or f"{kind} #{number}",
        "description": (item.get("body") or "").strip()[:500],
        "status": state,
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "author": item.get("user", {}).get("login"),
        "number": number,
        "merged": merged,
        "review_status": "pending",
    }

def search_items(query, kind):
    encoded = urllib.parse.quote(query, safe=":+")
    data = get_json(f"{API}/search/issues?q={encoded}&sort=updated&order=desc&per_page=100")
    return [normalize_search_item(x, kind) for x in data.get("items", [])]

def normalize_event(event):
    actor = (event.get("actor") or {}).get("login")
    if not actor or actor.lower() != USERNAME.lower():
        return None
    typ = event.get("type")
    payload = event.get("payload") or {}
    repo = (event.get("repo") or {}).get("name")
    base = {
        "id": f"event:{event.get('id')}",
        "source": "github_event",
        "repository": repo,
        "created_at": event.get("created_at"),
        "updated_at": event.get("created_at"),
        "author": actor,
        "review_status": "pending",
    }
    if typ == "PushEvent":
        commits = payload.get("commits") or []
        return {**base, "type": "push", "title": f"Pushed updates to {repo}",
                "description": f"{len(commits)} commit(s) in this push.", "status": "pushed",
                "commit_count": len(commits), "url": f"https://github.com/{repo}/commits"}
    if typ == "PullRequestReviewEvent":
        pr = payload.get("pull_request") or {}
        return {**base, "type": "review", "title": f"Reviewed: {pr.get('title', 'Pull request')}",
                "description": "", "status": payload.get("action", "submitted"),
                "url": pr.get("html_url")}
    if typ == "ReleaseEvent":
        rel = payload.get("release") or {}
        return {**base, "type": "release", "title": rel.get("name") or rel.get("tag_name") or "Published a release",
                "description": (rel.get("body") or "")[:500], "status": payload.get("action", "published"),
                "url": rel.get("html_url")}
    if typ == "IssuesEvent":
        issue = payload.get("issue") or {}
        return {**base, "type": "issue_event", "title": issue.get("title", "Issue activity"),
                "description": "", "status": payload.get("action", "updated"), "url": issue.get("html_url")}
    return None

def main():
    try:
        owned = paginate(f"{API}/users/{USERNAME}/repos?type=owner&sort=updated", max_pages=3)
        repos = [{
            "id": r.get("id"), "full_name": r.get("full_name"), "description": r.get("description"),
            "html_url": r.get("html_url"), "default_branch": r.get("default_branch"),
            "language": r.get("language"), "topics": r.get("topics", []),
            "updated_at": r.get("updated_at"), "pushed_at": r.get("pushed_at"),
            "archived": r.get("archived"), "fork": r.get("fork"),
        } for r in owned]
        activities = []
        activities += search_items(f"author:{USERNAME} is:pr", "pull_request")
        activities += search_items(f"author:{USERNAME} is:issue", "issue")
        events = paginate(f"{API}/users/{USERNAME}/events/public", max_pages=3)
        for event in events:
            item = normalize_event(event)
            if item:
                activities.append(item)
        by_id = {}
        for item in activities:
            key = item.get("id")
            if not key:
                continue
            old = by_id.get(key)
            if old is None or (item.get("updated_at") or "") >= (old.get("updated_at") or ""):
                by_id[key] = item
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "username": USERNAME,
            "repositories": repos,
            "activities": sorted(by_id.values(), key=lambda x: x.get("updated_at") or "", reverse=True),
        }
        dump_json("data/collected-activity.json", payload)
        print(f"Collected {len(repos)} owned repositories and {len(by_id)} activity candidates.")
    except Exception as exc:
        print(f"Collection failed: {exc}", file=sys.stderr)
        raise

if __name__ == "__main__":
    main()
