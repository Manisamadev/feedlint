import pytest

from feedlint.loader import FeedLoadError, load_feed


def write(tmp_path, name, content, encoding="utf-8"):
    path = tmp_path / name
    path.write_text(content, encoding=encoding)
    return path


def test_load_json_array(tmp_path):
    path = write(tmp_path, "feed.json", '[{"id": "A"}, {"id": "B"}]')
    assert load_feed(path) == [{"id": "A"}, {"id": "B"}]


def test_load_json_products_object(tmp_path):
    path = write(tmp_path, "feed.json", '{"products": [{"id": "A"}]}')
    assert load_feed(path) == [{"id": "A"}]


def test_load_csv(tmp_path):
    path = write(tmp_path, "feed.csv", "id,title\nA,Shirt\nB,Hat\n")
    assert load_feed(path) == [{"id": "A", "title": "Shirt"}, {"id": "B", "title": "Hat"}]


def test_load_csv_with_bom(tmp_path):
    path = write(tmp_path, "feed.csv", "id,title\nA,Shirt\n", encoding="utf-8-sig")
    assert load_feed(path) == [{"id": "A", "title": "Shirt"}]


def test_input_format_override(tmp_path):
    path = write(tmp_path, "feed.txt", '[{"id": "A"}]')
    assert load_feed(path, input_format="json") == [{"id": "A"}]


def test_unknown_extension(tmp_path):
    path = write(tmp_path, "feed.txt", "")
    with pytest.raises(FeedLoadError, match="--input-format"):
        load_feed(path)


def test_missing_file(tmp_path):
    with pytest.raises(FeedLoadError, match="File not found"):
        load_feed(tmp_path / "nope.json")


def test_invalid_json(tmp_path):
    path = write(tmp_path, "feed.json", "{not json")
    with pytest.raises(FeedLoadError, match="Invalid JSON"):
        load_feed(path)


def test_json_wrong_shape(tmp_path):
    path = write(tmp_path, "feed.json", '{"id": "A"}')
    with pytest.raises(FeedLoadError, match="array"):
        load_feed(path)


def test_json_non_object_item(tmp_path):
    path = write(tmp_path, "feed.json", '[{"id": "A"}, "oops"]')
    with pytest.raises(FeedLoadError, match="Item #2"):
        load_feed(path)


def test_empty_csv(tmp_path):
    path = write(tmp_path, "feed.csv", "")
    with pytest.raises(FeedLoadError, match="empty"):
        load_feed(path)


def test_csv_multiline_quoted_field(tmp_path):
    path = write(tmp_path, "feed.csv", 'id,description\nA,"Line one\nLine two"\n')
    assert load_feed(path) == [{"id": "A", "description": "Line one\nLine two"}]
