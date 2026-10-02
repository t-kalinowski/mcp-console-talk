"""Check the deployable HTML through the validation command."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublishedSite(unittest.TestCase):
    def test_embedded_resources_and_public_links(self) -> None:
        html = '<img src="data:image/png;base64,AA=="><a href="https://example.com">Source</a><a href="#slide">Next</a>'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            path.write_text(html)
            result = subprocess.run(
                [sys.executable, str(ROOT / "validate_site.py"), str(path)],
                capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_files_outside_the_published_html(self) -> None:
        for html in ('<img src="assets/plot.png">',
                     '<link href="styles.css" rel="stylesheet">',
                     '<a href="examples/README.md">Source</a>'):
            with self.subTest(html=html), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "index.html"
                path.write_text(html)
                result = subprocess.run(
                    [sys.executable, str(ROOT / "validate_site.py"), str(path)],
                    capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Unpublished local URL", result.stderr)


if __name__ == "__main__":
    unittest.main()
