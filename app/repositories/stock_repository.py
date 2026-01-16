class StockRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_movement(self, product_id, qty, movement_type, note=None):
        self.conn.execute(
            """
            INSERT INTO stock_movements (product_id, qty, movement_type, note)
            VALUES (?, ?, ?, ?)
            """,
            (product_id, qty, movement_type, note),
        )
