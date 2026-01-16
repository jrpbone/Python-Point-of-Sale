from pathlib import Path
from tkinter import messagebox

from app.db import DB_PATH, backup_database, get_connection, restore_database
from app.ui.dialogs import (
    AdminAuthDialog,
    ManageUsersDialog,
    PaymentDialog,
    ReportDialog,
    RestoreBackupDialog,
)
from app.ui.formatting import format_currency
from app.ui.importers import export_products_to_excel, load_products_from_excel
from app.ui.config import LOW_STOCK_THRESHOLD


class PosController:
    def __init__(self, root, service, state, cart_service):
        self.root = root
        self.service = service
        self.state = state
        self.cart_service = cart_service
        self.login_view = None
        self.pos_view = None

    def bind_views(self, login_view, pos_view):
        self.login_view = login_view
        self.pos_view = pos_view

    def show_login(self):
        self.pos_view.hide()
        self.login_view.show()
        self.root.attributes("-fullscreen", False)

    def show_pos(self):
        self.login_view.hide()
        self.pos_view.show()
        self.root.attributes("-fullscreen", True)
        self.refresh_cart()
        self.pos_view.focus_sku()

    def login(self, username, pin):
        user = self.service.login(username, pin)
        if not user:
            messagebox.showerror("Login failed", "Invalid username or PIN")
            return
        self.state.current_user = user
        self.state.db_mtime = self._get_db_mtime()
        display_name = user.first_name or user.username
        self.pos_view.set_user_label(f"Logged in as: {display_name} ({user.role})")
        self.show_pos()

    def logout(self):
        user = self.state.current_user
        last_db_mtime = self.state.db_mtime
        self.state.reset_session()
        self.login_view.clear_form()
        self.show_login()
        try:
            self.service.conn.commit()
        except Exception:
            pass
        if self._should_backup(last_db_mtime):
            self._backup_database(user_id=user.id if user else None)

    def refresh_cart(self):
        self.pos_view.update_cart(self.cart_service.items())

    def _require_admin(self, action_label):
        return bool(self._require_admin_user(action_label))

    def _require_admin_user(self, action_label):
        if self.state.current_user and self.state.current_user.role == "admin":
            return self.state.current_user
        dialog = AdminAuthDialog(self.root, self.state.colors)
        self.root.wait_window(dialog.top)
        if not dialog.result:
            return None

        pin = dialog.result
        user = self.service.authorize_admin_pin(pin)
        if not user or user.role != "admin":
            messagebox.showerror(
                "Authorization failed",
                f"Admin password is required to {action_label}.",
            )
            return None
        return user

    def add_item_from_entry(self):
        sku, qty_text = self.pos_view.get_entry_values()
        if not sku:
            messagebox.showerror("Missing SKU", "Enter a SKU or barcode to add.")
            return
        try:
            qty = int(qty_text or 1)
        except ValueError:
            messagebox.showerror("Invalid quantity", "Quantity must be a number.")
            return
        if qty <= 0:
            messagebox.showerror("Invalid quantity", "Quantity must be at least 1.")
            return

        product = self.service.get_product_by_sku(sku)
        if not product:
            messagebox.showerror("Not found", "SKU or barcode not found in the database.")
            return
        if 0 < product["quantity"] <= LOW_STOCK_THRESHOLD:
            if product["id"] not in self.state.low_stock_notified:
                messagebox.showwarning(
                    "Low stock",
                    f"Only {product['quantity']} units left for {product['name']}.",
                )
                self.state.low_stock_notified.add(product["id"])

        try:
            self.cart_service.add_product(product, qty)
        except ValueError as exc:
            messagebox.showerror("Stock limit", str(exc))
            return

        self.pos_view.reset_entry_fields()
        self.refresh_cart()

    def remove_from_cart(self):
        product_id = self.pos_view.get_selected_product_id()
        if product_id is None:
            messagebox.showwarning("Select cart item", "Select a cart item first.")
            return
        if not self._require_admin("remove product from the cart"):
            return
        if not self.cart_service.remove_one(product_id):
            return
        self.refresh_cart()

    def clear_cart(self):
        if not self._require_admin("clear the cart"):
            return
        self.cart_service.clear()
        self.refresh_cart()

    def checkout(self):
        if not self.cart_service.has_items():
            messagebox.showerror("Empty cart", "Add items to the cart first.")
            return
        subtotal = self.cart_service.subtotal()
        dialog = PaymentDialog(self.root, subtotal, self.state.colors)
        self.root.wait_window(dialog.top)
        if not dialog.result:
            return

        payment_method, received, discount = dialog.result
        cart_items = self.cart_service.checkout_items()

        try:
            sale = self.service.checkout(
                user_id=self.state.current_user.id,
                cart_items=cart_items,
                payment_method=payment_method,
                received_amount=received,
                discount=discount,
            )
        except ValueError as exc:
            messagebox.showerror("Checkout failed", str(exc))
            return

        receipt = (
            f"Sale #{sale['sale_id']}\n"
            f"Subtotal: {format_currency(sale['subtotal'])}\n"
            f"Discount: {format_currency(sale['discount'])}\n"
            f"Total: {format_currency(sale['total'])}\n"
            f"Change due: {format_currency(sale['change_due'])}"
        )
        messagebox.showinfo("Receipt", receipt)

        self.cart_service.clear()
        self.refresh_cart()

    def manage_users(self):
        admin_user = self._require_admin_user("manage users")
        if not admin_user:
            return
        try:
            users = self.service.list_users()
        except Exception as exc:
            messagebox.showerror("Manage users", str(exc))
            return

        def _update_username(user_id, new_username):
            self.service.update_username(user_id, new_username)
            self.service.log_admin_action(
                admin_user.id,
                "UPDATE_USERNAME",
                f"Updated username for user {user_id} to {new_username}",
            )

        def _reset_pin(user_id, new_pin):
            self.service.reset_user_pin(user_id, new_pin)
            self.service.log_admin_action(
                admin_user.id,
                "RESET_USER_PIN",
                f"Reset PIN for user {user_id}",
            )

        def _create_user(username, pin, first_name, role):
            user = self.service.create_user(username, pin, first_name, role)
            self.service.log_admin_action(
                admin_user.id,
                "CREATE_USER",
                f"Created user {user['id']} ({user['username']}) role {user['role']}",
            )
            return user

        def _set_user_active(user_id, active):
            user = self.service.set_user_active(user_id, active)
            action = "ACTIVATE_USER" if active else "DEACTIVATE_USER"
            label = "activated" if active else "deactivated"
            self.service.log_admin_action(
                admin_user.id,
                action,
                f"User {user['id']} ({user['username']}) {label}",
            )
            return user

        ManageUsersDialog(
            self.root,
            users,
            on_update_username=_update_username,
            on_reset_pin=_reset_pin,
            on_create_user=_create_user,
            on_set_active=_set_user_active,
            colors=self.state.colors,
        )

    def load_products_from_excel(
        self, default_path=None, prompt_if_missing=True, force_prompt=False
    ):
        admin_user = self._require_admin_user("import products")
        if not admin_user:
            return False
        default_path = default_path or self.state.default_excel_path
        def _on_complete(success, _stats):
            if success:
                self.state.products_loaded = True

        started = load_products_from_excel(
            self.service,
            default_path=default_path,
            prompt_if_missing=prompt_if_missing,
            parent=self.root,
            force_prompt=force_prompt,
            admin_user_id=admin_user.id,
            on_complete=_on_complete,
        )
        return started

    def export_products_to_excel(self, output_path=None):
        admin_user = self._require_admin_user("export product data")
        if not admin_user:
            return False
        output_path = output_path or self.state.default_excel_path.with_name(
            "dbProducts.xlsx"
        )
        def _on_complete(result):
            if result.get("success"):
                details = (
                    f"Exported {result.get('count', 0)} products to {Path(output_path).name}"
                )
                self.service.log_admin_action(admin_user.id, "EXPORT_PRODUCTS", details)

        started = export_products_to_excel(
            self.service,
            output_path=output_path,
            parent=self.root,
            on_complete=_on_complete,
        )
        return started

    def _backup_database(self, user_id=None):
        if not DB_PATH.exists():
            messagebox.showerror("Backup failed", "Database file not found.")
            return False
        try:
            try:
                self.service.conn.commit()
            except Exception:
                pass
            backup_path = backup_database()
        except Exception as exc:
            messagebox.showerror("Backup failed", str(exc))
            return False
        if user_id:
            self.service.log_admin_action(
                user_id, "BACKUP_DB", f"Backup saved to {backup_path.name}"
            )
        return True

    def _get_db_mtime(self):
        try:
            return DB_PATH.stat().st_mtime
        except Exception:
            return None

    def _should_backup(self, last_db_mtime):
        current_mtime = self._get_db_mtime()
        if last_db_mtime is None or current_mtime is None:
            return True
        return current_mtime != last_db_mtime

    def restore_database(self):
        admin_user = self._require_admin_user("restore the database")
        if not admin_user:
            return False
        backups = self._list_backup_files()
        if not backups:
            messagebox.showinfo(
                "No backups found",
                "No backup files were found from previous logouts.",
            )
            return False
        dialog = RestoreBackupDialog(self.root, backups, self.state.colors)
        self.root.wait_window(dialog.top)
        if not dialog.result:
            return False
        backup_path = dialog.result
        confirm = messagebox.askyesno(
            "Confirm restore",
            f"Restore database from {backup_path.name}? The app will close after restore.",
        )
        if not confirm:
            return False
        return self._restore_backup(backup_path, admin_user.id)

    def _list_backup_files(self):
        backup_dir = DB_PATH.parent / "backups"
        if not backup_dir.exists():
            return []
        backups = []
        for path in backup_dir.glob("pos_backup_*.db"):
            if not path.is_file():
                continue
            name = path.name
            timestamp = name[len("pos_backup_") : -len(".db")]
            if not timestamp or not timestamp[0].isdigit():
                continue
            backups.append(path)
        backups = sorted(backups, reverse=True)
        return backups

    def _restore_backup(self, backup_path, user_id=None):
        if not backup_path.exists():
            messagebox.showerror("Restore failed", "Selected backup file is missing.")
            return False
        if not DB_PATH.exists():
            messagebox.showerror("Restore failed", "Database file not found.")
            return False
        try:
            try:
                self.service.conn.commit()
            except Exception:
                pass
            try:
                self.service.conn.close()
            except Exception:
                pass

            safety_path = restore_database(backup_path)
        except Exception as exc:
            messagebox.showerror("Restore failed", str(exc))
            try:
                new_conn = get_connection()
                self.service.reset_connection(new_conn)
            except Exception:
                pass
            return False

        if user_id:
            details = f"Restored database from {backup_path.name}"
            if safety_path:
                details = f"{details}; pre-restore backup {safety_path.name}"
            self.service.log_admin_action(user_id, "RESTORE_DB", details)

        messagebox.showinfo(
            "Restore complete",
            "Database restored successfully. The app will now close. Please reopen it.",
        )
        self.root.destroy()
        return True

    def show_sales_report(self):
        admin_user = self._require_admin_user("view sales reports")
        if not admin_user:
            return False
        summary = self.service.get_sales_summary()
        dialog = ReportDialog(self.root, summary, self.state.colors)
        self.root.wait_window(dialog.top)
        return True

    def handle_app_exit(self):
        self.cart_service.clear()
        try:
            self.service.conn.commit()
        except Exception:
            pass
        self.root.destroy()
