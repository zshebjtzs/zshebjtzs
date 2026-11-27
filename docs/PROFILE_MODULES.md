# Profile presentation system

The profile is generated from four independent layers:

1. **Source data** — `profile/*.yml` and `activity/records.yml`
2. **Presentation tokens and module order** — `profile/modules.yml`
3. **Reusable renderers and asset generation** — `scripts/generate_profile.py`
4. **Page shell** — `templates/README.template.md`

## Visual system

The current direction is **Dark Technical Editorial**: a restrained GitHub-dark palette, cool-blue primary accent, amber secondary accent, consistent neutral surfaces, compact metadata, and reusable visual patterns.

Change semantic tokens in `profile/modules.yml` rather than scattering colors through the renderer. Badge SVGs are generated locally from these tokens and stored in `assets/badges/`.

## Self-hosted badge assets

All decorative badges (social links, language switch, project status, project type, and technology labels) are generated as small SVG files in this repository. README images use relative paths, so they do not depend on Shields.io, an external image proxy, or a badge service being reachable.

The generator uses deterministic filenames derived from badge content and color tokens. Re-running it updates the same asset when its content changes. The publish workflow commits generated SVG assets alongside both README files.

GitHub Stars are intentionally shown as repository links rather than live third-party image badges. This avoids making core project cards depend on a remote badge endpoint.

## Change layout without editing the page shell

Edit `profile/modules.yml`:

- Reorder entries under `modules` to change section order.
- Set `enabled: false` to hide a section without deleting its data.
- Change `project_columns` to adjust project-card density.
- Change semantic color tokens to retheme all locally generated badges and cards.

## Add a new module

1. Add a stable module ID and bilingual heading in `build_page()`.
2. Implement a renderer that accepts source data and presentation tokens.
3. Register the ID in `ALLOWED_MODULES` in `scripts/validate_data.py`.
4. Add the module to `profile/modules.yml`.
5. Reuse existing semantic tokens and components where possible.
6. Keep external services optional; a failed image must not prevent the rest of the README from rendering.

## Reliability boundary

The profile's badges and technology labels are self-hosted. GitHub statistics and contribution charts remain optional third-party visualizations and may be stale, rate-limited, or unavailable. The profile's identity, project information, reviewed activity, and local badges remain readable independently of those services.
