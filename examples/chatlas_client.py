"""chatlas function-tool example. Install mcp-console[chatlas]."""
from pathlib import Path
import os
from chatlas import ChatOpenAI
from mcp_console import MCPConsole, chatlas


def main() -> None:
    model = os.environ.get("MODEL_ID")
    if not model:
        raise SystemExit("Set MODEL_ID to a model available in your account; configure the provider credential as usual.")
    os.chdir(Path(__file__).resolve().parent)
    chat = ChatOpenAI(model=model)
    with MCPConsole() as console:
        chat.set_tools([*chat.get_tools(), chatlas.tool(console)])
        chat.chat("Use Console to summarize measurements.csv and compare groups. The data are synthetic.")


if __name__ == "__main__":
    main()
