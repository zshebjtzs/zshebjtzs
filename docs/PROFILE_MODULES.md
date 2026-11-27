# Profile presentation modules

The profile renderer separates source data, presentation configuration, reusable renderers, and the README shell.

## Change the layout without editing Python

Edit `profile/modules.yml`:

- Reorder entries under `modules` to change section order.
- Set `enabled: false` to hide a section without deleting its data.
- Adjust `presentation.project_columns` (1–3), `theme`, and `accent` to change visual settings.
- Replace `stats_provider` or `contribution_provider` to use another compatible SVG service.

The README template only defines the identity header, the module insertion point, and the footer. It does not own the section order.

## Add a new module

1. Add a stable module ID and bilingual heading in `build_page()` in `scripts/generate_profile.py`.
2. Add its renderer output to `module_bodies`; keep data loading separate from presentation.
3. Register the ID in `ALLOWED_MODULES` in `scripts/validate_data.py`.
4. Add the module to `profile/modules.yml` with an `enabled` flag.
5. Keep external services optional: a failed image must not prevent the rest of the README from rendering.

## External image services

GitHub stats and contribution graphics are loaded from configurable third-party SVG endpoints. They may be rate-limited, stale, or temporarily unavailable. Project information and the rest of the profile are generated locally from reviewed repository data and remain readable without those images.

## Project cards

Project cards are generated from `profile/projects.yml`. Names, descriptions, repository links, demos, status, technologies, and star badges are data-driven. The card grid column count is configurable; avoid putting project-specific facts in the renderer.
