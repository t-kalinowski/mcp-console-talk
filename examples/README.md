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
