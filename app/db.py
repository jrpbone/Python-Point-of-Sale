from datetime import datetime
from pathlib import Path
import shutil
import sqlite3

from app.security import hash_pin

DB_PATH = Path(__file__).resolve().parent / "data" / "pos.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT UNIQUE,
                barcode TEXT UNIQUE,
                category_id INTEGER REFERENCES categories(id),
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                brand TEXT,
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                pin TEXT NOT NULL,
                first_name TEXT,
                role TEXT NOT NULL DEFAULT 'cashier',
                active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                subtotal REAL NOT NULL,
                discount REAL NOT NULL,
                tax REAL NOT NULL,
                total REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL REFERENCES sales(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                line_total REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL REFERENCES sales(id),
                method TEXT NOT NULL,
                amount REAL NOT NULL,
                received REAL NOT NULL,
                change_due REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id),
                qty INTEGER NOT NULL,
                movement_type TEXT NOT NULL CHECK (movement_type IN ('IN','OUT','ADJUST')),
                note TEXT,
                occurred_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                action TEXT NOT NULL,
                details TEXT,
                occurred_at TEXT NOT NULL DEFAULT (datetime('now','+8 hours'))
            );

            """
        )
        conn.commit()
        _ensure_column(conn, "products", "brand", "TEXT")
        _ensure_column(conn, "products", "barcode", "TEXT")
        conn.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_products_category
                ON products(category_id);
            CREATE INDEX IF NOT EXISTS idx_products_sku
                ON products(sku);
            CREATE INDEX IF NOT EXISTS idx_products_barcode
                ON products(barcode);
            CREATE INDEX IF NOT EXISTS idx_sales_user
                ON sales(user_id);
            CREATE INDEX IF NOT EXISTS idx_sales_created_at
                ON sales(created_at);
            CREATE INDEX IF NOT EXISTS idx_sale_items_sale
                ON sale_items(sale_id);
            CREATE INDEX IF NOT EXISTS idx_sale_items_product
                ON sale_items(product_id);
            CREATE INDEX IF NOT EXISTS idx_stock_movements_product
                ON stock_movements(product_id);
            """
        )
        conn.commit()
        _ensure_column(conn, "users", "first_name", "TEXT")
    finally:
        conn.close()


def seed_data():
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()
        if row["count"] == 0:
            conn.executemany(
                "INSERT INTO users (username, pin, first_name, role) VALUES (?, ?, ?, ?)",
                [
                    ("admin", hash_pin("admin"), "Administrator", "admin"),
                ],
             ) 
        else:
            conn.execute(
                """
                UPDATE users
                SET first_name = ?
                WHERE username = ? AND (first_name IS NULL OR TRIM(first_name) = '')
                """,
                ("Cashier", "cashier"),
            )
            row = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                ("admin",),
            ).fetchone()
            if not row:
                conn.execute(
                    "INSERT INTO users (username, pin, first_name, role) VALUES (?, ?, ?, ?)",
                    ("admin", hash_pin("admin"), "Administrator", "admin"),
                )
            else:
                conn.execute(
                    """
                    UPDATE users
                    SET first_name = ?
                    WHERE username = ? AND (first_name IS NULL OR TRIM(first_name) = '')
                    """,
                    ("Admin", "admin"),
                )

        row = conn.execute("SELECT COUNT(*) AS count FROM categories").fetchone()
        if row["count"] == 0:
            conn.execute("INSERT INTO categories (name) VALUES (?)", ("General",))

        conn.commit()
    finally:
        conn.close()


def _ensure_column(conn, table, column, definition):
    info = conn.execute(f"PRAGMA table_info({table})").fetchall()
    if column in {row["name"] for row in info}:
        return
    conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
    conn.commit()


def backup_database(source_path=None, backup_dir=None, prefix="pos_backup"):
    source_path = Path(source_path) if source_path else DB_PATH
    if not source_path.exists():
        raise FileNotFoundError(f"Database file not found: {source_path}")
    backup_dir = Path(backup_dir) if backup_dir else source_path.parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = backup_dir / f"{prefix}_{timestamp}.db"
    shutil.copy2(source_path, backup_path)
    return backup_path


def restore_database(backup_path, target_path=None, create_pre_restore_backup=True):
    backup_path = Path(backup_path)
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_path}")
    target_path = Path(target_path) if target_path else DB_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Database file not found: {target_path}")
    safety_path = None
    if create_pre_restore_backup:
        safety_path = backup_database(
            source_path=target_path,
            backup_dir=target_path.parent / "backups",
            prefix="pos_backup_pre_restore",
        )
    shutil.copy2(backup_path, target_path)
    return safety_path
