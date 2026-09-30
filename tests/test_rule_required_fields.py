import pytest
from helpers import make_product

from feedlint import config
from feedlint.models import Severity
from feedlint.rules.required_fields import RequiredFieldsRule

rule = RequiredFieldsRule()


def test_valid_product():
    assert list(rule.check([make_product()])) == []


@pytest.mark.parametrize("field", config.REQUIRED_FIELDS)
def test_missing_field(field):
    issues = list(rule.check([make_product(**{field: None})]))
    assert len(issues) == 1
    assert issues[0].field == field
    assert issues[0].severity is Severity.ERROR
    assert issues[0].item_index == 1


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_field_counts_as_missing(blank):
    issues = list(rule.check([make_product(title=blank)]))
    assert [i.field for i in issues] == ["title"]


def test_item_id_is_reported():
    issues = list(rule.check([make_product(id="SKU-9", price=None)]))
    assert issues[0].item_id == "SKU-9"
