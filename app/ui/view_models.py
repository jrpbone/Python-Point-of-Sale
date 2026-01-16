from dataclasses import dataclass


@dataclass
class CartRow:
    product_id: int
    name: str
    sku: str
    unit_price: float
    quantity: int
    stock_available: int

    @property
    def line_total(self):
        return self.unit_price * self.quantity
