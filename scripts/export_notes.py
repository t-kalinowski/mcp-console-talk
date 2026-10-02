#!/usr/bin/env python3
"""Export optional reading copies from the notes embedded in deck.qmd.

The QMD is authoritative. Rendering slides does not need speaker-notes.md.
Requires only Python 3.10+.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def export_notes() -> int:
    source = (ROOT / "deck.qmd").read_text(encoding="utf-8")
    sections = re.split(r"(?m)(?=^## )", source)[1:]
    notes = [
        "# MCP Console — speaker notes\n",
        "Generated from the native `.notes` blocks in `deck.qmd`. "
        "Edit that file, not this reading copy.\n",
    ]
    index = []
    for number, section in enumerate(sections, 1):
        heading, body = section.split("\n", 1)
        title_match = re.fullmatch(r"## (.*?)\s*\{(.*?)\}\s*", heading)
        if not title_match:
            raise ValueError(f"Slide {number} has an invalid heading: {heading}")
        title, attrs = title_match.groups()
        id_match = re.search(r"#([\w-]+)", attrs)
        note_blocks = re.findall(
            r"(?ms)^::: \{\.notes\}\s*\n(.*?)^:::\s*$", body
        )
        if not id_match or len(note_blocks) != 1:
            raise ValueError(f"Slide {number} needs an ID and exactly one notes block")
        kicker = re.search(r"::: \{\.kicker\}\s*\n(.*?)\n\s*:::", body, re.S)
        notes.append(f"\n## {number:02d}. {title}\n\n{note_blocks[0].strip()}\n")
        index.append({
            "number": number, "title": title, "id": id_match.group(1),
            "section": kicker.group(1).strip() if kicker else "",
        })
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    (output / "speaker-notes.md").write_text("\n".join(notes), encoding="utf-8")
    (output / "slide-index.json").write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8"
    )
    return len(sections)


if __name__ == "__main__":
    print(f"Exported notes for {export_notes()} slides from deck.qmd")
