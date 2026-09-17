# Checks before presentation or capture

The slide copy uses the intended presentation-day feature set, as requested. These notes distinguish that target from the currently inspected implementation.

## Target-day assumptions

**`duckdb-requirements` — automatic DuckDB extension resolution.** Explicit `requirements.duckdb` is implemented. The currently inspected contract says SQL does not trigger package discovery. Keep the “resolve on demand” claim only after that path lands, or change the slide takeaway to explicit preparation followed by loading.

**`runtime-combinations` — independent runtime combinations.** Python without an R installation is a future direction in the vision document. The current combined worker still requires R on the execution host. Hiding the R code field is not evidence of an R-independent worker. Verify the actual runtime refactor before presenting this as finished.

**`install-r` — `install.packages("mcp.console")`.** This assumes publication to an R repository available in the presenter’s repository configuration. The inspected README currently uses `pak::pak("github::t-kalinowski/mcp-console/r")`. The binary download is triggered by first use when executable resolution needs it, not by `install.packages()` itself.

Richer named profiles, complete initial environment configuration, and configured SQL defaults remain broader design scope. This deck avoids presenting speculative YAML fields as runnable configuration; its displayed configuration examples use the implemented profile and override paths.

## Capture checks

Use a tested release or pinned executable. Confirm the actual MCP handshake, selected languages, requirement capability, plotting behavior, and file visibility in the chosen client. Check client startup/read deadlines separately from Console’s evaluation-wait timeout. Cold installation and explicit preparation can have different timing behavior.

The examples around SQL connection selection are alternatives. Restore managed DuckDB before demonstrating its extension requirements. R and Python frames are not automatically visible to every selected connection: retain the visible registration step on the Python SQL slide.

The direct Python client returns text and image placeholders. Use native MCP or an image-preserving adapter for a visual demo. Verify the exact chatlas and Anthropic adapter path instead of inferring image support from the existence of a tool wrapper.

The raw per-cell log retains up to 1 GiB, not unlimited output. Retrieval requires a filesystem tool with access to the **controller** recording directory. A worker-only filesystem tool on a remote host is not sufficient.

Generated Quarto source is not a full interactive session replay or live-memory checkpoint. External data, failed cells, dynamic requirements, and execution environment all matter. Remote/container projections default to non-executing. Rendering trusted source is separate from executing inside the worker sandbox.

Default host read access is not confidentiality protection. Package installation runs outside the worker sandbox and may execute build/install code. Docker and Docker Sandbox use prepared image/template dependencies and do not currently enable dynamic preparation.

## Language to keep precise

Use “compatible MCP stdio clients,” not an unqualified “works with everything.” Use “token-conscious” or explain the bounded-input/output mechanisms rather than claiming a measured token or latency reduction that was not benchmarked. State that interrupt is cooperative, ordinary errors can leave partial effects, and restart loses live objects while retaining prepared requirements.

Current platform support is macOS and Linux, with documented Linux glibc and sandbox prerequisites; not Windows. A supported native wheel avoids Rust compilation for that installation path, not every source build or dependency build.

## Local validation status

The submitted analysis, plots, progress, stdin, debugger, bounded-output, and transcript panels now use native R output or actual Console captures. The `yaml-transcripts` slide reproduces a checked-in CPU detection snapshot; that product test was not rerun here. No model API or client-integration recording was run. See [VALIDATION.md](VALIDATION.md) for the executable fingerprint, failed pinned-package rehearsal, sandbox probes, and remaining platform checks.
