# MCP Console presentation

45 main slides, an appendix divider, and 18 optional configuration, development-history, implementation, and testing slides (64 total). `deck.qmd` is the
canonical source, including one native Quarto speaker-notes block per slide.

The main narrative starts with why: a comprehensive execution system that teams
can reuse across AI projects. The model's language choice leads into the combined
capabilities and safety overview, including explicit runtime state. Client choices
establish the scope before the simple
R, Python, and SQL workflow. A Python call and plot lead into the shared-process
reveal; SQL and database connection selection follow together. Packages expand
the workflow, with the process topology showing where resolution happens.
Explicit requirements remain part of the model-facing interface.
Waiting, output handling, controls, readline input, and debugger interaction lead
into a call combining restart, requirements, input, and code
and the complete send interface. Sandbox defaults and built-in policies precede
concrete access examples and a complete proxy configuration. Then the talk moves
to local/SSH/Docker execution.
An SSH topology diagram shows which processes move to the remote host. One installation overview leads into CLI and SDK integration examples,
then session logs, the Markdown transcript, and an editable Quarto report as the lasting result of the
work. The appendix covers approved package repositories, proposed config.yaml
requirements, the resolver protocol, repository growth and composition, major
feature merges, instructions for coding agents, and testing. The proposed configuration
form is visibly labeled as not implemented.
The main talk ends at `closing`; an explicit appendix divider follows it.

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
