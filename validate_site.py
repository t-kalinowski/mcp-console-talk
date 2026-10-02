#!/usr/bin/env python3
"""Reject local URLs that would break when publishing the embedded HTML alone."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class PublishedHTML(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list) -> None:
        for name, value in attrs:
            if name not in ("src", "href") or not value or value.startswith("#"):
                continue
            if urlsplit(value).scheme not in ("https", "http", "data", "mailto"):
                raise SystemExit(f"Unpublished local URL in <{tag}>: {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", nargs="?", type=Path, default=Path("_site/index.html"))
    args = parser.parse_args()
    PublishedHTML().feed(args.html.read_text(encoding="utf-8"))
    print(f"Validated publication URLs in {args.html}.")


if __name__ == "__main__":
    main()
