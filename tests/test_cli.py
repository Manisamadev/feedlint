import json

import pytest
from helpers import make_product

from feedlint.cli import EXIT_OK, EXIT_PROBLEMS, EXIT_USAGE, main


def write_feed(tmp_path, products, name="feed.json"):
    path = tmp_path / name
    path.write_text(json.dumps(products), encoding="utf-8")
    return str(path)


def test_clean_feed_exits_zero(tmp_path, capsys):
    path = write_feed(tmp_path, [make_product()])
    assert main(["check", path]) == EXIT_OK
    assert "no problems found (1 item checked)" in capsys.readouterr().out


def test_problems_exit_one(tmp_path, capsys):
    path = write_feed(tmp_path, [make_product(price="100")])
    assert main(["check", path]) == EXIT_PROBLEMS
    out = capsys.readouterr().out
    assert "price-currency" in out
    assert "Found 1 problem (1 error, 0 warnings) in 1 item" in out


def test_warnings_only_still_exit_one(tmp_path):
    path = write_feed(tmp_path, [make_product(title="x" * 500)])
    assert main(["check", path]) == EXIT_PROBLEMS


def test_json_output(tmp_path, capsys):
    path = write_feed(tmp_path, [make_product(), make_product(availability="yes")])
    assert main(["check", path, "--format", "json"]) == EXIT_PROBLEMS
    report = json.loads(capsys.readouterr().out)
    assert report["file"] == path
    assert report["summary"] == {
        "items_checked": 2,
        "items_with_problems": 1,
        "problems": 2,
        "errors": 2,
        "warnings": 0,
    }
    assert {i["rule_id"] for i in report["issues"]} == {"invalid-availability", "duplicate-id"}
    assert report["issues"][0]["severity"] == "error"


def test_json_output_keeps_non_ascii(tmp_path, capsys):
    path = write_feed(tmp_path, [make_product(id="商品-1", price="100")])
    main(["check", path, "--format", "json"])
    assert "商品-1" in capsys.readouterr().out


def test_missing_file_exits_two(tmp_path, capsys):
    assert main(["check", str(tmp_path / "nope.json")]) == EXIT_USAGE
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "File not found" in captured.err


def test_input_format_override(tmp_path):
    path = tmp_path / "feed.txt"
    path.write_text("id,title\nA,Hat\n", encoding="utf-8")
    assert main(["check", str(path), "--input-format", "csv"]) == EXIT_PROBLEMS


def test_bad_arguments_exit_two():
    with pytest.raises(SystemExit) as exc:
        main(["check"])
    assert exc.value.code == EXIT_USAGE
