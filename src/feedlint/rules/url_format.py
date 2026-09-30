from __future__ import annotations

from collections.abc import Iterator
from urllib.parse import urlparse

from feedlint import config
from feedlint.models import Issue, Product, Severity, is_blank
from feedlint.rules.base import ItemRule


def is_valid_url(value: str) -> bool:
    """Return True for an absolute http(s) URL with a host and no whitespace."""
    if any(ch.isspace() for ch in value):
        return False
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


class UrlFormatRule(ItemRule):
    """URL fields must contain an absolute http(s) URL.

    This checks format only; it never makes network requests.
    """

    id = "invalid-url"
    description = "URL fields must be absolute http(s) URLs."

    def check_item(self, product: Product, index: int) -> Iterator[Issue]:
        for field in config.URL_FIELDS:
            value = product.get(field)
            if is_blank(value):
                continue
            url = str(value).strip()
            if not is_valid_url(url):
                yield self.issue(
                    Severity.ERROR,
                    f"Invalid URL in '{field}': '{url}' (expected an absolute http(s) URL)",
                    index=index,
                    product=product,
                    field=field,
                )
