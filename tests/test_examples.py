"""End-to-end checks against the sample feeds in examples/."""

import json
from pathlib import Path

import pytest

from feedlint.cli import EXIT_OK, EXIT_PROBLEMS, main
from feedlint.engine import lint
from feedlint.loader import load_feed
from feedlint.rules import ALL_RULES

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


@pytest.mark.parametrize("name", ["valid_products.json", "valid_products.csv"])
def test_valid_examples_pass(name):
    assert main(["check", str(EXAMPLES / name)]) == EXIT_OK


@pytest.mark.parametrize("name", ["invalid_products.json", "invalid_products.csv"])
def test_invalid_examples_trigger_every_rule(name, capsys):
    assert main(["check", str(EXAMPLES / name), "--format", "json"]) == EXIT_PROBLEMS
    report = json.loads(capsys.readouterr().out)
    assert {i["rule_id"] for i in report["issues"]} == {rule.id for rule in ALL_RULES}
    assert report["summary"]["errors"] > 0
    assert report["summary"]["warnings"] > 0


def test_json_and_csv_examples_agree():
    json_issues = lint(load_feed(EXAMPLES / "invalid_products.json"))
    csv_issues = lint(load_feed(EXAMPLES / "invalid_products.csv"))
    assert json_issues == csv_issues
