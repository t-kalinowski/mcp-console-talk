# MCP Console presentation

A presentation about a shared R, Python, and SQL workbench for agents. `deck.qmd` is the single source: 41 main slides, an appendix divider, and 19 reference slides, with speaker notes embedded in each slide.

## Preview and render

Install Quarto 1.10.18, R 4.6.1, and the R packages `knitr` and `rmarkdown`. The publishing workflow uses those Quarto and R versions.

```sh
quarto preview
quarto render
```

Rendering writes `_site/index.html`, with styles, diagrams, and images embedded. Press **S** for Speaker View when serving the deck over HTTP. Speaker notes are part of the HTML and will be readable by anyone who can access it.

The default render evaluates the small base-R analysis and plot through knitr. Other results and protocol panels read the supplied Console captures. Rendering does not launch Console, install analysis packages, or call a model API. To render the R results from the recorded captures too:

```sh
quarto render -P output_source:mcp
```

The [opening demo plan](recording-plan.md) describes an optional live penguins preamble and its saved plot.

## Edit and check

Use Python 3.10 or newer for the source tools:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests
python sync_cells.py --check
quarto render
python validate_source.py
python validate_site.py
```

Keep each slide's notes with its `##` section. `examples/cells.json` owns the marked example calls; run `python sync_cells.py` after changing them. Recapture changed calls before presenting their results as observations.

Editable diagrams live in `diagrams/`. `python make_diagrams.py` refreshes the SVG assets and their embedded copies. The repository-development charts have [frozen data and a separate generator](examples/repository-development/README.md).

`python export_notes.py` creates optional local reading notes and a slide index. `python build_preview.py` exports those copies and renders the deck. Generated HTML, notes, and indexes are ignored by Git; edits belong in the source.

See [capture instructions](examples/README.md), [validation and known limits](VALIDATION.md), and [source references](sources.md).

## Publishing

The **Slides** workflow builds and validates pushes to `main` and pull requests. It retains the rendered Pages artifact without deploying it. Manual runs also build only unless **publish** is selected; deployment is restricted to `main`.

When ready to publish, make the repository public, set **Settings → Pages → Source** to **GitHub Actions**, then manually run **Slides** on `main` with **publish** selected. No personal access token is needed for deployment. The intended address is `https://t-kalinowski.github.io/mcp-console-talk/`.

Only `_site/` is uploaded for hosting. Sources, examples, and capture evidence remain in the repository; slide links to that material use GitHub URLs.
