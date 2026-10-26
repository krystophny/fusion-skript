# Fusion Physics lecture slides

There is no Fusion Physics script for now. The lecture decks and the online
slide viewer <https://krystophny.github.io/fusion-skript/present/> are the
course reference. A future script will be written by hand, page by page; the
earlier generated chapters remain only in Git history.

Build with `bash scripts/build-site.sh` (Typst, Python, SymPy and Matplotlib).
Read `public/slides/00-energy-context.pdf` and serve `public/present/` over
HTTP. Chapter and section numbers and titles of the decks are in
`slides/outline.json`.

- [Specification](SPEC.md) and [data provenance](data/README.md)
- [Course plan](../../Nextcloud/lv/fusion/PLAN.md)
- [Plasma Skript](../plasma-skript/README.md)
- [Watch/cut archive](../fusion-course-archive/README.md) and [delivery audit](../fusion-course-archive/quality/delivery-audit.md)
- [FuEL project memory](../../Nextcloud/brain/projects/EUROfusion-FuEL-online-course-production.md)

Original content is CC BY 4.0, code MIT, fonts SIL OFL. Infrastructure was
adapted from Christopher Albert and Maximilian Philipp's plasma Skript;
the retained MIT notice and [CONTRIBUTORS.md](CONTRIBUTORS.md) record this reuse.

AI tools assisted drafting, calculations and layout. Christopher Albert reviews
the scientific content before student publication.

## Platform delivery

Use the shared [course delivery policy](../../Nextcloud/lv/AGENTS.md): curated
module routes in FuEL and TeachCenter and YouTube unlisted lecture videos.
Plasma animations use native players with stable Nextcloud streams; their
YouTube uploads were removed by request. Share the maintained player URLs
between decks and player pages.
Only TeachCenter additionally links the full 2026 Nextcloud material folder.
Course-description backups are in each course's `platform-backups/` folder.
Written examinations supersede the earlier instruction to preserve the old
format; current questions remain the baseline and may evolve until semester end.

FuEL File resource 746 (hidden) and TeachCenter start page 594148 still point
to the withdrawn script HTML bundle and PDF. FuEL start page 749 is hidden and
omits the bulk folder link.

## Publishing

Build, test, and refresh the public 2026 course folder:

```bash
bash scripts/publish.sh
```

The destination defaults to `~/Nextcloud/lv/fusion/2026/`; use `--dest`
or `COURSE_FOLDER` to choose another folder. The exporter copies every
built deck PDF, generated figures, derivation sources and registered
animations; it writes no `skript/` folder.
`.fusion-skript-export.json` records ownership and hashes. It removes stale
owned files, preserves unowned or locally modified files, and skips unchanged
copies. The folder is public at
<https://cloud.tugraz.at/index.php/s/cPHCeEDHxptSLek>.

To export before every Git push, explicitly opt in to the provided hook:

```bash
git config core.hooksPath scripts/hooks
```

The hook runs the same build, test and export flow. The release command skips
duplicate hook work during its two pushes.

| Remote | Repository | Visibility |
| --- | --- | --- |
| `origin` | `git@gitlab.tugraz.at:plasma/proj/teaching/fusion-skript.git` | Private TU Graz mirror |
| `github` | `git@github.com:krystophny/fusion-skript.git` | Public GitHub source |

After the pending chapter changes are committed on `main`, release with:

```bash
bash scripts/publish.sh --release
```

This rebuilds, tests, exports, then pushes `main` to both remotes. It never
creates commits or force-pushes. Each GitHub push to `main` deploys Pages
after the Actions checks pass.

| Output | URL |
| --- | --- |
| Site root (forwards to the presenter) | <https://krystophny.github.io/fusion-skript/> |
| Energy deck PDF | <https://krystophny.github.io/fusion-skript/slides/00-energy-context.pdf> |
| Presenter launcher | <https://krystophny.github.io/fusion-skript/present/> |
| Energy presenter | <https://krystophny.github.io/fusion-skript/present/00-energy-context/> |
| TU Graz mirror | <https://gitlab.tugraz.at/plasma/proj/teaching/fusion-skript> |

The workflow pins Typst 0.15.1, checks derivations and publishing behavior,
builds the site, decks and presenter, and uploads `public/`. Pull requests
build without deploying. Plasma's separate Nix workflow checks its flake and
VM; Fusion has no such project contract.

## Animations

Manim scenes live in `animations/` (shared `style.py`, dark canvas); model
modules such as `radial_coulomb.py` compute what the scenes draw and are
checked by `tests/test_animation_physics.py`. Data-driven scenes may draw code
exports in `animations/data/<code>/<export>/` with their `provenance.json`.
`bash scripts/render-animations.sh` renders changed scenes into
`.cache/animations/` (`<slug>.mp4` at 1080p60, poster `.png`, `.stamp`); it needs `manim`
0.21 with the stix2 TeX package and ffmpeg, for example from
`nix develop ~/proj/plasma-skript`. `python3 scripts/refresh-animation-media.py`
adopts a render into `media/animations.json` (checksum, `?v=` stream URL) and
`media/posters/`; each record also names its scene `source`, `title`,
`description` and `caption`. The MP4s are hosted in the course share's `animations/`
folder; `scripts/export-course-folder.sh` copies exactly the registered
revisions there together with `animation-sources/`. The site build
(`scripts/prepare-media.py`) checks each record's scene and checksum, stages
the registered MP4s and builds `animations/<slug>.html` from the record;
decks use `#animation-page(slug, name)`.

## Presenter metadata

`scripts/build-present.py --course "Fusion Physics" --short-name Fusion`
implements the [Typst introspection](https://typst.app/docs/reference/introspection/query/)
contract in `src/present/present.js`. It renders numbered decks with
`typst compile --format svg`, generates per-deck `manifest.json` and launcher
`decks.json`, and gives SVG/PDF/media URLs content revisions (`?v=<hash>`).
Course and author come from `decks.json`; the web-app manifest and service-worker
cache prefix are generated for the course. Appearance and controls are Plasma's
original presenter. Open `public/present/` through an HTTP server, not `file://`.

The theme imports `slides/present-meta.typ`; its page helpers add metadata to
title, slide, photo, animation and blank pages. Plot and summary pages use the
slide helper. Deck authors who make a page directly can call it like this:

```typst
#import "present-meta.typ": present-meta
#page[#present-meta() ...]
#page(fill: rgb("#111418"))[
  #present-meta(kind: "animation", background: "dark",
    video: "/media/example.mp4", loop: true)
  ... poster image ...
]
```

Call once per physical page. Use `background: "dark"` for dark/photo pages;
static white pages use the defaults. `video` and optional `poster` reference
files staged inside `public/`; an omitted poster uses that page's SVG.
The builder copies local media into the presenter for same-origin offline use.
The site build checks that every page has exactly one metadata record. The
metadata does not change the deck's visual layout.

`python3 scripts/check-present-browser.py` provides an optional local Chromium
check (Playwright and Pillow required), screenshots of every page, and a
contact sheet under `.cache/present-review/`. It checks the Pages repository
prefix, navigation, Pencil behavior, overview and offline deck/launcher reload.
`src/present/provenance.json` records the exact Plasma base commit, uncommitted
patch digest and imported-file checksums. Fusion additionally caches the
launcher directory URL (`present/`) alongside `index.html`, so returning to
the launcher works offline.
