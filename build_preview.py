#!/usr/bin/env python3
"""Render the presentation with Quarto's native reveal.js speaker view.

Requires Quarto on PATH. No custom viewer or Pandoc-only fallback is used.
For live preview, run: quarto preview deck.qmd
"""
from pathlib import Path
import shutil
import subprocess
import sys

from export_notes import export_notes

ROOT = Path(__file__).resolve().parent


def main() -> int:
    quarto = shutil.which("quarto")
    if quarto is None:
        print(
            "Quarto is required. Install Quarto, then run "
            "`quarto preview deck.qmd` or rerun this script.",
            file=sys.stderr,
        )
        return 1
    export_notes()
    result = subprocess.run(
        [quarto, "render", "deck.qmd", "--to", "revealjs"], cwd=ROOT
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
