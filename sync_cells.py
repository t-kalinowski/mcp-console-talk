#!/usr/bin/env python3
"""Generate displayed capture calls and R cells from examples/cells.json."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent


def display_call(arguments: dict) -> str:
    fields = []
    for name, value in arguments.items():
        if isinstance(value, str) and '\n' in value.rstrip('\n'):
            prefix = 'r' if '\\' in value else ''
            rendered = prefix + '\"\"\"\n' + value + '\n\"\"\"'
        else:
            rendered = repr(value)
        fields.append(f'{name}={rendered}')
    separator = ',\n    ' if 'requirements' in arguments else ', '
    return 'console.send(' + separator.join(fields) + ')'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    cells = json.loads((ROOT / 'examples/cells.json').read_text())
    r_source = '# Generated from examples/cells.json.\nconsole_cells <- list(\n'
    r_source += ',\n'.join(f'  {json.dumps(k)} = {json.dumps(v["r"])}'
                          for k, v in cells.items() if 'r' in v) + '\n)\n'
    deck = (ROOT / 'deck.qmd').read_text()
    deck = re.sub(r'<!-- cells:([\w,-]+) -->\n```python\n.*?\n```',
                  lambda m: m[0].split('```')[0] + '```python\n' +
                  '\n\n'.join(display_call(cells[k]) for k in m[1].split(',')) + '\n```',
                  deck, flags=re.S)
    for path, content in [(ROOT / 'examples/cells.R', r_source), (ROOT / 'deck.qmd', deck)]:
        if args.check:
            assert path.read_text() == content, f'{path.name} is stale; run python sync_cells.py'
        else:
            path.write_text(content)
    print('Cell source and displayed calls are synchronized.')


if __name__ == '__main__':
    main()
