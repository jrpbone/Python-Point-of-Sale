import tempfile
import unittest
from pathlib import Path

import app.db as db
from app.services.pos_service import PosService
from app.ui import importers


try:
    import openpyxl  # noqa: F401
    OPENPYXL_AVAILABLE = True
except Exception:
    OPENPYXL_AVAILABLE = False


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db_path = db.DB_PATH
        db.DB_PATH = Path(self.temp_dir.name) / "test.db"
        db.init_db()
        db.seed_data()
        self.conn = db.get_connection()
        self.service = PosService(self.conn)

    def tearDown(self):
        try:
            self.conn.close()
        except Exception:
            pass
        db.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def test_import_and_update(self):
        rows = [
            {
                "name": "Test A",
                "sku": "SKU-A",
                "category": "General",
                "price": 10.0,
                "quantity": 5,
                "brand": "Brand A",
                "barcode": "",
            },
            {
                "name": "Test B",
                "sku": "SKU-B",
                "category": "General",
                "price": 20.0,
                "quantity": 3,
                "brand": "Brand B",
                "barcode": "",
            },
        ]
        stats = self.service.import_products(rows)
        self.assertEqual(stats["added"], 2)
        self.assertEqual(stats["updated"], 0)

        stats = self.service.import_products(
            [
                {
                    "name": "Test A",
                    "sku": "SKU-A",
                    "category": "General",
                    "price": 10.0,
                    "quantity": 2,
                    "brand": "Brand A",
                    "barcode": "",
                }
            ]
        )
        self.assertGreaterEqual(stats["updated"], 1)
        product = self.service.get_product_by_sku("SKU-A")
        self.assertEqual(product["quantity"], 7)

    @unittest.skipUnless(OPENPYXL_AVAILABLE, "openpyxl not installed")
    def test_export_products(self):
        output_path = Path(self.temp_dir.name) / "export.xlsx"
        result = importers._export_products_worker(self.service, output_path)
        self.assertTrue(result["success"])
        self.assertTrue(output_path.exists())

    def test_backup_and_restore(self):
        backup_path = db.backup_database()
        self.assertTrue(backup_path.exists())

        conn = db.get_connection()
        conn.execute("INSERT INTO categories (name) VALUES (?)", ("TempCat",))
        conn.commit()
        conn.close()

        db.restore_database(backup_path, create_pre_restore_backup=False)
        conn = db.get_connection()
        row = conn.execute(
            "SELECT id FROM categories WHERE name = ?",
            ("TempCat",),
        ).fetchone()
        conn.close()
        self.assertIsNone(row)


if __name__ == "__main__":
    unittest.main()
