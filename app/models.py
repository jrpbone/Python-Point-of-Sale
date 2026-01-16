from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    sku: str | None
    barcode: str | None
    category: str | None
    price: float
    quantity: int
    brand: str | None


@dataclass
class User:
    id: int
    username: str
    first_name: str | None
    role: str
