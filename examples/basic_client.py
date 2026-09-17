"""Direct synchronous and asynchronous clients. Install mcp-console[client].
These examples create separate sessions; they do not share state with each other.
"""
import asyncio
import mcp_console


def synchronous() -> None:
    with mcp_console.MCPConsole() as console:
        print(console.send(r="x <- 40 + 2; x"))
        print(console.send(r="x + 1"))


async def asynchronous() -> None:
    async with mcp_console.AsyncMCPConsole() as console:
        print(await console.send(python="x = 40 + 2; x"))
        print(await console.send(python="x + 1"))


if __name__ == "__main__":
    synchronous()
    asyncio.run(asynchronous())
