# Fusion Physics Skript

Incremental local draft at `~/proj/fusion-skript`. The first chapter preserves
the quantitative energy opening and replaces book excerpts with original
explanations and reproducible plots. Later nuclear and plasma chapters will
follow the established course with deeper mathematical development.

Build with `bash scripts/build-site.sh` (Typst, Python, SymPy and Matplotlib).
Read `public/index.html`, `public/chapters/00-energy-context.html`,
`public/fusion-physics.pdf` and `public/slides/00-energy-context.pdf`.
These are local drafts; no public deployment is configured.

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
between Skript and slides.
Only TeachCenter additionally links the full 2026 Nextcloud material folder.
Course-description backups are in each course's `platform-backups/` folder.
Written examinations supersede the earlier instruction to preserve the old
format; current questions remain the baseline and may evolve until semester end.

The energy-opening HTML bundle is uploaded and browser-verified as hidden FuEL
File resource 746. TeachCenter start page 594148 links the current PDF and the
full 2026 folder. FuEL start page 749 is hidden and omits the bulk folder link.

## Publishing

Build, test, and refresh the public 2026 course folder:

```bash
bash scripts/publish.sh
```

The destination defaults to `~/Nextcloud/lv/fusion/2026/`; use `--dest`
or `COURSE_FOLDER` to choose another folder. The exporter copies the Skript
PDF, every built deck PDF, generated figures and derivation sources.
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
| Skript | <https://krystophny.github.io/fusion-skript/> |
| Skript PDF | <https://krystophny.github.io/fusion-skript/fusion-physics.pdf> |
| Energy deck PDF | <https://krystophny.github.io/fusion-skript/slides/00-energy-context.pdf> |
| Presenter launcher | <https://krystophny.github.io/fusion-skript/present/> |
| Energy presenter | <https://krystophny.github.io/fusion-skript/present/00-energy-context/> |
| TU Graz mirror | <https://gitlab.tugraz.at/plasma/proj/teaching/fusion-skript> |

The workflow pins Typst 0.15.0, checks derivations and publishing behavior,
builds the site, decks and presenter, and uploads `public/`. Pull requests
build without deploying. Plasma's separate Nix workflow checks its flake and
VM; Fusion has no such project contract.

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
