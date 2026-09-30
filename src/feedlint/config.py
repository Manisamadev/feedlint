"""Provisional rule settings.

TODO: Verify against official specs. These values are placeholders chosen for
this prototype. They are NOT confirmed to match any official product feed
specification (e.g. OpenAI Agentic Commerce Protocol, Google Merchant Center).
Review each value against the target spec before relying on it.
"""

# TODO: Verify against official specs - required fields differ between platforms.
REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "title",
    "description",
    "link",
    "image_link",
    "price",
    "availability",
)

# TODO: Verify against official specs - allowed values and their spelling
# (e.g. "in_stock" vs "in stock") differ between platforms.
ALLOWED_AVAILABILITY: frozenset[str] = frozenset(
    {"in_stock", "out_of_stock", "preorder", "backorder"}
)

# TODO: Verify against official specs - maximum title length differs between platforms.
TITLE_MAX_LENGTH: int = 150

# Fields that must contain an absolute http(s) URL.
URL_FIELDS: tuple[str, ...] = ("link", "image_link")
