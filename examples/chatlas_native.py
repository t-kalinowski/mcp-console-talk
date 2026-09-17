"""Native async MCP registration in chatlas. Install mcp-console[chatlas]."""
from pathlib import Path
import asyncio
import os
from chatlas import ChatOpenAI
import mcp_console


async def main() -> None:
    model = os.environ.get("MODEL_ID")
    if not model:
        raise SystemExit("Set MODEL_ID and the provider credential before running this example.")
    os.chdir(Path(__file__).resolve().parent)
    chat = ChatOpenAI(model=model)
    try:
        await mcp_console.chatlas.register(chat)
        await chat.chat_async("Use Console to summarize measurements.csv and plot it. The data are synthetic.")
    finally:
        await chat.cleanup_mcp_tools()


if __name__ == "__main__":
    asyncio.run(main())
