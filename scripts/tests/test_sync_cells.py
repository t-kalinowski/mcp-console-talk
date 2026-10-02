"""Exercise the source generator through its command-line entry point."""
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GeneratedCalls(unittest.TestCase):
    def test_readable_call_keeps_literal_arguments(self) -> None:
        arguments = {"r": "  library(dtplyr)\n  head(d)",
                     "requirements": {"r": ["dtplyr"]}}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            shutil.copy(ROOT / "scripts/sync_cells.py", root / "scripts")
            (root / "examples").mkdir()
            (root / "examples/cells.json").write_text(json.dumps({"example": arguments}))
            (root / "deck.qmd").write_text('<!-- cells:example -->\n```python\nold()\n```\n')
            subprocess.run([sys.executable, str(root / "scripts/sync_cells.py")], check=True)
            source = (root / "deck.qmd").read_text().split('```python\n')[1].split('```')[0]
            self.assertTrue(source.startswith('console.send(r="""\n  library'))
            self.assertIn('\n""",\n    requirements=', source)
            call = ast.parse(source).body[0].value
            actual = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
            actual['r'] = actual['r'].strip('\n')
            self.assertEqual(actual, arguments)
            subprocess.run([sys.executable, str(root / "scripts/sync_cells.py"), '--check'], check=True)


if __name__ == '__main__':
    unittest.main()
