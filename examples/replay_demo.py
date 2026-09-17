"""Deterministic Console driver for a real capture, not a model-generated session.
Run with mcp-console[client] installed and the execution-host R prerequisites met.
Output text is printed here; actual images are retained by Console's recording layer.
"""
from pathlib import Path
import os
import mcp_console

ROOT = Path(__file__).resolve().parent
PENDING = ("[running; poll with an empty send]", "[worker starting]")


def collect(console: MCPConsole, **kwargs: object) -> str:
    """Submit once, then collect each pending interval without resubmitting code."""
    text = console.send(**kwargs)
    print(text, flush=True)
    polls = 0
    while text.rstrip().endswith(PENDING):
        polls += 1
        if polls > 300:
            console.send(control="interrupt")
            raise RuntimeError("Capture poll limit reached; interruption requested.")
        text = console.send(timeout_ms=200)
        print(text, flush=True)
    return text


def main() -> None:
    os.chdir(ROOT)
    with mcp_console.MCPConsole() as console:
        collect(console, r='d <- read.csv("measurements.csv"); fit <- lm(response ~ temperature + group, d)', timeout_ms=200)
        collect(console, r="coef(fit)")
        collect(console, r='plot(d$temperature, d$response, xlab="Temperature", ylab="Response")')
        collect(console, r='source("bootstrap.R")', timeout_ms=200)
        collect(console, r='d$.residual <- residuals(fit)')
        collect(console, sql='SELECT "group", AVG(ABS(".residual")) AS error FROM d GROUP BY "group"')
        collect(console, python='frame = r.d\nframe.groupby("group").size()')


if __name__ == "__main__":
    main()
