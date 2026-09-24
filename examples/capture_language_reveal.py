"""Capture the Python and R bridge examples through the public MCP send tool.

Usage: python examples/capture_language_reveal.py OUT EXECUTABLE
"""

from pathlib import Path
import hashlib
import json
import shutil
import sys
import time

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'examples'))
from capture_console import StdioMCP, complete

assert len(sys.argv) == 3, __doc__
out = Path(sys.argv[1]).resolve()
assert not (out / 'wire.jsonl').exists()
out.mkdir(parents=True, exist_ok=True)
cells = json.loads((root / 'captures/language-reveal/cells.json').read_text())
(out / 'cells.json').write_text(json.dumps(cells, indent=2) + '\n')
command = [sys.argv[2], 'serve']
runs = root / '.agents/console/sessions'
before = set(runs.iterdir())
executable_hash = hashlib.sha256(Path(command[0]).resolve().read_bytes()).hexdigest()
client = StdioMCP(command, out)
try:
    init = client.initialize()
    complete(client, out, 'warmup', {'r': 'invisible(NULL)', 'timeout_ms': 30000})
    fit = json.loads((root / 'examples/cells.json').read_text())['fit']
    complete(client, out, 'fit', fit)
    for name, cell in cells.items():
        print('Capturing ' + name, flush=True)
        complete(client, out, name, cell)
    assert (out / 'python-simple.txt').read_text() == '17\n'
    assert (out / 'python-read-r.txt').read_text() == '240\n'
    assert (out / 'r-read-python.txt').read_text() == '[1] 4\n'
    assert (out / 'python-simple-plot-01.png').is_file()
    assert executable_hash == hashlib.sha256(Path(command[0]).resolve().read_bytes()).hexdigest(), 'Executable changed during capture'
    (out / 'provenance.json').write_text(json.dumps({
        'captured_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'command': command, 'cwd': str(root), 'initialize': init,
        'executable_sha256': executable_hash,
        'executable_unchanged_during_capture': True,
        'data_sha256': hashlib.sha256((root / 'examples/measurements.csv').read_bytes()).hexdigest(),
        'source_cells': cells, 'setup_cell': fit,
        'sandboxed': True, 'model_api_used': False,
    }, indent=2) + '\n')
finally:
    client.close()
    created = set(runs.iterdir()) - before
    assert len(created) == 1, created
    shutil.copytree(created.pop(), out / 'session-records')
print('All language reveal captures passed.')
