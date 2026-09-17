#!/usr/bin/env python3
"""Render edited diagrams/*.dot to assets/*.svg; requires Graphviz dot.
Edit diagrams/timeout.svg directly for the manually laid-out timing diagram.
"""
from pathlib import Path
import shutil
import subprocess
ROOT = Path(__file__).resolve().parent

def main() -> None:
    if not shutil.which("dot"):
        raise SystemExit("Graphviz dot is required to rebuild diagram SVGs.")
    for source in sorted((ROOT / "diagrams").glob("*.dot")):
        target = ROOT / "assets" / (source.stem + ".svg")
        subprocess.run(["dot", "-Tsvg", str(source), "-o", str(target)], check=True)
    shutil.copyfile(ROOT / "diagrams" / "timeout.svg", ROOT / "assets" / "timeout.svg")
    print("Rebuilt diagrams from their editable sources.")

if __name__ == "__main__":
    main()
