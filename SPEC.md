# Fusion Skript specification

The first checked draft preserves the energy opening of the existing course.
Develop subsequent chapters incrementally in the established sequence, with
greater mathematical depth where needed. The full reference may exceed live
coverage. The existing questions remain the exam baseline, subject to changes
until semester end and a final chapter cutoff.

## Authoring and sources

- Define symbols, assumptions, units and energy boundaries before calculations.
- Derive equations independently; include intermediate steps and limiting cases.
- Use the first lecture's original slides and multi-year transcripts as evidence
  of content and pacing. MacKay is a conceptual reference, not reusable artwork.
- Record the year, status, source and reuse terms of every empirical input.
  Distinguish preliminary statistics from final data and model scenarios.
- Generate canonical plots once for both script and slides. Include alternative
  descriptions; redundant labels and line styles supplement color.
- Every section ends with original checks and concise answers. Essential results
  remain visible; optional extended reasoning may use collapsible details.

## Build and release

Typst produces a static HTML bundle and PDF from the same chapter components.
STIX Two fonts and live layout are shared with plasma. SymPy verifies model
identities; Matplotlib generates original SVG/PDF plots. The build does not
publish. Hosting supports incremental publication. `public/` excludes all private evidence
and recordings. Use section URLs and PDF fallback in FuEL; HTML import requires
an authenticated platform pilot.

## Hosting

The public source is `krystophny/fusion-skript` on GitHub, with Actions-based
Pages at `https://krystophny.github.io/fusion-skript/`. `github` names
`git@github.com:krystophny/fusion-skript.git`; `origin` names the private TU Graz
mirror `git@gitlab.tugraz.at:plasma/proj/teaching/fusion-skript.git`.
`scripts/publish.sh` builds, tests and exports; `--release` also pushes `main`
to both remotes. Each push to GitHub `main` deploys after workflow checks pass.
The script never creates commits.

`scripts/build-site.sh` builds the site, PDF, numbered decks and SVG presenter
under `public/`. The presenter keeps Plasma's appearance and interaction,
reads course/author from `decks.json`, and generates course-specific web-app
identity and cache names. Every page needs one `<present-page>` metadata
record from `slides/present-meta.typ`; the build fails otherwise. Media are copied from local staged site
files to same-origin, checksum-versioned URLs; no legacy assets are fetched.

The current Nextcloud `lv/fusion/2026/` folder is publicly shared. Exports
include `skript/fusion-physics.pdf`, built deck PDFs, derived figures, and
derivation sources. An ownership
manifest controls stale-file removal and preserves files the exporter did
not write, including examination material and modified personal copies.

## Authorities

- [Fusion course plan](../../Nextcloud/lv/fusion/PLAN.md): live pacing and exam policy.
- [Shared teaching rules](../../Nextcloud/lv/AGENTS.md): private transition and CC release.
- [Delivery register](../fusion-course-archive/config/delivery.json): clips, gaps, reviews and uploads.
- [Plasma Skript](../plasma-skript/SPEC.md): infrastructure reference.

Original content and plots: CC BY 4.0. Code: MIT. Fonts: SIL OFL. Numeric facts
are cited individually; no provider chart, photograph or table image is reused.
Provider terms remain linked in `data/README.md` and are not relabelled as our licence.
