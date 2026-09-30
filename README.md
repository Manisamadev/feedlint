# feedlint

A command-line linter for e-commerce product feeds.

`feedlint` checks product data (JSON or CSV) for common problems such as missing
fields, prices without a currency, invalid availability values, malformed URLs,
and duplicate IDs, so you can catch them before the feed reaches a shopping
platform or an AI shopping agent.

> **Status: prototype.** The rules and their values (required fields, allowed
> availability values, maximum title length, price format) are **provisional
> placeholders**. They have **not** been verified against any official feed
> specification, such as the OpenAI Agentic Commerce Protocol or Google Merchant
> Center. Check the target platform's documentation before relying on the results.
> See [Configuration](#configuration).

## Requirements

- Python 3.11 or later
- No third-party runtime dependencies (the Python standard library only)

## Installation

feedlint is not published to a package index yet. Install it from source:

```sh
git clone <this-repository> feedlint
cd feedlint
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```sh
feedlint check products.json
feedlint check products.csv
feedlint check products.json --format json
feedlint check feed.txt --input-format csv
```

You can also run it as a module: `python -m feedlint check products.json`.

### Options

| Option | Description |
|---|---|
| `--format text\|json` | Output format. Defaults to `text`. |
| `--input-format json\|csv` | Feed format. Detected from the file extension if omitted. |
| `--version` | Show the version and exit. |

### Example output

```text
$ feedlint check examples/invalid_products.json
examples/invalid_products.json
  #2  id=SKU-101  error    missing-required-field  Missing required field 'price'
  #3  id=SKU-102  error    price-currency          Price '1800' has no currency code (expected e.g. '12000 JPY')
  #4  id=SKU-103  error    invalid-availability    Invalid availability 'in stock' (allowed: backorder, in_stock, out_of_stock, preorder)
  #5  id=SKU-104  error    invalid-url             Invalid URL in 'link': 'www.shop.example.com/products/sku-104' (expected an absolute http(s) URL)
  #5  id=SKU-104  error    invalid-url             Invalid URL in 'image_link': '/images/sku-104.jpg' (expected an absolute http(s) URL)
  #6  id=SKU-100  error    duplicate-id            Duplicate id 'SKU-100' (first seen at item #1)
  #7  id=SKU-106  warning  title-length            Title is 160 characters (max 150)
  #8  id=SKU-107  error    missing-required-field  Missing required field 'title'
Found 8 problems (7 errors, 1 warning) in 7 items (8 checked).
```

`#N` is the 1-based position of the product in the feed. In a CSV file, item
`#N` is on line `N + 1` because line 1 is the header row.

### JSON output

`--format json` prints a machine-readable report:

```json
{
  "file": "examples/invalid_products.json",
  "summary": {
    "items_checked": 8,
    "items_with_problems": 7,
    "problems": 8,
    "errors": 7,
    "warnings": 1
  },
  "issues": [
    {
      "rule_id": "missing-required-field",
      "severity": "error",
      "message": "Missing required field 'price'",
      "item_index": 2,
      "item_id": "SKU-101",
      "field": "price"
    }
  ]
}
```

(The `issues` array is shortened here.)

### Exit codes

| Code | Meaning |
|---|---|
| `0` | No problems found. |
| `1` | One or more problems found (errors **or** warnings). |
| `2` | The feed could not be checked: invalid arguments, file not found, or malformed JSON/CSV. |

Error messages for exit code `2` are written to stderr, so stdout always holds
only the report. This makes feedlint suitable for CI pipelines, for example:

```sh
feedlint check products.json --format json > feedlint-report.json
```

## Input formats

**JSON**: either a top-level array of product objects, or an object with a
`products` array:

```json
{ "products": [ { "id": "SKU-001", "title": "..." } ] }
```

**CSV**: UTF-8 (with or without a BOM), with a header row that names the fields.
Quoted cells may contain commas and line breaks.

## Rules

| Rule ID | Severity | What it checks |
|---|---|---|
| `missing-required-field` | error | Each required field is present and not empty or whitespace-only. |
| `price-currency` | error | `price` is an amount followed by a space and a 3-letter uppercase currency code, e.g. `12000 JPY` or `24.99 USD`. |
| `invalid-availability` | error | `availability` is one of the allowed values. |
| `invalid-url` | error | `link` and `image_link` are absolute `http`/`https` URLs with a host and no whitespace. Format only; no network requests are made. |
| `duplicate-id` | error | No two products share the same `id`. The first occurrence is accepted and each later one is reported. |
| `title-length` | warning | `title` is not longer than the maximum length. |

If a field is missing, only `missing-required-field` reports it. The other rules
skip missing fields so the same problem is not reported twice.

## Configuration

The provisional values live in [`src/feedlint/config.py`](src/feedlint/config.py):

| Setting | Current placeholder value |
|---|---|
| `REQUIRED_FIELDS` | `id`, `title`, `description`, `link`, `image_link`, `price`, `availability` |
| `ALLOWED_AVAILABILITY` | `in_stock`, `out_of_stock`, `preorder`, `backorder` |
| `TITLE_MAX_LENGTH` | `150` |
| `URL_FIELDS` | `link`, `image_link` |

The price format is defined in
[`src/feedlint/rules/price_currency.py`](src/feedlint/rules/price_currency.py).

Every one of these values is marked with a `TODO` to verify it against the
official specification of the target platform. There is no command-line or
file-based configuration yet.

## Adding a rule

Each rule is one class in its own module under `src/feedlint/rules/`.

1. Create a module, for example `src/feedlint/rules/description_length.py`:

   ```python
   from collections.abc import Iterator

   from feedlint.models import Issue, Product, Severity, is_blank
   from feedlint.rules.base import ItemRule


   class DescriptionLengthRule(ItemRule):
       id = "description-length"
       description = "Description should be at least 20 characters."

       def check_item(self, product: Product, index: int) -> Iterator[Issue]:
           value = product.get("description")
           if is_blank(value):
               return  # reported by missing-required-field
           if len(str(value).strip()) < 20:
               yield self.issue(
                   Severity.WARNING,
                   "Description is shorter than 20 characters",
                   index=index,
                   product=product,
                   field="description",
               )
   ```

2. Register it in `ALL_RULES` in
   [`src/feedlint/rules/__init__.py`](src/feedlint/rules/__init__.py).

3. Add tests in `tests/test_rule_<name>.py`.

Subclass `ItemRule` and implement `check_item()` for rules that look at one
product at a time. Subclass `Rule` and implement `check()` for rules that need
the whole feed, such as `duplicate-id`.

## Project layout

```text
src/feedlint/
  cli.py          Command-line interface and exit codes
  loader.py       JSON/CSV loading
  engine.py       Runs rules and collects issues
  reporters.py    Text and JSON output
  models.py       Issue and Severity types
  config.py       Provisional rule settings
  rules/          One module per rule
tests/            pytest test suite
examples/         Sample valid and invalid feeds (JSON and CSV)
```

## Development

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Try the sample feeds:

```sh
feedlint check examples/valid_products.json    # exit code 0
feedlint check examples/invalid_products.csv   # exit code 1
```

## Roadmap ideas

- Rule sets for specific platforms, verified against their official specs
- A configuration file to enable or disable rules and override values
- A `--fail-on error|warning` option
- Checking multiple files in one run
