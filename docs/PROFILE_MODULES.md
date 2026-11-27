# Profile presentation system

The profile is generated from four independent layers:

1. **Source data** — `profile/*.yml` and `activity/records.yml`
2. **Presentation tokens and module order** — `profile/modules.yml`
3. **Reusable renderers** — `scripts/generate_profile.py`
4. **Page shell** — `templates/README.template.md`

## Visual system

The current direction is **Dark Technical Editorial**: a restrained GitHub-dark palette, cool-blue primary accent, amber secondary accent, consistent neutral surfaces, compact metadata, and a small set of reusable visual patterns.

Change semantic tokens in `profile/modules.yml` rather than scattering colors through the renderer:

- `accent`, `secondary_accent`, `title_color`
- `text_color`, `panel_color`, `border_color`
- `badge_color`, `badge_logo_color`, `badge_style`
- `project_columns` (1–3)

Stats cards, project cards, focus cards, activity rows, social badges, and technology badges consume these tokens. External SVG providers are configurable and do not own the profile's content.

## Change layout without editing the page shell

Edit `profile/modules.yml`:

- Reorder entries under `modules` to change section order.
- Set `enabled: false` to hide a section without deleting its data.
- Change `project_columns` to adjust project-card density.
- Replace `stats_provider`, `contribution_provider`, or `badge_provider` with compatible services.

The README template only defines the identity header, module insertion point, and footer.

## Add a new module

1. Add a stable module ID and bilingual heading in `build_page()`.
2. Implement a renderer that accepts source data and presentation tokens.
3. Register the ID in `ALLOWED_MODULES` in `scripts/validate_data.py`.
4. Add the module to `profile/modules.yml`.
5. Reuse existing semantic tokens and components where possible.
6. Keep external services optional; a failed image must not prevent the rest of the README from rendering.

## Project cards

Cards are generated from `profile/projects.yml`. Names, descriptions, repository links, demos, status, technologies, and star badges are data-driven. Do not put project-specific facts or project ordering into renderer code.

## Reliability

GitHub statistics, contribution charts, and badges are third-party SVG images. They may be rate-limited, stale, or temporarily unavailable. The textual profile and project metadata are generated locally from reviewed repository data and remain readable without these images.
