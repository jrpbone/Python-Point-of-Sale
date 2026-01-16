from app.models import User
from app.security import hash_pin, is_hashed, verify_pin


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def authenticate(self, username, pin):
        username = username.strip()
        pin = pin.strip()
        row = self.conn.execute(
            """
            SELECT id, username, first_name, role, pin
            FROM users
            WHERE (username = ? OR first_name = ?) AND active = 1
            """,
            (username, username),
        ).fetchone()
        if not row:
            return None
        if not self._verify_pin(row, pin):
            return None
        return User(
            id=row["id"],
            username=row["username"],
            first_name=row["first_name"],
            role=row["role"],
        )

    def authenticate_admin(self, pin):
        pin = pin.strip()
        if not pin:
            return None
        rows = self.conn.execute(
            """
            SELECT id, username, first_name, role, pin
            FROM users
            WHERE role = 'admin' AND active = 1
            """
        ).fetchall()
        for row in rows:
            if self._verify_pin(row, pin):
                return User(
                    id=row["id"],
                    username=row["username"],
                    first_name=row["first_name"],
                    role=row["role"],
                )
        return None

    def list_users(self, active=None):
        if active is None:
            return self.conn.execute(
                """
                SELECT id, username, first_name, role, active
                FROM users
                ORDER BY username
                """
            ).fetchall()
        return self.conn.execute(
            """
            SELECT id, username, first_name, role, active
            FROM users
            WHERE active = ?
            ORDER BY username
            """,
            (1 if active else 0,),
        ).fetchall()

    def get_user_by_id(self, user_id):
        return self.conn.execute(
            """
            SELECT id, username, first_name, role, active
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    def set_active(self, user_id, active):
        value = 1 if active else 0
        cursor = self.conn.execute(
            "UPDATE users SET active = ? WHERE id = ?",
            (value, user_id),
        )
        if cursor.rowcount == 0:
            raise ValueError("User not found.")

    def create_user(self, username, pin, first_name=None, role="cashier"):
        cleaned_username = (username or "").strip()
        if not cleaned_username:
            raise ValueError("Username is required.")
        cleaned_pin = (pin or "").strip()
        if not cleaned_pin:
            raise ValueError("PIN is required.")
        cleaned_first_name = (first_name or "").strip() or None
        cleaned_role = (role or "").strip().lower() or "cashier"
        if cleaned_role not in {"cashier", "admin"}:
            raise ValueError("Role must be cashier or admin.")

        cursor = self.conn.execute(
            """
            INSERT INTO users (username, pin, first_name, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                cleaned_username,
                hash_pin(cleaned_pin),
                cleaned_first_name,
                cleaned_role,
            ),
        )
        return self.conn.execute(
            """
            SELECT id, username, first_name, role, active
            FROM users
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    def update_username(self, user_id, new_username):
        cleaned = (new_username or "").strip()
        if not cleaned:
            raise ValueError("Username is required.")
        self.conn.execute(
            "UPDATE users SET username = ? WHERE id = ?",
            (cleaned, user_id),
        )

    def reset_pin(self, user_id, new_pin):
        cleaned = (new_pin or "").strip()
        if not cleaned:
            raise ValueError("PIN is required.")
        self.conn.execute(
            "UPDATE users SET pin = ? WHERE id = ?",
            (hash_pin(cleaned), user_id),
        )

    def _verify_pin(self, row, pin):
        stored_pin = row["pin"] or ""
        if is_hashed(stored_pin):
            return verify_pin(pin, stored_pin)
        if pin != stored_pin:
            return False
        self.conn.execute(
            "UPDATE users SET pin = ? WHERE id = ?",
            (hash_pin(pin), row["id"]),
        )
        self.conn.commit()
        return True
