import pytest
from helpers import make_product

from feedlint import config
from feedlint.rules.availability import AvailabilityRule

rule = AvailabilityRule()


@pytest.mark.parametrize("value", sorted(config.ALLOWED_AVAILABILITY))
def test_allowed_values(value):
    assert list(rule.check([make_product(availability=value)])) == []


@pytest.mark.parametrize("value", ["in stock", "In_Stock", "sold_out", "yes"])
def test_invalid_values(value):
    issues = list(rule.check([make_product(availability=value)]))
    assert len(issues) == 1
    assert issues[0].field == "availability"
    assert "in_stock" in issues[0].message  # lists allowed values


def test_missing_availability_is_left_to_required_rule():
    assert list(rule.check([make_product(availability="")])) == []
