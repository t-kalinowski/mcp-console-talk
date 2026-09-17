# MCP Console — speaker notes

Generated from the native `.notes` blocks in `deck.qmd`. Edit that file, not this reading copy.


## 01. MCP Console

**Say:** This audience already knows how to give a model an evaluator. Skip the history of code execution tools. MCP Console is a place for models to work interactively: inspect a result, change direction, keep state, and continue. The subject of this talk is the model-facing interface, not a new chat UI.

**Show:** Open directly on the product name and the two-line thesis. No definition of MCP, shell-versus-notebook comparison, or installation instructions. Advance into the actual tool contract after one brief framing slide.

**Sources:** [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 02. Small surface. Deep runtime.

**Say:** The goal is token efficiency without making the environment artificially limited. Routine calls stay small. Package loading, object interchange, and database selection live naturally in the runtime; requirements and lifecycle controls are available when the model needs to be deliberate. Do not claim a measured speedup or superiority across model families.

**Show:** Use the three-box diagram. The same tool reaches a much larger runtime surface. This is the organizing idea for the sequence: introduce a field only when a concrete interaction needs it.

**Sources:** [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 03. Start with a cell

**Say:** The final expression is fit, so R prints its normal lm summary. The agent receives useful output immediately, not prose that stands in for output. This is a real, persistent R workspace; ordinary cells do not require another object-management API.

**Show:** Show the exact submitted R code beside the printed lm object. The code and renderer both read the same cell definition. The fit is reused on the next slide.

**Author / capture:** Default preview evaluates this cell in native R through knitr, not in MCP Console. With -P output_source:mcp, the panel reads the literal captured Console text. No simulated numerical output is committed.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 04. The next call uses the same fit

**Say:** Read the coefficients and then the first three predictions from the existing fit. Persistence is demonstrated by the relationship between these calls, not by commentary placed in an output block.

**Show:** Keep coefficients and predictions in the result panel and all interpretation beneath it. Native Quarto re-renders these values from the preceding model; capture mode displays actual tool results.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 05. Plots are results, not another tool

**Say:** This is the base-R plot produced by this exact plot() call. Plotting is part of the runtime contract, not another tool. All drawing for a managed plot belongs in the same cell.

**Show:** Let R render this figure during quarto preview. Do not substitute a Matplotlib graphic. Capture mode uses the PNG returned by Console instead.

**Author / capture:** Default uses the displayed base-R cell through knitr; plot capture mode reads captures/r-plot-01.png. Neither a stock image nor the previous illustrative SVG is used.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 06. A wait timeout is not an execution deadline

**Say:** A response can end while the cell remains active. Here the R code repeatedly rewrites one progress line, and timeout_ms returns control before the loop completes. This is an evaluation wait budget, not a deadline that kills the computation.

**Show:** Read both the compact progress line and the exact running notice. The panel reads the captured response; call boundaries remain timing-dependent.

**Author / capture:** Warm up the session before capturing this example. Do not promise exactly 15% at 450 ms. The local capture script retains actual responses rather than asserting fixed percentages.

**Sources:** [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 07. Polling advances the same computation

**Say:** These are separate responses to later polls, not a transcript dumped into one response. Each poll contains newly collected output. Carriage-return redraws within one response interval collapse to its current line; a later interval can return the next current line.

**Show:** Point to the two poll calls and their corresponding results. The last response has real output and no invented [done] appended. Emphasize that empty send() is also a poll.

**Author / capture:** Both rendering modes read the two literal captured responses. The wire exchange records the 600 ms poll followed by the 5000 ms poll. Exact progress fractions are not a public API guarantee.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 08. Progress redraws do not become a wall of text

**Say:** A carriage return replaces the current progress frame rather than adding another visible line. This deterministic example is separate from timing-sensitive polling: all three writes are in one short cell. Raw logs preserve the original bytes.

**Show:** Show the escaped raw characters on the left and the literal compacted result on the right. Both boxes identify their representation explicitly; the explanation stays outside them.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 09. Interrupt without replacing the runtime

**Say:** Add control. Interrupt requests the runtime or active resolver to stop its current work without deliberately replacing the worker. It is cooperative: code can delay or catch interruption. Keeping this distinct from restart makes state loss explicit rather than an accidental side effect of a timeout.

**Show:** Highlight only control in the signature. The single-line call is the main visual, followed by the two-line state-preservation message. Do not imply every interrupt must succeed immediately.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 10. Restart resets objects, not prepared requirements

**Say:** The other control value is restart. This replaces the worker and discards R objects, Python objects, the in-memory DuckDB catalog, debugger state, and unread input. The server retains successfully prepared requirements and recordings. This is a deliberate fresh runtime, not continuation disguised as recovery.

**Show:** Use the before/after worker diagram. The server box stays in place; the worker changes. Avoid suggesting that the interrupted or failed cell is replayed automatically.

**Sources:** [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 11. Errors are outcomes, not transactions

**Say:** An ordinary R error or Python exception does not normally destroy the worker. Also, cells are not transactions: assignments and other effects before the error can remain. That is a useful, explicit contract for an agent deciding whether to inspect, repair, retry, or restart.

**Show:** Show a failed cell followed by a successful inspection of the earlier assignment. No new argument appears. Keep the two responses visibly distinct from one response block.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 12. Interactive input is a separate channel

**Say:** The running cell asks for a line. Console exposes the input request, and the next call supplies the newline explicitly. The following result is the value returned by the same suspended evaluation.

**Show:** Keep the two Console responses in separate result panels. Both rendering modes read the complete real responses to these exact calls.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 13. The debugger uses the same field

**Say:** Stop inside inspect_mean, inspect x in that function frame, then continue to the mean. The same stdin field used for readline handles the debugger. A prompt is not new top-level code, and the session is not idle while it is waiting for debugger input.

**Show:** Use the multiline function at the left; browser() gets its own line. The two input responses include the returned R values and any new debugger prompt or waiting notice.

**Author / capture:** The panels read the complete captures/browser-start.txt, captures/browser-x.txt, and captures/browser-continue.txt responses. Do not run browser() in the knitr rendering process.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [send](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 14. Keep model context bounded

**Say:** The output is deliberately larger than the tool-result budget. Console keeps a bounded beginning and recent tail and reports omission and retention details. The beginning and tail are cropped to three lines each; the omission notice is shown in full.

**Show:** Show the actual kind of lines being printed, not useful opening output or latest diagnostic as if those words came from the runtime. The middle notice is copied unchanged from this capture, including the actual byte counts and raw-log path.

**Author / capture:** All panels are literal slices of captures/flood.txt. The full result, wire exchange, and raw log remain in captures. No identifiers or paths were normalized; captures/excerpts/provenance.json records the selected line ranges.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 15. Retain more than you put in context

**Say:** Console captures console output and raw stdout/stderr, including native and subprocess output. Longer emitted cell text is retained separately in per-cell files up to a 1 GiB cap; previews continue even if retention is partial. Retrieval requires a filesystem tool that can access the controller recording directory. The records are not unlimited or a lossless event chronology across independent streams.

**Show:** Split one output stream into two destinations: model context and a log file. Put the retention-limit caveat in speech rather than shrinking the diagram with implementation numbers. For remote execution, the log path is on the controller, not necessarily on the worker’s filesystem.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 16. Package loading is a runtime capability

**Say:** Only now introduce package resolution, after wait timeouts and the interactive contract. The simple model path is ordinary library() or pkg::fun() use. When execution reaches a supported missing-package operation, Console prepares the package and resumes that operation in the live worker. Quoted or unreachable code does not trigger a source-scanning installer.

**Show:** Keep the signature unchanged and show ordinary R. This is the first example of pushing capability into the runtime rather than expanding the tool schema. Resolver work may outlast the tool wait, using the timeout and polling behavior already explained.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 17. Pin what matters; leave the rest unpinned

**Say:** This is a reason to use explicit requirements even when missing packages resolve automatically. Pin the data.table version being tested while allowing the resolver to choose dtplyr and compatible dependencies. Preparation makes packages available; the code still attaches them.

**Show:** Highlight the == version spec and the unpinned name in the same requirements.r array. ir supports == pins; do not replace this with an unsupported ad hoc notation.

**Author / capture:** Run this in a fresh session before data.table is loaded. A compatible environment addition is not a promise to replace an already loaded R namespace with another version. Local validation on 2026-09-17 failed: data.table 1.17.8 did not compile against R 4.6.1 (undeclared SETLENGTH/ATTRIB APIs). A separate R 4.5 attempt also failed during package installation with “worker failed to start.” The pin is retained as requested; captures/requirements and captures/requirements-r45 preserve the failed wire exchanges. Rehearse this example with a compatible, prepared runtime before presenting it live.

**Sources:** [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [ir](https://github.com/r-lib/ir/blob/main/README.md)


## 18. Prepare now; keep working in the same session

**Say:** Requirements can also be prepared without submitting a cell. Supported compatible additions keep the existing worker state, and accepted requirements remain retained for later calls and restart. This is additive environment management, not arbitrary replacement or removal of already loaded packages.

**Show:** Show a requirements-only call followed by inspection of the same fit. The new field has gained another use without another tool. Mention that some incompatible or failed activations require an explicit restart; do not imply arbitrary upgrades can preserve every live object.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 19. Use the resolver, not another package manager

**Say:** Console coordinates the environment but delegates R dependency work to ir. This matters for reuse and for keeping package preparation separate from the evaluator. We will return to concrete versus managed environments and the sandbox boundary after the language sequence.

**Show:** Use one large dependency arrow, not an installation walkthrough. It is a fast acknowledgement of the underlying tooling, while the signature stays the same.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 20. Use Python’s ML libraries on the same data

**Say:** A reason to switch languages is access to another ecosystem. Here Python reads the existing R frame and uses scikit-learn to evaluate a nonlinear model. This is not a claim that Python plots better, or that this small demonstration selects the best model.

**Show:** The new python argument is the only interface expansion. The meaningful difference is the library being used: RandomForestRegressor and cross_val_score. Show the literal result on the next slide.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md)


## 21. The Python cell returns a numerical result

**Say:** The result is the five-fold cross-validation mean absolute error for the displayed code. It is an example computation, not a benchmark for Console or a claim about model quality. The data remain available in R and Python.

**Show:** Show the numerical print line, not a prose description of the score. The reference was computed locally in Python; switching the render parameter to mcp uses the real Console result.

**Author / capture:** Reference provenance and installed Python library versions are in examples/python-reference-provenance.json. Recompute or capture when changing code, data, or library versions.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 22. Python plotting has the same return contract

**Say:** Plotting works here too, but plotting is not the reason we switched to Python. An open pyplot figure is returned as image content. This complements R graphics rather than ranking the two plotting systems.

**Show:** Use the actual Matplotlib result from the displayed code. The local reference and the captured image use the same data and call definition.

**Sources:** [runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 23. The controls come with it

**Say:** These are independent example call shapes, not a script to execute consecutively. Python inherits the shared controls: bounded waits, polling, interruption, interactive input, supported debugger interaction, and explicit restart. There is no second Python-specific tool family to learn.

**Show:** Use a compact list of familiar calls rather than another control tutorial. Mark the panel as independent examples. The absence of a new signature field is the point.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 24. Missing imports resolve in place

**Say:** Managed Python resolves a missing import when normal import machinery cannot satisfy it. A curated mapping handles known import/distribution name differences, with conservative inference otherwise. It does not scan the cell in advance or replay the cell. Explicitly selected Python environments use their preinstalled packages instead of this managed path.

**Show:** Show an ordinary import and useful work. Do not promise that every arbitrary import name maps to the right distribution; that is what the explicit path on the next slide addresses.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 25. Versions and extras fit the existing field

**Say:** Requirements now carries Python distribution metadata: versions, extras, and markers within the accepted named-registry format. It can also correct an import-name inference. The model that understands the environment more precisely can use that precision through the same interface.

**Show:** Highlight the python entry inside requirements, not a new top-level field. This visually reinforces the difference between adding a capability to an existing contract and adding another tool.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 26. Both languages share one worker process

**Say:** In the combined runtime, R hosts Python through reticulate and DuckDB is in the same worker process. R globals are available through r in Python; Python globals through py in R. Conversions follow reticulate’s rules. Do not claim arbitrary zero-copy conversion or that the host R chat session is this worker.

**Show:** Use a single visible process boundary. The R/Python bridge is inside it. This is an overview of the current combined-runtime topology, not a claim that the planned Python-only mode is already this same implementation.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 27. Switch languages; reuse the objects

**Say:** Now make the object bridge concrete. A Python cell works on the R data frame and stores a Python result; the next R cell reads that Python object through py. The session stays live throughout. File export/import is not part of the normal handoff, though conversions can still allocate.

**Show:** Show the two calls stacked in one panel. Reuse variable names from the preceding slides so the audience can follow state without rereading a new scenario.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md)


## 28. And SQL

**Say:** Add sql, the last code-language field. SQL has its own cell input and a persistent managed DuckDB backend by default. The d relation here is the live R data frame already created; an unqualified relation name can discover it. A DuckDB table or view of the same name takes precedence.

**Show:** Reveal sql in the signature. The rest of the call/result composition remains unchanged. Again, r, python, and sql are alternatives per call, not three simultaneous code payloads.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 29. SQL can operate on live R data

**Say:** An R model result becomes a column, and SQL immediately summarizes it through managed DuckDB relation discovery. This is the point of one interactive workspace: each language builds on live work already done. The default managed backend discovers R frames; Python visibility is connection-dependent and needs the explicit setup shown next.

**Show:** Show a one-line R update followed by the SQL query. Keep the claim precise: this is live R relation discovery on the managed backend, not universal implicit visibility into every object in every runtime.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 30. Python relations use their connection

**Say:** For Python-side relations, select a Python DuckDB connection and register the frame there. Later SQL cells use that exact connection. This avoids the inaccurate implication that managed R-backed DuckDB automatically sees Python globals. Another route is to bind a Python frame to an R name before querying it through the managed backend.

**Show:** Keep registration visible: it is useful explicit runtime capability, not a new Console tool. The example uses the existing R frame via Python only to preserve the narrative; the frame could just as well have been created in Python.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 31. Select the database from either language

**Say:** DuckDB is the default, not a limitation of the SQL cell interface. R can select a DBI connection and Python can select a DB-API connection. The connection remains owned by its runtime. SQL semantics, transactions, and supported statements belong to the selected driver; these examples are alternatives, not shared cross-runtime connection objects.

**Show:** Use parallel code panels and one shared takeaway. The function console_sql_connection() belongs to runtime code, demonstrating how much functionality can be exposed without changing send.

**Sources:** [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 32. And DuckDB extensions

**Say:** Dependency preparation also covers DuckDB extensions. The explicit example is supported for the managed backend; preparation uses DuckDB’s install path outside the worker sandbox, while loading happens inside the runtime. For presentation day, include the intended on-demand extension path as well, without inventing a new top-level field.

**Show:** Show one extension requirement beside a query. Reset to the managed DuckDB connection before actually running this example after custom-connection slides. The automatic on-demand claim is a target-day assumption and must be verified before a live capture.

**Author check before presenting:** Target-day assumption: automatic DuckDB extension discovery is not documented as implemented; current SQL does not trigger package discovery. Explicit requirements.duckdb is implemented.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 33. That is the surface

**Say:** Now reveal the complete top-level surface. All fields are optional, with compatibility rules on combinations; at most one code-language field is supplied. The fields are not seven separate tools. Much of the capability just demonstrated lives in native runtime operations, so the schema does not need a method for every package, plot, connection, or debugger action.

**Show:** Drop the incremental signature rail and replace it with a single large schematic signature. Be explicit that this is named-argument shorthand for the MCP object schema, not a literal positional API declaration. Let the size contrast with the capabilities already demonstrated.

**Sources:** [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Send operation contract](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md)


## 34. Capture the model-facing interaction

**Say:** Record one real session in the client you actually use. Prefer the Codex TUI for legible expanded tool arguments; use the desktop client if it better exposes returned plots in the capture. The audience does not need a tour of the surrounding application. Crop tightly around tool requests and results and annotate the particular contract being exercised. Installation appears later.

**Show:** This is a designed recording slot, not a fabricated Codex screenshot. The package includes the synthetic data, a capture prompt, a fallback sequence, and a video replacement location. Once a real recording exists, replace this body with the video or a short sequence of authentic cropped stills. Do not narrate synthetic draft examples as recorded model behavior.

**Sources:** [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Official Codex MCP documentation](https://developers.openai.com/codex/mcp/)


## 35. It scales with what the model can use

**Say:** Summarize the design claim without a benchmark claim. Models that only write ordinary code benefit from native behavior and automatic resolution. Models that understand requirements, runtime state, and controls can be more deliberate. Both use the same interface. The benefit should be demonstrated in the interaction, not asserted as universal better results for every model.

**Show:** Use the converging three-path diagram. This closes the capability crescendo before switching from what the model can do to what the user configures and what the implementation owns.

**Sources:** [Requirements and environments](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Vision / intended design](https://github.com/t-kalinowski/mcp-console/blob/main/design-sketches/VISION.md)


## 36. An interaction journal, and the actual output

**Say:** The journal records calls and assembled results; each cell can also have a raw emitted-text log. The right-hand excerpt is the same printed fit seen earlier. Markdown and Quarto are projections with different purposes, not alternative names for the raw log.

**Show:** Show the concrete directory names and actual R text. Do not invent an internal JSONL schema merely to fill the slide. The collector copies the real internal/events.jsonl for inspection and later exact excerpts.

**Author / capture:** The right panel reads the actual fit cell raw log, copied under captures/session-records/outputs. The excerpt provenance names the source file. The complete journal and both transcripts remain in captures/session-records; no paths or identifiers were normalized.

**Sources:** [architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 37. The Markdown contains code and results

**Say:** This is the kind of content to inspect in transcript.md: the submitted R cell followed by literal returned text. Real transcripts additionally retain call options, errors, input interactions, and image references. Polls remain separate calls rather than being silently regrouped as one evaluation.

**Show:** Use a concrete excerpt from the same analysis. Read the actual call heading, R source fence, result heading, and returned coefficients.

**Author / capture:** This is a contiguous, literal excerpt of captures/session-records/transcript.md: one complete coefficient call and its result. The initial session metadata and other calls are outside the excerpt. No identifiers, values, or paths were normalized; line ranges are in captures/excerpts/provenance.json.

**Sources:** [architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 38. The Quarto source is editable and executable

**Say:** The source projection contains executable chunks rather than escaped code in a log. Rendering runs those cells again in a new Quarto environment. It does not replay stdin, interrupts, restarts, or prior outputs, and the required data and SQL connection still need to exist.

**Show:** Show literal Quarto chunk delimiters. The left panel contains the complete generated front matter. The right panel is the unchanged model cell; the preceding warmup cell and later cells are outside the excerpt.

**Author / capture:** These are literal source slices from the captured document. The long root.dir path is shortened to <project> only in this slide; the original is preserved in captures/excerpts/quarto-header.txt. Dependencies reflect the generated front matter of this build and do not include every inferred package. Local render occurs outside the Console worker sandbox. Remote projections default eval:false.

**Sources:** [architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 39. The user configures the boundary

**Say:** The agent-facing send interface is not a policy editor. The user chooses the execution conditions in a project YAML file. Console reads it from the launch directory, applies explicit command-line overrides, and captures the result before workers start.

**Show:** Start with a short complete file and name the categories we will expand. Do not show proposed top-level profile or environment keys as implemented schema.

**Sources:** [config](https://github.com/t-kalinowski/mcp-console/blob/main/docs/CONFIGURATION.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [settings](https://github.com/t-kalinowski/mcp-console/blob/main/src/settings.rs)


## 40. The sandbox runner is a separate executable

**Say:** This is an external runner, not sandbox code duplicated inside each language adapter. Console ships a separately compiled, pinned executable based on the Codex sandbox code. The launcher verifies its bundled identity and gives it immutable launch settings; it does not download sandbox code when a cell runs.

**Show:** Show the physical executable boundary and the policy path into it. Keep the resolver outside the worker sandbox. The native runner is distinct from Docker Sandbox’s compute provider.

**Author / capture:** Inspected runner manifest: t-kalinowski/codex, rust-v0.154.0, commit 2d0ad797210de821c07d1f18e4f1ffdcf06589cb, protocol 2. Check the manifest on the local presentation revision.

**Sources:** [runner](https://github.com/t-kalinowski/mcp-console/blob/main/sandbox-runner.json) · [architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 41. Control the workload’s environment

**Say:** inherit_environment controls ordinary workload variables. It does not erase Console’s selected R/Python runtime settings or configure the trusted dependency-preparation process. Values that look numeric must still be strings.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** This limits inherited variables, not filesystem access to secrets. Local resolver settings come from the trusted server launch environment; SSH runtime exceptions are documented separately.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 42. Choose a concrete runtime before launch

**Say:** A concrete installation and managed package preparation are different choices. Select the local runtime in trusted launch configuration. An explicitly selected Python environment disables managed Python additions; absence of a resolver bootstrap gives a bare runtime. This is not a new YAML environments schema.

**Show:** Show actual launch variables beside ordinary workload YAML. The paths are placeholders to replace locally, not portable R distribution paths.

**Author / capture:** Python-without-R remains an intended presentation-day capability. Do not invent a languages or environments YAML key: the inspected Project struct accepts extends, sandbox, target only. A local agent can add a real language selector example once implemented.

**Sources:** [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 43. Start from the read-only baseline

**Say:** Read-only means ordinary host writes are restricted, not that the worker cannot read the machine or write its private temporary files. Native sandboxing is the default on supported hosts. This is a process boundary around evaluated code and descendants.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 44. Permit project edits, protect metadata by default

**Say:** The workspace profile grants project edits while protecting common repository and agent metadata by default. The fixed launch workspace is the permission root; changing the R working directory does not move it. Explicit native rules can override defaults.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 45. Grant one persistent output directory

**Say:** Grant a specific directory rather than the entire project when the task only needs to save results. These are literal native path objects. Pre-create the directory for a portable Linux demonstration; Console does not widen the grant to its parent.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Create output before launching on Linux. Existing file-root and missing-path behavior differs by backend; do not promise identical behavior for every path kind.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 46. Read data, write results, hide secrets

**Say:** Now distinguish a read grant from a denial. Making data read-only prevents accidental modification; deny is the separate choice that prevents reading that path. Native specificity, symlink handling, and platform enforcement still matter.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Use pre-existing fixture paths. Native specificity is not array order. Linux has documented limits for nested deny/read reopenings; this simple example does not establish arbitrary cross-platform ACL equivalence.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 47. Keep scratch private, not shared

**Say:** These are real native workspace options. Console defaults both to true for the workspace profile. Private temporary storage is still available for plots, caches, and ordinary runtime work, then retired with the owned sandbox.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Do not confuse exclude_tmpdir_env_var with removing TMPDIR entirely. Console selects its private scratch location. Explicit null workspace_options chooses native defaults and has different behavior.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 48. Enable direct networking explicitly

**Say:** network: enabled is the broad direct-network choice. It does not grant filesystem writes. The following slide uses a managed proxy to make a narrower network choice instead.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 49. Allow selected destinations through a proxy

**Say:** This complete proxy configuration shows both the allowlist and the surrounding controls. The runner owns proxy routing, host normalization, and enforcement. A proxy object must include the required scalar fields; Console does not materialize omitted defaults for it.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Example domains are placeholders, not actual services. All seven required scalar proxy fields are present. mode: full does not erase the domain allowlist. Review PROTOCOL.md for mode, upstream proxy, UDP and local-binding semantics.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 50. Permit a local listener when the task needs one

**Say:** An interactive local server can need a binding exception. The policy exposes that choice separately from the domain allowlist. Do not conflate permission to bind with permission to publish a remote service, create a tunnel, or expose every Unix socket.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Validate the exact native behavior with the application used for the demo. This slide does not promise a Shiny viewer or automatic port forwarding. Keep all required proxy fields when changing a single flag.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 51. Override one launch; do not mutate live policy

**Say:** The file is the starting point. Repeated -c overrides merge in command-line order, and the final configuration is validated. The worker cannot change accepted launch policy by editing a file or printing configuration-shaped text. A new server session is required to read changed settings.

**Show:** Read the override as a launcher operation, not a tool call. Point out the shell quoting needed to preserve a string for OMP_NUM_THREADS. This example changes the profile deliberately without editing the file.

**Sources:** [config](https://github.com/t-kalinowski/mcp-console/blob/main/docs/CONFIGURATION.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 52. Native restrictions and external enforcement differ

**Say:** unrestricted and external-sandbox are different filesystem kinds. Unrestricted keeps the native network selection but removes filesystem restrictions and metadata protections. Without a proxy, external-sandbox delegates both filesystem and network enforcement to an outer boundary; network: restricted does not add a native block there.

**Show:** Contrast the two valid configurations. The right-hand file is not safe merely because restricted appears in it. Use it only where a real outer boundary is provided; the runner does not verify one exists.

**Author / capture:** Full filesystem access can undermine other restrictions indirectly and lies outside the restricted-policy isolation guarantee. Never use this slide to imply hostile workloads are contained in unrestricted mode.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 53. Expose the knobs without inventing a second policy engine

**Say:** Console forwards native policy values rather than maintaining a second allowlist of all native fields. Some settings, such as lifecycle ownership, are reserved for the launcher. Linux backend selection is explicit; a namespace failure is not permission to silently fall back to unsandboxed execution.

**Show:** Use the ordinary supervised Linux backend as the concrete example. Keep special standalone complete-policy and Landlock details in notes rather than suggesting they are interchangeable serve modes.

**Author / capture:** Current standalone runner also exposes explicit Landlock without process supervision; it rejects cleanup/private-temp/proxy combinations needed by ordinary serve. Do not present linux_backend: landlock as an equivalent working server configuration. macOS rejects linux_backend.

**Sources:** [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md) · [settings](https://github.com/t-kalinowski/mcp-console/blob/main/src/settings.rs)


## 54. Resolution crosses a different trust boundary

**Say:** The agent can use packages while worker networking is restricted because preparation is a separate trusted operation. The resolver may download packages and execute install or build code. Its authority is not the worker’s network authority, and automatic resolution must not be described as a sandbox escape.

**Show:** Keep actual YAML and a requirements call above the trust-boundary diagram. Follow the request out to ir/uv and the prepared environment back in; emphasize activation without automatic replay of the cell.

**Sources:** [requirements](https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md) · [architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 55. The process topology

**Say:** Show the whole architecture after its consequences are familiar. The MCP client talks to the Rust server. The execution launcher establishes the selected target and boundary; the relay owns worker communication and direct supervision; the worker owns language state. Dependency preparation is outside the worker sandbox. Native helper details differ by platform.

**Show:** This is the main architecture diagram. Keep the process boundary visible and distinguish the client, controller, and worker. The launcher node is an abstraction: native execution uses the sandbox runner, while compute targets have their own owners and provider behavior.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 56. State has an owner

**Say:** The architecture becomes easier to reason about when state ownership is explicit. The server owns logical-session and delivery state; the worker owns live computational state. That separation explains why prepared requirements and recordings survive worker restart while objects and debugger state do not.

**Show:** Use a two-column owner table without method names or module-level details. Tie it directly back to the restart behavior already demonstrated. Do not introduce a new peer-runtime coordinator as implemented unless that refactor has landed.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md)


## 57. Three worker paths, not prompt scraping

**Say:** Code/control messages, interactive input, and raw output have distinct channels. The relay keeps these concerns separate. Console does not have to guess whether a program is ready by matching a printed greater-than sign. Structured runtime state is part of why timeout, debugger, and failure behavior can have precise contracts.

**Show:** Use the stream diagram. It should make the distinction introduced by stdin visually concrete. This is not a deep dive into JSONL framing or file-descriptor bootstrap details.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Vision / intended design](https://github.com/t-kalinowski/mcp-console/blob/main/design-sketches/VISION.md)


## 58. SSH: the same policy, materialized remotely

**Say:** The target selects where execution happens; it does not grant permissions. Console reads YAML locally, captures it, and materializes the native policy on the SSH host. Dependencies are prepared there, while the controller retains the session record.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** analysis-host must be a configured OpenSSH destination; /srv/projects/analysis and data must already exist. SSH+Docker composition is not supported in this revision.

**Sources:** [ssh](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 59. Docker: explicit image, workspace, and binds

**Say:** An ordinary Docker image is a prepared execution environment. Dynamic preparation is disabled. This example deliberately delegates to the container boundary; it does not retain native metadata protection inside a writable project bind.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Build my-console:analysis first. Source paths are interpreted by the selected Docker daemon. Native sandboxing inside Docker is a separate supported selection where host capabilities permit it; no privileged-mode fallback is implied.

**Sources:** [docker](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 60. Docker Sandbox uses the compute provider

**Say:** Docker Sandbox is not ordinary Docker. The compute provider owns its boundary and accepts only environment and inheritance controls under sandbox. The native runner is not invoked on this path, and native filesystem, proxy, or extends settings are rejected.

**Show:** Walk through the visible YAML from top to bottom. This is a complete alternative configuration, not a patch to concatenate with the preceding example.

**Author / capture:** Replace <64-hex-digest> and paths with actual values. Prepare/import the template and provider policy separately. The tested SBX version requires the first shared path to be read/write. No dynamic dependency preparation in the template-backed worker.

**Sources:** [sbx](https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER_SANDBOX.md) · [sandbox](https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md)


## 61. The call stays the same

**Say:** Across targets, the model still submits cells, receives bounded results, and uses the same controls. Available environments and preparation capabilities can differ and the live schema reflects that. The claim is a stable interaction model, not identical permissions or package-management behavior everywhere.

**Show:** Return to one familiar call with four destinations beneath it. This is the bridge into client integrations: both the client above and execution target below can vary without changing the central idea.

**Sources:** [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 62. ellmer

**Say:** Give ellmer one slide. The R wrapper starts Console, reads its live tool schema, and presents it as an ellmer tool. It does not execute agent code in the R process running the chat. Provider choice remains with ellmer and the application. Keep the tool alive across the conversation so its session persists.

**Show:** Show only the registration example, with the registration line emphasized. No installation explanation here; that is the next section. The author notes include the asynchronous sequential-tool caveat from the R README.

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md) · [R tool wrapper implementation](https://github.com/t-kalinowski/mcp-console/blob/main/r/R/console-tool.R)


## 63. chatlas

**Say:** The chatlas adapter adds the same tool to an existing chat. Use the adapter and set_tools so the explicit server schema is preserved rather than inferred from a generic Python function annotation. The application still owns the chat loop and the Console connection lifetime.

**Show:** Keep the visual design identical to the ellmer slide. For a visual demo, verify image preservation on the chosen adapter path; the native MCP registration variant is included in the examples file.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 64. Codex

**Say:** Codex can launch Console through its MCP stdio configuration. The CLI command and configuration table are two alternatives, not two required steps. In the recording use the client surface you normally use, but make the model’s arguments and tool results legible rather than focusing on the application chrome. Client-side timeouts are separate from Console’s wait contract.

**Show:** Show the registration line and its equivalent configuration. Do not fabricate a Codex screenshot or imply that this local stdio configuration automatically applies to unrelated hosted web clients. Verify image visibility and client deadlines when capturing the final run.

**Sources:** [Official Codex MCP documentation](https://developers.openai.com/codex/mcp/) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md)


## 65. Anthropic Python SDK

**Say:** The Anthropic integration has native MCP and function-tool paths. Show the native async tools context here because visual workflows need image preservation. The SDK owns the model loop; Console owns execution. model_id and prompt are application inputs, not hard-coded recommendations.

**Show:** This is an async application excerpt, with the full runnable wrapper in examples/anthropic_client.py. Keep the connection open for the run and let the context close it. The concrete API follows the repository’s documented integration and should be rechecked before presentation.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 66. The direct Python client

**Say:** The direct client is useful for scripts, application integration, and deterministic checks. Both calls reuse one Console connection. The convenience return is text and uses placeholders for image content; native MCP or image-preserving adapters are the appropriate interface for a visual agent workflow. AsyncMCPConsole offers the parallel asynchronous API.

**Show:** Show a complete minimal synchronous example. Do not imply that printing the direct client result displays a plot. Keep the async counterpart in the accompanying example file and the compatibility list.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 67. OpenAI Responses

**Say:** The Responses adapter reads the connected server schema and supplies the function definition and function-call output conversion. The application still owns the continuation loop. This excerpt deliberately focuses on registration; the complete loop is provided as a companion example rather than squeezed onto the slide.

**Show:** Show the adapter line as the focus. model_id and prompt are supplied by the host application. The full example includes continuation and a turn limit; do not present this excerpt alone as a complete autonomous agent run.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 68. Other supported entry points

**Say:** Finish the client sequence with one list, not another onboarding section. These are the additional entry points documented by the project. Avoid the unqualified phrase works with everything: compatibility depends on the client’s transport, tool-schema handling, image support, and timeout behavior.

**Show:** Use a plain list of exact interface names. The source package contains a concise example for each documented integration family; there is no need to display every tool loop in the main talk.

**Sources:** [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml)


## 69. Now, installation from R

**Say:** Only after the value and client examples are clear, show the R installation story. For presentation day, assume mcp.console is published to the intended R package repository. Installing the R package gives the interface; creating the tool resolves the Console executable when necessary. Do not say the PyPI download occurs during install.packages itself.

**Show:** Show one large line. This is explicitly an intended publication pathway: the currently inspected R README uses a GitHub installation command. Keep the present-day command in the author checklist, not as competing text on this slide.

**Author check before presenting:** Target-day assumption: mcp.console is published to an R repository usable by install.packages(). Current README documents pak::pak("github::t-kalinowski/mcp-console/r").

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)


## 70. The R wrapper obtains the native application

**Say:** With no explicit selection, console_tool() first uses an mcp-console executable on PATH. If none is found, it resolves the published application with reticulate::uv_run_tool(). A named path or version gives explicit control. PyPI is the distribution channel for a native Rust application bundle, not a requirement for the R user to manually manage an analysis venv.

**Show:** Use the first-use chain. The installation trigger belongs on the arrow from wrapper to resolver. Keep executable selection separate from analysis runtime environment selection, which was covered earlier.

**Sources:** [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md) · [R tool wrapper implementation](https://github.com/t-kalinowski/mcp-console/blob/main/r/R/console-tool.R) · [Release and installed bundle](https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md)


## 71. Python or a standalone MCP launch

**Say:** Python users choose the base package or the extra for their integration. MCP clients can launch through uvx, or use a persistent uv tool installation. These are alternative routes into the same distribution, not three installation steps. Framework extras avoid installing every SDK when only the executable is needed.

**Show:** Show three short alternatives with explicit labels. Mention prerequisites only as needed: Python packaging and supported native wheels are not the same thing as the language runtime installed on a selected execution host.

**Sources:** [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md)


## 72. One distribution; separate execution environments

**Say:** A supported platform wheel carries the application and sandbox companions as an installed bundle. Language runtimes and analysis packages belong to the execution environment. Current support is macOS and Linux, with specific Linux glibc and sandbox prerequisites; Windows is not currently supported. Source builds still need the toolchain. An SSH or compute controller does not require its own local analysis environment.

**Show:** Use the two responsibility boxes. Do not put a green all-platforms checkmark on the slide. Keep exact release/platform requirements in the installation documentation, because those can change before presentation day.

**Sources:** [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md) · [Release and installed bundle](https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md) · [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 73. Interactive work, without a sprawling tool surface

**Say:** Close on the design, not on installation commands. The contribution is a compact model-facing interface with enough runtime capability and explicit control to remain useful as the model’s ability grows. The interaction carries across languages, clients, and execution targets while keeping ownership and trust boundaries visible.

**Show:** Return to the opening typography, now with the expanded capability set condensed into one line. Stop the main presentation here; the development-practices slides follow as an addendum.

**Sources:** [Canonical tool schema snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml) · [Built-in runtime](https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md) · [Implemented architecture](https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md)


## 74. Rust implementation. Python integration tests.

**Say:** The main integration suite is Python even though the application is Rust. It drives the built executable and observes the real process boundary. Small unit tests can still own pure parsing or validation policy; the claim is not that absolutely no Rust tests exist.

**Show:** Use two simple implementation/test boxes. Lead with why this matters: the test language can stay independent of implementation refactors while validating the product contract users and clients actually see.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Project README](https://github.com/t-kalinowski/mcp-console/blob/main/README.md)


## 75. Test the boundaries you intend to preserve

**Say:** The tests mirror architectural boundaries: client_server, server_relay, relay_worker, and cli. Public behavior belongs at the outermost boundary that can usefully observe it. Private-boundary cases cover their own protocol seams rather than replicating every public message at every layer.

**Show:** Reuse the process topology with test-boundary names on the arrows. This ties the development method to the earlier architecture rather than presenting a directory tree with no explanation.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 76. YAML is what the reviewer reads

**Say:** The wire protocols are JSON-based, but the reviewable test transcripts are YAML. This is an actual checked-in snapshot excerpt: the test executes R, asserts that CPU detection returns a valid result, and prints a stable message. Humans can review the code and result without reading escaped JSON strings or snapshotting a machine-specific core count. YAML is the human review surface, not the production transport.

**Show:** Display the request and result from `tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml` side by side. The initial shared-handshake document is omitted, but the displayed request and result content come from the fetched source. This fixture was not rerun in the slide-build environment; do not present it as a new test execution.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Checked-in CPU detection snapshot](https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml)


## 77. Normalize noise, not behavior

**Say:** Temporary paths, process identities, and similar unstable details should not obscure behavioral review. Normalize explicitly and narrowly. Preserve the fields, output, ordering, and failure distinctions the contract is meant to protect. The actual project normalizers and snapshot metadata are more specific than this schematic example.

**Show:** Use before/after panels with only incidental details changed. Call out that normalization is not a license to delete inconvenient evidence from a test.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 78. Synchronize; do not sleep and hope

**Say:** Concurrency and liveness tests need causal synchronization. Fixtures use gates and checkpoints so the test knows when the relevant state has actually been reached. Arbitrary sleeps are not proof that output was drained, an interrupt was delivered, or an owned resource was retired.

**Show:** Show one deterministic sequence and connect it to the timing and shutdown contracts from the talk. This is a development-practice slide, not an implementation recipe for every fixture.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 79. Portable behavior; real capability checks

**Say:** Reuse portable cases across execution modes and centralize capability discovery. A skipped target fixture is not target validation. Deterministic peers can establish orchestration behavior, but they cannot establish real container or microVM cleanup. Keep real-target evidence distinct from simulated protocol coverage.

**Show:** Use the two testing levels rather than an all-green platform matrix. Include lifecycle and security assertions where a textual snapshot alone cannot represent the guarantee.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 80. Snapshots are generated evidence

**Say:** Generate transcripts from running tests, then review the resulting diff. Do not hand-edit the expectation to make a test pass. The value of readable YAML is that review can focus on the actual changed behavior, while assertions still enforce facts that a snapshot cannot show.

**Show:** Show the update command and a diff review, not a large wall of green tests. The selector is schematic; replace BOUNDARY/SUITE::CASE with a real selected fixture for a live development demonstration.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md)


## 81. Test the installed product

**Say:** The delivered product includes the executable, companion binaries, Python interfaces, the R wrapper, and launch/lifetime behavior. Running a development binary alone does not establish that the installed bundle or each adapter works. Integration examples and packaging checks should be part of the release evidence, with actual target validation reported separately.

**Show:** Finish the addendum by connecting the install story to the test strategy. Avoid claiming every proposed integration test already exists: distinguish observed project coverage from the release checklist in the companion author notes.

**Sources:** [Boundary test guide](https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md) · [Release and installed bundle](https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md) · [Python clients and integrations](https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md) · [R package interface](https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md)
