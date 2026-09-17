#!/usr/bin/env python3
"""Capture actual MCP Console responses and artifacts without a model API.

Requires Python 3.10+ and a working mcp-console command, with its R/runtime
prerequisites. Reads/writes only within the extracted presentation project.
The server may resolve trusted R/Python dependencies using its normal setup.

  python examples/capture_console.py
  python examples/capture_console.py --command /path/to/mcp-console serve
  quarto preview deck.qmd -P output_source:mcp

Uses the stdio MCP protocol, rather than the direct client's text projection,
so returned PNGs and exact tool-result text are retained. Source examples live
in cells.json and are also used by the slide-authoring checks.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class MCPError(RuntimeError):
    pass


class StdioMCP:
    def __init__(self, command: list[str], out: Path, deadline: float = 600):
        self.out = out
        self.deadline = deadline
        self.counter = 0
        self.messages: queue.Queue[Any] = queue.Queue()
        self.log = (out / "wire.jsonl").open("w", encoding="utf-8")
        self.stderr = (out / "server-stderr.log").open("wb")
        try:
            self.proc = subprocess.Popen(
                command, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self.stderr, text=True, encoding="utf-8", bufsize=1,
            )
        except BaseException:
            self.log.close()
            self.stderr.close()
            raise
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self) -> None:
        assert self.proc.stdout is not None
        try:
            for line in self.proc.stdout:
                self.messages.put(json.loads(line))
        except BaseException as exc:
            self.messages.put(exc)
        finally:
            self.messages.put(None)

    def _write(self, payload: dict[str, Any]) -> None:
        assert self.proc.stdin is not None
        self.log.write(json.dumps({"direction": "client", "message": payload}) + "\n")
        self.log.flush()
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        message: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        self._write(message)

    def request(self, method: str, params: dict[str, Any]) -> Any:
        self.counter += 1
        request_id = self.counter
        self._write({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        stop = time.monotonic() + self.deadline
        while True:
            remaining = stop - time.monotonic()
            if remaining <= 0:
                raise MCPError(f"Request {method} exceeded capture deadline; see server-stderr.log")
            try:
                message = self.messages.get(timeout=remaining)
            except queue.Empty as exc:
                raise MCPError(f"No response to {method}; see server-stderr.log") from exc
            if message is None:
                raise MCPError(f"Server closed before replying to {method}; see server-stderr.log")
            if isinstance(message, BaseException):
                raise MCPError(f"Invalid server protocol output: {message}") from message
            self.log.write(json.dumps({"direction": "server", "message": message}) + "\n")
            self.log.flush()
            if "id" not in message:  # notifications may arrive between responses
                continue
            if message.get("method"):
                self._write({"jsonrpc": "2.0", "id": message["id"], "error": {
                    "code": -32601, "message": "Capture client does not implement this request"}})
                continue
            if message["id"] != request_id:
                raise MCPError(f"Unexpected response ID {message['id']}; expected {request_id}")
            if "error" in message:
                raise MCPError(f"{method}: {message['error']}")
            return message.get("result")

    def initialize(self) -> dict[str, Any]:
        result = self.request("initialize", {
            "protocolVersion": "2025-11-25", "capabilities": {},
            "clientInfo": {"name": "console-presentation-capture", "version": "1"},
        })
        self.notify("notifications/initialized")
        tools = self.request("tools/list", {})
        (self.out / "initialize.json").write_text(json.dumps(result, indent=2) + "\n")
        (self.out / "tools.json").write_text(json.dumps(tools, indent=2) + "\n")
        return result

    def send(self, arguments: dict[str, Any]) -> dict[str, Any]:
        result = self.request("tools/call", {"name": "send", "arguments": arguments})
        if not isinstance(result, dict):
            raise MCPError("send returned a non-object result")
        if result.get("isError"):
            raise MCPError("Console tool error: " + result_text(result))
        return result

    def close(self) -> None:
        # Closing MCP input asks Console to retire its own workers/resources.
        if self.proc.stdin:
            try:
                self.proc.stdin.close()
            except BrokenPipeError:
                pass
        try:
            self.proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=5)
        self.reader.join(timeout=2)
        if self.proc.stdout:
            self.proc.stdout.close()
        self.log.close()
        self.stderr.close()


def result_text(result: dict[str, Any]) -> str:
    # Text blocks retain their contents; an image is not replaced with prose.
    return "".join(block.get("text", "") for block in result.get("content", [])
                   if block.get("type") == "text")


def is_running(result: dict[str, Any]) -> bool:
    text = result_text(result).rstrip()
    return text.endswith("[running; poll with an empty send]") or text.endswith("[worker starting]")


def save_result(out: Path, name: str, result: dict[str, Any]) -> None:
    (out / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (out / f"{name}.txt").write_bytes(result_text(result).encode("utf-8"))
    image_no = 0
    for block in result.get("content", []):
        if block.get("type") != "image":
            continue
        image_no += 1
        mime = block.get("mimeType")
        if mime != "image/png":
            raise MCPError(f"Unexpected image type {mime}; update renderer explicitly")
        data = base64.b64decode(block["data"], validate=True)
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise MCPError("PNG signature mismatch")
        (out / f"{name}-{image_no:02d}.png").write_bytes(data)


def complete(client: StdioMCP, out: Path, name: str, args: dict[str, Any]) -> None:
    responses = [client.send(args)]
    started = time.monotonic()
    while is_running(responses[-1]):
        if time.monotonic() - started > client.deadline:
            raise MCPError(f"Cell {name} remained active past capture deadline")
        responses.append(client.send({"timeout_ms": 1000}))
    # Each response stays separately inspectable. The render text concatenates
    # actual content blocks without fabricating a terminal state or value.
    for index, response in enumerate(responses):
        save_result(out, f"{name}-response-{index:02d}", response)
    combined = {"content": [b for r in responses for b in r.get("content", [])], "isError": False}
    save_result(out, name, combined)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "captures")
    parser.add_argument("--deadline", type=float, default=600)
    parser.add_argument("--requirements-only", action="store_true",
                        help="Capture the pinned R requirements example in a fresh session")
    parser.add_argument("--command", nargs=argparse.REMAINDER, default=["mcp-console", "serve"])
    args = parser.parse_args()
    if not args.command:
        parser.error("--command requires an executable and its arguments")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if (out / "capture-manifest.json").exists() or (out / "wire.jsonl").exists():
        parser.error(f"{out} already contains a capture; rename it or choose --out")
    cells = json.loads((ROOT / "examples/cells.json").read_text())
    runs = ROOT / ".agents/console/sessions"
    before = set(runs.iterdir()) if runs.exists() else set()
    client = StdioMCP(args.command, out, args.deadline)
    ok = False
    try:
        initialize = client.initialize()
        if args.requirements_only:
            print("Capturing requirements in a fresh session", flush=True)
            complete(client, out, "requirements", cells["requirements"])
            complete(client, out, "versions", {"r": "sessionInfo()"})
        else:
            capture_deck(client, out, cells)
        executable = Path(shutil.which(args.command[0]) or args.command[0]).resolve()
        (out / "capture-manifest.json").write_text(json.dumps({
            "captured_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "command": args.command, "cwd": str(ROOT), "server_initialize": initialize,
            "executable": str(executable),
            "executable_sha256": hashlib.sha256(executable.read_bytes()).hexdigest(),
            "source_cells": cells, "provenance": "Actual MCP stdio responses; no model API used",
            "full_journal": "session-records/internal/events.jsonl",
            "requirements_example": "Captured in a fresh session" if args.requirements_only else
                "Not installed by this capture; validate separately in a fresh session",
        }, indent=2) + "\n")
        ok = True
    finally:
        client.close()
        after = set(runs.iterdir()) if runs.exists() else set()
        created = sorted(after - before)
        if len(created) == 1:
            shutil.copytree(created[0], out / "session-records")
        elif created:
            for index, run in enumerate(created):
                shutil.copytree(run, out / f"session-records-{index:02d}")
    if ok:
        print(f"Captured real responses in {out}\nRender: quarto preview deck.qmd -P output_source:mcp")
    return 0


def capture_deck(client: StdioMCP, out: Path, cells: dict[str, Any]) -> None:
    # Warm the runtime before the displayed calls. Keep that exchange on wire.
    complete(client, out, "warmup", {"r": "invisible(NULL)", "timeout_ms": 30000})
    complete(client, out, "inline-prepare", {"r": 'invisible(loadNamespace("inline"))',
                                          "timeout_ms": 30000})
    for name in ["fit", "coefficients", "predict", "r-plot"]:
        print(f"Capturing {name}", flush=True)
        complete(client, out, name, cells[name])
    print("Capturing timeouts and progress", flush=True)
    first = client.send(cells["progress"])
    save_result(out, "progress", first)
    polls = []
    response = first
    started = time.monotonic()
    while is_running(response):
        if time.monotonic() - started > client.deadline:
            raise MCPError("Progress capture remained active past its deadline")
        response = client.send(cells["poll-next"] if not polls else cells["poll-final"])
        polls.append(response)
        save_result(out, f"poll-{len(polls):02d}", response)
    if not polls:
        raise MCPError("Progress completed before the first wait expired; lower timeout_ms in cells.json")
    save_result(out, "poll-next", polls[0])
    save_result(out, "poll-final", polls[-1])
    if len(polls) != 2:
        raise MCPError("Expected two displayed polls; inspect timing before changing the slides")
    for name in ["compact", "flood", "error", "checkpoint", "prompt", "prompt-answer",
                 "browser-start", "browser-x", "browser-continue",
                 "r-fork", "python-fd", "python-first", "python-ml", "python-plot", "sql"]:
        print(f"Capturing {name}", flush=True)
        complete(client, out, name, cells[name])
        if name == "r-fork":
            assert (out / "r-fork.txt").read_text() == "native output\n"
        if name == "python-fd":
            assert (out / "python-fd.txt").read_text() == "hello directly on fd 1\n"
    # Exercise metadata preservation through the public MCP request envelope.
    result = client.request("tools/call", {
        "name": "send", "arguments": {"r": "1 + 1"},
        "_meta": {"progressToken": "recording-example", "example.com/harness": {
            "turn": 7, "label": "presentation capture"}},
    })
    assert not result.get("isError"), result
    save_result(out, "metadata", result)
    complete(client, out, "versions", {"r": "sessionInfo()",
             "timeout_ms": 30000})
    complete(client, out, "python-versions", {"python":
        "import sys, importlib.metadata as md\nprint(sys.version)\n"
        "for name in ['scikit-learn', 'pandas', 'matplotlib']:\n"
        "    print(f'{name}=={md.version(name)}')"})

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MCPError, OSError, ValueError) as exc:
        print(f"Capture failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
