from app.ui.view_models import CartRow


class CartService:
    def __init__(self, cart):
        self._cart = cart

    def items(self):
        return self._cart.values()

    def has_items(self):
        return bool(self._cart)

    def subtotal(self):
        return sum(item.line_total for item in self._cart.values())

    def add_product(self, product, qty):
        if product["quantity"] < qty:
            raise ValueError("Not enough stock available.")
        sku = product["sku"] if "sku" in product.keys() else ""
        barcode = product["barcode"] if "barcode" in product.keys() else ""
        display_sku = sku or barcode or ""
        row = self._cart.get(product["id"])
        if row:
            row.stock_available = product["quantity"]
            if row.quantity + qty > product["quantity"]:
                raise ValueError("Not enough stock available.")
            row.quantity += qty
        else:
            self._cart[product["id"]] = CartRow(
                product_id=product["id"],
                name=product["name"],
                sku=display_sku,
                unit_price=product["price"],
                quantity=qty,
                stock_available=product["quantity"],
            )

    def remove_one(self, product_id):
        row = self._cart.get(product_id)
        if not row:
            return False
        if row.quantity > 1:
            row.quantity -= 1
        else:
            del self._cart[product_id]
        return True

    def clear(self):
        self._cart.clear()

    def checkout_items(self):
        return list(self._cart.values())
