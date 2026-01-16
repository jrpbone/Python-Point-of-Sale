import logging
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from app.ui.config import apply_theme, get_palette
from app.ui.controllers.pos_controller import PosController
from app.ui.services.cart_service import CartService
from app.ui.state import MainWindowState
from app.ui.views.login_view import LoginView
from app.ui.views.pos_view import PosView


class MainWindow:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.state = MainWindowState(
            default_excel_path=Path(__file__).resolve().parents[2] / "products.xlsx",
            colors=get_palette(),
        )
        self.cart_service = CartService(self.state.cart)
        self.controller = PosController(self.root, self.service, self.state, self.cart_service)

        self.root.title("JMB Electronics & Electrical Supply POS")
        # Maximize window
        self.root.state("zoomed")

        self.setup_styles()

        self.container = ttk.Frame(self.root, style="Main.TFrame")
        self.container.pack(fill="both", expand=True)

        self.login_view = LoginView(self.container, self.controller.login)
        self.pos_view = PosView(
            self.container,
            on_logout=self.controller.logout,
            on_load_products=lambda: self.controller.load_products_from_excel(
                prompt_if_missing=True, force_prompt=True
            ),
            on_export_products=self.controller.export_products_to_excel,
            on_restore_db=self.controller.restore_database,
            on_show_reports=self.controller.show_sales_report,
            on_manage_users=self.controller.manage_users,
            on_add_item=self.controller.add_item_from_entry,
            on_remove_item=self.controller.remove_from_cart,
            on_clear_cart=self.controller.clear_cart,
            on_checkout=self.controller.checkout,
        )
        self.controller.bind_views(self.login_view, self.pos_view)
        self.controller.show_login()
        self.root.protocol("WM_DELETE_WINDOW", self.controller.handle_app_exit)
        self.root.bind("<Alt-F4>", lambda _e: self.controller.handle_app_exit())
        self.root.bind("<F1>", lambda _e: self.pos_view.focus_logout())
        self.root.bind("<F2>", lambda _e: self.pos_view.focus_load_products())

    def setup_styles(self):
        style = ttk.Style()
        apply_theme(style, self.state.colors)


def _install_exception_logger(root):
    original_handler = root.report_callback_exception

    def _report_callback_exception(exc, val, tb):
        logging.exception("Tkinter callback failed", exc_info=(exc, val, tb))
        original_handler(exc, val, tb)

    root.report_callback_exception = _report_callback_exception


def run_app(service):
    root = tk.Tk()
    _install_exception_logger(root)
    MainWindow(root, service)
    root.mainloop()
