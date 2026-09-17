# MCP Console — speaker notes

Generated from the native `.notes` blocks in `deck.qmd`. Edit that file, not this reading copy.


## 01. MCP Console

**Say:** I want the model to have R and Python available in the same session, and choose the language that helps with the task. That keeps R’s packages and methods in reach while opening up Python’s ecosystem too.

We also keep solving the same execution problems around each language: waiting, output, dependencies, records, and permissions. Console puts that work into a shared runtime, with the sandbox as part of the design from the beginning.

**Show:** Start with why. The small tool interface is a consequence of this design, which we will see in a few concrete examples.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 02. Choose the language for the task

**Say:** These are capabilities available to one model. R can fit the model, Python can use the same data with another library, and SQL can summarize it. The model can choose as the task develops.

Keeping R useful here means making its capabilities easy to reach from the agent’s ordinary workflow. We should not need to choose an R-only or Python-only product before the work begins.

**Show:** Each language has reasons to use it. The examples are illustrative uses, not exclusive assignments of what a language can do.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 03. Solve the execution problems once

**Say:** These are the problems we often solve piecemeal around a language tool. Duplicating the runtime means solving much of this again for each language. Console shares the execution lifecycle, output handling, recording, and sandbox boundary. Language-specific adapters still do their own work.

The aim is one coherent execution system. I’ll use three small details later to show what that means in practice.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 04. Give the model room to explore, with explicit permissions

**Say:** A useful agent needs to execute real code and use real libraries. That gives its mistakes consequences: writes, network access, subprocesses, and package code all deserve attention. The sandbox is central to making this useful.

The user chooses filesystem and network permissions. The worker runs the model’s code within those permissions. Trusted package preparation has a separate boundary, which I’ll make explicit when we get to dependencies. This is a scoped permission model, not a promise that arbitrary code or packages cannot cause harm.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 05. Start with a cell

**Say:** The final expression is fit, so R prints its normal lm summary. The agent receives useful output immediately, not prose that stands in for output. This is a real, persistent R workspace; ordinary cells do not require another object-management API.

**Show:** Show the exact submitted R code beside the printed lm object. The code and renderer both read the same cell definition. The data frame stays available for the following cells.

**Author / capture:** Default preview evaluates this cell in native R through knitr, not in MCP Console. With -P output_source:mcp, the panel reads the literal captured Console text. No simulated numerical output is committed.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 06. The R plot comes back with the result

**Say:** This is the base-R plot produced by this exact plot() call. Plotting is part of the runtime contract, not another tool. All drawing for a managed plot belongs in the same cell.

**Show:** Let R render this figure during quarto preview. Do not substitute a Matplotlib graphic. Capture mode uses the PNG returned by Console instead.

**Author / capture:** Default uses the displayed base-R cell through knitr; plot capture mode reads captures/r-plot-01.png. Neither a stock image nor the previous illustrative SVG is used.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 07. Python can read the R workspace

**Say:** Python works in the same session. Start with one expression: how many rows are in the R data frame? The r bridge exposes the existing object. Next we can use Python libraries on that data.

**Show:** This is an actual captured Python response.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 08. Use a Python library on the same data

**Say:** We already have the data in R. Python reads it through r.d and uses scikit-learn for cross-validation. This shows why both languages belong in one session: the choice follows the library we want to use. The numerical result is a real capture; comparing the statistical merits of the two models is outside this example.

**Show:** The meaningful difference is the library being used: RandomForestRegressor and cross_val_score. The result is shown below the call.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 09. Query the same data with SQL

**Say:** The same session can also query the live R data frame with DuckDB. The model can choose SQL for a grouped count without exporting the frame first. The connection and catalog persist across calls.

**Show:** d is the R data frame from the first example. This response comes from the same captured Console session.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 10. Make CRAN and PyPI available to the session

**Say:** In my experience, models often hesitate to install packages because installation sounds like a change to the user’s global setup. They may settle for a simpler approach using only what is already there. I want using the right library to be an ordinary part of the analysis.

Here the requirement belongs to the Console session and is resolved into a managed environment. That puts the breadth of trusted CRAN and PyPI packages in reach. The session’s retained requirement configuration is temporary; resolver caches and prepared environments may be reused on disk. This does not mean every package installs successfully or that all its installation code is sandboxed.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 11. Use the package; let the runtime prepare it

**Say:** The model writes ordinary R or Python. When execution reaches a supported missing-package operation, the runtime requests preparation, activates the result, and continues the original operation. It keeps the live workspace.

For R this uses ir; managed Python uses uv. We react to package use during execution rather than pre-scanning the source or replaying the whole cell. Explicit requirements remain available when the model needs a version pin or a distribution name that cannot be inferred from an import.

**Show:** These are illustrative package-use calls. Availability depends on a working managed resolver and the package’s system prerequisites. Docker’s prepared-image path is different and appears later.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 12. Separate trusted preparation from worker execution

**Say:** This separation is how we make package use work with the sandbox. A supported request crosses to trusted preparation. The prepared environment comes back to the worker; we do not give every cell unrestricted networking to install things itself.

Package installation is real code with the preparation account’s authority. Requirements and resolver configuration must be trusted. Caches can persist. The useful promise is a managed environment and a restricted worker, not that arbitrary packages are harmless. On SSH, preparation happens on the remote execution host.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 13. The wait expires. The work continues.

**Say:** A calculation can take longer than a tool call should hold the client. Here the client waits 450 milliseconds and receives the progress so far. The computation is still running in the same worker. The timeout describes how long to wait for output. We can poll for more without submitting the calculation again.

**Show:** Read both the compact progress line and the exact running notice. The panel reads the captured response; call boundaries remain timing-dependent.

**Author / capture:** Warm up the session before capturing this example. Do not promise exactly 15% at 450 ms. The local capture script retains actual responses rather than asserting fixed percentages.

**Sources:** [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 14. Pick up the next output from the same run

**Say:** These are separate responses to later polls, not a transcript dumped into one response. Each poll contains newly collected output. Carriage-return redraws within one response interval collapse to its current line; a later interval can return the next current line.

**Show:** Point to the two poll calls and their corresponding results. The last response has real output and no invented [done] appended. Emphasize that empty send() is also a poll.

**Author / capture:** Both rendering modes read the two literal captured responses. The wire exchange records the 600 ms poll followed by the 5000 ms poll. Exact progress fractions are not a public API guarantee.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 15. A progress bar should stay one progress bar

**Say:** A person sees a progress bar redraw itself. The model should receive the useful current display too. Console interprets carriage returns so repeated updates can compact instead of filling the context with stale frames. This deterministic example writes three states; the returned text keeps the final one. It is a small detail that makes ordinary libraries more usable by a model.

**Show:** Show the escaped raw characters on the left and the literal compacted result on the right. Both boxes identify their representation explicitly; the explanation stays outside them.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 16. Keep the response readable; retain the longer output

**Say:** A noisy cell should not use the whole context window. One response keeps a beginning, a recent tail, and a notice pointing to retained output. The model can inspect the longer record with an appropriate filesystem tool if needed. The text budget is 8 KiB per result, with a separate allowance for images; raw retention also has a limit. This slide shortens the response for display.

**Show:** This is one stylized response. The middle notice and path are shortened, and most preview lines are omitted to fit the slide. The complete literal response is in captures/flood.txt.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 17. Include output that bypasses the language hooks

**Say:** inline compiles a small C function that writes directly to file descriptor 1. The R call invokes it in a forked child and waits for that child to finish. The inline namespace was prepared before the displayed call; its compiler setup is preserved in the capture. The Python call writes bytes directly to file descriptor 1, bypassing Python’s sys.stdout object. Console captures both through the session’s output streams. Both examples bypass the ordinary language output hooks. The R fork example was captured on macOS and uses the Unix-only parallel::mcparallel API.

**Show:** Each example has its own actual captured response. Longer text is retained in per-cell logs, up to the retention limit, with a bounded preview returned to the client. The examples finish their children before returning.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 18. Start with restricted execution

**Say:** The default native policy permits host reads, private temporary writes, and restricted networking. This is a useful starting point for analysis without granting general filesystem writes. Read access is broad by default: sensitive paths need explicit denial or a more isolated execution target. The policy applies to the worker and its subprocesses. The native runner is a separate executable that applies the OS restrictions.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 19. Make the project’s permissions concrete

**Say:** For project work we can allow workspace writes, make the data directory read-only, and deny the secrets directory and .env. These are user-selected permissions captured when Console starts. The model can work inside that choice. The example shows why the sandbox needs more than a single on/off switch.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Use pre-existing fixture paths. Native specificity is not array order. Linux has documented limits for nested deny/read reopenings; this simple example does not establish arbitrary cross-platform ACL equivalence.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 20. Allow selected destinations through a proxy

**Say:** For example, a corporate warehouse can expose an HTTPS query endpoint at the allowed host. A database using another TCP protocol needs a SOCKS-aware client or an explicitly configured SOCKS tunnel; a domain allowlist does not rewrite arbitrary database drivers. Network reachability and database authentication remain separate. For a database on a private IP, the pinned proxy requires a literal allowed IP matching the destination (or the broader local-binding exception); a hostname allowlist alone does not grant private-address access. The placeholder host is illustrative and was not contacted.

 This complete proxy configuration shows both the allowlist and the surrounding controls. The runner owns proxy routing, host normalization, and enforcement. A proxy object must include the required scalar fields; Console does not materialize omitted defaults for it.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Example domains are placeholders, not actual services. All seven required scalar proxy fields are present. mode: full does not erase the domain allowlist. Review PROTOCOL.md for mode, upstream proxy, UDP and local-binding semantics.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 21. Develop a local Shiny app

**Say:** This configuration supports local Shiny development: the worker can bind the loopback port while outbound requests use the managed proxy. Start an app at app/ with shiny::runApp and open its URL locally. A long-running app uses the wait, poll, and interrupt contract introduced earlier.

 An interactive local server can need a binding exception. The policy exposes that choice separately from the domain allowlist. Do not conflate permission to bind with permission to publish a remote service, create a tunnel, or expose every Unix socket.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Validate the exact native behavior with the application used for the demo. This slide does not promise a Shiny viewer or automatic port forwarding. Keep all required proxy fields when changing a single flag.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 22. Choose where the work should run

**Say:** Language and location are separate choices. The model can choose the language for a cell while the user chooses where the session executes. Local work is convenient; SSH puts computation near remote data or a larger machine; Docker packages a prepared environment.

Local and SSH managed preparation require the documented runtime and resolver prerequisites. Docker deliberately uses packages already installed in the image. These are target choices for a session, rather than live migration of an existing workspace. SSH and Docker are separate target modes in the current implementation.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [Docker execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md)


## 23. Bring the session to the data over SSH

**Say:** Suppose the dataset is already on an analysis machine, or the task needs more memory. The client can stay where I work while the session uses that host’s files and compute. Console sends operations over SSH and records the returned results locally. Package preparation and the native sandbox run remotely too.

The remote host needs a compatible Console installation, the runtime prerequisites, and an existing workspace. The remote account’s permissions and the worker sandbox both matter. No transfer of the dataset to the local machine is required for the cells shown here.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md)


## 24. Point Console at the remote workspace

**Say:** This is the local project configuration. analysis-host is an existing SSH destination, and /srv/projects/analysis is an existing directory on that host. The workspace baseline and the read-only data rule are materialized there. Then the client starts mcp-console serve in the usual way. Relative worker paths refer to the remote workspace; records stay with the controller.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** analysis-host must be a configured OpenSSH destination; /srv/projects/analysis and data must already exist. SSH+Docker composition is not supported in this revision.

**Sources:** [ssh](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 25. Prepare an environment the team can reuse

**Say:** Docker is useful when the environment itself is something we want to prepare and share: language runtimes, packages, and native dependencies together. The controller starts a container from that image and supplies the selected mounts. Each worker generation gets a fresh Console-owned container.

This mode uses preinstalled packages. Dynamic package resolution is disabled; changing the package set means rebuilding the image and starting a new session. Builds and pulls are trusted setup, and writable bind mounts can still change host files. Container policy and mounts therefore belong to the execution design.

**Sources:** [Docker execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md)


## 26. Select the image and expose the workspace

**Say:** This example selects a prepared image and binds the project into /workspace. external-sandbox delegates enforcement to the existing Docker boundary; the enabled network setting permits ordinary container networking. The writable bind is deliberate and exposes those host files to changes. Use the permissions the task needs. The next slide returns to what the model sees.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Build my-console:analysis first. Source paths are interpreted by the selected Docker daemon. Native sandboxing inside Docker is a separate supported selection where host capabilities permit it; no privileged-mode fallback is implied.

**Sources:** [docker](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 27. Keep the interaction familiar across targets

**Say:** The model still sends a cell, receives results, and uses the same wait and control contract. It can use R and Python whether the worker is beside the local project, on an SSH host, or in a container. The client above and the target below can change while that interaction remains familiar. Available preparation capabilities differ by target and are reflected by the live tool schema.

**Show:** Return to one familiar call with four destinations beneath it. This is the bridge into client integrations: both the client above and execution target below can vary without changing the central idea.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 28. Leave a record that someone can inspect

**Say:** Exploration should leave something useful behind. Console retains the submitted calls and returned results, raw cell logs, and image artifacts. The directory tree shows where those records live. The event journal also preserves metadata supplied with a request; the complete wire capture made by our example collector is a separate file.

**Show:** The right panel reads the captured fit log. Full transport traffic, including initialization, is separately captured by our collector in captures/wire.jsonl.

**Sources:** [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 29. Turn the session into an editable starting point

**Say:** The source projection contains executable chunks rather than escaped code in a log. Rendering runs those cells again in a new Quarto environment. It does not replay stdin, interrupts, restarts, or prior outputs, and the required data and SQL connection still need to exist.

**Show:** Show literal Quarto chunk delimiters. The left panel contains the complete generated front matter. The right panel is the unchanged model cell; the preceding warmup cell and later cells are outside the excerpt.

**Author / capture:** These are literal source slices from the captured document. The long root.dir path is shortened to <project> only in this slide; the original is preserved in captures/excerpts/quarto-header.txt. Dependencies reflect the generated front matter of this build and do not include every inferred package. Local render occurs outside the Console worker sandbox. Remote projections default eval:false.

**Sources:** [architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 30. ellmer

**Say:** Give ellmer one slide. The R wrapper starts Console, reads its live tool schema, and presents it as an ellmer tool. It does not execute agent code in the R process running the chat. Provider choice remains with ellmer and the application. Keep the tool alive across the conversation so its session persists.

**Show:** Show only the registration example, with the registration line emphasized. No installation explanation here; that is the next section. The author notes include the asynchronous sequential-tool caveat from the R README.

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md) · [R tool wrapper implementation](https://github.com/t-kalinowski/mcp-console/blob/main/r/R/console-tool.R)


## 31. chatlas

**Say:** The chatlas adapter adds the same tool to an existing chat. Use the adapter and set_tools so the explicit server schema is preserved rather than inferred from a generic Python function annotation. The application still owns the chat loop and the Console connection lifetime.

**Show:** Keep the visual design identical to the ellmer slide. For a visual demo, verify image preservation on the chosen adapter path; the native MCP registration variant is included in the examples file.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 32. Register Console with your CLI client

**Say:** Both clients can launch the same Console server over MCP stdio. Run the registration command for the client you use. Client-side deadlines remain separate from Console’s wait timeout.

**Show:** The launcher and server arguments are identical. The commands were checked against the installed CLI help; no configuration was changed.

**Sources:** [Codex MCP](https://developers.openai.com/codex/mcp/) · [Claude Code MCP](https://code.claude.com/docs/en/mcp)


## 33. Now, installation from R

**Say:** Only after the value and client examples are clear, show the R installation story. For presentation day, assume mcp.console is published to the intended R package repository. Installing the R package gives the interface; creating the tool resolves the Console executable when necessary. Do not say the PyPI download occurs during install.packages itself.

**Show:** Show one large line. This is explicitly an intended publication pathway: the currently inspected R README uses a GitHub installation command. Keep the present-day command in the author checklist, not as competing text on this slide.

**Author check before presenting:** Target-day assumption: mcp.console is published to an R repository usable by install.packages(). Current README documents pak::pak("github::t-kalinowski/mcp-console/r").

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)


## 34. Python or a standalone MCP launch

**Say:** Python users choose the base package or the extra for their integration. MCP clients can launch through uvx, or use a persistent uv tool installation. These are alternative routes into the same distribution, not three installation steps. Framework extras avoid installing every SDK when only the executable is needed.

**Show:** Show three short alternatives with explicit labels. Mention prerequisites only as needed: Python packaging and supported native wheels are not the same thing as the language runtime installed on a selected execution host.

**Sources:** [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 35. R and Python, available for the work

**Say:** The reason for Console is to give the model access to R and Python together, with a common execution system underneath. That keeps R’s capabilities in reach, reduces duplicated runtime work, and lets us address the difficult parts in one place.

The three examples—waiting without losing the run, compacting a progress redraw, and retaining output beyond the context window—show the level of detail we want across that system. The sandbox and execution target are part of the same design.

**Show:** End the main talk here. The following eight slides are optional development-practice material for questions.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 36. Rust implementation. Python integration tests.

**Say:** The main integration suite is Python even though the application is Rust. It drives the built executable and observes the real process boundary. Small unit tests can still own pure parsing or validation policy; the claim is not that absolutely no Rust tests exist.

**Show:** Use two simple implementation/test boxes. Lead with why this matters: the test language can stay independent of implementation refactors while validating the product contract users and clients actually see.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md)


## 37. Test the boundaries you intend to preserve

**Say:** The tests mirror architectural boundaries: client_server, server_relay, relay_worker, and cli. Public behavior belongs at the outermost boundary that can usefully observe it. Private-boundary cases cover their own protocol seams rather than replicating every public message at every layer.

**Show:** Reuse the process topology with test-boundary names on the arrows. This ties the development method to the earlier architecture rather than presenting a directory tree with no explanation.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 38. YAML is what the reviewer reads

**Say:** The wire protocols are JSON-based, but the reviewable test transcripts are YAML. This is an actual checked-in snapshot excerpt: the test executes R, asserts that CPU detection returns a valid result, and prints a stable message. Humans can review the code and result without reading escaped JSON strings or snapshotting a machine-specific core count. YAML is the human review surface, not the production transport.

**Show:** Display the request and result from `tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml` side by side. The initial shared-handshake document is omitted, but the displayed request and result content come from the fetched source. This fixture was not rerun in the slide-build environment; do not present it as a new test execution.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Checked-in CPU detection snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml)


## 39. Normalize noise, not behavior

**Say:** Temporary paths, process identities, and similar unstable details should not obscure behavioral review. Normalize explicitly and narrowly. Preserve the fields, output, ordering, and failure distinctions the contract is meant to protect. The actual project normalizers and snapshot metadata are more specific than this schematic example.

**Show:** Use before/after panels with only incidental details changed. Call out that normalization is not a license to delete inconvenient evidence from a test.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 40. Synchronize; do not sleep and hope

**Say:** Concurrency and liveness tests need causal synchronization. Fixtures use gates and checkpoints so the test knows when the relevant state has actually been reached. Arbitrary sleeps are not proof that output was drained, an interrupt was delivered, or an owned resource was retired.

**Show:** Show one deterministic sequence and connect it to the timing and shutdown contracts from the talk. This is a development-practice slide, not an implementation recipe for every fixture.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 41. Portable behavior; real capability checks

**Say:** Reuse portable cases across execution modes and centralize capability discovery. A skipped target fixture is not target validation. Deterministic peers can establish orchestration behavior, but they cannot establish real container or microVM cleanup. Keep real-target evidence distinct from simulated protocol coverage.

**Show:** Use the two testing levels rather than an all-green platform matrix. Include lifecycle and security assertions where a textual snapshot alone cannot represent the guarantee.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 42. Snapshots are generated evidence

**Say:** Generate transcripts from running tests, then review the resulting diff. Do not hand-edit the expectation to make a test pass. The value of readable YAML is that review can focus on the actual changed behavior, while assertions still enforce facts that a snapshot cannot show.

**Show:** Show the update command and a diff review, not a large wall of green tests. The selector is schematic; replace BOUNDARY/SUITE::CASE with a real selected fixture for a live development demonstration.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 43. Test the installed product

**Say:** The delivered product includes the executable, companion binaries, Python interfaces, the R wrapper, and launch/lifetime behavior. Running a development binary alone does not establish that the installed bundle or each adapter works. Integration examples and packaging checks should be part of the release evidence, with actual target validation reported separately.

**Show:** Finish the addendum by connecting the install story to the test strategy. Avoid claiming every proposed integration test already exists: distinguish observed project coverage from the release checklist in the companion author notes.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Release and installed bundle](https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)
