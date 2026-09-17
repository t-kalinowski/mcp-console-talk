# Source notes

Repository documentation and wrapper/schema source were checked on 2026-09-16. Sources in slide notes support implemented behavior; user-authorized target-day scope is labeled in author checks. The diagrams are authored technical schematics, not screenshots.

- **Project README:** https://github.com/t-kalinowski/mcp-console/blob/main/README.md
- **Built-in runtime:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/BUILTIN_RUNTIME.md
- **Send operation contract:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/SEND_OPERATIONS.md
- **Canonical tool schema snapshot:** https://github.com/t-kalinowski/mcp-console/blob/main/tests/snapshots/client_server/server/test_tools/initializes_and_lists_tools.yaml
- **Requirements and environments:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/REQUIREMENTS.md
- **R package interface:** https://github.com/t-kalinowski/mcp-console/blob/main/r/README.md
- **R tool wrapper implementation:** https://github.com/t-kalinowski/mcp-console/blob/main/r/R/console-tool.R
- **Python clients and integrations:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/PYTHON.md
- **Implemented architecture:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/ARCHITECTURE.md
- **Configuration layering:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/CONFIGURATION.md
- **Sandbox configuration:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/SANDBOX_CONFIGURATION.md
- **SSH execution:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/SSH.md
- **Docker execution:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER.md
- **Docker Sandbox execution:** https://github.com/t-kalinowski/mcp-console/blob/main/docs/DOCKER_SANDBOX.md
- **Boundary test guide:** https://github.com/t-kalinowski/mcp-console/blob/main/tests/boundaries/README.md
- **Release and installed bundle:** https://github.com/t-kalinowski/mcp-console/blob/main/RELEASE.md
- **Vision / intended design:** https://github.com/t-kalinowski/mcp-console/blob/main/design-sketches/VISION.md
- **Proposed configuration:** https://github.com/t-kalinowski/mcp-console/blob/main/design-sketches/CONFIGURATION.md
- **Official Codex MCP documentation:** https://developers.openai.com/codex/mcp/
- **Quarto reveal.js presentation guide:** https://quarto.org/docs/presentations/revealjs/

## Verified content identifiers

- docs/PYTHON.md blob SHA: `ba287022f7d505eedf00766e166adf70f76178e8`
- r/README.md blob SHA: `6cc36cdf62f7e8d55e7e39064343e82d10b3073b`
- canonical tool schema snapshot blob SHA: `241b86f63b74e2383b796884f2a16e8be847c54a`

No MCP runtime or provider/model integration was executed to produce these slides. Code examples were reviewed against documented interfaces; static validation is not an end-to-end integration test.

## Actual YAML snapshot example

Slide 64 reproduces the request and result from `tests/snapshots/client_server/r/test_runtime/detects_cpu_cores.yaml`, fetched from the repository. Its initial shared-handshake document is omitted on the slide. Blob SHA: `33546e4d62a76cf2f55fabbc9446941d39a0b9db`. The complete source example is included in `examples/detects_cpu_cores.yaml`. It was not executed in this build environment.
