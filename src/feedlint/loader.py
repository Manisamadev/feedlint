"""Load product feeds from JSON or CSV into a list of dicts."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from feedlint.models import Product

SUPPORTED_FORMATS = ("json", "csv")


class FeedLoadError(Exception):
    """Raised when a feed file cannot be read or parsed."""


def detect_format(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    if suffix in SUPPORTED_FORMATS:
        return suffix
    raise FeedLoadError(
        f"Cannot detect feed format from extension '{path.suffix}'. "
        "Use --input-format json|csv."
    )


def load_feed(path: str | Path, input_format: str | None = None) -> list[Product]:
    """Load a feed file and return its products.

    JSON feeds may be a top-level array of objects, or an object with a
    "products" array. CSV feeds must have a header row.
    """
    path = Path(path)
    fmt = input_format or detect_format(path)
    if fmt not in SUPPORTED_FORMATS:
        raise FeedLoadError(f"Unsupported input format: {fmt}")

    try:
        # utf-8-sig transparently strips a BOM (common in CSVs saved by Excel).
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise FeedLoadError(f"File not found: {path}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise FeedLoadError(f"Cannot read {path}: {exc}") from None

    if fmt == "json":
        return _parse_json(text)
    return _parse_csv(text)


def _parse_json(text: str) -> list[Product]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise FeedLoadError(f"Invalid JSON: {exc}") from None

    if isinstance(data, dict) and "products" in data:
        data = data["products"]
    if not isinstance(data, list):
        raise FeedLoadError(
            'JSON feed must be an array of products or an object with a "products" array.'
        )
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise FeedLoadError(f"Item #{index} is not a JSON object.")
    return data


def _parse_csv(text: str) -> list[Product]:
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if not reader.fieldnames:
        raise FeedLoadError("CSV feed is empty or has no header row.")
    products = []
    for row in reader:
        # Extra cells beyond the header are stored under the None key; drop them.
        row.pop(None, None)
        products.append(row)
    return products
