def make_product(**overrides):
    """Return a product that passes every rule, with optional field overrides.

    Pass a field as None to remove it entirely.
    """
    product = {
        "id": "SKU-001",
        "title": "Organic Cotton T-Shirt",
        "description": "A soft, breathable t-shirt made from 100% organic cotton.",
        "link": "https://example.com/products/sku-001",
        "image_link": "https://example.com/images/sku-001.jpg",
        "price": "3500 JPY",
        "availability": "in_stock",
    }
    for key, value in overrides.items():
        if value is None:
            product.pop(key, None)
        else:
            product[key] = value
    return product
