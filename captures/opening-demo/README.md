# Opening demo evidence

Copied from the recorded session **Analyze Palmer penguins**, task
`01a0d048-5f66-7900-b6cd-39affebe5e8c`, in the penguins project.
Console run: `20260923T220029.270049000Z-86433`.

- `transcript.md`: the unmodified 13-call record, including errors and corrections.
- `transcript.qmd`: the unmodified generated code projection.
- `artifacts/call-000013-image-000001.png`: the unmodified returned image.
- `provenance.json`: original location and SHA-256 hashes for these files and
  the full deck backup.

The shorter alternative, `deck-short.qmd`, embeds the PNG directly. Its code overview selects lines from calls 4
and 11, plus three expressions from the SQL query in call 8; the SQL is reformatted.
It is an explanatory excerpt, not a separately executed three-call session.
The Markdown slide reads call 12 and its result directly from the copied record.

The plot shows bill length and depth for 342 complete observations. Pooled
correlation is −0.235; within species it is +0.391 (Adelie), +0.654 (Chinstrap),
and +0.643 (Gentoo). These are descriptive associations.

No model was called and no analysis was rerun while shortening the deck.
The recorded QMD includes failed exploratory cells and does not fully declare
the packages used. It requires curation before use as a reproducible report.
The shorter alternative shows an author-edited report selecting the penguins regression,
with an explicit palmerpenguins requirement and an added cutoff date. It is
identified as an edited example and was not rendered as an analysis in this revision.

The restored main deck uses this session as a live preamble. Its slides are
unchanged; the PNG is available as an external demo fallback.
