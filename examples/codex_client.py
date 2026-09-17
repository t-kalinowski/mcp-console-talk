"""Codex Python thread-SDK integration as documented by MCP Console.
Install mcp-console[codex]; configure Codex authentication and MODEL_ID.
"""
from pathlib import Path
import os
from openai_codex import Codex
import mcp_console


def main() -> None:
    model_id = os.environ.get("MODEL_ID")
    if not model_id:
        raise SystemExit("Set MODEL_ID and configure Codex authentication before running.")
    os.chdir(Path(__file__).resolve().parent)
    config = {
        "model": model_id,
        "mcp_servers": {"console": mcp_console.codex.server()},
    }
    with Codex() as client:
        thread = client.thread_start(config=config)
        result = thread.run("Use Console to summarize measurements.csv. The data are synthetic.")
        print(result.final_response)


if __name__ == "__main__":
    main()
