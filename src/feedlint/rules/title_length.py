from __future__ import annotations

from collections.abc import Iterator

from feedlint import config
from feedlint.models import Issue, Product, Severity, is_blank
from feedlint.rules.base import ItemRule


class TitleLengthRule(ItemRule):
    """Title should not exceed config.TITLE_MAX_LENGTH characters.

    Empty titles are reported by the missing-required-field rule.
    """

    id = "title-length"
    description = "Title should not be excessively long."

    def check_item(self, product: Product, index: int) -> Iterator[Issue]:
        value = product.get("title")
        if is_blank(value):
            return
        length = len(str(value).strip())
        if length > config.TITLE_MAX_LENGTH:
            yield self.issue(
                Severity.WARNING,
                f"Title is {length} characters (max {config.TITLE_MAX_LENGTH})",
                index=index,
                product=product,
                field="title",
            )
