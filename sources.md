# Source notes

## Standalone sandbox command — September 23, 2026

The public CLI and runner handoff were checked against the installed Console
0.0.4 help and local source at
`edaf0b394d4bca070c1abd9ecc0f2a0ce49b775b`, including
[src/sandbox/runner.rs](https://github.com/t-kalinowski/mcp-console/blob/edaf0b394d4bca070c1abd9ecc0f2a0ce49b775b/src/sandbox/runner.rs),
[the sandbox integration](https://github.com/t-kalinowski/mcp-console/blob/edaf0b394d4bca070c1abd9ecc0f2a0ce49b775b/docs/SANDBOX.md),
and [project configuration](https://github.com/t-kalinowski/mcp-console/blob/edaf0b394d4bca070c1abd9ecc0f2a0ce49b775b/docs/SANDBOX_CONFIGURATION.md).
The displayed base-R example was run through the native macOS sandbox.

## Repository development appendix — September 18, 2026

The development-history figures use a GitHub PR extraction at 19:08 UTC and
complete Git trees through main revision `657a5981983768967deed83c070973848ec800fb`
at 19:43 UTC. The PR charts include 279 merges directly into main; the size
charts include 307 first-parent snapshots, including direct commits.
See [the supplied data and methodology](examples/repository-development/README.md).

The high-level agent instructions and development loop were checked against
[AGENTS.md](https://github.com/t-kalinowski/mcp-console/blob/657a5981983768967deed83c070973848ec800fb/AGENTS.md)
and [docs/DEVELOPMENT.md](https://github.com/t-kalinowski/mcp-console/blob/657a5981983768967deed83c070973848ec800fb/docs/DEVELOPMENT.md)
at that revision. The slides describe the prescribed workflow, without claiming
historical compliance. The five feature annotations link to their merged PRs
in the speaker notes.

## Main talk and existing technical appendix

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
