import pytest
from helpers import make_product

from feedlint.models import Severity
from feedlint.rules.price_currency import PriceCurrencyRule

rule = PriceCurrencyRule()


def issues_for(price):
    return list(rule.check([make_product(price=price)]))


@pytest.mark.parametrize("price", ["12000 JPY", "19.99 USD", "0 EUR"])
def test_valid_prices(price):
    assert issues_for(price) == []


@pytest.mark.parametrize("price", ["12000", 12000, "19.99"])
def test_missing_currency(price):
    issues = issues_for(price)
    assert len(issues) == 1
    assert "no currency code" in issues[0].message
    assert issues[0].severity is Severity.ERROR


@pytest.mark.parametrize("price", ["JPY 12000", "12000JPY", "12,000 JPY", "12000 jpy", "free"])
def test_bad_format(price):
    issues = issues_for(price)
    assert len(issues) == 1
    assert "expected format" in issues[0].message


def test_missing_price_is_left_to_required_rule():
    assert list(rule.check([make_product(price=None)])) == []
