"""Base classes for lint rules.

To add a rule:
  1. Create a new module in feedlint/rules/ with a subclass of Rule or ItemRule.
  2. Register the class in ALL_RULES in feedlint/rules/__init__.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import ClassVar

from feedlint.models import Issue, Product, Severity, is_blank


class Rule(ABC):
    """A rule that inspects the whole feed at once (e.g. cross-item checks)."""

    id: ClassVar[str]
    description: ClassVar[str]

    @abstractmethod
    def check(self, products: list[Product]) -> Iterator[Issue]:
        """Yield an Issue for every problem found."""

    def issue(
        self,
        severity: Severity,
        message: str,
        *,
        index: int | None = None,
        product: Product | None = None,
        field: str | None = None,
    ) -> Issue:
        """Build an Issue tagged with this rule's id."""
        return Issue(
            rule_id=self.id,
            severity=severity,
            message=message,
            item_index=index,
            item_id=product_id(product) if product is not None else None,
            field=field,
        )


class ItemRule(Rule):
    """A rule that inspects one product at a time."""

    def check(self, products: list[Product]) -> Iterator[Issue]:
        for index, product in enumerate(products, start=1):
            yield from self.check_item(product, index)

    @abstractmethod
    def check_item(self, product: Product, index: int) -> Iterator[Issue]:
        """Yield an Issue for every problem found in a single product."""


def product_id(product: Product) -> str | None:
    value = product.get("id")
    return None if is_blank(value) else str(value)
