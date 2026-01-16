from app.models import Product


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def list_products(self):
        rows = self.conn.execute(
            """
            SELECT p.id, p.name, p.sku, p.barcode, c.name AS category, p.price, p.quantity, p.brand
            FROM products p
            LEFT JOIN categories c ON c.id = p.category_id
            WHERE p.active = 1
            ORDER BY p.name
            """
        ).fetchall()
        return [
            Product(
                id=row["id"],
                name=row["name"],
                sku=row["sku"],
                barcode=row["barcode"],
                category=row["category"],
                price=row["price"],
                quantity=row["quantity"],
                brand=row["brand"],
            )
            for row in rows
        ]

    def get_by_id(self, product_id):
        return self.conn.execute(
            "SELECT id, name, price, quantity FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()

    def get_by_sku(self, sku):
        return self.conn.execute(
            """
            SELECT id, name, price, quantity, sku, barcode
            FROM products
            WHERE (sku = ? OR barcode = ?) AND active = 1
            """,
            (sku, sku),
        ).fetchone()

    def get_by_exact_sku(self, sku):
        return self.conn.execute(
            "SELECT id, quantity FROM products WHERE sku = ?",
            (sku,),
        ).fetchone()

    def get_sku_map(self, skus, chunk_size=900):
        if not skus:
            return {}
        sku_map = {}
        for start in range(0, len(skus), chunk_size):
            chunk = skus[start : start + chunk_size]
            placeholders = ",".join("?" for _ in chunk)
            rows = self.conn.execute(
                f"SELECT id, sku, quantity FROM products WHERE sku IN ({placeholders})",
                chunk,
            ).fetchall()
            for row in rows:
                sku_map[row["sku"]] = row
        return sku_map

    def upsert_by_sku(self, name, sku, barcode, category_id, price, quantity, brand):
        row = self.conn.execute(
            "SELECT id FROM products WHERE sku = ?",
            (sku,),
        ).fetchone()
        if row:
            self.conn.execute(
                """
                UPDATE products
                SET name = ?, barcode = ?, category_id = ?, price = ?, quantity = ?, brand = ?, active = 1
                WHERE id = ?
                """,
                (name, barcode, category_id, price, quantity, brand, row["id"]),
            )
            return row["id"]
        cur = self.conn.execute(
            """
            INSERT INTO products (name, sku, barcode, category_id, price, quantity, brand)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, sku, barcode, category_id, price, quantity, brand),
        )
        return cur.lastrowid

    def update_quantity(self, product_id, new_qty):
        self.conn.execute(
            "UPDATE products SET quantity = ? WHERE id = ?",
            (new_qty, product_id),
        )

    def update_quantities_bulk(self, updates):
        if not updates:
            return
        self.conn.executemany(
            "UPDATE products SET quantity = ? WHERE id = ?",
            updates,
        )

    def insert_many(self, rows):
        if not rows:
            return
        self.conn.executemany(
            """
            INSERT INTO products (name, sku, barcode, category_id, price, quantity, brand)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
