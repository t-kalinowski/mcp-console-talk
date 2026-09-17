#!/usr/bin/env python3
"""Extract literal slide excerpts; retain the full original capture files."""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / 'captures'


def main() -> None:
    out = CAPTURES / 'excerpts'
    out.mkdir(exist_ok=True)
    provenance = {}

    def excerpt(name: str, source: Path, start: int, end: int) -> None:
        lines = source.read_text().splitlines(keepends=True)
        assert 0 <= start < end <= len(lines)
        (out / name).write_text(''.join(lines[start:end]))
        provenance[name] = {'source': str(source.relative_to(ROOT)),
                            'first_line': start + 1, 'last_line': end,
                            'normalization': None}

    flood = CAPTURES / 'flood.txt'
    lines = flood.read_text().splitlines()
    marker = next(i for i, line in enumerate(lines) if line.startswith('[output preview:'))
    excerpt('flood-head.txt', flood, 0, 3)
    excerpt('flood-marker.txt', flood, marker, marker+1)
    excerpt('flood-tail.txt', flood, len(lines)-3, len(lines))
    md = CAPTURES / 'session-records/transcript.md'
    text = md.read_text()
    match = re.search(r'(?m)^## Call (\d+): R\n\n```r\ncoef\(fit\)\n```', text)
    assert match
    start = text[:match.start()].count('\n')
    end_offset = text.index(f'## Call {int(match[1])+1}:', match.end())
    excerpt('markdown.txt', md, start, text[:end_offset].count('\n'))
    qmd = CAPTURES / 'session-records/transcript.qmd'
    text = qmd.read_text()
    excerpt('quarto-header.txt', qmd, 0, text[:text.index('\n---',3)+4].count('\n')+1)
    start_offset = re.search(r'```\{r\}\n\s*d <- read.csv\(', text).start()
    end_offset = text.index('\n```', start_offset+4)+4
    excerpt('quarto-cell.txt', qmd, text[:start_offset].count('\n'), text[:end_offset].count('\n')+1)
    lines = md.read_text().splitlines()
    call = re.search(r'(?m)^## Call (\d+): R\n\n```r\n\s*d <- read.csv', md.read_text())[1]
    raw = CAPTURES / f'session-records/outputs/call-{int(call):06d}.log'
    excerpt('recorded-fit.txt', raw, 0, len(raw.read_text().splitlines()))
    (out / 'provenance.json').write_text(json.dumps(provenance, indent=2)+'\n')
    journal = CAPTURES / 'session-records/internal/events.jsonl'
    event = next(json.loads(line) for line in journal.read_text().splitlines()
                 if json.loads(line).get('request', {}).get('_meta'))
    # YAML changes serialization only; preserve every recorded field.
    converted = subprocess.run(['yq', '-P', '-p=json', '.'], input=json.dumps(event),
                               text=True, capture_output=True, check=True).stdout
    (out / 'event-yaml.txt').write_text(converted)
    restored = subprocess.run(['yq', '-o=json', '.'], input=converted,
                             text=True, capture_output=True, check=True).stdout
    assert json.loads(restored) == event
    print(f'Extracted {len(provenance)} literal excerpts without normalization.')


if __name__ == '__main__':
    main()
