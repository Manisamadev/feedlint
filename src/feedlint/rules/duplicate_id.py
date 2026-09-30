from __future__ import annotations

from collections.abc import Iterator

from feedlint.models import Issue, Product, Severity
from feedlint.rules.base import Rule, product_id


class DuplicateIdRule(Rule):
    """Each product id must be unique within the feed.

    The first occurrence is considered valid; every later one is reported.
    """

    id = "duplicate-id"
    description = "Product ids must be unique."

    def check(self, products: list[Product]) -> Iterator[Issue]:
        first_seen: dict[str, int] = {}
        for index, product in enumerate(products, start=1):
            pid = product_id(product)
            if pid is None:
                continue
            pid = pid.strip()
            if pid in first_seen:
                yield self.issue(
                    Severity.ERROR,
                    f"Duplicate id '{pid}' (first seen at item #{first_seen[pid]})",
                    index=index,
                    product=product,
                    field="id",
                )
            else:
                first_seen[pid] = index
