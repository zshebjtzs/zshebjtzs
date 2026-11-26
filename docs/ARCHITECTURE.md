# Profile system architecture

## Data flow

```text
GitHub public API
      |
      v
scripts/collect_activity.py
      |
      v
data/collected-activity.json
      |
      v
scripts/normalize_activity.py
      |
      v
activity/inbox.json  ---- human review PR
                              |
                              v
                    activity/records.yml
                              |
profile/*.yml ---------------+
                              |
                              v
                    validate_data.py
                              |
                              v
                    generate_profile.py
                              |
                    +---------+---------+
                    |                   |
                    v                   v
                 README.md       activity/ACTIVITY.md
```

## Trust boundaries

The collector only writes candidate data. It never writes to reviewed records or generated public output. The publication workflow runs after reviewed source files are merged into `main`.

GitHub's lifecycle state (`open`, `closed`, `merged`, etc.) is not the same as editorial review state (`pending`, `verified`, `featured`, `archived`, `ignored`).

## Collection coverage and limitations

The collector combines:
- public repositories owned by the account;
- public pull requests and issues authored by the account, as exposed by GitHub Search;
- recent public account events, including pushes, reviews, releases, and issue events.

GitHub's public Events API is a rolling, limited history and does not provide a complete lifetime activity archive. The system therefore keeps manually curated records and allows manual additions for articles, competitions, offline projects, and other work not represented by GitHub APIs.

The initial workflow uses the repository-scoped `GITHUB_TOKEN`. Public endpoints are queried; API rate limits still apply. If collection reaches rate limits, the workflow fails visibly rather than silently publishing incomplete data.
