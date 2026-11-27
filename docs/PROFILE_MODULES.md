# Profile presentation system

The profile is a data-driven README renderer with a reusable visual system.

## Visual direction

**Tech-Dawn & Open-Source Minimalist**

- Deep-sea blue and cool silver form the structural palette.
- Soft cyan is the primary accent; sunrise orange is reserved for secondary emphasis.
- Use editorial hierarchy, restrained separators, compact metadata, and deliberate whitespace.
- Avoid turning every section into a bordered card. Cards are reserved for project comparisons and compact grouped data.
- Keep headings, typography, spacing, and metadata patterns consistent in both languages.

## Architecture

1. **Source data** — `profile/*.yml` and `activity/records.yml`
2. **Presentation tokens and module order** — `profile/modules.yml`
3. **Reusable renderers and local SVG asset generation** — `scripts/generate_profile.py`
4. **Page shell** — `templates/README.template.md`

The page shell controls the hero and overall structure. Each module has its own renderer. Adding a module must not require rewriting the other renderers.

## Technology badges

Technology badges use a separate component from generic metadata badges. They are generated as repository-hosted SVGs with brand-specific colors and a logo mark, inspired by the compact badge row used in the qdezJDS README.

The SVG assets live in `assets/badges/`; filenames are deterministic. If an official logo path is not embedded for a technology, the badge uses a short typographic mark rather than requesting a remote image. The README therefore does not depend on Shields.io for technology logos.

## Layout configuration

Edit `profile/modules.yml` to:

- Reorder or disable modules.
- Change the project grid column count.
- Retheme semantic colors without changing content data.

## Extension rules

1. Add a stable module ID and bilingual heading.
2. Implement an independent renderer receiving source data and presentation tokens.
3. Register the ID in the validator.
4. Add the module to `profile/modules.yml`.
5. Reuse semantic tokens and components.
6. Keep remote visualizations optional and ensure the rest of the profile remains readable if they fail.
