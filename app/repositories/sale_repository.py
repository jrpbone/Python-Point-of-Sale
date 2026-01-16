class SaleRepository:
    def __init__(self, conn):
        self.conn = conn

    def create_sale(self, user_id, subtotal, discount, tax, total):
        cur = self.conn.execute(
            """
            INSERT INTO sales (user_id, subtotal, discount, tax, total)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, subtotal, discount, tax, total),
        )
        return cur.lastrowid

    def add_line_item(self, sale_id, product_id, quantity, unit_price, line_total):
        self.conn.execute(
            """
            INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, line_total)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sale_id, product_id, quantity, unit_price, line_total),
        )

    def totals_since(self, start_expr):
        row = self.conn.execute(
            f"""
            SELECT COALESCE(SUM(total), 0) AS total, COUNT(*) AS count
            FROM sales
            WHERE datetime(created_at, 'localtime') >= {start_expr}
            """
        ).fetchone()
        return {"total": row["total"], "count": row["count"]}

    def top_skus_since(self, start_expr, limit=5):
        rows = self.conn.execute(
            f"""
            SELECT p.name, p.sku, SUM(si.quantity) AS quantity, SUM(si.line_total) AS total
            FROM sale_items si
            JOIN sales s ON s.id = si.sale_id
            JOIN products p ON p.id = si.product_id
            WHERE datetime(s.created_at, 'localtime') >= {start_expr}
            GROUP BY si.product_id
            ORDER BY quantity DESC, total DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return rows
