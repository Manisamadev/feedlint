from helpers import make_product

from feedlint.rules.duplicate_id import DuplicateIdRule

rule = DuplicateIdRule()


def test_unique_ids():
    products = [make_product(id="A"), make_product(id="B")]
    assert list(rule.check(products)) == []


def test_duplicates_report_every_later_occurrence():
    products = [make_product(id="A"), make_product(id="B"), make_product(id="A"), make_product(id="A")]
    issues = list(rule.check(products))
    assert [i.item_index for i in issues] == [3, 4]
    assert "first seen at item #1" in issues[0].message


def test_numeric_and_string_ids_compare_equal():
    # CSV always yields strings; JSON may yield numbers for the same id.
    products = [make_product(id=1), make_product(id="1")]
    assert len(list(rule.check(products))) == 1


def test_blank_ids_are_ignored():
    products = [make_product(id=""), make_product(id="")]
    assert list(rule.check(products)) == []
