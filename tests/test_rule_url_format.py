import pytest
from helpers import make_product

from feedlint.rules.url_format import UrlFormatRule

rule = UrlFormatRule()


@pytest.mark.parametrize(
    "url",
    ["https://example.com/p/1", "http://example.com", "https://shop.example.co.jp/a?b=c#d"],
)
def test_valid_urls(url):
    assert list(rule.check([make_product(link=url, image_link=url)])) == []


@pytest.mark.parametrize(
    "url",
    [
        "example.com/p/1",
        "/products/1",
        "ftp://example.com/file",
        "https://",
        "https://example.com/my product",
        "javascript:alert(1)",
    ],
)
def test_invalid_urls(url):
    issues = list(rule.check([make_product(image_link=url)]))
    assert [i.field for i in issues] == ["image_link"]


def test_checks_both_url_fields():
    issues = list(rule.check([make_product(link="bad", image_link="also-bad")]))
    assert [i.field for i in issues] == ["link", "image_link"]
