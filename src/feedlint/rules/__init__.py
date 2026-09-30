"""Registry of all built-in rules."""

from feedlint.rules.availability import AvailabilityRule
from feedlint.rules.base import ItemRule, Rule
from feedlint.rules.duplicate_id import DuplicateIdRule
from feedlint.rules.price_currency import PriceCurrencyRule
from feedlint.rules.required_fields import RequiredFieldsRule
from feedlint.rules.title_length import TitleLengthRule
from feedlint.rules.url_format import UrlFormatRule

# Add new rule classes here to enable them.
ALL_RULES: list[type[Rule]] = [
    RequiredFieldsRule,
    PriceCurrencyRule,
    AvailabilityRule,
    UrlFormatRule,
    DuplicateIdRule,
    TitleLengthRule,
]


def default_rules() -> list[Rule]:
    return [rule_cls() for rule_cls in ALL_RULES]


__all__ = ["ALL_RULES", "ItemRule", "Rule", "default_rules"]
