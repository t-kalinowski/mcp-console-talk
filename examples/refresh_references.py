# /// script
# requires-python = ">=3.12"
# dependencies = ["scikit-learn==1.9.1", "pandas==3.0.5", "matplotlib==3.11.2"]
# ///
"""Recompute the native-preview Python references without starting Console."""
from pathlib import Path
from types import SimpleNamespace
from contextlib import redirect_stdout
import hashlib
import importlib.metadata as metadata
import io
import json
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
cells = json.loads((ROOT / 'examples/cells.json').read_text())
frame = pd.read_csv(ROOT / 'examples/measurements.csv')
namespace = {'r': SimpleNamespace(d=frame)}
output = io.StringIO()
with redirect_stdout(output):
    exec(cells['python-ml']['python'], namespace)
(ROOT / 'examples/python-ml-reference.txt').write_text(output.getvalue())
plt.figure(figsize=(7, 5.2), dpi=144)
exec(cells['python-plot']['python'], namespace)
plt.savefig(ROOT / 'assets/python-scatter.png')
plt.close()
(ROOT / 'examples/python-reference-provenance.json').write_text(json.dumps({
    'python': sys.version,
    'packages': {name: metadata.version(name) for name in ['scikit-learn', 'pandas', 'matplotlib']},
    'data_sha256': hashlib.sha256((ROOT / 'examples/measurements.csv').read_bytes()).hexdigest(),
    'source_cells': {name: cells[name] for name in ['python-ml', 'python-plot']},
    'method': 'Executed unchanged cell code with r.d bound to the measurements CSV; no model API',
}, indent=2)+'\n')
print(output.getvalue(), end='')
