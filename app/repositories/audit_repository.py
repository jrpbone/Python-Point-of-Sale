class AuditRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_entry(self, user_id, action, details=None):
        self.conn.execute(
            """
            INSERT INTO audit_logs (user_id, action, details, occurred_at)
            VALUES (?, ?, ?, datetime('now','+8 hours'))
            """,
            (user_id, action, details),
        )

    def add_entries(self, entries):
        if not entries:
            return
        self.conn.executemany(
            """
            INSERT INTO audit_logs (user_id, action, details, occurred_at)
            VALUES (?, ?, ?, datetime('now','+8 hours'))
            """,
            entries,
        )
