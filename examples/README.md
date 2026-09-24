# Integration and capture examples

These examples follow the project interfaces cited in `../sources.md`. The provider integration examples were syntax-checked, not executed against provider APIs. The non-model capture script was executed against the installed Console; see `../VALIDATION.md`. Running a provider example performs real API calls and can incur usage charges.

Use the corresponding extra from `mcp-console[client]`, `[chatlas]`, `[openai]`, `[openai-agents]`, `[anthropic]`, or `[codex]`. Configure the provider’s normal credentials. The Python provider examples read `MODEL_ID`; no particular current model ID is hard-coded.

The current combined runtime requires a supported execution-host R installation and the prerequisites described by MCP Console. R-independent operation is a presentation-day feature, not assumed by these scripts.

`measurements.csv` is synthetic. All Python analysis examples change their own working directory to this examples directory so the worker can find it. Run `ellmer.R` from this directory as well. The model controls which cells to run; prompts do not guarantee a particular language sequence.

`replay_demo.py` is a deterministic non-model driver. It submits once, then polls without replaying the cell. `bootstrap.R` includes deliberate sleeps to make the timing behavior visible, not to benchmark performance.

The Responses slide displays a registration excerpt; `openai_responses.py` includes the continuation loop and a 24-round limit. The native Anthropic and chatlas examples are the intended visual paths. Direct `MCPConsole.send()` returns text and image placeholders, not a graphical display widget.

## Capture and refresh

`cells.json` is the source for captured calls, the marked send calls in the deck, and
`cells.R`. Run `python sync_cells.py` from the project directory after editing it.
`capture_console.py` uses the MCP stdio protocol and saves text, PNGs, complete
responses, the wire exchange, and generated session files. It never calls a model.
Options precede `--command`; choose an empty output directory for each run.

The native-output example prepares `inline`, compiles a C function, and writes
to stdout from a forked R child. It requires a C/C++ compiler and a Unix R runtime.
Its output and Python's `os.write()` output are asserted during capture.
`refresh_capture_excerpts.py` also requires Mike Farah's `yq`; the metadata event
is converted to YAML and checked by converting it back to JSON.

Configurations whose `slide` is null in `configs/index.json` remain as reference
examples after the shorter sandbox sequence was adopted. The two files under
`configs/excerpts/` are focused slide fragments, not complete launch configurations.
Their `excerpt_of` entries point to the complete configurations. `proxy-options.yaml`
shows every field of the proxy object with an explicit enabled-proxy baseline;
its empty rule maps allow no destinations.

`../captures/language-reveal/` contains a separate sandboxed session for the simple
Python call, Matplotlib plot, and both directions of R/Python object access. Its
own `cells.json`, wire exchange, returned PNG, and provenance identify those
examples. Both render modes use these captures. The source validator checks the
displayed calls and returned text/images against that record.
Run `python examples/capture_language_reveal.py OUT EXECUTABLE` to recapture them
in an empty output directory before replacing the published capture.

`Dockerfile` shows the presentation's minimal environment setup: `rocker/tidyverse`,
the standard uv and rig installers, and `uv tool install r-lib-ir`. The YAML
launches `uvx mcp-console`. This example assumes on-demand package preparation in
Docker by presentation day. The current inspected Console implementation disables
that capability; installing uv and ir alone does not enable it. The installer
commands were checked, but this is not a validated current-release Docker launch
recipe. No image build or container session was run.

```sh
python examples/capture_console.py --command /absolute/path/to/mcp-console serve
python examples/refresh_capture_excerpts.py
```

The pinned R example is a separate fresh session:

```sh
python examples/capture_console.py --requirements-only \
  --out captures/requirements --command /absolute/path/to/mcp-console serve
```

That pin did not pass the local rehearsal; preserve the failed recordings and use
another empty output directory when retrying. Do not change the pin to mask it.

`uv run examples/refresh_references.py` regenerates the Python reference score,
plot, and provenance. `check_sandbox.py` requires PyYAML and exercises only the
local YAML in a disposable directory. Its network probes use example.com and
substitute that domain for the proxy's example allow entry.

`summarize.R` is the interactive script on the combined-call slide. It asks for a
group through `readline()`, reads the measurements CSV with `readr`, and prints a
summary. The displayed request combines restart, a `readr` requirement, `A\n` on
stdin, and `source("./summarize.R")`. Launch from this examples directory.
`captures/combined-input/` holds the exact request and its single response, plus
checks that the old workspace was replaced and group A was selected. Its collector
and generated session records are in `../../archived/2026-09-18-stdin-requirements/`.
The source validator checks the displayed call, literal result, and script/data
hashes against this recording.

The earlier base-R script remains in `analyze.R`. `captures/controls/` preserves
its three-argument request and the restart-and-devtools-test rehearsal. Their
fixture and collector remain in `../../archived/2026-09-17-final-slide-review/`.
The readline introduction and debugger reuse the original prompt/input captures.

`sandbox-analysis.R` is the standalone sandbox example. From the presentation
directory, run `mcp-console sandbox -- Rscript examples/sandbox-analysis.R`.
It uses base R to read the measurements CSV and print model coefficients under
the default read-only policy; it does not need an MCP server or package resolver.
