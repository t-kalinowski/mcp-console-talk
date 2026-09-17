# Local validation — 2026-09-17

The revised project contains 81 slides with one native notes block each.
`mcp-console.html` is the current native R render. The alternate Console-capture
render used for validation is preserved in the
[handoff archive](../archived/2026-09-17-105015-talk-handoff/README.md), alongside the original
agent delivery and superseded working files. Both HTML files are native Quarto
reveal.js renders with embedded resources. `examples/measurements.csv` is unchanged.

## Completed

- Quarto 1.10.18 passed `quarto check`; both output modes rendered using R 4.6.1,
  knitr 1.51, and rmarkdown 2.32.
- The MCP stdio collector ran against the sandboxed installed Console without a
  model API or `--no-sandbox`. It captured fitted-model output, coefficients,
  predictions, R and Python PNGs, progress/polls, redraw compaction, bounded
  output, an R error and surviving state, stdin, debugger interaction, and SQL.
- The displayed 600 ms and 5000 ms polls match their actual wire requests.
  Captured progress fractions remain observations of this run, not guarantees.
- Transcript and raw-log excerpts are literal slices of the generated records.
  `captures/excerpts/provenance.json` records their source lines. The displayed
  Quarto front matter alone replaces the absolute `root.dir` with `<project>`;
  this normalization is disclosed in the slide notes. Original files are intact.
- The Python reference score and plot were recomputed from the unchanged CSV and
  displayed cell definitions. The score is `CV MAE: 2.015`; library versions and
  the data hash are in `examples/python-reference-provenance.json`.
- All 81 slides were inspected through the in-app browser for code clipping,
  vertical overflow, notes presence, image loading, and embedded diagrams.
  All passed. The 12 capture-sensitive slides also passed in the captured-output
  render. Code soft wrapping is disabled; individual layouts and source line
  breaks provide the required space. All 11 inline diagrams load.
- The `S` shortcut opened native Speaker View in a separate app window, confirmed
  by the presenter. Automated access to that app window was unavailable, so
  speaker-window diagram visibility and synchronization were not independently
  inspected. Browser fullscreen activation was not established; slide layout
  was checked at the intended 1600 × 900 CSS viewport.
- Fifteen local YAML examples passed public `mcp-console sandbox` probes on
  macOS: file grants, read-only data, denied synthetic paths, environment
  inheritance, private scratch writes, direct networking, proxy allow/deny rules,
  and local binding. The Linux-only backend example was rejected with the
  expected platform diagnostic. Proxy probes substituted `example.com` for the
  placeholder allowed host; only disposable fixture files were read or written.
  Details are in `captures/sandbox-validation.json`.
- `sync_cells.py --check`, `validate_source.py`, Python syntax checks, and the
  diagram CLI regression passed. The diagram check edited a source in a temporary
  project and verified that rebuilding updated the embedded QMD. The source
  validator checks capture text/PNG identity, displayed calls, excerpt bytes,
  YAML copies, slide IDs, notes, and SVG IDs. Source diff whitespace checks pass;
  literal R output retains its original trailing spaces in generated HTML.

## Executable and source provenance

The final deck capture completed at `2026-09-17T14:35:32Z` using
`/Users/tomasz/.local/bin/mcp-console serve`. The binary reports `mcp-console 0.0.3`.
Its SHA-256 identifies the exact executable used:

```text
b80f9b67a2bbe4f418c1821ff1f41af1479d19533394eead181c7fbb884fbc6f
```

See `captures/capture-manifest.json`, `wire.jsonl`, `server-stderr.log`, and
`session-records/` for the original exchange and session records. Runtime versions
are in `captures/versions.txt` and `captures/python-versions.txt` (R 4.6.1,
Python 3.12.14, scikit-learn 1.9.1, pandas 3.0.5, Matplotlib 3.11.2).

The configuration review used the local Console source at
`682d7b953747e63395e5a42e3bef53287794d147` and its sandbox, configuration, SSH,
Docker, and Docker Sandbox documentation. Its runner manifest pins
`rust-v0.154.0`, commit `2d0ad797210de821c07d1f18e4f1ffdcf06589cb`, protocol 2;
the protocol was read at that exact commit. This is the reviewed source revision,
not an inferred build commit for the installed executable.

## Failed and unavailable checks

The requested `data.table==1.17.8` plus unpinned `dtplyr` example was attempted in
separate fresh Console sessions and did **not** pass. Under R 4.6.1, data.table
compilation failed with undeclared `SETLENGTH`, `ATTRIB`, and related APIs. An
attempt with the installed R 4.5 runtime failed during dependency installation
with `worker failed to start`. Their wire exchanges, diagnostics, and generated
records remain in `captures/requirements/` and `captures/requirements-r45/`.
The exact pin is preserved, and the failure is documented in the slide notes.
It needs a successful rehearsal in a compatible runtime before a live demo.

Linux enforcement and SSH, Docker, and Docker Sandbox targets were not run.
Their displayed YAML was checked against the local documentation and parsed;
no target execution is implied. Model-provider integrations and the recording
slot were not exercised. No model API, publication, pull request, or MCP Console
product modification was performed.
