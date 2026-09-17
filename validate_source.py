#!/usr/bin/env python3
"""Check the authored deck, generated calls, capture provenance, and native HTML."""
from pathlib import Path
from html.parser import HTMLParser
import ast
import base64
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent


class Slides(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack = []
        self.slides = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attrs = dict(attrs)
        if tag == 'section':
            assert not self.stack, f'Unexpected nested slide: {attrs.get("id")}'
            item = {'id': attrs.get('id'), 'notes': 0}
            self.slides.append(item)
            self.stack.append(item)
        if tag == 'aside' and 'notes' in attrs.get('class', '').split():
            self.stack[-1]['notes'] += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == 'section':
            self.stack.pop()


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / 'sync_cells.py'), '--check'], check=True)
    source = (ROOT / 'deck.qmd').read_text()
    parts = re.split(r'(?m)(?=^## )', source)[1:]
    assert parts, 'No authored slides'
    ids = []
    cells = json.loads((ROOT / 'examples/cells.json').read_text())
    for part in parts:
        ids.append(re.search(r'\{#([\w-]+)', part)[1])
        assert len(re.findall(r'^::: \{\.notes\}$', part, re.M)) == 1, ids[-1]
    assert len(set(ids)) == len(ids)
    for code in re.findall(r'```(?:python|\{\.python[^}]*\})\n(.*?)\n```', source, re.S):
        for call in ast.walk(ast.parse(code)):
            if isinstance(call, ast.Call):
                for kw in call.keywords:
                    if kw.arg == 'python' and isinstance(kw.value, ast.Constant):
                        compile(kw.value.value, '<displayed Python cell>', 'exec')
    for names, code in re.findall(r'<!-- cells:([\w,-]+) -->\n```python\n(.*?)\n```', source, re.S):
        calls = ast.parse(code).body
        assert len(calls) == len(names.split(','))
        for name, expr in zip(names.split(','), calls):
            args = {kw.arg: ast.literal_eval(kw.value) for kw in expr.value.keywords}
            args = {k: v.strip('\n') if k in ('r', 'python', 'sql') else v for k,v in args.items()}
            assert args == cells[name], name
    svg_ids = []
    for svg in re.findall(r'<svg\b.*?</svg>', source, re.S):
        root = ET.fromstring(svg)
        svg_ids.extend(node.attrib['id'] for node in root.iter() if 'id' in node.attrib)
    assert len(set(svg_ids)) == len(svg_ids), 'Duplicate SVG identifiers'
    for asset in re.findall(r'<!-- inline-svg:([^\n]+) -->', source):
        assert (ROOT / asset).is_file(), f'Missing editable diagram asset: {asset}'
    manifest = json.loads((ROOT / 'captures/capture-manifest.json').read_text())
    assert manifest['source_cells'] == cells, 'Capture source is stale'
    wire = [json.loads(line) for line in (ROOT / 'captures/wire.jsonl').read_text().splitlines()]
    args = [row['message']['params']['arguments'] for row in wire if
            row['direction'] == 'client' and row['message'].get('method') == 'tools/call']
    i = args.index(cells['progress'])
    assert args[i+1:i+3] == [cells['poll-next'], cells['poll-final']]
    for name in ('fit','coefficients','predict','r-plot','compact','flood','error','checkpoint',
                 'prompt','prompt-answer','browser-start','browser-x','browser-continue',
                 'r-fork','python-fd','python-first','python-ml','python-plot','sql'):
        assert cells[name] in args, f'{name} was not submitted'
        result = json.loads((ROOT / f'captures/{name}.json').read_text())
        text = ''.join(b['text'] for b in result['content'] if b['type']=='text')
        assert (ROOT / f'captures/{name}.txt').read_bytes() == text.encode(), name
        images = [b for b in result['content'] if b['type']=='image']
        for i, image in enumerate(images, 1):
            assert (ROOT / f'captures/{name}-{i:02d}.png').read_bytes() == base64.b64decode(image['data'])
    assert (ROOT / 'captures/session-records/internal/events.jsonl').is_file()
    journal = [json.loads(line) for line in
               (ROOT / 'captures/session-records/internal/events.jsonl').read_text().splitlines()]
    event = next(item for item in journal if item.get('request', {}).get('_meta'))
    yaml_event = subprocess.check_output(
        ['yq', '-o=json', '.', str(ROOT / 'captures/excerpts/event-yaml.txt')], text=True)
    assert json.loads(yaml_event) == event
    assert (ROOT / 'captures/r-fork.txt').read_text() == 'native output\n'
    assert (ROOT / 'captures/python-fd.txt').read_text() == 'hello directly on fd 1\n'
    excerpts = json.loads((ROOT / 'captures/excerpts/provenance.json').read_text())
    for name, info in excerpts.items():
        lines = (ROOT / info['source']).read_text().splitlines(keepends=True)
        assert (ROOT / 'captures/excerpts' / name).read_text() == ''.join(
            lines[info['first_line']-1:info['last_line']]), name
    configs = json.loads((ROOT / 'examples/configs/index.json').read_text())
    for name, info in configs.items():
        if info['slide'] is None:
            continue  # Reference-only configuration, retained outside the deck.
        part = next(p for p in parts if f'{{#{info["slide"]} ' in p)
        assert (ROOT / 'examples/configs' / name).read_text().rstrip() in re.findall(
            r'```yaml\n(.*?)\n```', part, re.S), name
    html = Slides()
    html.feed((ROOT / 'mcp-console.html').read_text())
    assert [s['id'] for s in html.slides] == ids
    assert all(s['notes']==1 for s in html.slides)
    print(f'Validated {len(ids)} native slides, matching notes, displayed calls, SVG IDs, and MCP records.')


if __name__ == '__main__':
    main()
