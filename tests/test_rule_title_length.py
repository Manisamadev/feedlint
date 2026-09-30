from helpers import make_product

from feedlint import config
from feedlint.models import Severity
from feedlint.rules.title_length import TitleLengthRule

rule = TitleLengthRule()


def test_title_at_limit_is_ok():
    title = "x" * config.TITLE_MAX_LENGTH
    assert list(rule.check([make_product(title=title)])) == []


def test_title_over_limit_is_warning():
    title = "x" * (config.TITLE_MAX_LENGTH + 1)
    issues = list(rule.check([make_product(title=title)]))
    assert len(issues) == 1
    assert issues[0].severity is Severity.WARNING


def test_empty_title_is_left_to_required_rule():
    assert list(rule.check([make_product(title="")])) == []
