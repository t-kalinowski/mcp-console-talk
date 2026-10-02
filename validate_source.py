#!/usr/bin/env python3
"""Check the authored deck, generated calls, capture provenance, and native HTML."""
from pathlib import Path
from html.parser import HTMLParser
import ast
import base64
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import yaml

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
                 'r-fork','r-fork-cat','python-fd','python-first','python-ml','python-plot','sql'):
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
    yaml_event = yaml.safe_load((ROOT / 'captures/excerpts/event-yaml.txt').read_text())
    assert yaml_event == event
    assert (ROOT / 'captures/r-fork.txt').read_text() == 'native output\n'
    assert (ROOT / 'captures/r-fork-cat.txt').read_text() == 'hello from fork\n'
    assert (ROOT / 'captures/python-fd.txt').read_text() == 'hello directly on fd 1\n23\n'
    controls = ROOT / 'captures/controls'
    control_cells = json.loads((controls / 'cells.json').read_text())
    control_provenance = json.loads((controls / 'provenance.json').read_text())
    assert hashlib.sha256((ROOT / 'examples/analyze.R').read_bytes()).hexdigest() == control_provenance['script_sha256']
    assert hashlib.sha256((ROOT / 'examples/measurements.csv').read_bytes()).hexdigest() == control_provenance['data_sha256']
    control_wire = [json.loads(line) for line in (controls / 'wire.jsonl').read_text().splitlines()]
    control_args = [row['message']['params']['arguments'] for row in control_wire if
                    row['direction'] == 'client' and row['message'].get('method') == 'tools/call']
    for name, arguments in control_cells.items():
        assert arguments in control_args, f'{name} was not submitted'
        response = json.loads((controls / f'{name}.json').read_text())
        text = ''.join(block['text'] for block in response['content'] if block['type'] == 'text')
        assert (controls / f'{name}.txt').read_bytes() == text.encode(), name
        assert '[worker stopped: in-memory state lost]' in text and text.endswith('[done]'), name
    assert 'FAIL 0' in (controls / 'restart-test.txt').read_text()
    assert 'Group to summarize:' in (controls / 'restart-script.txt').read_text()
    reveal = ROOT / 'captures/language-reveal'
    reveal_cells = json.loads((reveal / 'cells.json').read_text())
    assert json.loads((reveal / 'provenance.json').read_text())['source_cells'] == reveal_cells
    reveal_wire = [json.loads(line) for line in (reveal / 'wire.jsonl').read_text().splitlines()]
    reveal_args = [row['message']['params']['arguments'] for row in reveal_wire if
                   row['direction'] == 'client' and row['message'].get('method') == 'tools/call']
    for name, arguments in reveal_cells.items():
        assert arguments in reveal_args, f'{name} was not submitted'
        result = json.loads((reveal / f'{name}.json').read_text())
        text = ''.join(block['text'] for block in result['content'] if block['type'] == 'text')
        assert (reveal / f'{name}.txt').read_bytes() == text.encode(), name
        images = [block for block in result['content'] if block['type'] == 'image']
        for i, image in enumerate(images, 1):
            assert (reveal / f'{name}-{i:02d}.png').read_bytes() == base64.b64decode(image['data'])
    for name, code in re.findall(r'<!-- reveal-cell:([\w-]+) -->\n```python\n(.*?)\n```', source, re.S):
        call = ast.parse(code).body[0].value
        arguments = {kw.arg: ast.literal_eval(kw.value).strip('\n') for kw in call.keywords}
        assert arguments == reveal_cells[name], name
    script_slide = next(part for part in parts if '{#restart-input ' in part)
    assert (ROOT / 'examples/summarize.R').read_text().rstrip() in re.findall(r'```r\n(.*?)\n```', script_slide, re.S)
    combined = ROOT / 'captures/combined-input'
    combined_cells = json.loads((combined / 'cells.json').read_text())
    provenance = json.loads((combined / 'provenance.json').read_text())
    assert hashlib.sha256((ROOT / provenance['script']).read_bytes()).hexdigest() == provenance['script_sha256']
    assert hashlib.sha256((ROOT / 'examples/measurements.csv').read_bytes()).hexdigest() == provenance['data_sha256']
    combined_wire = [json.loads(line) for line in (combined / 'wire.jsonl').read_text().splitlines()]
    for name, code in re.findall(r'<!-- combined-cell:([\w-]+) -->\n```python\n(.*?)\n```', source, re.S):
        call = ast.parse(code).body[0].value
        arguments = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
        assert arguments == combined_cells[name], name
        requests = [row['message'] for row in combined_wire if row['direction'] == 'client'
                    and row['message'].get('method') == 'tools/call'
                    and row['message']['params']['arguments'] == arguments]
        assert len(requests) == 1, name
        responses = [row['message']['result'] for row in combined_wire if row['direction'] == 'server'
                     and row['message'].get('id') == requests[0]['id']]
        response = json.loads((combined / f'{name}.json').read_text())
        assert responses == [response], name
        text = ''.join(block['text'] for block in response['content'] if block['type'] == 'text')
        assert (combined / f'{name}.txt').read_bytes() == text.encode(), name
        assert '[worker stopped: in-memory state lost]' in text and text.endswith('[done]'), name
    for name, code in re.findall(r'<!-- control-cell:([\w-]+) -->\n```python\n(.*?)\n```', source, re.S):
        call = ast.parse(code).body[0].value
        arguments = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
        arguments = {k: v.strip('\n') if k in ('r', 'python', 'sql') else v for k, v in arguments.items()}
        assert arguments == control_cells[name], name
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
    html.feed((ROOT / '_site/index.html').read_text())
    assert [s['id'] for s in html.slides] == ids
    assert all(s['notes']==1 for s in html.slides)
    print(f'Validated {len(ids)} native slides, matching notes, displayed calls, SVG IDs, and MCP records.')


if __name__ == '__main__':
    main()
