# MCP Console — speaker notes

Generated from the native `.notes` blocks in `deck.qmd`. Edit that file, not this reading copy.


## 01. MCP Console

**Say:** Hello everyone. I'd like to take a few minutes to talk about a project I've been working on called MCP Console. It's a ground-up rewrite of MCP REPL. There were a couple of problems with MCP REPL, and I reached the point where starting from scratch looked like less work than trying to repair it. I'll get to some of those problems throughout the talk.

One was conceptual. MCP REPL is really two products: an R REPL and a Python REPL. When you get into the weeds, they take substantially different code paths and expose different semantics to the model. That kind of doubled the workload. It also forces the user to choose R or Python, and I don't think that's where the choice belongs. It should be R and Python.

That was the original seed for MCP Console: a single product, a single binary, that handles R, Python, and SQL. My hope is that we can share the effort of building one execution tool to equip agents with, instead of each building an ad hoc implementation for the needs at hand.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 02. Equip the model with R, Python, and SQL

**Say:** The choice I want to give the model is which language fits the task it's doing right now. If R has the methods or plotting tools it wants, use R. If the Python ecosystem is a better fit, use Python. And SQL gives it another way to query data, locally or through a database connection.

The user can steer that choice, of course. But they shouldn't have to pick an R-only or Python-only product before the work begins. I'd like the model to choose the best tool for the job.

For that to work, we need to give it the full capabilities of those runtimes, with a sandbox that controls what resources it can access.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 03. Full capabilities and full safety

**Say:** The goal is full capabilities and full safety. I don't want to restrict the language to a small subset just to make execution manageable. The model should be able to use libraries, native code, and subprocesses, within the permissions the user allows.

That means handling the less obvious cases too. Output can come from a forked child or directly from a file descriptor. A computation can take a long time, need an interrupt, or produce enough output to flood the model's context. A script can ask for input over stdin. We want the model to be able to drive a real interactive session through all of that.

We run the languages embedded, so the runtime reports when it is evaluating, waiting for managed input, or finished. We don't have to parse printed output to guess that state. Output from background activity can still be collected while the session is idle, and Console tracks the controls it sends, including shutdown and escalation.

Around that session, we handle plots as images, compact progress updates, oversized responses with files the model can inspect, and logs with readable transcripts and Quarto source. Package resolution and environment management are built in too.

And the sandbox is central: filesystem permissions, network restrictions, and a configurable proxy, applying to the worker and its subprocesses. The session can run locally, over SSH, or in Docker. That's the breadth of the shared solution; the rest of the talk goes through the details.

**Reference (not spoken):** “Full safety” is the design goal, not a claim that arbitrary code is risk-free. Trusted package preparation runs outside the worker sandbox. Broad host reads need explicit denials for confidential files. Managed runtime reads emit input_requested/input_received events; arbitrary native reads are not all observable as managed input. Worker readiness and evaluation completion use explicit protocol frames, while raw and background output are separate streams. Console tracks requested controls and lifecycle operations; this is not introspection into every background thread. Target capabilities and enforcement differ, as explained later.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Worker protocol](https://github.com/t-kalinowski/mcp-console/blob/main/docs/WORKER_PROTOCOL.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 04. Connect Console to your agent harness

**Say:** Those are the capabilities we expose to the model, and the execution choices the user can configure. On the client side, there are several ways to equip an agent with Console.

It works with compatible MCP harnesses, including Codex and Claude. In R, it works with ellmer as a tool you register with the chat. There are also integrations for the Python SDKs: Anthropic, Codex, OpenAI Responses, the Agents SDK, and chatlas.

And there are SDK-agnostic synchronous and asynchronous clients. You can use those from another harness or just drive the session manually.

**Reference (not spoken):** The adapters are documented in the source checkout; the older PyPI wheel used for some captures lacks newer clients and extras. Verify the release and image support of the chosen adapter before a live demo.

**Sources:** [Python integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)


## 05. Send a cell of code

**Say:** Despite that long tail of capabilities, we've optimized for the simplest use case: evaluating a chunk of code. The model sends a string of R code, it gets evaluated, and the model gets back output.

This is the only tool exposed: a single send tool. Here the code defines d, a data frame, then fits a linear model and prints the fitted object. The objects stay in the session, ready for the next turn.

**Author / capture:** Default preview evaluates this cell in native R through knitr, not in MCP Console. With -P output_source:mcp, the panel reads the literal captured Console text. No simulated numerical output is committed.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 06. Return plots

**Say:** On the next turn, maybe the model wants to generate a graphic. It sends plotting code using the objects already in the session, and the graphic comes back as an image. It works as you'd expect.

**Author / capture:** Default uses the displayed base-R cell through knitr; plot capture mode reads captures/r-plot-01.png. Neither a stock image nor the previous illustrative SVG is used.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 07. Python uses the same call

**Say:** If the model wants to send Python, it changes the keyword argument. The previous call used r; this one uses python.

Now the string is evaluated as a Python cell, and the model gets its printed output. The usage pattern is the same.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 08. Python plots return images too

**Say:** Plots work in Python as you'd expect too. Here the model uses Matplotlib to plot the values from the preceding cell, and the image comes back in the response.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 09. R and Python share the same process

**Say:** And the R and Python runtimes are embedded in the same process. You can access values defined in R from Python, and vice versa. Reticulate provides that bridge.

On the left, Python accesses d, the data frame in R's global environment. On the right, R accesses values from Python's main dictionary. The model can work with the same data across the two languages.

**Reference (not spoken):** Reticulate conversion depends on the object type; shared process does not imply universal zero-copy or reference-sharing behavior.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 10. Query the same data with SQL

**Say:** SQL works the same way: the model sends code with the sql argument. Notice that the query refers to d, the data frame defined in the R namespace.

The default DuckDB connection can find R data frames by name. If we replace that data frame in R, a later query sees the updated binding. We don't need to export it to a separate database first.

It's one runtime, with different ways for the model to interact with it.

**Reference (not spoken):** The managed DuckDB backend scans the R global environment. A view over an R name observes later rebinding. Python data frames must first be bound or converted to an R global for this backend.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 11. SQL uses the connection you choose

**Say:** SQL doesn't have to use the built-in DuckDB connection. The model can select a different connection from either the R or Python runtime.

From R, that can be a DBI connection. From Python, it can be a DB-API connection. These examples use SQLite, but the same pattern works with a remote database, given the driver, credentials, and network access.

After selecting the connection, the model keeps sending SQL through the same tool. The queries go to that connection and use its tables and state.

**Reference (not spoken):** A selected connection sees its own tables and state; it does not inherit managed DuckDB registrations. Restore managed SQL with console_sql_connection(NULL) in R or console_sql_connection(None) in Python before closing a custom connection.

**Sources:** [SQL connection selection](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md#sql)


## 12. Make CRAN and PyPI available to the session

**Say:** In my experience, models often hesitate to install packages because installation sounds like a change to the user’s global setup. They may settle for a simpler approach using only what is already there. I want using the right library to be an ordinary part of the analysis.

Here the requirement belongs to the Console session and is resolved into a managed environment. That puts the breadth of trusted CRAN and PyPI packages in reach. The session’s retained requirement configuration is temporary; resolver caches and prepared environments may be reused on disk. This does not mean every package installs successfully or that all its installation code is sandboxed.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 13. Use the package; let the runtime prepare it

**Say:** The model writes ordinary R or Python. When execution reaches a supported missing-package operation, the runtime requests preparation, activates the result, and continues the original operation. It keeps the live workspace.

For R this uses ir; managed Python uses uv. We react to package use during execution rather than pre-scanning the source or replaying the whole cell. Explicit requirements remain available when the model needs a version pin or a distribution name that cannot be inferred from an import.

**Show:** These are illustrative package-use calls. Availability depends on a working managed resolver and the package’s system prerequisites. Docker’s prepared-image path is different and appears later.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 14. Separate session control from code execution

**Say:** This is how package resolution fits into the process layout. The LLM client talks to the Console server. The server owns the session and its records, and a relay carries code, input, controls, and results to and from the worker.

R, Python, and SQL run in that worker, inside the sandbox. The package resolvers are separate trusted processes outside it. When the runtime reaches a missing package, it can make a structured request for preparation. The resolver prepares the package, makes the result available, and the worker continues inside the sandbox.

That separation is what lets us prepare dependencies without giving the evaluated code the same access as the resolver.

**Reference (not spoken):** Trusted package preparation can execute installation or build code. It is outside the worker sandbox. The protocol-level request/response example remains in the appendix.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 15. Declare package requirements explicitly

**Say:** So far we've let the runtime discover packages as the code uses them. The model can also declare requirements explicitly.

Here it asks for an R package and a particular version of a Python package. It can prepare those dependencies on their own, as shown here, or include them with a code cell. Preparation happens before that cell runs.

This is useful when the model wants a specific version or when a distribution name can't be inferred from the import.

**Author / capture:** This is an illustrative preparation request; no response is presented as a capture. scikit-learn 1.9.1 is the version in the existing Python reference capture. The earlier data.table==1.17.8 rehearsal failed on the installed R toolchains and remains documented in VALIDATION.md. That older request is retained in the reference files, not represented as a successful run here. Requirements are available only on targets that support managed preparation.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 16. Use a Python library on the same data

**Say:** We already have the data in R. Python reads it through r.d and uses scikit-learn for cross-validation. This shows why both languages belong in one session: the choice follows the library we want to use. The numerical result is a real capture; comparing the statistical merits of the two models is outside this example.

**Transition:** We have seen the ordinary analysis loop: write code, inspect the result, and continue. A session also has to handle work that takes time, asks for input, or produces more output than the model can use at once. The next examples show how the same tool handles those situations.

**Show:** The meaningful difference is the library being used: RandomForestRegressor and cross_val_score. The result is shown below the call.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 17. Collect progress while the code keeps running

**Say:** This uses R’s built-in txtProgressBar and setTxtProgressBar; no extra package is needed. Sys.sleep stands in for each unit of work. A calculation can take longer than a tool call should hold the client. Here the client waits 450 milliseconds and receives the progress so far. The computation is still running in the same worker. The timeout describes how long to wait for output. We can poll for more without submitting the calculation again.

**Show:** Read both the compact progress line and the exact running notice. The panel reads the captured response; call boundaries remain timing-dependent.

**Author / capture:** Warm up the session before capturing this example. Do not promise a particular percentage at 450 ms. The local capture script retains actual responses rather than asserting fixed percentages.

**Sources:** [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 18. Pick up the next output from the same run

**Say:** These are separate responses to later polls, not a transcript dumped into one response. Each poll contains newly collected output. Carriage-return redraws within one response interval collapse to its current line; a later interval can return the next current line.

**Show:** Point to the two poll calls and their corresponding results. The last response has real output and no invented [done] appended. Emphasize that empty send() is also a poll.

**Author / capture:** Both rendering modes read the two literal captured responses. The wire exchange records the 600 ms poll followed by the 5000 ms poll. Exact progress fractions are not a public API guarantee.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 19. Protect the model’s context from oversized output

**Say:** When a response comes back from send, Console also puts a guardrail around its size. We want to prevent the model from accidentally flooding its own context by running code that produces too much output.

For an oversized response, we keep the beginning and the end, cut out the middle, and give the model a path to the fuller output. If it needs more detail, it can inspect that file with a filesystem tool.

**Reference (not spoken):** The text response budget is 8 KiB, with a separate image allowance. Raw retention is also bounded. This slide is a stylized, shortened response; captures/flood.txt holds the literal response.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 20. Capture output below the language hooks

**Say:** If you've built one of these before, another detail that may be interesting is where we capture output. We capture below the language-level hooks, so we can see output from a forked child or a direct write to a file descriptor.

On the left, an R child process sends text through a pipe to the native cat command. On the right, Python writes directly to file descriptor 1, bypassing sys.stdout. Both outputs come back through Console. That is the kind of detail we want the shared execution system to handle.

**Author / capture:** Both panels use actual responses. Plain cat() in a fork completed without visible text in the captured build; the displayed R child → pipe → native cat route was captured successfully. The 23 after Python output is os.write()'s returned byte count.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 21. Interrupt or restart the session

**Say:** Interrupt a long-running computation while keeping the workspace, like pressing Escape in the RStudio console. It requests SIGINT; code can catch or delay it. Changes already made by the computation remain. Restart retires the worker and starts a replacement. R objects, Python state, the managed DuckDB catalog, debugger state, and unread input are discarded; successfully prepared dependencies remain available.

A control and a code cell can be combined in one send call. A common package-development pattern is to restart and then call devtools::load_all() or devtools::test() in the same send. The package files remain on disk, while the operation runs in a fresh R session. Launch from the package directory for these examples. The two calls are alternatives. The ellipsis after load_all is a placeholder for the package code the model wants to evaluate next, not literal R code to run.

**Show:** There are exactly two accepted control values. A control-only interrupt can overlap a pending send. If interrupt includes a new cell, that cell runs only after the previous evaluation has stopped; an uncooperative evaluation prevents it from running. Use the simpler restart example here to make ordering visible.

**Author / capture:** The restart-plus-test call was exercised against the local package fixture in the controls capture. The following examples introduce stdin, use it with the debugger, and combine restart, requirements, input, and a sourced script.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [Interruption and restart](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md#interruption)


## 22. Send input to an R prompt

**Say:** Some R code needs to consume standard input. Here readline asks for a name, and the cell pauses while it waits for an answer. Console returns the prompt and tells the model that the runtime is waiting for input.

The model sends Ada followed by a newline through the stdin argument. That supplies the bytes to the running session. The same cell resumes, assigns the answer to name, and prints it. We don't need to submit the R code again.

That is the input mechanism for an ordinary interactive prompt. It also lets the model drive a debugger, which is the next example.

**Author / capture:** The two calls and responses are literal captures from the existing sandboxed session. stdin does not add a newline automatically. Quarto reads the captured output instead of running an interactive prompt during rendering.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 23. Send input to a paused debugger

**Say:** The same stdin argument also lets the model drive a debugger. Here a function calls browser(), and execution pauses at the debugger prompt.

The model sends x and a newline through stdin to inspect the argument. It gets the value back, along with another prompt. Then it sends c and a newline to continue, and the function returns its result.

This uses the same input mechanism as readline. The session stays alive while the model inspects values and decides how to continue.

**Author / capture:** Each call is paired with its literal Console response. All three calls were captured in the same sandboxed session. Quarto reads the saved output; it does not enter an interactive debugger during rendering. stdin does not add a newline automatically.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 24. Run an interactive script in a fresh session

**Say:** Now we can combine four things in one call: a restart, package requirements, standard input, and an R cell. This script asks which group to summarize, reads the data with readr, and prints a summary.

Console prepares the declared dependency first, then replaces the worker. Once the fresh session is ready, it queues A and a newline and sources the script. When readline asks for the group, the answer is already there. The replacement notices and the script's output come back in one response.

**Reference (not spoken):** Run from examples/ so ./summarize.R and ./measurements.csv exist. Requirements are prepared before worker retirement; a resolution failure at that stage leaves the old worker available. Only the replacement receives the queued input. Preparation makes readr available; the script calls readr::read_csv explicitly. source() does not automatically print each visible expression, so the script prints its summary. An answer that depends on unseen output should be supplied in a later stdin-only call.

**Author / capture:** The four-argument request and its single literal response were captured in captures/combined-input. A subsequent assertion verified that the old session's sentinel was gone, readr returned a tibble, and group A was selected. The earlier three-argument example and its base-R script remain in captures/controls and examples/analyze.R.

**Sources:** [Send operation order](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md#operations)


## 25. The complete send() interface

**Say:** That's the model-facing interface: one tool with a set of optional arguments. It accepts one language cell at a time, in R, Python, or SQL.

We can combine that with a session control operation or standard input. We can declare package requirements, including specific versions, and set how long the call waits for output.

And we can leave out the code: poll for more output, answer a prompt, interrupt or restart the session, or prepare dependencies. The model can start with the simple call we saw earlier and use these other arguments when it needs them.

**Reference (not spoken):** This schematic overview lists fields, not three cells to submit together. Requirements are exposed only when supported by the execution target. An empty send collects output. Explicit preparation and control precede the evaluation wait. Code-free preparation cannot also carry nonempty stdin.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 26. Default policy: read-only

**Say:** Now let's look more closely at the sandbox. The default policy is called read-only. The model has read access to the host files available to the account, but it can write only in its own private temporary storage. Direct network access is restricted.

Those restrictions apply to the worker and its subprocesses. On an explicit restart or server shutdown, Console stops the worker and cleans up its child processes and temporary storage. There is a grace period, followed by forceful termination if needed.

That's the default. If there are sensitive files the model shouldn't read, the user can deny those paths explicitly.

**Reference (not spoken):** Cleanup runs on restart and server shutdown. Console allows a worker grace period before escalation. On Linux the runner waits for PID namespace retirement; on macOS it covers the owned process group and observed descendants, with an orphaning race limitation. Runner death has no independent cleanup guarantee. Prepared dependencies, records, and project files persist. Inherited environment variables and broad host reads may expose secrets; configuration can restrict them.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 27. Choose between two built-in sandbox policies

**Say:** There are two built-in policies. Read-only is the default. Workspace adds write access under the working directory where Console is launched.

It still protects the .git, .agents, .codex, and .claude directories from writes. The network restrictions and private temporary storage are the same. The user can select either policy at the command line.

**Reference (not spoken):** The leading colon is part of the built-in name. -c overrides extends while retaining other project configuration. external-sandbox and unrestricted are enforcement modes, not additional named presets.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [Configuration layering](https://github.com/t-kalinowski/mcp-console/blob/main/docs/CONFIGURATION.md)


## 28. Extend a built-in policy for the project

**Say:** If the user wants to customize a built-in policy, Console also reads .agents/console/config.yaml from the launch directory.

Here we start with workspace and adjust the filesystem permissions: keep the data directory read-only, and deny access to the secrets directory and .env. This is the user's configuration. It sets the permissions the model gets for that session.

**Author / capture:** Use pre-existing fixture paths. Native specificity is not array order. Linux has documented limits for nested deny/read reopenings; this simple example does not establish arbitrary cross-platform ACL equivalence.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 29. Example: connect to a corporate data warehouse

**Say:** The same configuration lets us make a specific exception to the network restrictions. For example, suppose we want the model to query a corporate data warehouse through an HTTPS API.

We enable the managed proxy and allow that warehouse host. The model still needs the usual database credentials, but we can give it that connection without opening general network access.

This excerpt shows the part of the policy that selects the destination. I'll show the complete proxy configuration after the next example.

**Reference (not spoken):** This is a focused YAML excerpt, not a standalone config. examples/configs/network-proxy.yaml contains the full version. Arbitrary database TCP protocols need a SOCKS-aware client or tunnel. Private-IP destinations need the appropriate literal-IP rule or local-network exception; a hostname rule alone does not grant private-address access. Placeholder domains were not contacted.

**Author / capture:** Example domains are placeholders, not actual services. All seven required scalar proxy fields are present. mode: full does not erase the domain allowlist. Review PROTOCOL.md for mode, upstream proxy, UDP and local-binding semantics.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 30. Example: develop a local Shiny app

**Say:** Here's another example: local Shiny development. We can enable local binding so the model can launch the app on a loopback port, and then open it in a browser.

The app can keep running while the model polls for output, and the model can interrupt it when it's finished. This is another permission we can configure for the work we want the agent to do.

**Reference (not spoken):** This is a focused YAML excerpt, not a standalone config. examples/configs/network-listener.yaml contains the full version. The flag permits local networking exceptions beyond a single Shiny port; it is not a port-specific allowlist. This does not promise a viewer or automatic port forwarding.

**Author / capture:** Validate the exact native behavior with the application used for the demo. This slide does not promise a Shiny viewer or automatic port forwarding. Keep all required proxy fields when changing a single flag.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 31. The complete proxy configuration

**Say:** Here is the complete proxy configuration behind those two examples. Enabling the proxy is an explicit choice; it isn't part of the default read-only policy.

These are all the fields on the proxy object. We can set destination rules, choose whether to allow local binding, and control SOCKS, UDP, upstream proxies, and Unix sockets. The empty maps here grant no destinations. Add the warehouse rule or change the local-binding flag for the examples we just saw.

**Reference (not spoken):** The seven scalar fields are required when a proxy object is supplied; Console forwards it without filling in missing values. domains and unixSockets may be omitted, null, or empty. The shown values are an explicit enabled-proxy baseline, not automatically materialized defaults. mode: full permits the supported HTTP methods; destination policy still applies. The two preceding excerpts omit required surrounding fields for readability; their full runnable alternatives remain in examples/configs. This slide expands the proxy settings, not every platform-specific sandbox option.

**Sources:** [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 32. Configure where the session runs

**Say:** Finally, the session doesn't have to run locally. Local is the default: the worker runs on the same host as the Console server.

We can also configure an SSH host or a Docker container. The architecture separates the session interface from the execution environment, so where the worker runs is a user choice.

**Reference (not spoken):** Local and SSH support managed package preparation. The currently inspected Docker path uses prepared-image dependencies; installing uv and ir alone does not enable managed preparation.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [Docker execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md)


## 33. Move execution to the remote host

**Say:** This is the earlier diagram with execution moved to a remote host. On your machine, the LLM client talks to the Console server over MCP stdio. The server launches a worker relay on the SSH host, and the worker runs there.

The trusted package resolvers run on that host too, outside the worker sandbox. The sandbox policy can still apply to the worker and its subprocesses. The placement has changed, but the relationship between the parts is the same.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md)


## 34. Send code to the remote host; receive results

**Say:** With that separation, the Console server keeps the session records local, while the computation and sandbox live on the remote host. The worker uses the files available there, and sends results back.

So if the project and data already live on that machine, we can work with them there without first staging the dataset locally.

**Sources:** [SSH execution](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md)


## 35. Point Console at the remote workspace

**Say:** To configure an SSH host, the user names the host and the working directory where the worker should start. That directory and the runtime prerequisites need to exist on the remote machine.

Then we can layer sandbox permissions on top. Here, the workspace policy and the data directory rule apply on the remote host. The client still launches the Console server in the usual way.

**Author / capture:** analysis-host must be a configured OpenSSH destination; /srv/projects/analysis and data must already exist. SSH+Docker composition is not supported in this revision.

**Sources:** [ssh](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 36. Build the session's Docker image at launch

**Say:** Besides SSH hosts, users can configure a Docker container. Here we start from rocker/tidyverse and add uv, rig, and ir. We give Console the Dockerfile path, specify the project mount, and launch it with uvx inside the container.

The interaction between the native sandbox and Docker's networking controls isn't fully fleshed out. In this example, enforcement is delegated to Docker, and the launch uses its bridge network. That does not give us the destination restrictions from the earlier proxy example. If someone is interested in helping with that integration, I'd welcome the help.

**Author / target-day assumption:** This is the requested minimal setup for on-demand resolution. The inspected Console checkout at 6cd4cfd4f61ec5df723cc0e25b8f35a90ba8377e still disables managed package preparation for Docker, even when uv and ir are installed. Installing these tools alone does not enable that capability in the current implementation. This example assumes Docker preparation support by presentation day; it is not a validated current-release launch recipe. No image build or container session was run. Confirm this support before a live demo. The installer commands and r-lib-ir distribution name were checked against their official documentation.

**Sources:** [Rocker analysis images](https://rocker-project.org/images/versioned/rstudio.html) · [Install uv](https://docs.astral.sh/uv/getting-started/installation/) · [Install rig](https://rig.r-lib.org/install.html) · [Install ir](https://github.com/r-lib/ir#install) · [Current Docker behavior](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md)


## 37. The agent uses the same interface on every host

**Say:** Regardless of where the worker runs, the model gets the same interface. It sends a cell, receives results, and uses the same input, wait, and control operations.

The user configures the execution environment, and the model can keep working through the send tool.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 38. Launch or install Console

**Say:** The most common way to launch Console will be uvx mcp-console serve. uvx manages resolution and installation for you, and picks up updates as its cache refreshes. You don't have to manage a separate installation and remember to update it yourself.

If you want a persistent installation in your Python environment, use uv pip install. The base package gives you the executable, and the optional extras add the Python integrations. This command lists all the supported extras; pick the ones you need.

For R, the intended installation is install.packages("mcp.console"). It isn't on CRAN yet, but that's the plan. The current source installation is available from GitHub. The R package provides the interface and connects it to the core executable. It doesn't ship the Rust binary itself: when a download is needed, it uses reticulate's uv integration to resolve the binary from PyPI.

**Reference (not spoken):** uvx uses registry caching, so this is not a fresh lookup on every launch. An explicitly installed compatible tool or a version pin can retain an older version. uv pip install targets an existing Python environment. The current R source command is pak::pak("github::t-kalinowski/mcp-console/r"). console_tool() first checks PATH unless path or version is supplied; when resolution is needed it uses reticulate::uv_run_tool(). The inspected wrapper does not yet provide the richer S7 configuration surface mentioned in the rehearsal.

**Sources:** [uv tools](https://docs.astral.sh/uv/concepts/tools/) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)


## 39. Register Console with your CLI client

**Say:** To use Console with Codex or Claude, register that launch command with the client. When the client needs Console, it starts the server through uvx.

**Reference (not spoken):** Client-side deadlines remain separate from Console evaluation waits.

**Sources:** [uv tools](https://docs.astral.sh/uv/concepts/tools/) · [Codex MCP](https://developers.openai.com/codex/mcp/) · [Claude Code MCP](https://code.claude.com/docs/en/mcp)


## 40. ellmer

**Say:** Once the package is installed, create your ellmer chat object as usual and register console_tool as another tool. Then the model can use the same persistent session through that chat.

The R package handles the connection and the tool interface. The model's code still runs in the Console worker, separate from the R process running ellmer.

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md) · [R tool wrapper implementation](https://github.com/t-kalinowski/mcp-console/blob/main/r/R/console-tool.R)


## 41. chatlas

**Say:** The Python integrations are straightforward too. For chatlas, import mcp_console and register its chatlas tool with the chat.

The other supported clients have similar adapters. The application keeps control of the conversation, and Console provides the execution session.

**Reference (not spoken):** Registration and a direct call through the registered tool were checked with chatlas 0.23.0, without a model API call. In this version, register_tool() rebuilds the schema from Console's Python send annotations; it does not preserve the server-provided schema verbatim. The seven send arguments remain available. Use set_tools() when exact schema preservation is required.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [chatlas registration](https://posit-dev.github.io/chatlas/reference/Chat.html#chatlas.Chat.register_tool)


## 42. Keep session logs and readable transcripts

**Say:** Each recorded session gets a directory under .agents/console/sessions, relative to the Console server's working directory. Recording starts on the first send call.

The events.jsonl file records the tool calls and responses, including metadata attached by the client. For example, a client can attach a thread ID and other information that helps reconstruct the session.

The outputs directory preserves the fuller output that the model can inspect when a response is too large. The artifacts directory holds captured images. These are files on the server side, so other tools with access to that directory can use them. The server can save a plot there even when the worker has read-only permissions on the project.

Then we maintain human-readable transcripts. You can think of these as projections of the session record. The Markdown shows what was submitted and what came back. The Quarto file gives us the submitted code as a starting point for another analysis.

**Reference (not spoken):** The exact default root is .agents/console/sessions/, with a unique directory for each recorded session. The path is on the controller for remote workers. internal/events.jsonl records tool requests, assembled results, and lifecycle metadata; it is not a byte-for-byte capture of every MCP message or proof of delivery. The capture script records the complete transport separately in wire.jsonl. The current artifacts/ mechanism persists returned images; it is not a general worker-writable export directory or an automatic export API for arbitrary files. Raw per-cell output retention is bounded at 1 GiB. Other tools need access to the controller's recording workspace.

**Sources:** [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 43. Read the session as Markdown

**Say:** Here's the Markdown version. If the model sends some R code, we get a fenced code block, followed by the captured output in a text block.

It's a readable presentation of the session. A reader can follow the calls and results in order, and links point to captured images or fuller retained output.

**Sources:** [Session records](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 44. Turn the session into an editable starting point

**Say:** We also maintain a QMD file. The submitted R code becomes an R chunk; Python and SQL code become chunks in those languages. The earlier output isn't copied into this source document. The idea is to evaluate the code again when we render it.

The front matter includes an ir section with the managed defaults and declared package requirements recorded during the session. That gives us a starting point for preparing the environment as well as the analysis itself.

On this slide, I've copied the generated transcript into report.qmd, shortened the package list, and added a package snapshot date. We can edit that copy and run ir render report.qmd. With the data and connections in place, it's a starting point for a reproducible artifact from an interactive session the model had.

**Reference (not spoken):** The ir declarations include managed defaults and explicit requirements submitted in recorded calls, not every inferred package or a lockfile of successful resolutions. ir.exclude-newer is author-added. The QMD omits recorded outputs, stdin, polls, and controls; it can include source from rejected or failed calls. Rendering evaluates cells again outside the worker sandbox. SQL chunks need a configured DBI connection. Remote projections default to eval:false and need an appropriate execution environment for replay.

**Sources:** [ir Quarto integration](https://r-lib.github.io/ir/quarto.html) · [Architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 45. R, Python, and SQL, available for the work

**Say:** So those are the core ideas behind Console. Let the model choose the language. Users configure the execution host and the permissions for the work. It's all in service of giving the agent an interactive workbench, with full capabilities and a sandbox.

My hope is that we can share this execution system and keep solving the difficult parts in one place. I have some appendix material on the internals and testing if you're curious, but I'll stop here for now.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Sandbox configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 46. Appendix

**Say:** The main talk ends here. These slides are available for questions about package configuration, how the project evolved, and how its behavior is checked. The development history leads into the instructions given to coding agents and some examples from the test suite.

**Show:** Pause at this divider before entering the development material.


## 47. Example: use approved package repositories

**Say:** Making packages available doesn't mean we have to expose all of CRAN or PyPI. We can point the resolvers at a corporate mirror or a Posit Package Manager instance. Those repositories can contain an approved set of packages and versions.

Here the user sets the R repository and Python index in the environment used to launch Console. The organization manages the approved set, and the model can still request a package when the task needs it.

These are client launch settings. The config.yaml examples in the main talk control the worker sandbox. The resolver runs outside that sandbox, so exclusive access to approved sources also needs network policy on the resolver host. A preinstalled, administrator-managed environment is another option when dynamic additions aren't wanted.

**Reference (not spoken):** This is the common mcpServers client configuration shown as YAML for readability; use JSON for clients that require it. Replace the illustrative PPM URLs with the repository's setup URLs. PKG_CRAN_MIRROR configures the pak resolver used by ir; UV_DEFAULT_INDEX replaces uv's default PyPI index. Supply these in the Console server's launch environment, not sandbox.environment in .agents/console/config.yaml. On SSH, configure the trusted remote preparation environment.

Repository selection is not a complete package allowlist. Remove unapproved additional indexes and sources, account for Bioconductor and explicit R remote references, and restrict the resolver host's egress as needed. Preinstalled packages and reused caches also belong to the approved environment. ir tooling bootstrap can use its public PPM endpoint, and uvx needs the Console distribution and any resolver tooling; provision these through the approved environment before restricting access. Current Console config.yaml has no package-allowlist field. A selected RETICULATE_PYTHON disables managed Python additions; current Docker targets use preinstalled environments for all languages.

**Author / validation:** Repository selection was checked with pak and uv. The example does not represent a connection to a live corporate PPM instance or an end-to-end network-enforcement test.

**Sources:** [Resolver configuration](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md#server-owned-uv-configuration) · [Worker environment scope](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [pak configuration](https://pak.r-lib.org/reference/pak-config.html) · [uv package indexes](https://docs.astral.sh/uv/concepts/indexes/) · [PPM curated CRAN](https://docs.posit.co/rspm/admin/r-packaging/curated-cran.html) · [PPM curated PyPI](https://docs.posit.co/rspm/admin/python-packaging/curated-pypi.html)


## 48. Proposed: declare requirements in config.yaml

**Say:** The model can declare session dependencies through send, as we saw in the main talk. On the right is a proposed way for the user to supply the same requirements in config.yaml.

It uses YAML sequences of package names or version specifications, matching the requirements supplied through send. This configuration form is not implemented yet.

**Reference (not spoken):** The proposed requirements field would supply session dependencies, not restrict which other packages can be requested. The inspected config schema accepts only extends, sandbox, and target and rejects unknown fields. Do not use this YAML with the current implementation.

**Author / capture:** This is an illustrative preparation request; no response is presented as a capture. scikit-learn 1.9.1 is the version in the existing Python reference capture. The earlier data.table==1.17.8 rehearsal failed on the installed R toolchains and remains documented in VALIDATION.md. That older request is retained in the reference files, not represented as a successful run here. Requirements are available only on targets that support managed preparation.

**Sources:** [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 49. Follow a package-resolution request

**Say:** The request comes from the runtime inside the worker, through the relay to the server. The server validates it and uses a trusted resolver outside the sandbox to prepare the library. The result is a library path, which the worker adds to its live library search path. It acknowledges activation before continuing the package load. The server commits the retained environment only for a matching activation from the current worker generation.

These are private worker-protocol messages, not MCP tool calls the model has to make. The field names match the documented protocol; /cache/r/library is an illustrative path. Python follows the analogous resolve_python exchange and activates a prepared interpreter environment.

Installation and build code run with the preparation account’s permissions, so requirements and resolver configuration must be trusted. Caches can persist. The worker’s filesystem and network policy continues to apply. On SSH, preparation runs on the remote execution host.

**Sources:** [Worker protocol](https://github.com/t-kalinowski/mcp-console/blob/main/docs/WORKER_PROTOCOL.md#nested-managed-r-resolution) · [Requirements and trust](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 50. Capabilities arriving on main

**Say:** This is a little under eight weeks of development. Each dot is a PR merged directly into main. The vertical axis is logarithmic so that small and large changes are both visible. Python cells arrived on August 3 and SQL on August 4. On-demand R and Python packages landed on August 24, sandboxed Linux on September 9, and Docker targets on September 12.

**Show:** Follow the dates across the top, then point out the range of PR sizes underneath. A feature can span several PRs; these annotations mark specific capability merges rather than the whole development effort. Linux without the sandbox preceded the sandboxed Linux milestone.

**Data:** GitHub snapshot at September 18, 19:08 UTC. Of 298 merged PRs, 279 targeted main; 19 targeting intermediate branches are excluded. The dot heights count additions plus deletions, including moves and generated snapshots. The chart is not a measure of effort or complexity.

**Sources:** [Python #24](https://github.com/t-kalinowski/mcp-console/pull/24) · [SQL #36](https://github.com/t-kalinowski/mcp-console/pull/36) · [R packages #123](https://github.com/t-kalinowski/mcp-console/pull/123) · [Python packages #124](https://github.com/t-kalinowski/mcp-console/pull/124) · [Sandboxed Linux #262](https://github.com/t-kalinowski/mcp-console/pull/262) · [Docker targets #302](https://github.com/t-kalinowski/mcp-console/pull/302)


## 51. How much is in the repository?

**Say:** This counts the files actually present in the repository at each point in time. Deleted lines come out of the total. It starts with a 21-line initial commit and reaches about 143,000 lines across 1,086 tracked text files. This includes comments, blank lines, tests, transcripts, documentation, and build files.

**Show:** Point out that the total can fall as code and tests are simplified. This is a count of repository contents, not cumulative PR activity. Adding PR sizes together would double-count work that is later changed or removed.

**Data:** Every first-parent commit through main commit 657a5981, September 18 at 19:43 UTC. Each snapshot is counted from the full Git tree. Binary and untracked files are excluded. UTC commit times determine the horizontal position.

**Sources:** [Pinned main snapshot](https://github.com/t-kalinowski/mcp-console/tree/657a5981983768967deed83c070973848ec800fb) · [Analysis definitions and data](examples/repository-development/README.md)


## 52. What grew alongside the core code?

**Say:** The blue area is core code. The darker orange is test code, harnesses, and other fixtures. The lighter orange is YAML test transcripts: the requests and expected responses that a reviewer can read. Documentation and examples are yellow, and build tooling is gray.

**Show:** Compare the orange areas with the blue one. Much of the repository records how the system should behave and how to exercise it. The testing slides that follow show what those transcripts look like.

**Data:** These are file categories, not line-by-line semantic classifications: core files can contain inline tests and documentation comments. Transcript detection uses .yaml or .yml under tests/, r/tests/, or python/tests/, regardless of historical subdirectory. CI YAML remains tooling. The #197 reorganization has 17,224 transcript lines on both sides, so moving transcripts does not create artificial growth in this category.

**Sources:** [Analysis definitions and checks](examples/repository-development/README.md) · [Test reorganization #197](https://github.com/t-kalinowski/mcp-console/pull/197)


## 53. How the proportions changed

**Say:** Here the total height is always 100 percent. Early on, documentation occupies most of a small repository. As implementation and tests accumulate, that mix changes. At the latest snapshot, test code and fixtures account for about 42 percent, and YAML transcripts another 24 percent. Together they are about 65 percent of the tracked lines.

**Show:** Use the preceding slide to keep absolute size in mind. A category can shrink as a proportion while still growing in lines. The first snapshot contains only 21 lines, so the earliest shares are particularly sensitive to small changes.

**Data:** Each category's line count is divided by the total at the same commit. All 307 snapshots sum to 100 percent before rounding. The colors and classification match the absolute-size chart. Shares describe repository contents, not developer time, test coverage, or software quality.

**Sources:** [Analysis definitions and data](examples/repository-development/README.md)


## 54. Why some PRs look so large

**Say:** The largest diffs deserve a closer look. The three largest PRs here changed no core-code files under this classification. They reorganized tests or simplified test support. The largest changed about 37,000 lines but added only about 1,700 net lines. File moves and rewritten snapshots can create substantial review volume without adding the same amount of repository content.

**Show:** Compare the top bar with the Docker feature farther down. The categories help explain what a PR contains; line count alone cannot tell us how difficult it was or how much new capability it introduced.

**Data:** The same GitHub snapshot as the timeline. Per-file additions and deletions reconcile with every PR total. YAML transcript files use the suffix-based classification in the repository charts. Labels shorten PR titles for readability.

**Sources:** [Test reorganization #197](https://github.com/t-kalinowski/mcp-console/pull/197) · [Test contracts #258](https://github.com/t-kalinowski/mcp-console/pull/258) · [Transcript support #202](https://github.com/t-kalinowski/mcp-console/pull/202) · [Sandbox supervision #266](https://github.com/t-kalinowski/mcp-console/pull/266) · [Docker targets #302](https://github.com/t-kalinowski/mcp-console/pull/302) · [CLI tests #205](https://github.com/t-kalinowski/mcp-console/pull/205)


## 55. AGENTS.md gives the model project context

**Say:** AGENTS.md is a checked-in Markdown file that gives a coding agent context about the repository. In this project it provides a map to the architecture, the public contracts, and the development guide, along with rules for making changes. The detailed behavior lives in source, protocol documents, and public tests.

The instructions ask for coherent PRs, readable code, tests through public interfaces, and deliberate review of generated snapshots. They also explain which process owns which responsibility, so a change does not accidentally move behavior across a boundary.

**Show:** Read these as three kinds of guidance: where to look, what to preserve, and how to make a change. The file supplies instructions; the checks and review provide evidence that a particular change follows them.

**Sources:** [AGENTS.md at the analysis snapshot](https://github.com/t-kalinowski/mcp-console/blob/657a5981983768967deed83c070973848ec800fb/AGENTS.md) · [Development guide](https://github.com/t-kalinowski/mcp-console/blob/657a5981983768967deed83c070973848ec800fb/docs/DEVELOPMENT.md)


## 56. The development loop starts with behavior

**Say:** For a behavior change, the project instructions start with a public acceptance or regression test and ask the agent to confirm that it fails. Then comes the implementation, a focused rerun, and review of any changed snapshots. After that, formatting and the full check suite precede the PR, and passing CI and approval from the configured reviewer are required on the current revision before merging.

For an internal refactor, the existing public suite is the contract; the instructions do not ask for a new test of a private helper. Tests should use observable checkpoints instead of timing guesses. Generated transcripts should preserve the behavior a user sees, with only incidental noise normalized.

**Show:** This describes the written workflow at the snapshot date, not an audit that every historical PR followed it. The following slides show the kinds of tests and review artifacts those instructions refer to.

**Sources:** [Working rules in AGENTS.md](https://github.com/t-kalinowski/mcp-console/blob/657a5981983768967deed83c070973848ec800fb/AGENTS.md) · [Validation ladder](https://github.com/t-kalinowski/mcp-console/blob/657a5981983768967deed83c070973848ec800fb/docs/DEVELOPMENT.md)


## 57. Rust implementation. Python integration tests.

**Say:** The main integration suite is Python even though the application is Rust. It drives the built executable and observes the real process boundary. Small unit tests can still own pure parsing or validation policy; the claim is not that absolutely no Rust tests exist.

**Show:** Use two simple implementation/test boxes. Lead with why this matters: the test language can stay independent of implementation refactors while validating the product contract users and clients actually see.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md)


## 58. Test the boundaries you intend to preserve

**Say:** The tests mirror architectural boundaries: client_server, server_relay, relay_worker, and cli. Public behavior belongs at the outermost boundary that can usefully observe it. Private-boundary cases cover their own protocol seams rather than replicating every public message at every layer.

**Show:** Reuse the process topology with test-boundary names on the arrows. This ties the development method to the earlier architecture rather than presenting a directory tree with no explanation.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 59. YAML is what the reviewer reads

**Say:** The wire protocols are JSON-based, but the reviewable test transcripts are YAML. This is an actual checked-in snapshot excerpt: the test executes R, asserts that CPU detection returns a valid result, and prints a stable message. Humans can review the code and result without reading escaped JSON strings or snapshotting a machine-specific core count. YAML is the human review surface, not the production transport.

**Show:** Display the request and result from `tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml` side by side. The initial shared-handshake document is omitted, but the displayed request and result content come from the fetched source. This fixture was not rerun in the slide-build environment; do not present it as a new test execution.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Checked-in CPU detection snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml)


## 60. Normalize noise, not behavior

**Say:** Temporary paths, process identities, and similar unstable details should not obscure behavioral review. Normalize explicitly and narrowly. Preserve the fields, output, ordering, and failure distinctions the contract is meant to protect. The actual project normalizers and snapshot metadata are more specific than this schematic example.

**Show:** Use before/after panels with only incidental details changed. Call out that normalization is not a license to delete inconvenient evidence from a test.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 61. Synchronize; do not sleep and hope

**Say:** Concurrency and liveness tests need causal synchronization. Fixtures use gates and checkpoints so the test knows when the relevant state has actually been reached. Arbitrary sleeps are not proof that output was drained, an interrupt was delivered, or an owned resource was retired.

**Show:** Show one deterministic sequence and connect it to the timing and shutdown contracts from the talk. This is a development-practice slide, not an implementation recipe for every fixture.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 62. Portable behavior; real capability checks

**Say:** Reuse portable cases across execution modes and centralize capability discovery. A skipped target fixture is not target validation. Deterministic peers can establish orchestration behavior, but they cannot establish real container or microVM cleanup. Keep real-target evidence distinct from simulated protocol coverage.

**Show:** Use the two testing levels rather than an all-green platform matrix. Include lifecycle and security assertions where a textual snapshot alone cannot represent the guarantee.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 63. Snapshots are generated evidence

**Say:** Generate transcripts from running tests, then review the resulting diff. Do not hand-edit the expectation to make a test pass. The value of readable YAML is that review can focus on the actual changed behavior, while assertions still enforce facts that a snapshot cannot show.

**Show:** Show the update command and a diff review, not a large wall of green tests. The selector is schematic; replace BOUNDARY/SUITE::CASE with a real selected fixture for a live development demonstration.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 64. Test the installed product

**Say:** The delivered product includes the executable, companion binaries, Python interfaces, the R wrapper, and launch/lifetime behavior. Running a development binary alone does not establish that the installed bundle or each adapter works. Integration examples and packaging checks should be part of the release evidence, with actual target validation reported separately.

**Show:** Finish the addendum by connecting the install story to the test strategy. Avoid claiming every proposed integration test already exists: distinguish observed project coverage from the release checklist in the companion author notes.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Release and installed bundle](https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)
