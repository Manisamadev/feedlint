from __future__ import annotations

import re
from collections.abc import Iterator

from feedlint.models import Issue, Product, Severity, is_blank
from feedlint.rules.base import ItemRule

# TODO: Verify against official specs - some specs put the currency in a
# separate field, use minor units, or allow thousands separators.
PRICE_PATTERN = re.compile(r"^\d+(\.\d+)? [A-Z]{3}$")
NUMBER_ONLY_PATTERN = re.compile(r"^\d+(\.\d+)?$")


class PriceCurrencyRule(ItemRule):
    """Price must be a number followed by a 3-letter currency code, e.g. "12000 JPY"."""

    id = "price-currency"
    description = "Price must include a currency code (e.g. '12000 JPY')."

    def check_item(self, product: Product, index: int) -> Iterator[Issue]:
        value = product.get("price")
        if is_blank(value):
            return
        price = str(value).strip()
        if PRICE_PATTERN.match(price):
            return
        if NUMBER_ONLY_PATTERN.match(price):
            message = f"Price '{price}' has no currency code (expected e.g. '12000 JPY')"
        else:
            message = (
                f"Price '{price}' is not in the expected format "
                "'<amount> <CURRENCY>' (e.g. '12000 JPY')"
            )
        yield self.issue(Severity.ERROR, message, index=index, product=product, field="price")
