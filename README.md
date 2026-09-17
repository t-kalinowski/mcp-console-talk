# MCP Console presentation

69 slides: 61 main slides and 8 development-practice slides. `deck.qmd` is the
canonical source for both the slides and their speaker notes. Slide content,
diagrams, order, and existing notes are preserved in this revision.

## View slides and speaker notes

From this directory, with Quarto installed:

```sh
quarto preview deck.qmd
```

Open the presentation in an external browser. Press **S** to open Quarto / reveal.js
Speaker View, with the current slide, next slide, timer, and the notes for the
current slide. Allow browser pop-ups if prompted. Notes remain hidden on the
audience-facing slides. **N** means next slide in native reveal.js; it is no longer
the notes-panel shortcut from the previous custom preview.

Prefer `quarto preview` rather than opening a downloaded HTML through a `file://`
URL, so the slides and speaker window use a local HTTP origin. The browser may
restrict communication between windows opened directly from local files.

For a saved HTML presentation:

```sh
quarto render deck.qmd --to revealjs
```

This writes `mcp-console.html`, with embedded resources. `python build_preview.py`
is a convenience wrapper for that same native Quarto render; it no longer builds
a separate viewer. The previous custom HTML is intentionally not included in
this source archive. Native Quarto is not installed in the editing environment,
so an updated Quarto-rendered HTML is not supplied.

## Edit the speaker notes

Notes live directly below each slide in Quarto's native syntax:

````markdown
## Slide title

Audience-facing slide content.

::: {.notes}
**Say:** What to say for this slide.

**Show:** What the slide shows and any demonstration cues.

**Sources:** Supporting references and author checks.
:::
````

Move the complete `##` section, including its `.notes` block, to reorder a slide.
Every slide has exactly one notes block. No external notes file or custom notes
JavaScript is required by Quarto. The `show-notes: false` setting keeps the notes
off the audience-facing slides; it does not disable Speaker View.

`speaker-notes.md` is an optional generated reading copy. To refresh it after
editing the QMD, run:

```sh
python export_notes.py
```

## Diagrams and examples

`styles.css` supplies the shared slide design. The 16 Graphviz diagram sources
are in `diagrams/*.dot`; the timing diagram is `diagrams/timeout.svg`. With
Graphviz installed, rebuild these 17 technical diagrams with:

```sh
python make_diagrams.py
quarto render deck.qmd --to revealjs
```

`examples/`, `author-checklist.md`, and `sources.md` are unchanged.
The recording plan now points to the native Quarto render commands. Runtime exchanges remain illustrative; no real Codex recording is
implied. The checked-in YAML test excerpt and synthetic data remain in place.

## Validation

The source was parsed as reveal.js slides with Pandoc: 69 slides, exactly one
native `<aside class="notes">` per slide, and the same slide IDs and note text
as the previous revision. Slide bodies were checked for unintended changes.
All local images and include files are present. Native Quarto execution and
browser Speaker View were not available for validation in this environment;
`validation.json` records those limits explicitly.

Native Quarto documentation:
https://quarto.org/docs/presentations/revealjs/presenting.html#speaker-view
