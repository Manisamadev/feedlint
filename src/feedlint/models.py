"""Core data types shared across feedlint."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

# A single product record, as loaded from JSON or CSV.
Product = dict[str, Any]


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Issue:
    """A single problem found in a feed."""

    rule_id: str
    severity: Severity
    message: str
    item_index: int | None = None  # 1-based position in the feed; None for feed-level issues
    item_id: str | None = None
    field: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


def is_blank(value: Any) -> bool:
    """Return True if a field value should be treated as missing."""
    return value is None or (isinstance(value, str) and value.strip() == "")
