import tkinter as tk
from tkinter import ttk

from app.ui.config import (
    DANGER_BUTTON_WIDTH,
    ADMIN_BUTTON_WIDTH,
    CART_CARD_PADDING,
    CART_COL_NAME_MIN,
    CART_COL_NAME_WIDTH,
    CART_COL_PRICE_MIN,
    CART_COL_PRICE_WIDTH,
    CART_COL_QTY_MIN,
    CART_COL_QTY_WIDTH,
    CART_COL_SKU_MIN,
    CART_COL_SKU_WIDTH,
    CART_COL_TOTAL_MIN,
    CART_COL_TOTAL_WIDTH,
    CART_COL_STOCK_MIN,
    CART_COL_STOCK_WIDTH,
    CONTENT_PADDING,
    ENTER_ITEM_PADDING,
    ENTER_BUTTON_WIDTH,
    KEYPAD_BACK_LABEL,
    KEYPAD_BUTTON_GRID_PADX,
    KEYPAD_BUTTON_GRID_PADY,
    KEYPAD_SECTION_PADY,
    LEFT_COL_PADX,
    LOAD_PRODUCTS_PADX,
    POS_CART_CARD_OUTER_PAD,
    POS_ENTRY_CARD_OUTER_PAD,
    POS_ENTRY_FONT_SIZE,
    POS_QTY_ENTRY_FONT_SIZE,
    POS_USER_LABEL_FONT_SIZE,
    QTY_ACTION_PADY,
    QTY_ENTRY_WIDTH,
    QTY_LABEL_PADX,
    RIGHT_COL_PADX,
    SKU_ENTRY_PADY,
    TOTAL_LABEL_PADY,
    TOTALS_BOTTOM_PAD,
    TOP_BAR_PADDING,
)
from app.ui.formatting import format_currency
from app.ui.config import FONT_FAMILY


class PosView(ttk.Frame):
    def __init__(
        self,
        parent,
        on_logout,
        on_load_products,
        on_export_products,
        on_restore_db,
        on_show_reports,
        on_manage_users,
        on_add_item,
        on_remove_item,
        on_clear_cart,
        on_checkout,
    ):
        super().__init__(parent, style="Main.TFrame")
        self.on_logout = on_logout
        self.on_load_products = on_load_products
        self.on_export_products = on_export_products
        self.on_restore_db = on_restore_db
        self.on_show_reports = on_show_reports
        self.on_manage_users = on_manage_users
        self.on_add_item = on_add_item
        self.on_remove_item = on_remove_item
        self.on_clear_cart = on_clear_cart
        self.on_checkout = on_checkout
        self.active_entry = None
        self._build()

    def _build(self):
        top = ttk.Frame(self, style="Main.TFrame", padding=TOP_BAR_PADDING)
        top.pack(fill="x")

        self.user_label = ttk.Label(
            top, text="Logged in as: ", font=(FONT_FAMILY, POS_USER_LABEL_FONT_SIZE)
        )
        self.user_label.pack(side="left")

        top_actions = ttk.Frame(top, style="Main.TFrame")
        top_actions.pack(side="right")

        self.remove_button = ttk.Button(
            top_actions,
            text="Remove",
            style="Danger.TButton",
            width=DANGER_BUTTON_WIDTH,
            command=self.on_remove_item,
        )
        self.remove_button.pack(side="left")

        self.clear_button = ttk.Button(
            top_actions,
            text="Clear",
            style="Danger.TButton",
            width=DANGER_BUTTON_WIDTH,
            command=self.on_clear_cart,
        )
        self.clear_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))

        self.load_products_button = ttk.Button(
            top_actions,
            text="Import Data",
            width=ADMIN_BUTTON_WIDTH,
            command=self.on_load_products,
        )
        self.load_products_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))
        self.load_products_button.bind("<Return>", lambda _e: self.on_load_products())

        self.export_products_button = ttk.Button(
            top_actions,
            text="Export Data",
            width=ADMIN_BUTTON_WIDTH,
            command=self.on_export_products,
        )
        self.export_products_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))
        self.export_products_button.bind(
            "<Return>", lambda _e: self.on_export_products()
        )

        self.restore_db_button = ttk.Button(
            top_actions,
            text="Restore",
            width=ADMIN_BUTTON_WIDTH,
            command=self.on_restore_db,
        )
        self.restore_db_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))
        self.restore_db_button.bind("<Return>", lambda _e: self.on_restore_db())

        self.reports_button = ttk.Button(
            top_actions,
            text="Reports",
            width=ADMIN_BUTTON_WIDTH,
            command=self.on_show_reports,
        )
        self.reports_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))
        self.reports_button.bind("<Return>", lambda _e: self.on_show_reports())

        self.manage_users_button = ttk.Button(
            top_actions,
            text="Manage Users",
            width=ADMIN_BUTTON_WIDTH,
            command=self.on_manage_users,
        )
        self.manage_users_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))
        self.manage_users_button.bind(
            "<Return>", lambda _e: self.on_manage_users()
        )

        self.logout_button = ttk.Button(top_actions, text="Logout", command=self.on_logout)
        self.logout_button.pack(side="left", padx=(LOAD_PRODUCTS_PADX, 0))
        self.logout_button.bind("<Return>", lambda _e: self.on_logout())

        content = ttk.Frame(self, style="Main.TFrame", padding=CONTENT_PADDING)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=0)

        left_col = ttk.Frame(content, style="Main.TFrame")
        left_col.grid(row=0, column=0, sticky="nsew", padx=LEFT_COL_PADX)

        left_actions = ttk.Frame(content, style="Main.TFrame")
        left_actions.grid(
            row=1, column=0, sticky="ew", padx=LEFT_COL_PADX, pady=(0, TOTALS_BOTTOM_PAD)
        )

        entry_card = ttk.Labelframe(
            left_col,
            text="Enter Item",
            style="TLabelframe",
            padding=ENTER_ITEM_PADDING,
        )
        entry_card.pack(fill="x", pady=POS_ENTRY_CARD_OUTER_PAD)

        entry_grid = ttk.Frame(entry_card, style="Main.TFrame")
        entry_grid.pack(fill="x")

        ttk.Label(entry_grid, text="SKU / Barcode").pack(anchor="w")

        self.sku_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")

        self.sku_entry = ttk.Entry(
            entry_grid, textvariable=self.sku_var, font=(FONT_FAMILY, POS_ENTRY_FONT_SIZE)
        )
        self.sku_entry.pack(fill="x", pady=SKU_ENTRY_PADY)

        self.sku_entry.bind("<FocusIn>", lambda _e: self._set_active_entry(self.sku_entry))
        self.sku_entry.bind("<Return>", lambda _e: self.on_add_item())
        self.sku_entry.bind("<Tab>", self._focus_checkout)
        self.sku_entry.bind("<Shift-Tab>", self._focus_qty)

        keypad_frame = ttk.Frame(left_col, style="Main.TFrame")
        keypad_frame.pack(fill="both", expand=True, pady=KEYPAD_SECTION_PADY)

        keys = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["0", KEYPAD_BACK_LABEL, "C"],
        ]

        for r, row in enumerate(keys):
            keypad_frame.rowconfigure(r, weight=1)
            for c, key in enumerate(row):
                keypad_frame.columnconfigure(c, weight=1)
                colspan = 1
                style_name = "Keypad.TButton"

                btn = ttk.Button(
                    keypad_frame,
                    text=key,
                    style=style_name,
                    command=lambda k=key: self._keypad_press(k),
                )
                btn.grid(
                    row=r,
                    column=c,
                    columnspan=colspan,
                    padx=KEYPAD_BUTTON_GRID_PADX,
                    pady=KEYPAD_BUTTON_GRID_PADY,
                    sticky="nsew",
                )
                if key == KEYPAD_BACK_LABEL:
                    self.backspace_button = btn

        self.keypad_enter_button = ttk.Button(
            left_actions,
            text="Enter",
            style="Success.TButton",
            width=ENTER_BUTTON_WIDTH,
            command=lambda: self._keypad_press("Enter"),
        )
        self.keypad_enter_button.pack(side="left")

        qty_action = ttk.Frame(entry_card, style="Main.TFrame")
        qty_action.pack(fill="x", pady=QTY_ACTION_PADY)

        self.checkout_button = ttk.Button(
            qty_action,
            text="CHECKOUT / PAY",
            style="Success.TButton",
            command=self.on_checkout,
        )
        self.checkout_button.pack(side="left")
        self.checkout_button.bind("<Return>", lambda _e: self.on_checkout())
        self.checkout_button.bind("<Tab>", self._focus_qty)
        self.checkout_button.bind("<Shift-Tab>", self._focus_sku)

        qty_box = ttk.Frame(qty_action, style="Main.TFrame")
        qty_box.pack(side="right")

        ttk.Label(qty_box, text="Quantity", style="Card.TLabel").pack(
            side="left", padx=QTY_LABEL_PADX
        )
        self.qty_entry = ttk.Entry(
            qty_box,
            textvariable=self.qty_var,
            font=(FONT_FAMILY, POS_QTY_ENTRY_FONT_SIZE),
            width=QTY_ENTRY_WIDTH,
        )
        self.qty_entry.pack(side="left")

        self.qty_entry.bind("<FocusIn>", lambda _e: self._set_active_entry(self.qty_entry))
        self.qty_entry.bind("<Return>", lambda _e: self.on_add_item())
        self.qty_entry.bind("<Tab>", self._focus_sku)
        self.qty_entry.bind("<Shift-Tab>", self._focus_checkout)

        # Lock the left column width to avoid layout shifts when focus changes.
        left_col.update_idletasks()
        left_col.configure(width=left_col.winfo_reqwidth())
        left_col.pack_propagate(False)

        right_col = ttk.Frame(content, style="Main.TFrame")
        right_col.grid(row=0, column=1, sticky="nsew", padx=RIGHT_COL_PADX)

        right_actions = ttk.Frame(content, style="Main.TFrame")
        right_actions.grid(
            row=1, column=1, sticky="ew", padx=RIGHT_COL_PADX, pady=(0, TOTALS_BOTTOM_PAD)
        )
        right_actions.columnconfigure(0, weight=1)
        right_actions.columnconfigure(1, weight=1)

        cart_card = ttk.Labelframe(
            right_col,
            text="Current Sale",
            style="TLabelframe",
            padding=CART_CARD_PADDING,
        )
        cart_card.pack(fill="both", expand=True, pady=POS_CART_CARD_OUTER_PAD)

        columns = ("name", "sku", "price", "stock", "qty", "total")
        self.cart_tree = ttk.Treeview(
            cart_card, columns=columns, show="headings", selectmode="browse"
        )

        self.cart_tree.heading("name", text="Product Name", anchor="center")
        self.cart_tree.heading("sku", text="SKU", anchor="center")
        self.cart_tree.heading("price", text="Price", anchor="center")
        self.cart_tree.heading("stock", text="Available", anchor="center")
        self.cart_tree.heading("qty", text="Qty", anchor="center")
        self.cart_tree.heading("total", text="Total", anchor="center")

        self.cart_tree.column(
            "name",
            anchor="w",
            width=CART_COL_NAME_WIDTH,
            minwidth=CART_COL_NAME_MIN,
            stretch=True,
        )
        self.cart_tree.column(
            "sku",
            anchor="center",
            width=CART_COL_SKU_WIDTH,
            minwidth=CART_COL_SKU_MIN,
            stretch=False,
        )
        self.cart_tree.column(
            "price",
            anchor="e",
            width=CART_COL_PRICE_WIDTH,
            minwidth=CART_COL_PRICE_MIN,
            stretch=False,
        )
        self.cart_tree.column(
            "stock",
            anchor="center",
            width=CART_COL_STOCK_WIDTH,
            minwidth=CART_COL_STOCK_MIN,
            stretch=False,
        )
        self.cart_tree.column(
            "qty",
            anchor="center",
            width=CART_COL_QTY_WIDTH,
            minwidth=CART_COL_QTY_MIN,
            stretch=False,
        )
        self.cart_tree.column(
            "total",
            anchor="e",
            width=CART_COL_TOTAL_WIDTH,
            minwidth=CART_COL_TOTAL_MIN,
            stretch=False,
        )

        scrollbar = ttk.Scrollbar(cart_card, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)

        self.cart_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.total_label = ttk.Label(
            right_actions, text="Total: $0.00", style="Money.TLabel"
        )
        self.total_label.grid(row=0, column=1, sticky="e", pady=TOTAL_LABEL_PADY)

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()

    def set_user_label(self, text):
        self.user_label.config(text=text)

    def get_entry_values(self):
        return (self.sku_var.get() or "").strip(), (self.qty_var.get() or "").strip()

    def reset_entry_fields(self):
        self.sku_var.set("")
        self.qty_var.set("1")

    def focus_sku(self):
        self.sku_entry.focus_set()

    def focus_logout(self):
        self.logout_button.focus_set()

    def focus_load_products(self):
        self.load_products_button.focus_set()

    def update_cart(self, cart_items):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        total = 0
        for item in cart_items:
            available = max(item.stock_available - item.quantity, 0)
            self.cart_tree.insert(
                "",
                tk.END,
                iid=str(item.product_id),
                values=(
                    item.name,
                    item.sku,
                    format_currency(item.unit_price),
                    available,
                    item.quantity,
                    format_currency(item.line_total),
                ),
            )
            total += item.line_total
        self.total_label.config(text=f"Subtotal: {format_currency(total)}")

    def get_selected_product_id(self):
        selection = self.cart_tree.selection()
        if not selection:
            return None
        return int(selection[0])

    def _set_active_entry(self, entry):
        self.active_entry = entry

    def _get_backspace_target(self):
        widget = self.focus_get()
        if isinstance(widget, (tk.Entry, ttk.Entry)):
            return widget
        if self.active_entry is not None:
            return self.active_entry
        return self.sku_entry

    def _apply_backspace(self, target):
        if target is None:
            return
        current = target.get()
        if not current:
            return
        target.delete(0, tk.END)
        target.insert(0, current[:-1])

    def _focus_sku(self, _event):
        self.sku_entry.focus_set()
        return "break"

    def _focus_checkout(self, _event):
        self.checkout_button.focus_set()
        return "break"

    def _focus_qty(self, _event):
        self.qty_entry.focus_set()
        return "break"

    def _keypad_press(self, key):
        entry = self.active_entry
        if entry is None:
            entry = self.sku_entry
            self.active_entry = entry
        if key == "C":
            entry.delete(0, tk.END)
            return
        if key == KEYPAD_BACK_LABEL:
            target = self._get_backspace_target()
            self._apply_backspace(target)
            return
        if key == "Enter":
            self.on_add_item()
            return
        entry.insert(tk.END, key)
