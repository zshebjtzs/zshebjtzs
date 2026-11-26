# Review workflow

The collector and publisher are deliberately separate. The inbox is a review queue; it is never rendered directly into the public profile.

## Candidate collection and review

1. The scheduled collector opens or updates a pull request on `automation/activity-inbox`.
2. Inspect `activity/inbox.json`. Verify authorship, repository, activity type, status, and the actual contribution.
3. Keep the stable candidate `id`; use these editorial states:
   - `featured`: a high-signal contribution suitable for the profile highlights.
   - `archived`: valid and useful history, but not a profile highlight.
   - `ignored`: duplicate, empty, or low-value collection noise.
   - `pending`: still in progress or not yet verifiable.
4. Merge the candidate pull request only after the inbox classification is reviewed. Merging this PR updates the review queue; it does **not** publish activities.

## Publication

5. After the candidate PR has been merged, separately update `activity/records.yml` on `main`. Copy only reviewed `featured` and `archived` records; map their editorial state to `review_status` and retain a concise `review_note`.
6. Do not copy `ignored` or `pending` candidates into `records.yml`. Do not edit `records.yml` on the collector branch: the collector PR is restricted to collection data.
7. The publication workflow validates `records.yml` and regenerates the Chinese/English profile and activity archives.

## Data hygiene

- Push events with zero exposed commits are discarded.
- Issue lifecycle events are not collected as separate activities because authored Issues and PRs are represented by their canonical Search API records.
- PRs and Issues must retain their correct distinct `type` values.
- The inbox is part of a public repository. Never store private information in it.
