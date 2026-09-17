# Local validation — 2026-09-17

The revised project contains 49 slides (40 main, an appendix divider, and 8 optional appendix slides),
with one native notes block each.
`mcp-console.html` is the current native R render. The current Console-capture
render used for validation is preserved in
[the review archive](../archived/2026-09-17-controls-review/mcp-console-captured.html).
The original agent delivery remains in the separate handoff archive. Both HTML files
are native Quarto reveal.js renders with embedded resources. `examples/measurements.csv` is unchanged.

## Completed

- Quarto 1.10.18 passed `quarto check` in the earlier validation; both current
  output modes rendered using R 4.6.1, knitr 1.51, and rmarkdown 2.32.
- The MCP stdio collector ran against the sandboxed installed Console without a
  model API or `--no-sandbox`. It captured fitted-model output, coefficients,
  predictions, R and Python PNGs, progress/polls, redraw compaction, bounded
  output, an R error and surviving state, stdin, debugger interaction, and SQL.
  The review capture includes both a C-level stdout write and a pipe-to-cat write
  from forked R children, Python `os.write()` with its returned byte count, Python
  reading `r.d`, and a request with harness metadata.
- The displayed 600 ms and 5000 ms polls match their actual wire requests.
  Captured progress fractions remain observations of this run, not guarantees.
- Transcript and raw-log excerpts are literal slices of the generated records.
  `captures/excerpts/provenance.json` records their source lines. The displayed
  Quarto excerpt replaces the absolute `root.dir` with `<project>`, shortens the
  package lists, adds an author-selected `ir.exclude-newer` date, and omits the
  generated-file warning. These edits are disclosed
  in the notes; original files are intact.
  The bounded-output slide deliberately uses one shortened, stylized response;
  its notes identify the changes, and captures/flood.txt retains the full response.
- The Python reference score and plot were recomputed from the unchanged CSV and
  displayed cell definitions. The score is `CV MAE: 2.015`; library versions and
  the data hash are in `examples/python-reference-provenance.json`.
- All 49 slides were inspected through the in-app browser for code clipping,
  vertical overflow, notes presence, image loading, and embedded diagrams.
  All passed. The 11 capture-sensitive slides also passed in the captured-output
  render. Code soft wrapping is disabled; individual layouts and source line
  breaks provide the required space. Both inline SVGs load.
- The `S` shortcut opened native Speaker View in a separate app window, confirmed
  by the presenter. Automated access to that app window was unavailable, so
  speaker-window diagram visibility and synchronization were not independently
  inspected. Browser fullscreen activation was not established; slide layout
  was checked in the fixed 1600 × 900 slide coordinates at the current browser viewport.
- In the earlier validation, fifteen local YAML examples passed public `mcp-console sandbox` probes on
  macOS: file grants, read-only data, denied synthetic paths, environment
  inheritance, private scratch writes, direct networking, proxy allow/deny rules,
  and local binding. The Linux-only backend example was rejected with the
  expected platform diagnostic. Proxy probes substituted `example.com` for the
  placeholder allowed host; only disposable fixture files were read or written.
  Details are in `captures/sandbox-validation.json`.
- The new R DBI and Python DB-API examples passed a separate sandboxed session:
  SQL read connection-specific marker tables and returned to the managed connection.
  Both built-in policy CLI commands passed local read, project-write, and protected
  metadata-write probes in a disposable directory. Results are in the language-review archive.
- The current `sync_cells.py --check` and `validate_source.py` pass. Earlier
  Python syntax checks, the source-generator regression, and diagram CLI
  regression also passed; those scripts are unchanged in this revision. The
  diagram check edited a source in a temporary
  project and verified that rebuilding updated the embedded QMD. The source
  validator checks capture text/PNG identity, displayed calls, excerpt bytes,
  YAML copies, slide IDs, notes, and SVG IDs. The source-generator CLI regression
  failed before the formatting change and passed afterward. Embedded Python
  cells compile, and the YAML journal event round-trips to the original JSON.
  Source diff whitespace checks pass;
  literal R output retains its original trailing spaces in generated HTML.

## Executable and source provenance

The final deck capture completed at `2026-09-17T19:33:51Z` using
`/Users/tomasz/.local/bin/mcp-console serve`. The binary reports `mcp-console 0.0.3`.
Its SHA-256 identifies the exact executable used:

```text
44d7bb321a2d590fb9b16d7e91b4d8ca7821cb94fdab306a228232ac54bc0e4a
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

The narrative revision rechecked the requirements, sandbox, SSH, and Docker
documentation at source commit `43706f40460934503eec056a7e6cf57b6582c6ad`.
The full runtime capture was refreshed for the progress bar and fork-output
examples. The capture collector and source validator assert both new output shapes.
The superseded captures are preserved in the slide-review archive.

## Failed and unavailable checks

The requested `data.table==1.17.8` plus unpinned `dtplyr` example was attempted in
separate fresh Console sessions and did **not** pass. Under R 4.6.1, data.table
compilation failed with undeclared `SETLENGTH`, `ATTRIB`, and related APIs. An
attempt with the installed R 4.5 runtime failed during dependency installation
with `worker failed to start`. Their wire exchanges, diagnostics, and generated
records remain in `captures/requirements/` and `captures/requirements-r45/`.
The exact pin is preserved in examples/cells.json as a reference example; it is
no longer in the shorter main deck.
It needs a successful rehearsal in a compatible runtime before a live demo.

Linux enforcement and SSH, Docker, and Docker Sandbox targets were not run.
Their displayed YAML was checked against the local documentation and parsed;
no target execution is implied. Model-provider integrations were not exercised. The unused recording slot was removed. No model API, publication, pull request, or MCP Console
product modification was performed.

## Review boundaries

The full 77-slide presentation is committed as `ab89d0c`; the previous narrative
revision is `272ffa3`. The current deck has 40 main slides, a visible appendix
divider, and eight optional development slides.
The opener explains R, Python, and SQL together, shared execution infrastructure, and
why sandbox permissions belong in the design. The examples combine wait/poll continuity and progress compaction in two slides,
followed by retained output, a Python descriptor write, and a forked R child. The progress
bar uses R’s built-in txtProgressBar and setTxtProgressBar.
Execution targets use three capability cards, an explicit SSH explanation,
and one Docker configuration slide.
Slide 2's former directional diagram is replaced by language-capability cards.

The new package story describes a session's managed requirements, reusable caches,
trusted preparation outside the worker sandbox, and restricted worker execution.
Model hesitation to install packages is presented as the speaker's experience.
Docker's preinstalled image environment is distinguished from local/SSH dynamic
resolution. These claims were checked against the current local REQUIREMENTS.md,
SSH.md, DOCKER.md, and SANDBOX_CONFIGURATION.md. The progress cell and full capture were refreshed. No remote sessions or model
calls were made. Ordinary preview still does not launch Console or resolve packages.

The sandbox default now precedes configuration and covers reads, writes, networking,
subprocess policy, and process/private-storage cleanup. The event-directory slide
is a single annotated tree, and the Quarto example is one shortened source excerpt.
The interface overview lists native MCP, R ellmer, direct Python clients, and the
Python adapters documented in the current checkout. The closing names the model
as the language chooser and the user as the execution-host chooser.

An exploratory `cat()` call inside an R fork produced no visible text in this
installed runtime. The slide uses a verified pipe-to-cat write from a forked
R child beside Python os.write(). The original C-level R write remains in the
reference captures. Opening /dev/stdout directly was denied by the sandbox.
The focused probes are in the topology-review archive. The deck does not claim
every R output hook is fork-safe.
No Console product code was changed during this investigation.

`internal/events.jsonl` is a structured journal of Console calls, results and
recording events. It preserves request `_meta`; the YAML excerpt remains in the reference captures.
The collector's separate `wire.jsonl` includes the complete MCP transport exchange.
The transcript files are siblings of `outputs/`, matching the actual directory.

The corporate database example needs an HTTPS API or SOCKS-aware connection.
For private-address destinations, the pinned proxy requires an explicit literal
IP grant matching the target, or its broader local-binding exception. The example
warehouse was not contacted. The Shiny configuration reuses the previously tested
local-binding policy; a live Shiny app was not launched under that policy.

The local process topology precedes the package examples and marks the worker
sandbox separately from trusted resolver processes. The resolve_r, r_resolved,
and r_activated messages match WORKER_PROTOCOL.md at the reviewed source revision;
the library path is illustrative. Configuration YAML consistently appears on the
right, and the network example names the corporate-warehouse use case. Execution
targets are presented as configurable adapters, with local, SSH, and Docker as
current examples.

The language review adds database connection selection, introduces the two built-in
policies before custom YAML, and uses bullets for the read-only default. Integration
code retains full text opacity with background highlighting. The closing reads
“Give the agent an interactive workbench.”

The editable report example adds `ir.exclude-newer: "2026-09-17"` and uses
`ir render report.qmd`. This setting was checked against the local ir Quarto guide
at `9986ce5f6c3421e2a050a59929a2b2c3b7f5a3cc` and installed CLI help; a dated report
render was not run. It constrains package snapshot resolution, not every external
source or system dependency.

Plain `uvx` is retained. Its ordinary cached-tool path resolves requirements using
registry cache freshness and can pick up newer versions after expiration. The
implementation was checked at uv `4d4f3e3b31307265ce4f510844f38fcabb2c463a`
(`tool/run.rs`, `project/environment.rs`, and the cached HTTP client).
The slide promises managed installation and updates, not a refresh on every launch.

The controls revision restores a schematic overview of all seven send fields,
adds interrupt/restart examples including fresh-session devtools calls, and shows
restart, queued stdin, and source() in one request. The sourced `examples/analyze.R`
uses readline() to select a group from the unchanged measurements CSV.

`captures/controls/` preserves a separate sandboxed MCP exchange using the same
executable fingerprint above. `devtools::test()` passed the local package fixture's
test after restart. Restart plus `stdin="A\n"` plus sourcing the script returned
the lifecycle notices and group A summary together. A follow-up cell verified that
an old-session object was absent and the script had selected group A. The fixture,
collector script, and superseded load_all-input capture are in the controls-review
archive. Validation checks displayed-call identity, literal response text, and
the source script and CSV hashes. No model API was called.
