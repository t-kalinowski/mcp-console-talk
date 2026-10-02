#!/usr/bin/env python3
"""Render edited assets/diagrams/*.dot to assets/*.svg; requires Graphviz dot.
Edit assets/diagrams/*.svg directly for the manually laid-out diagrams.
"""
from pathlib import Path
import re
import shutil
import subprocess
ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    if not shutil.which("dot"):
        raise SystemExit("Graphviz dot is required to rebuild diagram SVGs.")
    for source in sorted((ROOT / "assets/diagrams").glob("*.dot")):
        target = ROOT / "assets" / (source.stem + ".svg")
        subprocess.run(["dot", "-Tsvg", str(source), "-o", str(target)], check=True)
    for source in sorted((ROOT / "assets/diagrams").glob("*.svg")):
        shutil.copyfile(source, ROOT / "assets" / source.name)
    deck = ROOT / "deck.qmd"
    pattern = r'<!-- inline-svg:([^\n]+) -->\n```\{=html\}\n(.*?)\n```\n<!-- /inline-svg -->'
    count = 0

    def embed(match: re.Match) -> str:
        nonlocal count
        count += 1
        source = (ROOT / match[1]).read_text()
        svg = source[source.index("<svg"):].strip()
        label = re.search(r'aria-label="([^"]+)"', match[2])
        assert label, f"Missing diagram label: {match[1]}"
        svg = re.sub(r' (?:role|aria-label)="[^\"]*"', "", svg, count=2)
        svg = svg.replace("<svg ", f'<svg role="img" aria-label="{label[1]}" ', 1)
        for identifier in re.findall(r'\bid="([^"]+)"', svg):
            replacement = f"diagram-{count}-{identifier}"
            svg = svg.replace(f'id="{identifier}"', f'id="{replacement}"')
            svg = svg.replace(f'"#{identifier}"', f'"#{replacement}"')
        return (f'<!-- inline-svg:{match[1]} -->\n```{{=html}}\n'
                f'<div class="embedded-diagram">\n{svg}\n</div>\n```\n<!-- /inline-svg -->')

    deck.write_text(re.sub(pattern, embed, deck.read_text(), flags=re.S))
    assert count, "No embedded diagrams found"
    print(f"Rebuilt diagrams and refreshed {count} inline SVGs.")

if __name__ == "__main__":
    main()
