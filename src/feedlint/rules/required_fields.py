from __future__ import annotations

from collections.abc import Iterator

from feedlint import config
from feedlint.models import Issue, Product, Severity, is_blank
from feedlint.rules.base import ItemRule


class RequiredFieldsRule(ItemRule):
    """Every product must have a non-empty value for each required field.

    Other rules skip blank fields, so a missing field is reported only here.
    """

    id = "missing-required-field"
    description = "Required fields must be present and non-empty."

    def check_item(self, product: Product, index: int) -> Iterator[Issue]:
        for field in config.REQUIRED_FIELDS:
            if is_blank(product.get(field)):
                yield self.issue(
                    Severity.ERROR,
                    f"Missing required field '{field}'",
                    index=index,
                    product=product,
                    field=field,
                )
