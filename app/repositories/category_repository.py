class CategoryRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_or_create(self, name):
        if not name:
            return None
        cleaned = name.strip()
        row = self.conn.execute(
            "SELECT id FROM categories WHERE name = ?",
            (cleaned,),
        ).fetchone()
        if row:
            return row["id"]
        cur = self.conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (cleaned,),
        )
        return cur.lastrowid
