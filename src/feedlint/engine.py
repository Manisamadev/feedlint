"""Run rules against a feed and collect issues."""

from __future__ import annotations

from feedlint.models import Issue, Product
from feedlint.rules import Rule, default_rules


def lint(products: list[Product], rules: list[Rule] | None = None) -> list[Issue]:
    """Return all issues found, ordered by item (feed-level issues first)."""
    if rules is None:
        rules = default_rules()
    issues = [issue for rule in rules for issue in rule.check(products)]
    # Stable sort: within an item, issues keep rule registration order.
    issues.sort(key=lambda issue: issue.item_index or 0)
    return issues
