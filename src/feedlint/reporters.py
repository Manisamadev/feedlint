"""Format lint results for humans (text) or machines (JSON)."""

from __future__ import annotations

import json
from typing import Any

from feedlint.models import Issue, Severity

FORMATS = ("text", "json")


def summarize(issues: list[Issue], item_count: int) -> dict[str, int]:
    errors = sum(1 for i in issues if i.severity is Severity.ERROR)
    return {
        "items_checked": item_count,
        "items_with_problems": len({i.item_index for i in issues if i.item_index is not None}),
        "problems": len(issues),
        "errors": errors,
        "warnings": len(issues) - errors,
    }


def render(fmt: str, file: str, issues: list[Issue], item_count: int) -> str:
    if fmt == "json":
        return render_json(file, issues, item_count)
    return render_text(file, issues, item_count)


def render_json(file: str, issues: list[Issue], item_count: int) -> str:
    report: dict[str, Any] = {
        "file": file,
        "summary": summarize(issues, item_count),
        "issues": [issue.to_dict() for issue in issues],
    }
    # ensure_ascii=False keeps non-ASCII product data (e.g. Japanese titles) readable.
    return json.dumps(report, indent=2, ensure_ascii=False)


def render_text(file: str, issues: list[Issue], item_count: int) -> str:
    summary = summarize(issues, item_count)
    if not issues:
        return f"{file}: no problems found ({_plural(item_count, 'item')} checked)"

    rows = [
        (
            f"#{i.item_index}" if i.item_index is not None else "feed",
            f"id={i.item_id}" if i.item_id is not None else "id=-",
            i.severity.value,
            i.rule_id,
            i.message,
        )
        for i in issues
    ]
    # Pad every column except the last (the message) to its widest value.
    widths = [max(len(row[col]) for row in rows) for col in range(len(rows[0]) - 1)]
    lines = [file]
    for row in rows:
        cells = [cell.ljust(width) for cell, width in zip(row, widths)] + [row[-1]]
        lines.append("  " + "  ".join(cells))

    lines.append(
        f"Found {_plural(summary['problems'], 'problem')} "
        f"({_plural(summary['errors'], 'error')}, {_plural(summary['warnings'], 'warning')}) "
        f"in {_plural(summary['items_with_problems'], 'item')} "
        f"({item_count} checked)."
    )
    return "\n".join(lines)


def _plural(count: int, word: str) -> str:
    return f"{count} {word}" if count == 1 else f"{count} {word}s"
