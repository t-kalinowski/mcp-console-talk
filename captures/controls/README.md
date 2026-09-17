# Separate control-operation capture

These are literal responses from a sandboxed Console session, without a model API.
`cells.json` records the two illustrated requests. `wire.jsonl` retains the MCP
exchange; response files preserve individual frames and the combined result.

- `restart-test`: restart and run devtools::test() in a small package fixture.
- `restart-script`: restart, queue `A\n`, and source examples/analyze.R.
- `state-check`: verify old-session state is absent and the script selected group A.

The sourced script and measurements CSV are copied from the presentation project;
provenance.json records their hashes and the executable fingerprint. The fixture
and collector script are in ../../../archived/2026-09-17-controls-review/.
