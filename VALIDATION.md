# Local validation — 2026-09-23

The main presentation is restored to the fuller 68-slide version: 49 main slides,
an appendix divider, and 18 reference slides. `deck.qmd` matches `deck-full.qmd`
byte for byte. The 39-slide alternative is preserved in `deck-short.qmd`.
`mcp-console.html`, the reading notes, and the slide index describe the full deck.

## Restore the fuller presentation — 2026-09-23

- Restored the source without slide or speaker-note edits. The penguins demo is
  now documented as a live preamble, with the saved PNG as an external fallback.
  The shorter deck and its embedded demo remain available separately.
- Regenerated the main HTML, notes, and index. Native Quarto rendered without
  warnings, and `validate_source.py` passed for all 68 slides. The browser confirms
  the full opening slide and 68-slide count. No new full layout sweep was needed:
  the source is restored exactly and the short-deck CSS additions are scoped.
- No new live demo, model run, timing rehearsal, or runtime test was performed.
  The previous short-version checks below apply to `deck-short.qmd`.

## Short presentation — 2026-09-23

- Opens with the language-choice motivation, then the nominated penguins session:
  original prompt, actual returned image, and selected cross-language excerpts.
  The unmodified transcript, generated QMD, and PNG are retained under
  `captures/opening-demo/`, with original location and SHA-256 provenance.
- Reduces the main talk from 49 to 24 slides. The standalone sandbox command,
  local and remote topology, current send interface, and pre-release work remain
  in the main talk. Exhaustive configurations and proposed API extensions are
  backup material; the full deck preserves the remaining reference material.
- Spoken notes are approximately 1,600 words, with a two-minute live-demo budget.
  The 15-minute talk target has not been timed in a new rehearsal. The broad
  prompt requests all three languages and is not presented as evidence of
  unprompted optimal language choice.
- Runtime examples reuse existing captures. The Markdown slide reads a literal
  excerpt from the penguins record. The edited Quarto example selects one
  penguins regression and adds an explicit requirement and package cutoff date;
  that report was not executed. No new model, runtime, package-resolution,
  sandbox, SSH, or Docker test was run for this presentation edit.
- Native Quarto rendered without warnings. `validate_source.py` passed for all
  39 slides, including matching notes, existing calls and captures, configuration
  snippets, and inline SVGs. The full backup matches the pre-edit source; copied
  demo files match their recorded hashes. Source whitespace checks pass.
- All 39 slides passed browser bounds and code-overflow checks in the in-app
  browser at 703 × 852. The new image is loaded and has nonzero visible dimensions.
  The opener, demo plot, shared-session excerpts, progress pairing, policies,
  integrations, report source, and release slide were visually inspected.
  A Quarto auto-stretch issue on the new image was found and corrected.
  Speaker View and the alternate capture-mode render were not repeated.

Earlier validation below refers to prior deck revisions. The older 65-slide
captured-output HTML remains in
[the render archive](../archived/2026-09-23-standalone-sandbox/mcp-console-captured.html).
The existing runtime captures and `examples/measurements.csv` are unchanged.

## Possible API extensions — 2026-09-23

- Labeled slide 25 as the current send interface. Added slides 26 and 27,
  `future-sessions` and `future-notes`, immediately afterward. They progressively
  add and highlight session selection and prose notes, with both slides visibly
  marked as ideas that are not implemented. The note/comment name remains open.
- Speaker notes describe concurrent sessions and an append-only lab notebook
  containing intentions, observations, and conclusions for later interpretation
  and curated exports. The diagrams are schematic signatures, not executable
  calls or product changes.
- Regenerated notes, index, and native R HTML. Quarto rendered without warnings,
  and source validation passed for all 68 slides. All three signature slides
  passed bounds checks in the in-app browser at 1258 × 1180; the two new slides
  were visually inspected. Code does not soft wrap. Runtime examples and captures
  are unchanged. Captured-output rendering and Speaker View were not repeated.

## Pre-release work — 2026-09-23

- Added slide 46, `before-release`, between the Quarto transcript and the
  conclusion. Six bullets cover Windows, sans-R mode, human-facing configuration,
  tool descriptions and evals, curated exports, and artifact handoff.
- Expanded the author's dictated priorities in native speaker notes, including
  config discovery and storage defaults, R/Python export functions, a lab-notebook
  workflow, and persistent output locations accessible to other authorized tools.
  Implementation status reflects the author's update; no PR audit was performed.
- Regenerated the notes, slide index, and native R HTML. The render completed
  without warnings, and source validation passed for all 66 slides. The new slide
  was visually inspected in the in-app browser at 1422 × 800 and fits without
  overflow. Existing slide source, runtime examples, and captures are unchanged.
  Captured-output rendering and Speaker View were not repeated for this text-only
  addition.

## Standalone sandbox command — 2026-09-23

- Added a main-talk slide after the complete proxy configuration. It shows the
  public sandbox command, shared project policy, the native runner handoff, and
  ordinary subprocess streams and exit status for application integrations.
- Added examples/sandbox-analysis.R, using base R and the existing measurements
  CSV. The displayed command ran successfully with Console 0.0.4 on macOS and
  printed model coefficients. The enclosing agent sandbox initially prevented
  nested Seatbelt initialization; the approved host-level retry succeeded while
  retaining Console's own sandbox enforcement.
- Checked the installed CLI help and local source at
  edaf0b394d4bca070c1abd9ecc0f2a0ce49b775b. The notes distinguish the public
  standalone command from the external-sandbox filesystem mode and explain its
  local execution scope. No MCP server, model API, or dependency resolver was
  used for this example. Runtime captures and the CSV are unchanged.

- Both Quarto modes render without warnings and pass source validation for all
  65 slides. The new slide fits without code wrapping or overflow at 1422 × 800
  in both browser modes. Existing slide source is unchanged. Notes, index, and
  native preview are regenerated. Speaker View was not retested.

## Repository development in the appendix — 2026-09-18

- Added seven slides (50–56) between package resolution and the existing
  testing material: annotated PR timeline, total repository size, category
  sizes, category proportions, the six largest PRs, AGENTS.md, and the
  prescribed development loop. Updated the divider and speaker notes.
- Generated five figures in MCP Console with R. PR charts use 279 merges
  directly into main from the 19:08 UTC GitHub snapshot. Repository charts
  use 307 complete Git trees through main commit 657a5981 at 19:43 UTC.
  Frozen CSVs, definitions, verification records, and the R generator are
  supplied under examples/repository-development/.
- Category sums match all repository totals, and every proportion snapshot
  sums to 100 percent before rounding. Per-file PR totals reconcile with
  GitHub's additions and deletions. YAML transcript detection is independent
  of historical test subdirectories; the #197 reorganization preserves
  17,224 transcript lines on both sides.
- Both native R and captured-output renders finish without warnings and pass
  validate_source.py for 64 slides with matching notes. All five SVGs load
  and display. The divider and all seven new slides pass browser bounds
  checks at 1422 × 800 in both modes. The new slides were visually inspected
  in native mode. Speaker View was not retested.
- The source before the appendix matches the preceding commit. Runtime
  captures and measurements are unchanged. The delivered HTML is the
  native R render; both renders are retained in the archive above.

## Package configuration in the appendix — 2026-09-18

- Moved the approved-repository example and proposed config.yaml requirements
  into the appendix. Restored the main talk's explicit send requirements slide.
- Updated the appendix divider, notes, slide index, and current slide counts.
  The main talk contains 45 slides; the proposed configuration remains clearly
  labeled as not implemented.
- Both Quarto modes render without warnings and pass source validation for all
  57 slides. The revised divider and configuration slide pass browser layout
  checks in both modes. The main talk source matches the preceding commit.
  Runtime captures and the measurements CSV are unchanged.

## Requirements in config.yaml — 2026-09-18

- Corrected the requirements-list interpretation. The explicit requirements slide
  now shows R and Python YAML sequences beside the equivalent send call. The YAML
  is visibly labeled proposed and not implemented.
- Checked src/settings.rs in Console source
  e6e94127706fdb3d71a77a733bc478ac48651ec7. Its Project schema accepts only
  extends, sandbox, and target, with unknown fields rejected. No product feature
  was added, and the proposed configuration was not run as a supported example.
- Restored the preceding slide's corporate-mirror example. The PPM list-file
  detour is superseded; those three illustrative files are preserved under
  ../archived/2026-09-18-package-lists/package-policy/ alongside its old renders.

- Regenerated notes and index. Both native and captured-output Quarto renders
  pass source validation for 56 slides. Both changed slides fit without code
  wrapping or overflow in the in-app browser at 1422 × 800. Runtime captures
  and the measurements CSV are unchanged. Speaker View was not retested.

## Approved package repositories — 2026-09-18

- Added an example after process topology, before explicit requirements. It shows
  PKG_CRAN_MIRROR and UV_DEFAULT_INDEX in client launch settings, displayed as
  YAML, pointing to illustrative PPM repositories. The slide distinguishes
  curated package sets from resolver-host network enforcement.
- Checked the local Console resolver configuration, ir/pak repository handling,
  and official uv and PPM documentation. Console config.yaml governs workload
  settings; its sandbox.environment does not configure trusted resolvers.
  Curated lists belong to the repository manager, not a Console allowlist key.
- A public pak::repo_get() probe selected the configured R repository even when
  options(repos) contained the default public PPM URL. An isolated uv invocation
  with UV_DEFAULT_INDEX requested a missing package from a loopback index and
  failed without falling back to PyPI. The probe installed no packages and made
  no model API calls. No corporate PPM service or full Console enforcement setup
  was tested. Scripts and results are in the render archive.
- Refreshed notes and the slide index. Native and captured-output Quarto renders
  pass source validation. The new layout was checked in the in-app browser.
  Existing runtime captures and the measurements CSV are unchanged.

## Simpler chatlas registration — 2026-09-18

- The chatlas example now calls
  `chat.register_tool(mcp_console.chatlas.tool(console))` directly, removing the
  temporary variable and tool-list manipulation. Adjusted the highlighted lines
  and panel label, and regenerated the notes.
- A disposable uv environment with chatlas 0.23.0 and MCP SDK 2.2.0 registered the
  tool and invoked it against the sandboxed Console. All seven send arguments
  were registered, and `1 + 1` returned `[1] 2`. No model API was called. The probe
  and schema comparison are in the render archive. This version of chatlas
  rebuilds the schema from annotations; the slide no longer claims to preserve
  the server schema, and the speaker notes explain that distinction.
- Both Quarto modes render without warnings and pass source validation. The
  chatlas slide fits without wrapping or overflow in the in-app browser.

## Consolidated installation — 2026-09-18

- Combined the R and Python installation slides into one overview before the
  client registration examples. It leads with `uvx mcp-console serve`, followed
  by `uv pip install` with the supported extras and the planned CRAN command.
- Preserved the current GitHub R installation route and package-resolution
  details in the notes. Checked Python extras and uv installation syntax against
  their local source repositories. No packages were installed for this edit.
- Regenerated the notes and index. Both Quarto modes render without warnings and
  pass source validation for 55 slides. The installation and CLI registration
  slides fit without wrapping or overflow in the in-app browser at a
  2723 × 1738 CSS viewport in both modes. Captures and measurements are unchanged.

## Standard input and four-argument call — 2026-09-18

- Added a readline introduction before the debugger, reusing the literal prompt
  and answer captures. Updated the transitions into the combined-call example.
- The combined request now supplies control, requirements, stdin, and an R cell.
  examples/summarize.R uses the declared readr package to read the unchanged CSV.
  A fresh sandboxed capture against Console 0.0.4 returned one complete response.
  Follow-up assertions checked that the old workspace sentinel was absent, readr
  created a tibble, and the queued input selected group A. No model API was used.
- captures/combined-input records the wire exchange, literal response, checks,
  source/data hashes, and executable fingerprint. The collector and generated
  session directory are archived. The older three-argument capture and base-R
  script remain intact.
- The source check failed against the old displayed script before the slide was
  updated, then passed. It now verifies the four arguments and single wire result,
  as well as the displayed script and retained response bytes.
- Both Quarto modes rendered without warnings. The source validator passes for
  all 56 slides. The input, debugger, and combined-call slides pass browser checks
  in both modes with no code wrapping, clipping, or vertical overflow. A targeted
  reduction in combined-panel padding accommodates the extra argument and script
  line without reducing the code font size. Speaker View was not retested.

## Second run-through — 2026-09-18

- Moved language choice immediately after the introduction and merged the former
  capability inventory with the safety slide. The notes explain explicit runtime
  state before the overview of output handling, packages, records, and hosts.
- Updated the dictated opening, ordinary R/Python examples, record descriptions,
  and conclusion. The middle of the presentation and all captured cells are
  unchanged. The source now has 55 slides, with one notes block per slide.
- The recording tree names `.agents/console/sessions/<session-id>/`. Local product
  documentation confirms the path, the structured journal's scope, image-artifact
  persistence, and how the QMD's package declarations are generated.
- Both Quarto modes rendered without warnings and passed the source validator.
  The language-choice, combined capabilities/safety, and recording slides passed
  browser geometry and overflow checks in both modes at a 2723 × 1738 CSS viewport.
  Screenshots of the two edited layouts were inspected. The preceding revision's
  full 56-slide check remains historical evidence for the unchanged layouts.
- Notes and index were regenerated; source whitespace checks pass. Runtime
  captures and measurements are unchanged. No new runtime or provider calls were
  needed, and Speaker View was not retested.

## Dictated run-through — 2026-09-18

- Reworked the dictated portions into spoken notes, with technical references
  separated from the spoken passages. The six slides spanning the lost recording
  (old slides 13–18) remain byte-for-byte unchanged.
- Restored explicit requirements and the captured debugger/input sequence. Moved
  process topology into the package section and output handling before the full
  send overview. Removed the dedicated cleanup slide; the default-policy notes
  retain the cleanup explanation and platform limits.
- Reduced the warehouse and Shiny YAML to five and four lines, respectively.
  They are labeled excerpts and match subsets of their complete configurations.
  Added a complete proxy-object slide with every supported field, explicitly
  distinguishing this enabled-proxy baseline from the default no-proxy policy.
- The new full proxy configuration passed a public `mcp-console sandbox` startup
  with `/usr/bin/true` in a disposable workspace. No external network request was
  needed. The broader sandbox suite was not rerun.
- Native R and captured-output Quarto renders completed without warnings. The
  source validator passed for both. All 56 native slides passed browser checks
  for geometry, code overflow, notes presence, and image loading at a 1422 × 800
  CSS viewport. The debugger, requirements, complete proxy, R cell, and R plot
  also passed in capture mode. Screenshots of the restored debugger and complete
  proxy configuration were inspected. Speaker View was not retested this turn.
- Existing runtime captures were reused, and the measurements CSV is unchanged.
  The notes generator, displayed-call checks, exact configuration-copy checks,
  excerpt subset checks, and source whitespace checks passed.

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
- The preceding 53 slides were inspected through the in-app browser for code clipping,
  vertical overflow, notes presence, image loading, and embedded diagrams.
  All passed. The 13 capture-sensitive slides also passed in the captured-output
  render. Code soft wrapping is disabled; individual layouts and source line
  breaks provide the required space. All three inline SVGs load. The revised
  Docker slide and new Markdown slide passed these checks in both output modes;
  the other layouts are unchanged.
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

The final deck capture completed at `2026-09-17T21:17:43Z` using
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
revision is `272ffa3`. The current deck has 44 main slides, a visible appendix
divider, and nine optional implementation and development slides.
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

The local process topology precedes the resolver protocol and sandbox policies,
and marks the worker sandbox separately from trusted resolver processes. The resolve_r, r_resolved,
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
test after restart. Restart plus `stdin="A\n"` plus sourcing ./analyze.R returned
the lifecycle notices and group A summary together. A follow-up cell verified that
an old-session object was absent and the script had selected group A. The fixture,
collector script, and superseded load_all-input capture are in the controls-review
archive. Validation checks displayed-call identity, literal response text, and
the source script and CSV hashes. No model API was called.

The review after checkpoint `30e2079` balances the progress columns, preserves the
running banner on one line, and aligns the signature comments. It clarifies the
context guardrail, interruption, and package-development examples; shortens the
script paths; and strengthens the uvx and thin R interface explanations.
The sourced script now calls readline() first and runs from the examples directory.
Both the full runtime capture and the separate controls capture were refreshed.

A new shutdown slide explains the worker grace period, forceful termination,
process-group/descendant cleanup, and private-storage cleanup. The local source
at `43706f40460934503eec056a7e6cf57b6582c6ad` defines a one-second worker grace and
force-stops the child if it does not exit. Native guarantees were reviewed against
LIFECYCLE.md at runner commit `2d0ad797210de821c07d1f18e4f1ffdcf06589cb`;
platform-specific lifecycle tests were not rerun for this prose change. The two
named presets are :read-only and :workspace; external-sandbox is a distinct
filesystem enforcement mode. Workspace is defined as the launch directory.
The final-slide-review archive retains the preceding captures and updated fixture.

The narrative pass committed as `da2af41` preserved all 50 slides and their IDs. It leads with
comprehensiveness and reuse for an audience already familiar with AI code
execution. Capability and safety are two equal requirements. Language and client
choices precede the everyday call, followed by the analysis workflow, API details,
architecture, sandbox, execution hosts, and setup. Session logs and the editable
report close the main story. Notes supply transitions between these sections.

This pass also makes the shutdown triggers explicit and compares the two built-in
policies in separate columns, defining the workspace within its own policy.
Both render modes passed; all 50 native slides and 11 capture-sensitive slides
passed the browser layout, code scrolling, notes, and image checks. No runtime
cells or captured results changed in this narrative pass. The narrative-shuffle
archive preserves the preceding source, render, notes, and slide index.


## Language reveal and host placement revision

The language overview now names what the model can execute, and the following
slide names the harness that calls Console. A simple Python cell and a returned
Matplotlib image precede the R/Python shared-process reveal, which demonstrates
both directions of object access. SQL and connection selection stay together.
Control and input examples precede the complete send signature; the control slide
explicitly combines a control and a cell. The private resolver protocol is in the
appendix, while local topology stays in the main talk.

A new SSH diagram keeps the client, server, and records local while placing the
relay, worker, sandbox, and trusted preparation on the remote host. The Docker
slide displays an actual Dockerfile beside YAML that selects it with
`build.dockerfile`; the current schema does not support inline Dockerfile text.
The build uses a user-prepared base image. Docker builds and SSH execution were
not run. Python installation lists all six supported extras, checked against the
local pyproject.toml. The R installation slide describes the package without
calling it thin. The closing explicitly names full language capabilities and
enforced sandbox permissions.

The new examples were captured together through sandboxed MCP stdio at
`2026-09-17T22:43:39Z`, using the installed Console 0.0.4. Its executable SHA-256,
verified unchanged before and after capture, is:

```text
ea006d9e93ea2c3c23128afbbce8b44ed289598b803f21aa661c577c223fb864
```

`captures/language-reveal/` keeps the requests, literal responses, returned PNG,
wire exchange, generated session records, and data hash. No model API was used.
The earlier 0.0.3 captures remain unchanged. The source validator checks this new
capture separately, including both displayed bridge calls. It first rejected the
missing provenance record, then passed with the complete capture.

The Docker schema, remote preparation placement, Python extras, and R wrapper
were checked against the local source reviewed at
`6cd4cfd4f61ec5df723cc0e25b8f35a90ba8377e`. Shell snippets parse, the displayed
Dockerfile matches its file, and the CSV is unchanged. Both renders and all
53 native slide layouts pass, along with the 13 capture-sensitive slides in MCP
mode. Notes, the slide index, and the saved native preview are regenerated.

On September 24, slide 9's Python bridge call was changed to `len(r.d)` and the
focused language-reveal session was recaptured. The new call returned `240\n`;
`captures/language-reveal/provenance.json` records the current run and executable.


## Framing comparison with the useR! lightning talk

The comparison used
`/Users/tomasz/github/t-kalinowski/useR-2026-mcp-repl/mcp-repl-lightning-talk.qmd`.
The revision adapts three ideas: real work requires multiple turns, capabilities
live in the runtime behind one compact tool, and sandbox policy applies to the
runtime and its subprocesses. The opening still leads with comprehensiveness and
reuse for an audience familiar with AI execution systems. Notes connect the
ordinary analysis loop to waiting, input, output handling, and enforced access.

The slide count, ordering, code, captures, and configuration examples are
unchanged. Product-specific claims from the lightning talk, including its default
policy, platform coverage, output limits, and recovery behavior, were not
transferred. The process-policy wording was checked against Console's local
SANDBOX.md and SANDBOX_CONFIGURATION.md.

Both Quarto modes rendered without warnings. The three slides with visible text
changes passed layout and code-fit checks in both modes; the prior full-deck
layout checks remain applicable to the unchanged slides. The source validator
passes, including all 53 notes blocks and existing capture provenance. No runtime
capture or product test was rerun for this prose-only pass.

## Community Docker image and Markdown transcript

The Docker example now starts from `rocker/r-ver:4.6.1` and uses Rocker's
`install_python.sh` to prepare Python and reticulate. It adds Console 0.0.4,
the runtime prerequisites from Console's example image, and analysis packages.
The versioned image definition and helper were checked against Rocker's upstream
sources; the Linux wheel was checked on PyPI. The displayed recipe matches
`examples/Dockerfile`, and its shell commands parse. The local Docker daemon was
unavailable, so the image build and target remain untested.

A new Markdown slide precedes the Quarto source. It uses the existing literal
call-and-result excerpt from `captures/session-records/transcript.md`, with
source-line provenance retained in `captures/excerpts/provenance.json`.
No captured outputs changed.

Both Quarto modes rendered without warnings. The Docker and Markdown slides
passed in-app browser checks for layout, code clipping, and native notes in both
modes. The source validator passes for all 54 slides and their notes. The saved
preview uses native R output; the captured-output render is in the archive linked
above. The notes, slide index, and project documentation are refreshed.

## Minimal Docker setup

The Docker slide now follows the requested setup: `rocker/tidyverse`, the
standard uv and rig installers, `uv tool install r-lib-ir`, and a workspace.
The YAML launches `uvx mcp-console`. Explicit Python selection, package lists,
version pins, and apt installation are omitted. The tools install into
`/usr/local/bin` without changing PATH. A wider Dockerfile pane keeps the
installer commands on single lines; both panes fit without scrolling.

The installer commands and ir distribution name were checked against official
sources. This is a presentation-day example: the inspected Console checkout
`6cd4cfd4f61ec5df723cc0e25b8f35a90ba8377e` disables managed package preparation
for Docker even when uv and ir are installed. The speaker notes and author
checklist record that dependency. This is not a validated current-release Docker
launch recipe, and no container build or session was run.

The recipe and displayed YAML match their files, and the shell commands parse.
Both Quarto modes and the source validator pass. The revised slide passes native
browser layout and code-fit checks. All runtime captures are unchanged.
