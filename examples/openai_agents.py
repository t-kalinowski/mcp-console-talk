"""OpenAI Agents SDK adapter. Install mcp-console[openai-agents]."""
from pathlib import Path
import os
from agents import Agent, Runner
import mcp_console


def main() -> None:
    model_id = os.environ.get("MODEL_ID")
    if not model_id:
        raise SystemExit("Set MODEL_ID and OPENAI_API_KEY before running this example.")
    os.chdir(Path(__file__).resolve().parent)
    with mcp_console.MCPConsole() as console:
        agent = Agent(
            name="Data analyst",
            model=model_id,
            tools=[mcp_console.openai.agents_tool(console)],
        )
        result = Runner.run_sync(
            agent,
            "Use Console to summarize measurements.csv. The data are synthetic.",
        )
        print(result.final_output)


if __name__ == "__main__":
    main()
