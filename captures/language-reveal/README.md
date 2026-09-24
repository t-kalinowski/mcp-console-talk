# Language reveal captures

These MCP stdio responses show a Python cell, a Matplotlib image, Python reading
an R data frame, and R reading the Python list, all within one sandboxed session.
The data frame is loaded by the same fitted-model cell used in the main deck.

`cells.json` contains the four displayed requests. `wire.jsonl` retains the full
exchange, and each response has its literal JSON/text and returned PNGs.
`session-records/` contains Console's generated records.

`provenance.json` records the installed executable fingerprint, checked before
and after capture, the data hash, and the capture time. No model API was used.
The collector is `examples/capture_language_reveal.py`.
