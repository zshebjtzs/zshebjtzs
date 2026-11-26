# Maintaining this profile

## Source-of-truth rules

- `profile/identity.yml`: manually maintained identity and public links.
- `profile/current-focus.yml`: machine-suggested, human-confirmed focus.
- `profile/projects.yml`: project facts and editorial visibility.
- `profile/milestones.yml`: dated, evidence-backed milestones.
- `activity/inbox.json`: automatically collected candidates; never public by itself.
- `activity/records.yml`: manually reviewed records eligible for publication.
- `README.md` and `activity/ACTIVITY.md`: generated outputs; edit source files instead.

## Activity review

For each candidate in `activity/inbox.json`:

1. Verify that the activity belongs to this account.
2. Check the repository, title, URL, and current GitHub state.
3. Set `review_status` to `verified`, `featured`, `archived`, or `ignored`.
4. Copy only relevant reviewed entries into `activity/records.yml`.
5. Set `featured: true` only when the activity is worth highlighting publicly.
6. Preserve the GitHub status separately from the editorial review status.

Do not treat an open PR as a merged contribution. Do not infer maintainer status from a single contribution. Avoid publishing routine comments or low-signal activity.

## Project review

- `visibility: featured`: shown in the main project section.
- `visibility: other`: shown in the secondary project section.
- `visibility: draft`: hidden from the public profile.
- `development_status` describes the project's actual state and is independent of visibility.
- Stars, commits, and update timestamps must not automatically change editorial selection or ordering.

## Milestones

A milestone must have a valid date and evidence URL. Prefer releases, substantial architecture changes, major merged contributions, and published technical work. Do not invent dates or infer significance from activity volume.

## Local validation

```bash
pip install -r requirements.txt
python scripts/validate_data.py
python scripts/generate_profile.py
```
