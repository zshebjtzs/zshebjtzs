# Review workflow

1. The scheduled collector opens or updates a pull request on `automation/activity-inbox`.
2. Inspect `activity/inbox.json`; verify authorship and relevance.
3. Preserve the candidate record's stable `id`.
4. Update its editorial status and notes in the inbox as needed.
5. Copy selected records to `activity/records.yml`.
6. Merge the review PR.
7. The publication workflow validates source data and regenerates the public README and activity archive.

The inbox is not rendered into the profile, but the repository itself is public. Do not store private information in the inbox.
