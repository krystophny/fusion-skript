# Fusion Skript specification

There is no script for now (decision of 26 October 2026). The lecture decks
and the online slide viewer <https://krystophny.github.io/fusion-skript/present/>
are the course reference. A future script will be hand-written page by page;
the withdrawn generated chapters remain only in Git history. Develop decks in
the established sequence, with greater mathematical depth where needed. The existing questions remain the exam baseline, subject to changes
until semester end and a final chapter cutoff.

## Authoring and sources

- Define symbols, assumptions, units and energy boundaries before calculations.
- Derive equations independently; include intermediate steps and limiting cases.
- Use the first lecture's original slides and multi-year transcripts as evidence
  of content and pacing. MacKay is a conceptual reference, not reusable artwork.
- Record the year, status, source and reuse terms of every empirical input.
  Distinguish preliminary statistics from final data and model scenarios.
- Generate canonical plots once for slides and derivations. Include alternative
  descriptions; redundant labels and line styles supplement color.
- Every section ends with original checks and concise answers. Essential results
  remain visible; optional extended reasoning may use collapsible details.

## Build and release

Typst produces the deck PDFs and the SVG pages of the viewer.
STIX Two fonts and live layout are shared with plasma. SymPy verifies model
identities; Matplotlib generates original SVG/PDF plots. The build does not
publish. Hosting supports incremental publication. `public/` excludes all private evidence
and recordings. Link deck PDFs and the viewer in FuEL; HTML import requires
an authenticated platform pilot.

## Hosting

The public source is `krystophny/fusion-skript` on GitHub, with Actions-based
Pages at `https://krystophny.github.io/fusion-skript/`. `github` names
`git@github.com:krystophny/fusion-skript.git`; `origin` names the private TU Graz
mirror `git@gitlab.tugraz.at:plasma/proj/teaching/fusion-skript.git`.
`scripts/publish.sh` builds, tests and exports; `--release` also pushes `main`
to both remotes. Each push to GitHub `main` deploys after workflow checks pass.
The script never creates commits.

`scripts/build-site.sh` builds the numbered decks, animation player pages and
SVG presenter under `public/`; the site root forwards to `present/`. The presenter keeps Plasma's appearance and interaction,
reads course/author from `decks.json`, and generates course-specific web-app
identity and cache names. Every page needs one `<present-page>` metadata
record from `slides/present-meta.typ`; the build fails otherwise. Media are copied from local staged site
files to same-origin, checksum-versioned URLs; no legacy assets are fetched.

Chapter and section numbers and titles come from the checked-in
`slides/outline.json`; edit it by hand when a deck gains a chapter or section.
A deck whose chapter is not listed there supplies its number and title on the
title page. Every registered animation in `media/animations.json` names its
scene source, title, description and caption, so it needs no script chapter.

The current Nextcloud `lv/fusion/2026/` folder is publicly shared. Exports
include built deck PDFs, derived figures, derivation sources and registered
animations; no `skript/` folder is written. An ownership
manifest controls stale-file removal and preserves files the exporter did
not write, including examination material and modified personal copies.

## Authorities

- [Fusion course plan](../../Nextcloud/lv/fusion/PLAN.md): live pacing and exam policy.
- [Shared teaching rules](../../Nextcloud/lv/AGENTS.md): private transition and CC release.
- [Delivery register](../fusion-course-archive/config/delivery.json): clips, gaps, reviews and uploads.
- [Plasma Skript](../plasma-skript/SPEC.md): infrastructure reference.

Original content and plots: CC BY 4.0. Code: MIT. Fonts: SIL OFL. Numeric facts
are cited individually. Chapter 0 plots are independently generated; Chapter 1
retains the lecturer’s original discovery artwork and attributed photographs
at Chris’s request. Third-party assets retain their own terms, documented in
`slides/photos/discovering-fusion/original/credits.md`; they are not covered by
the original-content licence. Provider terms remain linked in `data/README.md`.
