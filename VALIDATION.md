# Validation and capture provenance

## Presentation checks

`quarto render` builds the 61-slide presentation from `deck.qmd` into `_site/index.html`. `validate_source.py` checks the slide order, one speaker-note block per slide, displayed calls, configuration snippets, SVG identifiers, source hashes, and literal capture text and images. `validate_site.py` rejects local links and resources that would be missing from the hosted HTML.

Run the commands in [README.md](README.md) after editing. The GitHub Actions workflow runs the same checks. Rendering validates the presentation, not the current behavior of every Console feature illustrated in it.

## Retained runtime evidence

The main sandboxed capture completed at `2026-09-17T21:17:43Z` with Console 0.0.3. Its executable SHA-256 is:

```text
44d7bb321a2d590fb9b16d7e91b4d8ca7821cb94fdab306a228232ac54bc0e4a
```

`captures/capture-manifest.json` identifies the executable and source cells. `captures/wire.jsonl` retains the MCP exchange; `captures/session-records/` contains the generated journal, transcripts, logs, and images. The wire capture and structured journal have different scopes. Repeated response files preserve individual frames and assembled results and are used by the provenance checks.

Runtime versions are recorded in `captures/versions.txt` and `captures/python-versions.txt`. Additional sessions have their own provenance:

- `captures/language-reveal/`: Python expressions, plotting, and both directions of R/Python object access.
- `captures/combined-input/`: restart, package requirements, queued input, and script evaluation in one request, with script and data hashes.
- `captures/controls/`: the earlier base-R script and restart/test examples.
- `captures/opening-demo/`: the penguins session, including errors and corrections, generated QMD, and the returned plot.
- `captures/sandbox-validation.json`: the earlier local macOS policy probes.

These recordings are historical evidence. Their local paths and session IDs identify the original environment; they are not setup instructions. The original collectors for the combined-input and control rehearsals are not supplied here. The recorded requests, results, and provenance remain available for inspection.

## Known limits

The reference `data.table==1.17.8` with unpinned `dtplyr` did **not** pass its package-installation rehearsals. R 4.6.1 rejected obsolete data.table C APIs; the R 4.5 attempt failed during dependency installation with `worker failed to
start`. The failed recordings remain in `captures/requirements/` and `captures/requirements-r45/`. Do not treat that version pin as a validated recipe.

The forked R output example uses a verified pipe to the native `cat` command. Plain `cat()` in the fork produced no visible output in the recorded build. The slide does not claim that every R output hook is fork-safe.

Linux enforcement, SSH, Docker, Docker Sandbox, and provider integrations were not exercised for this presentation. Provider examples were syntax-checked; running them makes real API calls. The standalone sandbox example was exercised on macOS with Console 0.0.4. SQL connection examples used RSQLite and Python sqlite3; other drivers and remote databases need their own setup.

The Docker slide follows the prepared-image contract at Console revision `ea5c1e737f329a86d957b12d7d1f15690824e398`, checked October 2, 2026. Docker sessions use preinstalled runtimes and packages. The referenced image recipe belongs to the Console repository; it was not built during this presentation update.

The platform slide was checked at the same revision: macOS and Linux are supported, Windows is not, and Python and SQL work without R. Other roadmap bullets preserve the author's design priorities rather than promise delivery. Proposed API and configuration slides remain labeled as ideas.

The repository-development figures are a September 18, 2026 snapshot. Their [data definitions and checks](examples/repository-development/README.md) explain the date range and classification. They are not current repository metrics.

Transcript excerpts and the editable report illustrate recording and curation. A transcript is not a complete environment lock; replay needs its packages, data, and connections. The package cutoff date in the report is author-added. The live demo and talk still need a timed rehearsal together.
