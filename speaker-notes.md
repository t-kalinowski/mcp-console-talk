# MCP Console — speaker notes

Generated from the native `.notes` blocks in `deck.qmd`. Edit that file, not this reading copy.


## 01. MCP Console

**Say:** We know how to let a model execute R code. We have built that more than once within the company. The reason for Console is to give us a comprehensive execution system we can reuse across the AI systems we build.

Once execution becomes part of a real workflow, we need persistent state, packages, input, cancellation, useful output, records, remote hosts, and a sandbox. My hope is that the next team can use this and spend its effort on the AI system it is building.

R, Python, and SQL belong in that shared workbench. The model can choose the language for the task, and we can solve the surrounding execution problems together.

**Show:** Lead with reuse and completeness. This audience already builds AI systems; code execution is familiar. The opening establishes why the shared system is worth adopting, and the later examples demonstrate its coverage and care.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 02. One execution system we can reuse

**Say:** This is the scope of the solution. A useful execution tool needs much more than a way to evaluate a string of code. These concerns turn up together, and we have been addressing them in separate, ad hoc implementations.

The goal is a common workbench teams can adopt: persistent sessions, interactive control, dependencies, bounded output, records, local or remote compute, and sandboxing. Language-specific adapters still do their own work, while the surrounding infrastructure is shared.

I hope we can stop needing a new console implementation for each project. When we find another execution problem, we can solve it in the shared system. The examples later in the talk show a few details that make this breadth usable.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 03. Full capabilities and full safety

**Say:** We want the model to have the languages’ full capabilities. That includes libraries, native code, and subprocesses. Those capabilities also carry risks: a mistake can change files, read secrets, contact a remote service, or leave work running.

The sandbox constrains what that code can access, and the runner owns its lifecycle. Safety depends on those permissions and on trusted setup. This does not make arbitrary execution risk-free. Package preparation runs outside the worker sandbox, and the default host-read policy needs explicit denials for confidential files.

**Show:** Present two equal requirements: full language capabilities and enforced safety. The sandbox limits access to resources while preserving the languages and their libraries. The later policy examples show how the user sets that access. Full safety is the design goal; do not describe arbitrary code or trusted package installation as risk-free.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 04. Equip the model with R, Python, and SQL

**Say:** These are capabilities available to one model. R can fit the model and visualize the results. Python offers another set of libraries. SQL can query a local or remote database, letting its engine optimize filters, joins, and aggregations. The model can choose as the task develops, including the syntax it works best with. Data visualization is available in both R and Python; these cards do not assign exclusive strengths. A selected DBI or Python DB-API connection supplies the SQL backend; remote access needs the relevant driver, credentials, and network permission.

Keeping R useful here means making its capabilities easy to reach from the agent’s ordinary workflow. We should not need to choose an R-only or Python-only product before the work begins.

**Show:** Each language has reasons to use it. The examples are illustrative uses, not exclusive assignments of what a language can do.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 05. Connect Console to your agent harness

**Say:** The previous slide showed the languages the model can execute. This slide shows the harness or application making those calls. Console is an MCP server, so a compatible MCP client can use it directly. There is an ellmer tool in the R package, and Python offers direct clients and adapters for these frameworks. We will return to registration near the end. First, follow what this shared workbench provides as the task grows.

The adapters preserve the live tool schema. Image support and client deadlines vary by interface, so check the chosen path before a demo. These interfaces are documented in the current source checkout; the installed PyPI 0.0.3 wheel used for runtime captures does not include the newer Python clients and extras.

**Sources:** [Python integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)


## 06. Send a cell of code

**Say:** The execution system is comprehensive, but the common call stays simple. This is the interaction we optimize for: send a cell, inspect its output, and continue with the objects already in the session. A simple call is enough.

The final expression is fit, so R calls the fitted object’s default print method. The model receives that printed text; the fitted object remains in the R session. The agent receives useful output immediately, not prose that stands in for output. This is a real, persistent R workspace; ordinary cells do not require another object-management API.

**Show:** Show the exact submitted R code beside the printed lm object. The code and renderer both read the same cell definition. The data frame stays available for the following cells.

**Author / capture:** Default preview evaluates this cell in native R through knitr, not in MCP Console. With -P output_source:mcp, the panel reads the literal captured Console text. No simulated numerical output is committed.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 07. Return plots

**Say:** This is the base-R plot produced by this exact plot() call. Plotting is part of the runtime contract, not another tool. All drawing for a managed plot belongs in the same cell.

**Show:** Let R render this figure during quarto preview. Do not substitute a Matplotlib graphic. Capture mode uses the PNG returned by Console instead.

**Author / capture:** Default uses the displayed base-R cell through knitr; plot capture mode reads captures/r-plot-01.png. Neither a stock image nor the previous illustrative SVG is used.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 08. Python uses the same call

**Say:** The same send tool also accepts Python. Choose the python argument, define a list, and print its sum. The calling pattern is the same as the R example.

**Show:** Stay with ordinary Python for this slide. The response is captured from Console, and values remains available for the next cell.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 09. Python plots return images too

**Say:** Plotting works here too. Use Matplotlib on the values from the preceding cell and receive the image in the tool response, just as with R graphics.

**Show:** This is the actual returned PNG. The full response also contains Matplotlib's text representation of its final label object; the slide shows the image block. Both rendering modes use the capture.

**Transition:** So far these look like two familiar language consoles. They are also connected to each other.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 10. R and Python share the same process

**Say:** And these are the same process. Python can read d, the data frame we created in R, and R can read values, the list we just created in Python. The model can use the language it needs while continuing the same analysis.

Reticulate supplies the bridge and converts values between the languages. Sharing the worker does not mean every object has zero-copy or reference-sharing behavior; conversion depends on the type.

**Show:** Each call has its own response directly below it. These calls, the initial R data frame, and the preceding Python cells were captured in one Console session.

**Transition:** SQL can use the R data frame too.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 11. Query the same data with SQL

**Say:** The same session can also query the live R data frame with DuckDB. The model can choose SQL for a grouped count without exporting the frame first. The connection and catalog persist across calls.

**Show:** d is the R data frame from the first example. This response comes from the same captured Console session.

**Transition:** That is the default DuckDB connection. The model can also select a database connection owned by R or Python.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 12. SQL uses the connection you choose

**Say:** SQL defaults to the session’s DuckDB connection. The model can instead select a valid DBI connection owned by R, or a DB-API connection owned by Python. These SQLite examples are alternatives; a remote database connection follows the same selection pattern. The driver supplies the SQL dialect and transaction state.

Later sql calls go to the selected connection. The object stays in its owning runtime, with its connection-local state. These are supported database connection interfaces, not arbitrary objects. A selected database sees its own tables and registrations; it does not automatically inherit the default DuckDB connection’s access to R data frames.

Restore the managed connection with console_sql_connection(NULL) in R or console_sql_connection(None) in Python before closing a custom connection. A remote connection still needs its driver, credentials, and network permissions.

**Show:** Read the R and Python panels as two alternatives, followed by the same SQL call. No model or remote database call is needed for this illustration.

**Transition:** Now that the languages and database connections are in place, we can expand the session with packages from CRAN and PyPI.

**Sources:** [SQL connection selection](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md#sql)


## 13. Make CRAN and PyPI available to the session

**Say:** In my experience, models often hesitate to install packages because installation sounds like a change to the user’s global setup. They may settle for a simpler approach using only what is already there. I want using the right library to be an ordinary part of the analysis.

Here the requirement belongs to the Console session and is resolved into a managed environment. That puts the breadth of trusted CRAN and PyPI packages in reach. The session’s retained requirement configuration is temporary; resolver caches and prepared environments may be reused on disk. This does not mean every package installs successfully or that all its installation code is sandboxed.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 14. Use the package; let the runtime prepare it

**Say:** The model writes ordinary R or Python. When execution reaches a supported missing-package operation, the runtime requests preparation, activates the result, and continues the original operation. It keeps the live workspace.

For R this uses ir; managed Python uses uv. We react to package use during execution rather than pre-scanning the source or replaying the whole cell. Explicit requirements remain available when the model needs a version pin or a distribution name that cannot be inferred from an import.

**Show:** These are illustrative package-use calls. Availability depends on a working managed resolver and the package’s system prerequisites. Docker’s prepared-image path is different and appears later.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 15. Use a Python library on the same data

**Say:** We already have the data in R. Python reads it through r.d and uses scikit-learn for cross-validation. This shows why both languages belong in one session: the choice follows the library we want to use. The numerical result is a real capture; comparing the statistical merits of the two models is outside this example.

**Transition:** The session can now use the libraries the work calls for. Next, follow what happens when a cell runs longer or needs input.

**Show:** The meaningful difference is the library being used: RandomForestRegressor and cross_val_score. The result is shown below the call.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 16. Collect progress while the code keeps running

**Say:** This uses R’s built-in txtProgressBar and setTxtProgressBar; no extra package is needed. Sys.sleep stands in for each unit of work. A calculation can take longer than a tool call should hold the client. Here the client waits 450 milliseconds and receives the progress so far. The computation is still running in the same worker. The timeout describes how long to wait for output. We can poll for more without submitting the calculation again.

**Show:** Read both the compact progress line and the exact running notice. The panel reads the captured response; call boundaries remain timing-dependent.

**Author / capture:** Warm up the session before capturing this example. Do not promise a particular percentage at 450 ms. The local capture script retains actual responses rather than asserting fixed percentages.

**Sources:** [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 17. Pick up the next output from the same run

**Say:** These are separate responses to later polls, not a transcript dumped into one response. Each poll contains newly collected output. Carriage-return redraws within one response interval collapse to its current line; a later interval can return the next current line.

**Show:** Point to the two poll calls and their corresponding results. The last response has real output and no invented [done] appended. Emphasize that empty send() is also a poll.

**Author / capture:** Both rendering modes read the two literal captured responses. The wire exchange records the 600 ms poll followed by the 5000 ms poll. Exact progress fractions are not a public API guarantee.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 18. Interrupt or restart the session

**Say:** Interrupt a long-running computation while keeping the workspace, like pressing Escape in the RStudio console. It requests SIGINT; code can catch or delay it. Changes already made by the computation remain. Restart retires the worker and starts a replacement. R objects, Python state, the managed DuckDB catalog, debugger state, and unread input are discarded; successfully prepared dependencies remain available.

A control and a code cell can be combined in one send call. A common package-development pattern is to restart and then call devtools::load_all() or devtools::test() in the same send. The package files remain on disk, while the operation runs in a fresh R session. Launch from the package directory for these examples. The two calls are alternatives. The ellipsis after load_all is a placeholder for the package code the model wants to evaluate next, not literal R code to run.

**Show:** There are exactly two accepted control values. A control-only interrupt can overlap a pending send. If interrupt includes a new cell, that cell runs only after the previous evaluation has stopped; an uncooperative evaluation prevents it from running. Use the simpler restart example here to make ordering visible.

**Author / capture:** The restart-plus-test call was exercised against the local package fixture in the controls capture. The next slide captures restart plus a sourced script with queued input.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [Interruption and restart](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md#interruption)


## 19. Run an interactive script in a fresh session

**Say:** An existing analysis script asks which group to summarize. The model can run it in a fresh session without editing out its interactive prompt. One request restarts the worker, queues A followed by a newline, and sources the script. When readline asks for the group, that input is already available. The server returns lifecycle notices and the script's output in one response.

Launch this example from the examples directory, where ./analyze.R and ./measurements.csv are present. The source path names the real checked-in script. It reads the same measurements CSV used earlier in the talk. source does not automatically print each visible expression, so the script prints its summary explicitly. The newline is explicit because stdin does not add one.

**Show:** Read the script, then the call and response. Only the replacement receives same-call input. This is captured output, including the managed read notice; startup messages and prompt formatting can vary by runtime. The capture separately checks that an object from the old session is gone and the script selected group A. If the answer depends on output not yet seen, run the script first and answer its prompt with a later stdin-only call.

**Sources:** [Send operation order](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md#operations)


## 20. The complete send() interface

**Say:** These are the seven top-level fields in the managed session's send interface. All are optional, and a call accepts at most one complete R, Python, or SQL cell. Requirements contain lists of R packages, Python distributions, or managed DuckDB extensions. The live schema exposes preparation only when the execution environment supports it.

An empty send collects output. stdin answers a prompt or debugger; its text is queued exactly, so a line of input normally needs a trailing newline. Control interrupts or restarts the session. timeout_ms limits how long the call waits for an evaluation, rather than stopping the evaluation when that wait expires. Explicit preparation and control happen before that wait.

**Show:** This is a schematic field overview, not a call that supplies three languages at once. Keep the walkthrough brief. The preceding examples introduced evaluation, waiting, polling, interruption, restart, and input. This slide brings those arguments together. Requirements can also prepare an environment explicitly before a cell runs. Code-free standalone preparation cannot carry nonempty stdin. Use stdin alone to answer an already active prompt.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 21. Protect the model’s context from oversized output

**Say:** A noisy cell should not use the whole context window. One response keeps a beginning, a recent tail, and a notice pointing to retained output. The model can inspect the longer record with an appropriate filesystem tool if needed. The text budget is 8 KiB per result, with a separate allowance for images; raw retention also has a limit. This slide shortens the response for display.

**Show:** This is one stylized response. The middle notice and path are shortened, and most preview lines are omitted to fit the slide. The complete literal response is in captures/flood.txt.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 22. Capture output below the language hooks

**Say:** The R example forks with parallel::mcparallel. Inside that child, R’s cat writes to a pipe; the native cat command forwards the bytes to stdout. Closing the pipe finishes that command, and mccollect waits for the forked child. This uses Unix process APIs and was captured on macOS.

The Python example writes directly to file descriptor 1, bypassing sys.stdout. The text is followed by 23, the number of bytes returned by os.write and displayed as the cell’s final expression. There is no assignment to discard that value.

**Show:** Both panels use actual Console responses. Read each call with its own result. The R child → pipe → native cat route is deliberate: ordinary cat() in the fork completed but its text was absent in this installed build. Do not present the plain call as captured successfully. The older C-level fork example remains in the reference captures.

**Transition:** Those details describe what the agent sees. Next, look at the process arrangement that makes dependency preparation and sandbox enforcement possible.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 23. Separate session control from code execution

**Say:** The LLM client talks to the Console server over MCP. The server owns the session and its records. A relay carries cells, input, output, and control messages to the worker, where R, Python, and SQL run. The sandbox enforces permissions and owns process cleanup.

Package resolvers are separate trusted processes, outside the worker sandbox. That is how the server can prepare a package without giving the worker direct network access. A protocol-level example of that exchange is in the appendix.

**Show:** This is the simplified local layout. Arrows indicate the labeled two-way exchanges, not a strict parent-process tree. Native setup helpers are omitted. The native runner is a separate executable; the shaded area identifies the processes whose permissions it restricts. Remote targets change placement and transport while retaining the session interface.

**Transition:** The shaded boundary marks where the evaluated code runs. Next, look at the permissions it gets by default.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 24. Default policy: read-only

**Say:** The default is the read-only policy, available explicitly as :read-only. Before changing anything, here is what it provides: broad host reads, writes confined to private temporary storage, restricted direct networking, and the same policy for subprocesses. Project files and shared temporary directories are not generally writable.

The runner owns worker cleanup on restart and shutdown, removes its private temporary storage, and handles caller loss while it remains alive. On Linux, it waits for namespace retirement. On macOS, cleanup covers the owned process group and detached descendants the runner observes; it cannot promise to catch every orphaning race. Runner death has no independent recovery guarantee.

Read access and inherited environment variables can expose secrets, so configure explicit denials and environment controls when needed. Trusted package preparation is outside this worker policy. Session records, package caches, and intentionally written project files persist; temporary cleanup does not remove those.

**Show:** Explain these defaults before introducing a configuration file. Next, compare the built-in policies at launch, then add project-specific permissions.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 25. Choose between two built-in sandbox policies

**Say:** The two named built-ins are :read-only and :workspace. The default gives read access and private scratch. Workspace mode additionally grants writes under the launch working directory while protecting .git, .agents, .codex, and .claude from writes. Networking and private-storage behavior remain restricted.

The -c option selects the policy for this launch. There are two built-in names in the current interface; external-sandbox and unrestricted are enforcement modes rather than additional named presets. The next slide puts the workspace choice in a project file and adds explicit read and deny entries.

**Show:** These are alternative launch commands. The leading colon is part of each built-in name. Project configuration is read first; -c overrides its extends field while retaining other configured fields. Demonstrate in a clean project when showing just the built-in baseline.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [Configuration layering](https://github.com/t-kalinowski/mcp-console/blob/main/docs/CONFIGURATION.md)


## 26. Extend a built-in policy for the project

**Say:** Console reads .agents/console/config.yaml in the launch directory once at startup. This is trusted user configuration. The default requires no file. extends: ":workspace" makes the previous launch choice part of the project configuration. For project work we can allow workspace writes, make the data directory read-only, and deny the secrets directory and .env. These are user-selected permissions captured when Console starts. The model can work inside that choice. The example shows why the sandbox needs more than a single on/off switch.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Use pre-existing fixture paths. Native specificity is not array order. Linux has documented limits for nested deny/read reopenings; this simple example does not establish arbitrary cross-platform ACL equivalence.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 27. Example: connect to a corporate data warehouse

**Say:** For example, a corporate warehouse can expose an HTTPS query endpoint at the allowed host. A database using another TCP protocol needs a SOCKS-aware client or an explicitly configured SOCKS tunnel; a domain allowlist does not rewrite arbitrary database drivers. Network reachability and database authentication remain separate. For a database on a private IP, the pinned proxy requires a literal allowed IP matching the destination (or the broader local-binding exception); a hostname allowlist alone does not grant private-address access. The placeholder host is illustrative and was not contacted.

 This complete proxy configuration shows both the allowlist and the surrounding controls. The runner owns proxy routing, host normalization, and enforcement. A proxy object must include the required scalar fields; Console does not materialize omitted defaults for it.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Example domains are placeholders, not actual services. All seven required scalar proxy fields are present. mode: full does not erase the domain allowlist. Review PROTOCOL.md for mode, upstream proxy, UDP and local-binding semantics.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 28. Example: develop a local Shiny app

**Say:** This configuration supports local Shiny development: the worker can bind the loopback port while outbound requests use the managed proxy. Start an app at app/ with shiny::runApp and open its URL locally. A long-running app uses the wait, poll, and interrupt contract introduced earlier.

 An interactive local server can need a binding exception. The policy exposes that choice separately from the domain allowlist. Do not conflate permission to bind with permission to publish a remote service, create a tunnel, or expose every Unix socket.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Validate the exact native behavior with the application used for the demo. This slide does not promise a Shiny viewer or automatic port forwarding. Keep all required proxy fields when changing a single flag.

**Transition:** A running app can create child processes. The next slide explains what happens to that process tree when the session restarts or the server shuts down.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 29. Clean up on restart or server shutdown

**Say:** This sequence runs when an explicit session restart is requested or the Console server shuts down. File and network permissions are only part of the sandbox. Console asks the worker to shut down and gives it a short grace period. The current default is one second. If the worker does not exit, the relay force-stops it. The sandbox also cleans up the process tree, so a child that outlives its parent is part of the shutdown contract.

On Linux, the runner waits for the kernel to finish terminating the owned PID namespace. On macOS, it watches fork and exit events, tracks process identity, and stops the original process group and observed descendants, including those that detach. A descendant that detaches and becomes orphaned before observation can fall outside the macOS guarantee. The worker grace period and the runner's separate descendant-cleanup deadline are different limits.

The runner confirms process cleanup before removing private storage. A cleanup failure is reported as an error; if termination cannot be established, it retains the storage. Server or relay loss triggers cleanup while the runner remains alive. The runner's own death does not guarantee temporary-directory deletion or macOS workload termination. Prepared package caches, records, and project files are retained.

**Show:** The sequence applies to the normal native sandbox. It is separate from the cooperative interrupt control. The notes retain platform boundaries; the visible point is that the session owns the child processes it launches.

**Transition:** These responsibilities belong to the execution environment. The worker itself can also live on another host.

**Sources:** [Console runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md#limitations) · [Pinned native runner lifecycle](https://github.com/t-kalinowski/codex/blob/2d0ad797210de821c07d1f18e4f1ffdcf06589cb/codex-rs/mcp-console-sandbox/LIFECYCLE.md)


## 30. Configure where the session runs

**Say:** The architecture separates session control from its execution target, so target adapters can support different environments. These cards show local, SSH, and Docker examples supported today. The session worker does not have to run beside the client. It can run locally, on an SSH host, or in Docker. The user selects the target at session launch, and the model still chooses R, Python, or SQL. Additional targets need an implementation of the relevant transport, environment, and lifecycle contracts; arbitrary environments do not work just by naming them.

Local and SSH targets support managed package preparation on the execution host. Docker uses the packages prepared in its image. The current implementation treats SSH and Docker as separate target modes.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [Docker execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md)


## 31. Move execution to the remote host

**Say:** This is the earlier process diagram with execution moved to another host. The LLM client and Console server stay on your machine. SSH carries cells, input, controls, and results between the server and the remote relay. R, Python, and SQL run in the remote worker under that host's sandbox policy.

Package preparation moves too. A separate SSH connection reaches the trusted preparation processes on the remote host, outside the worker sandbox. Prepared packages and their caches belong there. Session logs, returned images, and output records remain with the local Console server.

**Show:** Compare the same client, server, relay, worker, and resolver boxes with the local diagram. The warm outer box is the remote host; the green dashed box is its sandbox. Arrows show communication, not parent-process relationships. SSH helpers and setup processes are omitted. The existing remote workspace and runtime prerequisites must already be present.

**Transition:** With this placement, the worker can use data already on that host.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md)


## 32. Send code to the remote host; receive results

**Say:** This is an SSH session on an existing host. The project and source data are already there. Console sends code and control messages to that worker and receives its output, plots, and artifacts. It does not copy the project into a Docker sandbox.

Results can of course contain data selected by the submitted code. The point is that the dataset does not need to be staged locally to run the analysis. The remote host needs a compatible Console installation, runtime prerequisites, and the workspace. Both the account permissions and the worker sandbox apply.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md)


## 33. Point Console at the remote workspace

**Say:** This is the local project configuration. analysis-host is an existing SSH destination, and /srv/projects/analysis is an existing directory on that host. The workspace baseline and the read-only data rule are materialized there. Then the client starts mcp-console serve in the usual way. Relative worker paths refer to the remote workspace; records stay with the controller.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** analysis-host must be a configured OpenSSH destination; /srv/projects/analysis and data must already exist. SSH+Docker composition is not supported in this revision.

**Sources:** [ssh](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 34. Build the session's Docker image at launch

**Say:** The Dockerfile starts from a prepared Console image and adds scikit-learn. The YAML asks Console to build that image during initial setup, then run the session in it with the project mounted at /workspace. Both build paths are relative to the local launch directory. Packages come from the image; this target does not resolve them dynamically during evaluation.

external-sandbox delegates file and network enforcement to the Docker boundary; network: enabled permits ordinary container networking. The writable mount exposes those host files to changes. There are no implicit home, credential, or Docker socket mounts.

**Show:** The Dockerfile and YAML are separate files displayed together. Inline Dockerfile text is not accepted in the current target schema; build.dockerfile names a file. Docker build runs before the analysis worker and uses trusted setup permissions. It is not governed by the worker's network policy.

**Author / capture:** my-console:base is a user-prepared image, not a published image supplied by this talk. It needs a compatible Linux Console installation and companion bundle, R and its SQL/bridge dependencies, and a Python environment on PATH. The repository's full example Dockerfile documents that base. This slide demonstrates an analysis-specific layer. The Docker target and image build were not run locally.

**Sources:** [Docker execution and base image](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md) · [Full example Dockerfile](https://github.com/t-kalinowski/mcp-console/blob/main/examples/docker/Dockerfile)


## 35. The agent uses the same interface on every host

**Say:** The model still sends a cell, receives results, and uses the same wait and control contract. It can use R, Python, and SQL whether the worker is beside the local project, on an SSH host, or in a container. The client above and the target below can change while the agent keeps the same send, result, and control interface. Available preparation capabilities differ by target and are reflected by the live tool schema.

**Show:** Return to one familiar call with three destinations beneath it. This is the bridge into client integrations: both the client above and execution target below can vary without changing the central idea.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 36. Register Console with your CLI client

**Say:** Both clients can launch the same Console server over MCP stdio. Run the registration command for the client you use. Client-side deadlines remain separate from Console’s wait timeout. In the ordinary uvx-managed path, uv resolves requirements using its registry cache and picks up newer versions as that cache expires. It does not promise a new registry lookup on every launch. An explicitly installed compatible tool can be reused instead, and version pins remain intentional. Keep those details in the notes; the visible point is that the launcher manages installation and updates.

**Show:** The launcher and server arguments are identical. The commands were checked against the installed CLI help; no configuration was changed.

**Sources:** [uv tools](https://docs.astral.sh/uv/concepts/tools/) · [Codex MCP](https://developers.openai.com/codex/mcp/) · [Claude Code MCP](https://code.claude.com/docs/en/mcp)


## 37. Install the R package

**Say:** With the execution model established, show the R installation route before registering the tool in ellmer. For presentation day, assume mcp.console is published to the intended R package repository. The R package connects R applications to Console, handles the tool schema and results, and resolves the core binary from PyPI using reticulate’s uv integration. Executable resolution occurs when the tool is created, not during install.packages. An explicit path or a compatible executable already on PATH can be used instead of a download; an explicit version selects that PyPI release.

**Show:** Show one large line. This is explicitly an intended publication pathway: the currently inspected R README uses a GitHub installation command. Keep the present-day command in the author checklist, not as competing text on this slide.

**Author check before presenting:** Target-day assumption: mcp.console is published to an R repository usable by install.packages(). Current README documents pak::pak("github::t-kalinowski/mcp-console/r").

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)


## 38. ellmer

**Say:** Give ellmer one slide. The R wrapper starts Console, reads its live tool schema, and presents it as an ellmer tool. It does not execute agent code in the R process running the chat. Provider choice remains with ellmer and the application. Keep the tool alive across the conversation so its session persists.

**Show:** Show only the registration example, with the registration line emphasized. The preceding slide installed the R package; this connects it to an ellmer chat. The author notes include the asynchronous sequential-tool caveat from the R README.

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md) · [R tool wrapper implementation](https://github.com/t-kalinowski/mcp-console/blob/main/r/R/console-tool.R)


## 39. Python or a standalone MCP launch

**Say:** This first command includes every supported Python client extra. Use only the extras your harness needs. MCP clients can launch through uvx, or use a persistent uv tool installation. These are alternative routes into the same distribution, not three installation steps. Framework extras avoid installing every SDK when only the executable is needed.

**Show:** The comma-separated extras name the supported integrations directly. The three panels are alternative installation routes with explicit labels. Mention prerequisites only as needed: Python packaging and supported native wheels are not the same thing as the language runtime installed on a selected execution host.

**Sources:** [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 40. chatlas

**Say:** The chatlas adapter adds the same tool to an existing chat. Use the adapter and set_tools so the explicit server schema is preserved rather than inferred from a generic Python function annotation. The application still owns the chat loop and the Console connection lifetime.

**Show:** Keep the visual design identical to the ellmer slide. For a visual demo, verify image preservation on the chosen adapter path; the native MCP registration variant is included in the examples file.

**Transition:** Whichever client you use, the session leaves a record of its work. End with what can be inspected and turned into a report.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 41. Keep session logs and readable transcripts

**Say:** Exploration should leave something useful behind. These files retain calls and results, raw output, plots, and two views of the session. Per-cell logs retain output up to the documented 1 GiB limit. The Markdown is a readable history. The Quarto source is a starting point for a report.

The structured event journal preserves request metadata supplied by the harness. It is not the entire MCP transport exchange; our capture script records that separately in wire.jsonl. Session records remain on the controller when the worker is remote.

**Show:** Walk down the tree. The comments are explanatory annotations, and the filenames reflect the captured layout.

**Sources:** [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 42. Turn the session into an editable starting point

**Say:** Add a snapshot date to the editable copy and render it with ir render report.qmd. ir consumes ir.exclude-newer to select dated default CRAN and Bioconductor repositories; declared Python requirements inherit the cutoff unless separately configured. This keeps subsequent resolution tied to the analysis date. It does not by itself pin every system dependency or arbitrary external source.

This is one Quarto document: front matter followed by an executable R chunk. Copy it into a report, edit the analysis, and render it in a suitable environment. Console owns the generated original; edit a copy.

Rendering runs the cells again. It does not replay interactive input, interrupts, or prior outputs. The data and any selected SQL connection still need to exist, and trusted rendering happens outside the worker sandbox. Remote projections default to eval:false.

**Show:** Read it from top to bottom as one source file. The snapshot date is an author-added setting, not a field emitted by the captured Console build. The root directory is shortened to <project>, the generated-file warning is omitted, and the dependency lists are shortened for display. The full source remains in captures/session-records/transcript.qmd. Dependencies reflect this captured build; they are not a complete record of inferred packages.

**Transition:** This is the result of the whole path: the agent worked interactively, used the needed languages and host, and left an editable analysis behind.

**Sources:** [ir Quarto integration](https://r-lib.github.io/ir/quarto.html) · [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 43. R, Python, and SQL, available for the work

**Say:** The reason for Console is to give the model access to R, Python, and SQL together, with a common execution system underneath. That keeps R’s capabilities in reach, reduces duplicated runtime work, and lets us address the difficult parts in one place.

The examples—waiting without losing the run, compacting progress, and retaining output beyond the context window—show the level of detail we want across that system. The sandbox is central to that design: it enforces file and network permissions and cleans up the processes the session starts. We want the model to use the full languages and libraries within the access the user allows. Trusted package setup remains a separate boundary.

My hope is that the next AI project can build on this workbench, without needing another ad hoc execution tool. Its comprehensiveness is what makes that reuse possible.

**Show:** End the main talk here. After the appendix divider, the remaining slides cover the resolver protocol and development practices for questions.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 44. Appendix

**Say:** The main talk ends here. These slides are available for questions about the implementation and how its behavior is checked.

**Show:** Pause at this divider before entering the development material.


## 45. Follow a package-resolution request

**Say:** The request comes from the runtime inside the worker, through the relay to the server. The server validates it and uses a trusted resolver outside the sandbox to prepare the library. The result is a library path, which the worker adds to its live library search path. It acknowledges activation before continuing the package load. The server commits the retained environment only for a matching activation from the current worker generation.

These are private worker-protocol messages, not MCP tool calls the model has to make. The field names match the documented protocol; /cache/r/library is an illustrative path. Python follows the analogous resolve_python exchange and activates a prepared interpreter environment.

Installation and build code run with the preparation account’s permissions, so requirements and resolver configuration must be trusted. Caches can persist. The worker’s filesystem and network policy continues to apply. On SSH, preparation runs on the remote execution host.

**Sources:** [Worker protocol](https://github.com/t-kalinowski/mcp-console/blob/main/docs/WORKER_PROTOCOL.md#nested-managed-r-resolution) · [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 46. Rust implementation. Python integration tests.

**Say:** The main integration suite is Python even though the application is Rust. It drives the built executable and observes the real process boundary. Small unit tests can still own pure parsing or validation policy; the claim is not that absolutely no Rust tests exist.

**Show:** Use two simple implementation/test boxes. Lead with why this matters: the test language can stay independent of implementation refactors while validating the product contract users and clients actually see.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md)


## 47. Test the boundaries you intend to preserve

**Say:** The tests mirror architectural boundaries: client_server, server_relay, relay_worker, and cli. Public behavior belongs at the outermost boundary that can usefully observe it. Private-boundary cases cover their own protocol seams rather than replicating every public message at every layer.

**Show:** Reuse the process topology with test-boundary names on the arrows. This ties the development method to the earlier architecture rather than presenting a directory tree with no explanation.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 48. YAML is what the reviewer reads

**Say:** The wire protocols are JSON-based, but the reviewable test transcripts are YAML. This is an actual checked-in snapshot excerpt: the test executes R, asserts that CPU detection returns a valid result, and prints a stable message. Humans can review the code and result without reading escaped JSON strings or snapshotting a machine-specific core count. YAML is the human review surface, not the production transport.

**Show:** Display the request and result from `tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml` side by side. The initial shared-handshake document is omitted, but the displayed request and result content come from the fetched source. This fixture was not rerun in the slide-build environment; do not present it as a new test execution.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Checked-in CPU detection snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml)


## 49. Normalize noise, not behavior

**Say:** Temporary paths, process identities, and similar unstable details should not obscure behavioral review. Normalize explicitly and narrowly. Preserve the fields, output, ordering, and failure distinctions the contract is meant to protect. The actual project normalizers and snapshot metadata are more specific than this schematic example.

**Show:** Use before/after panels with only incidental details changed. Call out that normalization is not a license to delete inconvenient evidence from a test.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 50. Synchronize; do not sleep and hope

**Say:** Concurrency and liveness tests need causal synchronization. Fixtures use gates and checkpoints so the test knows when the relevant state has actually been reached. Arbitrary sleeps are not proof that output was drained, an interrupt was delivered, or an owned resource was retired.

**Show:** Show one deterministic sequence and connect it to the timing and shutdown contracts from the talk. This is a development-practice slide, not an implementation recipe for every fixture.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 51. Portable behavior; real capability checks

**Say:** Reuse portable cases across execution modes and centralize capability discovery. A skipped target fixture is not target validation. Deterministic peers can establish orchestration behavior, but they cannot establish real container or microVM cleanup. Keep real-target evidence distinct from simulated protocol coverage.

**Show:** Use the two testing levels rather than an all-green platform matrix. Include lifecycle and security assertions where a textual snapshot alone cannot represent the guarantee.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 52. Snapshots are generated evidence

**Say:** Generate transcripts from running tests, then review the resulting diff. Do not hand-edit the expectation to make a test pass. The value of readable YAML is that review can focus on the actual changed behavior, while assertions still enforce facts that a snapshot cannot show.

**Show:** Show the update command and a diff review, not a large wall of green tests. The selector is schematic; replace BOUNDARY/SUITE::CASE with a real selected fixture for a live development demonstration.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 53. Test the installed product

**Say:** The delivered product includes the executable, companion binaries, Python interfaces, the R wrapper, and launch/lifetime behavior. Running a development binary alone does not establish that the installed bundle or each adapter works. Integration examples and packaging checks should be part of the release evidence, with actual target validation reported separately.

**Show:** Finish the addendum by connecting the install story to the test strategy. Avoid claiming every proposed integration test already exists: distinguish observed project coverage from the release checklist in the companion author notes.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Release and installed bundle](https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)
