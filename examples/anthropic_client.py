"""Native MCP integration with the Anthropic async runner.
Install mcp-console[anthropic]; supply MODEL_ID and ANTHROPIC_API_KEY.
"""
from pathlib import Path
import asyncio
import os
from anthropic import AsyncAnthropic
from mcp_console import anthropic as console_anthropic


async def main() -> None:
    model_id = os.environ.get("MODEL_ID")
    if not model_id:
        raise SystemExit("Set MODEL_ID to a model available in your Anthropic account.")
    os.chdir(Path(__file__).resolve().parent)
    prompt = "Use Console to analyze measurements.csv, inspect a plot, and compare groups. The data are synthetic."
    async with AsyncAnthropic() as client:
        async with console_anthropic.tools() as tools:
            runner = client.beta.messages.tool_runner(
                model=model_id,
                max_tokens=4096,
                tools=tools,
                messages=[{"role": "user", "content": prompt}],
            )
            async for message in runner:
                print(message)


if __name__ == "__main__":
    asyncio.run(main())
