# Checks before presentation or capture

The slide copy uses the intended presentation-day feature set, as requested. These notes distinguish that target from the currently inspected implementation.

## Target-day assumptions

**`install-python` — `install.packages("mcp.console")`.** The slide labels this as the planned CRAN installation, and the spoken notes say the package is not on CRAN yet. The current source command is `pak::pak("github::t-kalinowski/mcp-console/r")`. Binary download happens when executable resolution needs it, not during `install.packages()` itself. The richer S7 configuration surface mentioned in the rehearsal is not present in the inspected R wrapper.

Richer named profiles, complete initial environment configuration, and configured SQL defaults remain broader design scope. This deck avoids presenting speculative YAML fields as runnable configuration; its displayed configuration examples use the implemented profile and override paths.

**`interfaces` — Python adapters.** The overview follows the current source checkout. The PyPI 0.0.3 wheel used for runtime captures does not contain the newer Python clients and extras; use a release or source installation that includes them.

## Capture checks

Use a tested release or pinned executable. Confirm the actual MCP handshake, selected languages, requirement capability, plotting behavior, and file visibility in the chosen client. Check client startup/read deadlines separately from Console’s evaluation-wait timeout. Cold installation and explicit preparation can have different timing behavior.

The direct Python client returns text and image placeholders. Use native MCP or an image-preserving adapter for a visual demo. Verify the exact chatlas and Anthropic adapter path instead of inferring image support from the existence of a tool wrapper.

The raw per-cell log retains up to 1 GiB, not unlimited output. Retrieval requires a filesystem tool with access to the **controller** recording directory. A worker-only filesystem tool on a remote host is not sufficient.

Generated Quarto source is not a full interactive session replay or live-memory checkpoint. External data, failed cells, dynamic requirements, and execution environment all matter. Remote/container projections default to non-executing. Rendering trusted source is separate from executing inside the worker sandbox.

The native default permits broad host reads; deny sensitive paths explicitly. Package installation runs outside the worker sandbox and may execute build/install code. Docker and Docker Sandbox use prepared image/template dependencies and do not currently enable dynamic preparation.

## Language to keep precise

Use “compatible MCP stdio clients,” not an unqualified “works with everything.” Use “token-conscious” or explain the bounded-input/output mechanisms rather than claiming a measured token or latency reduction that was not benchmarked. State that interrupt is cooperative, ordinary errors can leave partial effects, and restart loses live objects while retaining prepared requirements.

Current platform support is macOS and Linux, with documented Linux glibc and sandbox prerequisites; not Windows. A supported native wheel avoids Rust compilation for that installation path, not every source build or dependency build.

## Local validation status

The submitted analysis, plots, progress, stdin, debugger, bounded-output, and transcript panels now use native R output or actual Console captures. The `yaml-transcripts` slide reproduces a checked-in CPU detection snapshot; that product test was not rerun here. No model API or client-integration recording was run. See [VALIDATION.md](VALIDATION.md) for the executable fingerprint, failed pinned-package rehearsal, sandbox probes, and remaining platform checks.

## Narrative claims

The package-installation hesitation is the presenter's experience and motivation,
not a measured comparison of models. Describe access to trusted packages from
CRAN and PyPI rather than promising that every package can install or run safely.

Session requirements are retained in server memory. Package caches and prepared
environments may persist on disk. Trusted preparation runs outside the worker
sandbox on the execution host. The worker uses the result under its own policy.
Docker uses packages built into the image; it does not dynamically resolve them.

The detail examples combine wait/poll continuity with progress compaction, then
show bounded responses and retained output, including a direct descriptor write and output from a forked R child.
The last slide of the main talk is `closing`; the appendix divider introduces nine slides of
optional technical material. The earlier full API walkthrough is preserved in
presentation commit `ab89d0c`.

The forked R example deliberately sends cat() output through a pipe to the native
cat command. Plain cat() in the fork completed without visible text in the tested
build. Do not replace the displayed example with the plain call without a new
capture. The private resolver exchange uses documented fields and an illustrative
library path; it is not presented as a literal captured exchange.

The Docker build example uses `examples/Dockerfile` alongside the YAML. The
configuration accepts a Dockerfile path, not inline Dockerfile text. The recipe
starts from `rocker/tidyverse`, installs uv and rig with their standard scripts,
and runs `uv tool install r-lib-ir`. The YAML launches `uvx mcp-console`.
**Target-day assumption:** this minimal example relies on Docker supporting
managed package preparation. The inspected implementation currently disables it,
even with uv and ir present. Confirm that support before using this as a live
example. The image build and container session have not been run.

The report's `ir.exclude-newer` date is added to an editable copy. Use
`ir render report.qmd` to consume it. It is a package snapshot cutoff rather than
a complete environment lock, and was checked in the local ir guide without a
dated render rehearsal.

Plain `uvx` manages installation and picks up updates as its registry cache expires.
Do not promise a fresh lookup on every launch. Explicit pins and a compatible
installed tool can retain an older version.

SQL connection examples were exercised with local RSQLite and Python sqlite3
connections. Other drivers and remote database access still need their own setup.

The default-policy notes combine Console's one-second worker grace with the native
runner's separate descendant cleanup. Keep the platform limits in the notes:
macOS covers the owned process group and observed detached descendants; Linux
uses namespace retirement. Do not present the worker grace as the native cleanup
deadline or promise cleanup after the runner itself is killed.


## Dictated run-through revision

The notes follow the presenter's dictation, with repetition and timestamps removed.
The missing segment (old slides 13–18) retains its previous notes. Debugger input
now precedes the combined restart/input/cell call, explicit requirements are back,
and the complete send interface ends the model-facing walkthrough. The local
process diagram accompanies package resolution. The dedicated cleanup slide was
removed; its platform details remain in the default-policy notes and the archive.

The warehouse and Shiny slides show labeled excerpts. The full proxy configuration
follows them. Current proxy scalar fields have no implicit defaults, so these
excerpts must not be used as standalone configs. The complete files are retained
under examples/configs, and fragments are under examples/configs/excerpts.

Keep the distinction between the structured events journal and the full MCP wire
exchange. The transcript front matter records known requirements; it is not a
complete inventory of every inferred package. The snapshot date is added to the
editable report, and rendering also requires its data and external connections.


## Second run-through

The opening now goes from the rewrite and shared-effort motivation to the model's
language choice, then to one combined capabilities and safety slide. Its spoken
notes explain explicit runtime-state reporting, including managed input and idle
output, before listing the surrounding capabilities. The middle of the talk is
unchanged.

The recording slide shows `.agents/console/sessions/<session-id>/`. The journal
records tool requests and assembled results with metadata; it is not a complete
wire capture. The current artifact recorder saves returned images. It does not
grant the worker a general-purpose export directory. The QMD front matter holds
managed defaults and explicit declarations, not every dynamically inferred
package or a lockfile. These boundaries were checked in the current local
architecture and worker-protocol documentation.


## Input and combined calls

Introduce stdin with a two-call readline example before the debugger. Both reuse
literal captures. The following combined request has four arguments: control,
requirements, stdin, and an R cell sourcing examples/summarize.R. Its readr
requirement is used by the script, and its response was captured in a fresh
sandboxed rehearsal. The order is preparation, worker replacement, input enqueue,
and script evaluation. The response is one actual tool result, not concatenated
polls. The three-argument base-R capture remains available as historical evidence.
