# Incremental site build: `make -j` rebuilds only what changed.
# `make site` writes public/; `make check` runs the tests whose inputs changed.
# scripts/build-site.sh and scripts/publish.sh call these targets.
SHELL := bash
.SHELLFLAGS := -euo pipefail -c
.DELETE_ON_ERROR:
PYTHON ?= python3
TYPST := typst compile --root . --font-path fonts --ignore-system-fonts
S := build/.make

# Any Python or data change reruns all derivations and figures (about 25 s);
# slide text, notebook and media changes do not touch them.
PY_INPUTS := $(shell git ls-files 'derivations/*.py' 'slides/figures*.py' 'scripts/plot-*.py' data)
DERIVATIONS := derivations/energy.py \
  derivations/chapters/ch00_energy_context.py \
  derivations/chapters/ch00_electricity_costs.py \
  derivations/chapters/ch02_fusion_reactions.py \
  derivations/chapters/ch02_reactivity.py \
  derivations/chapters/ch04_power_balance.py
PLOTS := scripts/plot-ch00-teaching.py scripts/plot-electricity-costs.py
FIGURES := $(wildcard slides/figures*.py)
DECKS := $(wildcard slides/[0-9]*-*.typ)
DECK_PDFS := $(patsubst slides/%.typ,public/slides/%.pdf,$(DECKS))
TYP_SHARED := $(filter-out $(DECKS),$(wildcard slides/*.typ)) $(wildcard fonts/*.otf)
MEDIA := $(shell git ls-files media)
QMDS := $(wildcard notebooks/*.qmd)
NOTEBOOK_HTML := $(patsubst notebooks/%.qmd,public/notebooks/%.html,$(QMDS))
NB_SHARED := notebooks/_quarto.yml $(wildcard notebooks/*.js notebooks/*.json notebooks/*.css notebooks/*.html) notebooks/data-files.txt

.PHONY: site check
site: $(S)/present public/index.html public/.nojekyll $(S)/fonts
check: $(S)/pytest $(S)/test-publishing

$(S)/derivations: $(PY_INPUTS)
	@mkdir -p $(@D)
	for f in $(DERIVATIONS); do $(PYTHON) $$f; done
	touch $@

# Plot and figure scripts read derivation outputs, not each other.
$(S)/plot-%: scripts/plot-%.py $(S)/derivations
	$(PYTHON) $< ; touch $@
$(S)/fig-%: slides/%.py $(S)/derivations
	$(PYTHON) $< >/dev/null ; touch $@
$(S)/figures: $(patsubst scripts/plot-%.py,$(S)/plot-%,$(PLOTS)) $(patsubst slides/%.py,$(S)/fig-%,$(FIGURES))
	touch $@

public/slides/%.pdf: slides/%.typ $(TYP_SHARED) $(S)/figures $(MEDIA)
	@mkdir -p $(@D)
	# Dated by the deck's last commit, so an unchanged deck rebuilds byte-identical.
	SOURCE_DATE_EPOCH=$$(git log -1 --format=%ct -- $<) $(TYPST) $< $@

$(S)/media: $(MEDIA) scripts/prepare-media.py
	$(PYTHON) scripts/prepare-media.py public ; touch $@

# One Quarto project directory: renders run one at a time.
build/notebooks/.staged: $(NB_SHARED) $(QMDS) $(S)/derivations
	mkdir -p build/notebooks/data
	cp -p notebooks/_quarto.yml notebooks/*.qmd notebooks/*.js notebooks/*.json notebooks/*.css notebooks/*.html build/notebooks/
	xargs -a notebooks/data-files.txt cp -p -t build/notebooks/data/
	touch $@
public/notebooks/%.html: notebooks/%.qmd $(NB_SHARED) build/notebooks/.staged
	@mkdir -p $(@D)
	cd build/notebooks && flock ../notebooks.lock quarto render $*.qmd --quiet
	cp build/notebooks/_site/$*.html $@

$(S)/present: $(DECK_PDFS) $(NOTEBOOK_HTML) $(S)/media scripts/build-present.py
	$(PYTHON) scripts/build-present.py --course "Fusion Physics" --short-name Fusion --strict-metadata
	touch $@

public/index.html: src/index.html
	@mkdir -p $(@D) ; cp $< $@
public/.nojekyll:
	@mkdir -p $(@D) ; touch $@
$(S)/fonts: $(wildcard fonts/*.otf) fonts/OFL.txt
	mkdir -p public/fonts $(@D) ; cp fonts/*.otf fonts/OFL.txt public/fonts/ ; touch $@

$(S)/pytest: $(PY_INPUTS) $(shell git ls-files tests) $(NB_SHARED) $(S)/derivations
	$(PYTHON) -m pytest -q ; touch $@
$(S)/test-publishing: $(shell git ls-files scripts)
	$(PYTHON) -m pytest -q scripts/test-publishing.py ; touch $@
