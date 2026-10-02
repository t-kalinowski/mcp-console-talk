# Integration and capture examples

These examples follow the project interfaces cited in `../docs/sources.md`. The provider integration examples were syntax-checked, not executed against provider APIs. The non-model capture script was executed against the installed Console; see `../docs/validation.md`. Running a provider example performs real API calls and can incur usage charges.

Use the corresponding extra from `mcp-console[client]`, `[chatlas]`, `[openai]`, `[openai-agents]`, `[anthropic]`, or `[codex]`. Configure the provider’s normal credentials. The Python provider examples read `MODEL_ID`; no particular current model ID is hard-coded.

The mixed-language examples require R and the prerequisites described by MCP Console. Console also supports Python and SQL without R; these examples intentionally exercise all three languages.

`measurements.csv` is synthetic. All Python analysis examples change their own working directory to this examples directory so the worker can find it. Run `ellmer.R` from this directory as well. The model controls which cells to run; prompts do not guarantee a particular language sequence.

`replay_demo.py` is a deterministic non-model driver. It submits once, then polls without replaying the cell. `bootstrap.R` includes deliberate sleeps to make the timing behavior visible, not to benchmark performance.

The Responses slide displays a registration excerpt; `openai_responses.py` includes the continuation loop and a 24-round limit. The native Anthropic and chatlas examples are the intended visual paths. Direct `MCPConsole.send()` returns text and image placeholders, not a graphical display widget.

## Capture and refresh

`cells.json` is the source for captured calls, the marked send calls in the deck, and `cells.R`. Run `python scripts/sync_cells.py` from the project directory after editing it. `capture_console.py` uses the MCP stdio protocol and saves text, PNGs, complete responses, the wire exchange, and generated session files. It never calls a model. Options precede `--command`; choose an empty output directory for each run.

The native-output example prepares `inline`, compiles a C function, and writes to stdout from a forked R child. It requires a C/C++ compiler and a Unix R runtime. Its output and Python's `os.write()` output are asserted during capture. `refresh_capture_excerpts.py` also requires Mike Farah's `yq`; the metadata event is converted to YAML and checked by converting it back to JSON.

Configurations whose `slide` is null in `configs/index.json` remain as reference examples outside the slide sequence. The two files under `configs/excerpts/` are focused slide fragments, not complete launch configurations. Their `excerpt_of` entries point to the complete configurations. `proxy-options.yaml` shows every field of the proxy object with an explicit enabled-proxy baseline; its empty rule maps allow no destinations.

`../captures/language-reveal/` contains a separate sandboxed session for the simple Python call, Matplotlib plot, and both directions of R/Python object access. Its own `cells.json`, wire exchange, returned PNG, and provenance identify those examples. Both render modes use these captures. The source validator checks the displayed calls and returned text/images against that record. Run `python examples/capture_language_reveal.py OUT EXECUTABLE` to recapture them in an empty output directory before replacing the published capture.

`configs/docker.yaml` selects a prepared image named `my-console:analysis`. Build that image from the [Console repository's Dockerfile](https://github.com/t-kalinowski/mcp-console/blob/ea5c1e737f329a86d957b12d7d1f15690824e398/examples/docker/Dockerfile), following its [Docker guide](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md). Console uses preinstalled packages in Docker; it does not resolve new packages in a running container. No image build or container session was run for this presentation.

```sh
python examples/capture_console.py --command /absolute/path/to/mcp-console serve
python examples/refresh_capture_excerpts.py
```

The pinned R example is a separate fresh session:

```sh
python examples/capture_console.py --requirements-only \
  --out captures/requirements --command /absolute/path/to/mcp-console serve
```

That pin did not pass the local rehearsal; preserve the failed recordings and use another empty output directory when retrying. Do not change the pin to mask it.

`uv run examples/refresh_references.py` regenerates the Python reference score, plot, and provenance. `check_sandbox.py` requires PyYAML and exercises only the local YAML in a disposable directory. Its network probes use example.com and substitute that domain for the proxy's example allow entry.

`summarize.R` is the interactive script on the combined-call slide. It asks for a group through `readline()`, reads the measurements CSV with `readr`, and prints a summary. The displayed request combines restart, a `readr` requirement, `A\n` on stdin, and `source("./summarize.R")`. Launch from this examples directory. `captures/combined-input/` holds the exact request and its single response, plus checks that the old workspace was replaced and group A was selected. The original collector is not included; the recorded requests, responses, and provenance are retained. The source validator checks the displayed call, literal result, and script/data hashes against this recording.

The earlier base-R script remains in `analyze.R`. `captures/controls/` preserves its three-argument request and the restart-and-devtools-test rehearsal. Their original fixture and collector are not included in this repository. The readline introduction and debugger reuse the original prompt/input captures.

`sandbox-analysis.R` is the standalone sandbox example. From the presentation directory, run `mcp-console sandbox -- Rscript examples/sandbox-analysis.R`. It uses base R to read the measurements CSV and print model coefficients under the default read-only policy; it does not need an MCP server or package resolver.
