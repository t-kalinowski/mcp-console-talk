# Opening demo

Use the penguins session as a live preamble to the fuller presentation. Console
should already be registered with the agent. Allow about two minutes for the
interaction, then start the existing deck; no demo slide is needed.

A brief introduction can still establish why before the demo:

> I wanted R, Python, and SQL available to the agent in one session. Let me show what that looks like, then I'll walk through how it works.

## Prompt

> Use console to find out something interesting about the palmer penguins. Exercise use SQL, R, and Python for different parts of the analysis, and tell me something interesting that I haven't heard before.

Follow with “Can you visualize that?” The original session used the longer
follow-up “Are there any interesting data visualizations you can spin up to
illustrate these findings?”

Keep the original open-ended prompt. The presenter has observed it returning the
same finding over repeated runs. That is a rehearsal observation, not a guarantee
about another run. Asking for three languages demonstrates their availability;
it does not establish that the model independently chose the best language.

## What to show

1. The prompt and visible Console calls.
2. The finding and returned plot.
3. Point out the shared state: R defines the data frame, SQL queries it, and
   Python accesses it through `r.penguins`.
4. Begin the full deck: “That's the interaction. Now I'll walk through what
   Console makes available and how the session is controlled.”

There is no need to narrate every call or wait for a specific call sequence.
The retained session includes an unsuccessful SQL query and a Python namespace
error followed by corrections. A later run may take a different path.

## Client and fallback

Use a client that shows images. In Codex desktop, ask the agent to embed the saved
PNG in its reply. The inspected Codex TUI represents MCP image results with a
text placeholder; switching terminal emulators alone does not change that.

Keep the [saved penguins plot](captures/opening-demo/artifacts/call-000013-image-000001.png)
available in an image viewer. It is the actual returned image from the rehearsal.
If the live interaction takes too long or the client does not show it, open that
saved result, identify it as the earlier run, and continue into the full deck.

The shorter alternative, `deck-short.qmd`, also retains its embedded demo slides.
They are not part of the restored main presentation.

The evidence is in [captures/opening-demo](captures/opening-demo/README.md).
The older synthetic measurements examples remain available for the API detail
slides; they are not the opening demo.
