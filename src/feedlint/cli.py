"""Command-line interface.

Exit codes:
  0  no problems found
  1  one or more problems (errors or warnings) found
  2  the feed could not be checked (bad arguments, unreadable or malformed file)
"""

from __future__ import annotations

import argparse
import sys

from feedlint import __version__
from feedlint.engine import lint
from feedlint.loader import SUPPORTED_FORMATS, FeedLoadError, load_feed
from feedlint.reporters import FORMATS, render

EXIT_OK = 0
EXIT_PROBLEMS = 1
EXIT_USAGE = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="feedlint",
        description="Lint e-commerce product feeds (JSON/CSV).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Check a product feed file.")
    check.add_argument("file", help="Path to a .json or .csv product feed.")
    check.add_argument(
        "--format",
        choices=FORMATS,
        default="text",
        help="Output format (default: text).",
    )
    check.add_argument(
        "--input-format",
        choices=SUPPORTED_FORMATS,
        help="Feed format. Detected from the file extension if omitted.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        products = load_feed(args.file, args.input_format)
    except FeedLoadError as exc:
        print(f"feedlint: error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    issues = lint(products)
    print(render(args.format, args.file, issues, len(products)))
    return EXIT_PROBLEMS if issues else EXIT_OK
