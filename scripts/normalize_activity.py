#!/usr/bin/env python3
"""Merge newly collected candidates into the review inbox without publishing them."""
from common import load_json, dump_json

def main():
    collected = load_json("data/collected-activity.json", {})
    existing = load_json("activity/inbox.json", [])
    by_id = {x.get("id"): x for x in existing if x.get("id")}
    for item in collected.get("activities", []):
        key = item.get("id")
        if not key:
            continue
        old = by_id.get(key, {})
        merged = {**item, **{
            k: old[k] for k in ("review_status", "review_note", "featured", "quality")
            if k in old
        }}
        merged.setdefault("review_status", "pending")
        by_id[key] = merged
    result = sorted(by_id.values(), key=lambda x: x.get("updated_at") or "", reverse=True)
    dump_json("activity/inbox.json", result)
    print(f"Inbox now contains {len(result)} unique candidates.")

if __name__ == "__main__":
    main()
