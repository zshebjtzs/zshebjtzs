# Profile Visual System

## Direction

**Tech-Dawn & Open-Source Minimalist**

- Deep-sea blue and cool silver are the structural palette.
- Soft cyan is the primary accent; sunrise orange is secondary.
- Visual hierarchy comes from spacing, typography, diagrams, and selective panels rather than enclosing every paragraph in a card.
- Keep all public profile information readable as text. SVGs are supporting visual components, not the only carrier of essential meaning.

## Rendering pipeline

1. `profile/*.yml` contains identity, focus, projects, technology groups, and module configuration.
2. `scripts/collect_stats.py` snapshots public GitHub statistics into `data/stats.json`.
3. `scripts/generate_visuals.py` creates repository-hosted SVG assets and technology badges.
4. `scripts/generate_profile.py` composes the Chinese and English README pages and activity archives.
5. `publish-profile.yml` validates and regenerates on source changes, weekly schedule, or manual dispatch.

## Components

| Component | Source | Generated asset |
|---|---|---|
| Hero banner | Identity and design tokens | `assets/profile/hero.svg` |
| Engineering workflow | Engineering approach | `assets/profile/about.*.svg` |
| Focus matrix | `profile/current-focus.yml` | `assets/profile/focus.*.svg` |
| GitHub overview | `data/stats.json` | `assets/stats/overview.svg` |
| Language distribution | Repository language byte totals | `assets/stats/languages.svg` |
| Contribution calendar | GitHub GraphQL contribution calendar | `assets/stats/contributions.svg` |
| Technology badges | `profile/settings.yml` | `assets/badges/tech-*.svg` |

## Statistics semantics

- **Commits**: count returned by GitHub public Commit Search for `author:zshebjtzs`. Search indexing may lag; this is not a count of private commits.
- **Repositories**: non-fork public repositories owned by the profile.
- **Stars**: sum of stars across those owned public repositories.
- **Pull Requests**: public pull requests authored by the profile, as indexed by GitHub Search.
- **Languages**: aggregated source-code byte counts from the Languages API across owned, non-fork public repositories.
- **Contribution calendar**: public GitHub contributions for the trailing 365-day period.

The collector retains the last valid snapshot if an API request fails. The README uses local SVG files, so a transient third-party image-provider outage cannot break the statistics area. The displayed timestamp is stored in `data/stats.json`.

## Technology badges

The badges follow the compact, flat, brand-color style used at the beginning of the qdezJDS README: recognizable brand color, a logo/monogram, consistent height, and a short label. They are generated locally and committed with the profile; README rendering does not depend on Shields.io availability.

Technology groups describe domains, not skill levels. Add or remove technologies in `profile/settings.yml`; do not add tools merely because they appear in a generator's logo catalog.

## Extension rules

- Add content to source YAML, not generated README files.
- Add modules through a stable ID in `profile/modules.yml`.
- Keep module renderers independent.
- Put reusable colors and layout settings in presentation tokens.
- Keep generated SVGs deterministic and self-hosted.
- Preserve bilingual parity and validate both pages after changes.
