# Repository development figures

These frozen inputs describe `t-kalinowski/mcp-console` from July 27 through
September 18, 2026. R and ggplot2 generated the figures through MCP Console.
The deck embeds the SVGs and does not query GitHub when rendered.

## Sources and scope

- `merged-prs.csv`: 298 merged PRs retrieved with `gh` at September 18,
  19:08:23 UTC. The timeline and largest-PR figures include only the 279 whose
  base branch was `main`. The 19 intermediate-branch merges are excluded.
- `pr-categories.csv`: per-file additions and deletions from those PRs,
  aggregated into the five categories below. Every PR total reconciles with
  its GitHub additions and deletions. Lines changed means additions plus
  deletions; net means additions minus deletions.
- `feature-milestones.csv`: six verified PRs, grouped into five capability
  annotations. The package milestone groups R #123 and Python #124, both
  merged on August 24. Linux means sandboxed Linux #262; the earlier
  unsandboxed support is not the annotated milestone.
- `repository-size.csv`: complete tracked file contents at each of the 307
  first-parent commits through main revision
  `657a5981983768967deed83c070973848ec800fb` (September 18, 19:43:53 UTC).
  This later endpoint includes #356, after the PR extraction above.
  `size-provenance.json` records the measurement and extraction details.

The repository-size series counts physical text lines, including blank lines,
comments, and a nonempty unterminated final line. It excludes untracked files,
Git metadata, non-regular tree entries, and binary files (a NUL in the first
8,000 bytes). Files are counted from each complete Git tree, so deletions reduce
the total and a pure file move does not change it. This is neither code-only
SLOC nor disk usage. Committer and merge times are in UTC.

## Categories

Rules are applied in order, at each historical path:

1. **Test transcripts:** `.yaml` or `.yml` files under `tests/`, `r/tests/`, or
   `python/tests/`, regardless of historical subdirectory.
2. Non-YAML files in `tests/snapshots/` or the historical
   `tests/transcripts/golden/` are **Test code & fixtures**.
3. **Docs & examples:** `docs/`, `design-sketches/`, `examples/`, `r/man/`, or
   files ending in `.md`, `.qmd`, `.rst`, or `.Rd`.
4. Remaining files in the test directories are **Test code & fixtures**.
5. **Core code:** remaining files under `src/`, `python/mcp_console/`, `r/R/`,
   or `r/src/`.
6. Everything else is **Build & tooling**, including CI configuration YAML.

This is a file classification: inline tests and documentation comments remain
with their containing core file. The same rules classify repository contents
and PR changes. GitHub rename handling determines a moved file's reported PR
additions and deletions; PR diff volume is not repository growth.

The proportion chart divides each category by the total at the same commit.
Every date sums to 100% before rounding. The legend gives the final shares.
The initial 21-line repository makes early proportions particularly sensitive
to small changes. Shares describe contents, not effort, coverage, or quality.

## Checks and reproduction

`archive-verification.json` records independent line-count checks from Git
archives at the first, midpoint, largest-drop, and final snapshots.
`transcript-split-verification.json` confirms that the five-category split
preserves all 307 totals and combined test counts. Around the #197 test
reorganization, YAML transcript lines remain 17,224 on both sides.

`plot.R` asserts category sums, proportion sums, the pinned endpoint, and the
main-branch PR population. It constructs explicit stepped area boundaries to
handle several commits with the same timestamp. To regenerate the five SVGs,
PNGs, and latest-share table from the presentation directory:

```sh
Rscript examples/repository-development/plot.R examples/repository-development assets/repository-development
```

Required R packages: ggplot2, dplyr, tidyr, patchwork, scales, and svglite.
`collect-snapshots.py` is the original Git-tree collector; it accepts a local
repository path, revision, and output directory. Chart rendering uses the
supplied CSVs, without a live checkout or network connection.

The workflow slides describe the instructions in `AGENTS.md` and
`docs/DEVELOPMENT.md` at the pinned revision. They are not an audit of historical
compliance with those instructions.
