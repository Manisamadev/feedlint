from __future__ import annotations

from collections.abc import Iterator

from feedlint import config
from feedlint.models import Issue, Product, Severity, is_blank
from feedlint.rules.base import ItemRule


class AvailabilityRule(ItemRule):
    """Availability must be one of the allowed values in config.ALLOWED_AVAILABILITY."""

    id = "invalid-availability"
    description = "Availability must be one of the allowed values."

    def check_item(self, product: Product, index: int) -> Iterator[Issue]:
        value = product.get("availability")
        if is_blank(value):
            return
        if str(value).strip() not in config.ALLOWED_AVAILABILITY:
            allowed = ", ".join(sorted(config.ALLOWED_AVAILABILITY))
            yield self.issue(
                Severity.ERROR,
                f"Invalid availability '{value}' (allowed: {allowed})",
                index=index,
                product=product,
                field="availability",
            )
