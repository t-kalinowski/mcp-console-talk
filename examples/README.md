# Integration and capture examples

These examples follow the project interfaces cited in `../sources.md`. They were syntax-checked, not executed against Console or provider APIs in the build environment. Running a provider example performs real API calls and can incur usage charges.

Use the corresponding extra from `mcp-console[client]`, `[chatlas]`, `[openai]`, `[openai-agents]`, `[anthropic]`, or `[codex]`. Configure the provider’s normal credentials. The Python provider examples read `MODEL_ID`; no particular current model ID is hard-coded.

The current combined runtime requires a supported execution-host R installation and the prerequisites described by MCP Console. R-independent operation is a presentation-day feature, not assumed by these scripts.

`measurements.csv` is synthetic. All Python analysis examples change their own working directory to this examples directory so the worker can find it. Run `ellmer.R` from this directory as well. The model controls which cells to run; prompts do not guarantee a particular language sequence.

`replay_demo.py` is a deterministic non-model driver. It submits once, then polls without replaying the cell. `bootstrap.R` includes deliberate sleeps to make the timing behavior visible, not to benchmark performance.

The Responses slide displays a registration excerpt; `openai_responses.py` includes the continuation loop and a 24-round limit. The native Anthropic and chatlas examples are the intended visual paths. Direct `MCPConsole.send()` returns text and image placeholders, not a graphical display widget.
