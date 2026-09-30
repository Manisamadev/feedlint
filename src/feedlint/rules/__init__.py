"""Registry of all built-in rules."""

from feedlint.rules.base import ItemRule, Rule
from feedlint.rules.required_fields import RequiredFieldsRule

# Add new rule classes here to enable them.
ALL_RULES: list[type[Rule]] = [
    RequiredFieldsRule,
]


def default_rules() -> list[Rule]:
    return [rule_cls() for rule_cls in ALL_RULES]


__all__ = ["ALL_RULES", "ItemRule", "Rule", "default_rules"]
