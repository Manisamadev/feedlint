from helpers import make_product

from feedlint.engine import lint
from feedlint.models import Severity
from feedlint.rules import Rule, default_rules


class FeedLevelRule(Rule):
    id = "feed-level"
    description = "Always reports one feed-level issue."

    def check(self, products):
        yield self.issue(Severity.WARNING, "feed-level problem")


def test_valid_feed_has_no_issues():
    assert lint([make_product(), make_product(id="SKU-002")]) == []


def test_empty_feed_has_no_issues():
    assert lint([]) == []


def test_issues_sorted_by_item_with_feed_level_first():
    products = [make_product(), make_product(title="")]
    issues = lint(products, rules=[*default_rules(), FeedLevelRule()])
    assert [i.item_index for i in issues] == [None, 2]
