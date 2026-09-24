# MCP Console presentation

49 main slides, an appendix divider, and 18 optional configuration, development-history, implementation, and testing slides (68 total). `deck.qmd` is the
canonical source, including one native Quarto speaker-notes block per slide.

The fuller presentation is the main deck again, unchanged from `deck-full.qmd`.
The shorter alternative is preserved as `deck-short.qmd` (24 main slides,
an appendix divider, and 14 backup slides). Its added layouts are scoped in the
shared stylesheet.

Use the penguins demo as a live preamble, then begin the existing slide sequence.
No demo slides have been added to the full deck. See
[recording-plan.md](recording-plan.md) for the prompt, transition, and saved plot.
The demo and fuller talk still need a timed rehearsal together.

To render the shorter alternative without replacing the main preview:

```sh
quarto render deck-short.qmd --to revealjs --output mcp-console-short.html
```

Both alternate QMD files retain the main output filename in their front matter;
use an explicit `--output` when rendering an alternate. Generated notes and the
slide index always describe `deck.qmd`.

The repository-development sequence starts at `development-timeline` and
includes absolute and proportional views that distinguish YAML test transcripts
from test code. Frozen data, definitions, and the R figure generator are in
[examples/repository-development](examples/repository-development/README.md).

## View the deck

```sh
quarto preview deck.qmd
```

Press **S** for native Speaker View. It opens a separate window containing the
current slide, next slide, timer, and notes. Serve the deck over local HTTP so the
presentation and speaker window can communicate.

The default preview evaluates the fitted model and base-R plot through knitr.
Python and SQL results use the supplied Console captures. Protocol panels
and transcript excerpts read the supplied real captures in both modes. Preview
does not launch Console, install packages, or call a model API.

To use captured Console outputs and PNGs throughout:

```sh
quarto preview deck.qmd -P output_source:mcp
```

For a saved presentation with embedded resources:

```sh
quarto render deck.qmd --to revealjs
```

This writes `mcp-console.html`. `python build_preview.py` refreshes the notes and
runs that same native renderer. The delivered HTML uses the native R mode.

## Edit and regenerate

Keep each slide's notes with its `##` section. `speaker-notes.md` and
`slide-index.json` are generated reading and navigation copies. The main-talk
notes incorporate the dictated run-through. The missing recording segment's notes
are preserved; technical references are separated from the new spoken passages.

```sh
python sync_cells.py
python export_notes.py
quarto render deck.qmd --to revealjs
python validate_source.py
```

`examples/cells.json` owns the captured cells and marked displayed calls. After
changing a cell, recapture it before rendering a result as an observation. The
validator checks the calls against the capture manifest and wire exchange.

Technical diagrams are inline SVG in the QMD. Editable Graphviz and SVG sources
live in `diagrams/`; `python make_diagrams.py` refreshes `assets/` and the embedded
copies, preserving accessible labels and unique SVG IDs.

Code preserves source line breaks. Wider columns and deliberate source line
breaks keep examples readable without soft wrapping. Raw output notices may wrap.

## Captures and validation

See [examples/README.md](examples/README.md) for capture commands and
[VALIDATION.md](VALIDATION.md) for the exact build fingerprint, checks, and limits.
The current deck, notes, and examples occupy their established paths. The
original delivery and superseded working files are in the
[handoff archive](../archived/2026-09-17-105015-talk-handoff/README.md).
`examples/measurements.csv` is unchanged.

The native R render, sandboxed MCP capture, and local macOS policy probes passed.
The explicit `data.table==1.17.8` example failed its separate package-installation
rehearsals; its reference capture remains documented in VALIDATION.md. Linux, SSH, Docker, Docker Sandbox,
and model-provider integrations were not exercised.

The separate [Shiny Chat investigation](../shinychat-investigation-2026-09-17/FINDINGS.md)
contains replay prototypes and the limits of static Quarto embedding.
