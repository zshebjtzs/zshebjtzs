#!/usr/bin/env python3
"""Collect public GitHub profile metrics into a cacheable, reproducible JSON snapshot."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
USERNAME = os.getenv("GITHUB_USERNAME", "zshebjtzs")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUTPUT = ROOT / "data" / "stats.json"


def request_json(url, method="GET", payload=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "zshebjtzs-profile-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    with urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def search_count(query):
    url = "https://api.github.com/search/commits?" + urlencode({"q": query, "per_page": 1})
    return int(request_json(url).get("total_count", 0))


def issue_count(query):
    url = "https://api.github.com/search/issues?" + urlencode({"q": query, "per_page": 1})
    return int(request_json(url).get("total_count", 0))


def collect_repositories():
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/repos?" + urlencode({
            "type": "owner", "per_page": 100, "page": page, "sort": "updated"
        })
        batch = request_json(url)
        repos.extend(r for r in batch if not r.get("fork") and not r.get("private"))
        if len(batch) < 100:
            break
        page += 1
    return repos


def collect_contributions(now):
    """Fetch the last 365 days of public contribution-calendar data."""
    start = now - timedelta(days=364)
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date contributionCount }
            }
          }
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "login": USERNAME,
            "from": start.strftime("%Y-%m-%dT00:00:00Z"),
            "to": now.strftime("%Y-%m-%dT23:59:59Z"),
        },
    }
    result = request_json("https://api.github.com/graphql", method="POST", payload=payload)
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL returned errors")
    user = (result.get("data") or {}).get("user") or {}
    calendar = user.get("contributionsCollection", {}).get("contributionCalendar")
    if not calendar:
        raise RuntimeError("Contribution calendar is unavailable")
    days = []
    for week in calendar.get("weeks", []):
        days.extend(week.get("contributionDays", []))
    return {
        "total": int(calendar.get("totalContributions", 0)),
        "days": [
            {"date": d["date"], "count": int(d["contributionCount"])}
            for d in days if d.get("date")
        ],
    }


def main():
    now = datetime.now(timezone.utc)
    previous = {}
    if OUTPUT.exists():
        try:
            previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            previous = {}

    try:
        repos = collect_repositories()
        languages = {}
        for repo in repos:
            try:
                values = request_json(repo["languages_url"])
                for name, size in values.items():
                    languages[name] = languages.get(name, 0) + int(size)
            except (HTTPError, URLError, TimeoutError, ValueError):
                continue

        metrics = {
            "total_commits": search_count(f"author:{USERNAME}"),
            "total_pull_requests": issue_count(f"author:{USERNAME} type:pr"),
            "total_issues": issue_count(f"author:{USERNAME} type:issue"),
        }
        try:
            contributions = collect_contributions(now)
        except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError, KeyError):
            contributions = previous.get("contributions", {"total": 0, "days": []})

        data = {
            "schema_version": 1,
            "username": USERNAME,
            "generated_at": now.isoformat(),
            "source": "GitHub REST and GraphQL APIs; public data only",
            "metrics": {
                **metrics,
                "public_repositories": len(repos),
                "stars": sum(int(r.get("stargazers_count", 0)) for r in repos),
                "forks": sum(int(r.get("forks_count", 0)) for r in repos),
                "followers": int(request_json(f"https://api.github.com/users/{USERNAME}").get("followers", 0)),
                "yearly_contributions": int(contributions.get("total", 0)),
            },
            "languages": dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)[:8]),
            "contributions": contributions,
        }
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Updated public GitHub profile statistics.")
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        if previous:
            print(f"Collection failed; retaining previous stats snapshot: {exc}", file=sys.stderr)
            return
        raise


if __name__ == "__main__":
    main()
