class PaymentRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_payment(self, sale_id, method, amount, received, change_due):
        self.conn.execute(
            """
            INSERT INTO payments (sale_id, method, amount, received, change_due)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sale_id, method, amount, received, change_due),
        )
