"""Complete Responses continuation loop. Install mcp-console[openai].
Supply MODEL_ID and OPENAI_API_KEY. This performs real provider calls when run.
"""
from pathlib import Path
import os
from openai import OpenAI
import mcp_console


def main() -> None:
    model_id = os.environ.get("MODEL_ID")
    if not model_id:
        raise SystemExit("Set MODEL_ID to a model available in your OpenAI account.")
    os.chdir(Path(__file__).resolve().parent)
    prompt = "Use Console to analyze measurements.csv, compare groups, and inspect a plot. The data are synthetic."
    with OpenAI() as client, mcp_console.MCPConsole() as console:
        tool = mcp_console.openai.responses_tool(console)
        response = client.responses.create(
            model=model_id, input=prompt, tools=[tool.definition]
        )
        for _ in range(24):
            calls = [item for item in response.output if item.type == "function_call"]
            if not calls:
                print(response.output_text)
                return
            unknown = [call.name for call in calls if call.name != "send"]
            if unknown:
                raise RuntimeError(f"Unexpected function calls: {unknown}")
            # Serial routing preserves the one-session dependency ordering.
            outputs = [tool(call) for call in calls]
            response = client.responses.create(
                model=model_id,
                previous_response_id=response.id,
                input=outputs,
                tools=[tool.definition],
            )
        raise RuntimeError("Stopped after 24 tool rounds; review the session before continuing.")


if __name__ == "__main__":
    main()
