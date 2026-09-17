# Recording plan

## What the recording should establish

Show the **model-facing interaction**, not that a chat application can call an evaluator. The useful sequence is a real model choosing code, inspecting a result, continuing with retained state, dealing with a wait, and seeing a plot or switching language without a second session setup.

Use the Codex TUI when it gives the clearest expanded tool arguments and results. Use the desktop client when it makes the actual returned images materially clearer. Keep the application chrome out of most frames. The static slides use editable function-call panels so the explanation does not depend on a particular client version or theme.

## Prompt

> Use `measurements.csv` to investigate the temperature effect. Check whether it differs by group, inspect the residuals, and summarize the evidence. Use Console as your workbench. The dataset is synthetic.

Do not claim that the model will spontaneously take a particular language path. Capture its actual choices. A deliberate follow-up can request a cross-language step or a bootstrap calculation when needed to demonstrate the contract honestly.

## Suggested shots

1. Brief establishing view: the existing client and Console tool availability, not the installation process.
2. Expanded first call and returned result: crop tightly enough that the argument keys are readable.
3. A dependent call that uses existing objects without reloading the data.
4. A real long-running operation with a wait timeout and empty polling call. The supplied bootstrap script is deliberately slowed for this demonstration; do not use it as performance evidence.
5. A returned plot or a cross-language step, with the actual input and output visible.
6. The real `transcript.md` and `transcript.qmd` generated for that session.

Keep a short recording with natural pauses or edit points; use the static feature slides to explain individual mechanics rather than making the recording carry every capability.

## Data and fallback

`examples/measurements.csv` contains 240 synthetic observations with temperature, group, and response columns. It is not an external experiment or evidence about a real-world population. `examples/bootstrap.R` fits repeated resamples and inserts deliberate sleeps to expose polling.

`examples/replay_demo.py` drives a deterministic subset of the session. It is a **scripted fallback**, not model-generated behavior. It can help test the environment and produce a real Console record before recording the model session. The direct client prints text and image placeholders; inspect Console’s retained artifacts or use the native MCP client for the actual visual capture.

## Insert the recording

The slide with stable ID `demo` is the replacement point. Put a genuine recording at `assets/demo.mp4` and replace its body with an HTML video element, leaving its notes intact. Do not relabel the existing placeholder as an actual recording.

```html
<video controls preload="metadata" style="width:100%;max-height:590px">
  <source src="assets/demo.mp4" type="video/mp4">
</video>
```

Render the edited deck with `quarto preview deck.qmd` or `quarto render deck.qmd --to revealjs`. Add a real recording using Quarto-supported video markup and verify its playback in the browser before presenting. Speaker notes remain in the slide’s native `.notes` block and are available with S.
