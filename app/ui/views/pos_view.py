import tkinter as tk
from tkinter import ttk

from app.ui.config import (
    CART_COL_NAME_MIN,
    CART_COL_NAME_WIDTH,
    CART_COL_PRICE_MIN,
    CART_COL_PRICE_WIDTH,
    CART_COL_QTY_MIN,
    CART_COL_QTY_WIDTH,
    CART_COL_SKU_MIN,
    CART_COL_SKU_WIDTH,
    CART_COL_STOCK_MIN,
    CART_COL_STOCK_WIDTH,
    CART_COL_TOTAL_MIN,
    CART_COL_TOTAL_WIDTH,
    CONTENT_PADDING,
    FONT_FAMILY,
    KEYPAD_BACK_LABEL,
    KEYPAD_BUTTON_GRID_PADX,
    KEYPAD_BUTTON_GRID_PADY,
    LEFT_COL_PADX,
    POS_ENTRY_FONT_SIZE,
    POS_QTY_ENTRY_FONT_SIZE,
    QTY_ENTRY_WIDTH,
    RIGHT_COL_PADX,
    get_palette,
)
from app.ui.formatting import format_currency


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
        self.colors = get_palette()
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
        self._build_header()
        self._build_toolbar()

        content = ttk.Frame(self, style="Main.TFrame", padding=CONTENT_PADDING)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=0, minsize=370)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        left_col = ttk.Frame(content, style="Main.TFrame")
        left_col.grid(row=0, column=0, sticky="nsew", padx=LEFT_COL_PADX)
        left_col.rowconfigure(1, weight=1)
        left_col.columnconfigure(0, weight=1)

        self._build_item_entry(left_col)
        self._build_keypad(left_col)

        right_col = ttk.Frame(content, style="Main.TFrame")
        right_col.grid(row=0, column=1, sticky="nsew", padx=RIGHT_COL_PADX)
        right_col.rowconfigure(0, weight=1)
        right_col.columnconfigure(0, weight=1)
        self._build_cart(right_col)

    def _build_header(self):
        header = ttk.Frame(self, style="Topbar.TFrame", padding=(22, 14))
        header.pack(fill="x")

        brand = ttk.Frame(header, style="Topbar.TFrame")
        brand.pack(side="left")
        ttk.Label(brand, text="PyPOS", style="TopbarTitle.TLabel").pack(anchor="w")
        ttk.Label(
            brand,
            text="POINT OF SALE",
            style="TopbarText.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        account = ttk.Frame(header, style="Topbar.TFrame")
        account.pack(side="right")
        self.user_label = ttk.Label(
            account, text="Signed in", style="TopbarPill.TLabel"
        )
        self.user_label.pack(side="left", padx=(0, 10))
        self.logout_button = ttk.Button(
            account,
            text="LOG OUT",
            style="Topbar.TButton",
            command=self.on_logout,
        )
        self.logout_button.pack(side="left")
        self.logout_button.bind("<Return>", lambda _e: self.on_logout())

    def _build_toolbar(self):
        toolbar = ttk.Frame(self, style="Main.TFrame", padding=(20, 16, 20, 0))
        toolbar.pack(fill="x")

        tools = ttk.Frame(toolbar, style="Main.TFrame")
        tools.pack(side="right")

        tool_specs = (
            ("IMPORT", self.on_load_products, "load_products_button"),
            ("EXPORT", self.on_export_products, "export_products_button"),
            ("RESTORE", self.on_restore_db, "restore_db_button"),
            ("REPORTS", self.on_show_reports, "reports_button"),
            ("USERS", self.on_manage_users, "manage_users_button"),
        )
        for index, (label, command, attribute) in enumerate(tool_specs):
            button = ttk.Button(
                tools,
                text=label,
                style="Secondary.TButton",
                command=command,
            )
            button.pack(side="left", padx=((8 if index else 0), 0))
            button.bind("<Return>", lambda _e, callback=command: callback())
            setattr(self, attribute, button)

    def _surface(self, parent, padding=0):
        border = tk.Frame(parent, background=self.colors["border"], padx=1, pady=1)
        card = ttk.Frame(border, style="Card.TFrame", padding=padding)
        card.pack(fill="both", expand=True)
        return border, card

    def _build_item_entry(self, parent):
        border, card = self._surface(parent, padding=20)
        border.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text="ADD TO CART", style="Eyebrow.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(card, text="Scan or enter an item", style="CardTitle.TLabel").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(5, 3)
        )

        self.sku_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")

        ttk.Label(card, text="SKU / BARCODE", style="CardMuted.TLabel").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(14, 5)
        )
        self.sku_entry = ttk.Entry(
            card,
            textvariable=self.sku_var,
            font=(FONT_FAMILY, POS_ENTRY_FONT_SIZE),
        )
        self.sku_entry.grid(row=3, column=0, columnspan=2, sticky="ew", ipady=4)

        qty_group = ttk.Frame(card, style="Card.TFrame")
        qty_group.grid(row=4, column=0, sticky="w", pady=(16, 0))
        ttk.Label(qty_group, text="QUANTITY", style="CardMuted.TLabel").pack(
            anchor="w", pady=(0, 5)
        )
        self.qty_entry = ttk.Entry(
            qty_group,
            textvariable=self.qty_var,
            font=(FONT_FAMILY, POS_QTY_ENTRY_FONT_SIZE),
            width=QTY_ENTRY_WIDTH,
            justify="center",
        )
        self.qty_entry.pack(ipady=3)

        self.add_item_button = ttk.Button(
            card,
            text="ADD ITEM",
            command=self.on_add_item,
        )
        self.add_item_button.grid(row=4, column=1, sticky="se", pady=(16, 0), ipady=3)

        self.sku_entry.bind("<FocusIn>", lambda _e: self._set_active_entry(self.sku_entry))
        self.sku_entry.bind("<Return>", lambda _e: self.on_add_item())
        self.sku_entry.bind("<Tab>", self._focus_qty)
        self.sku_entry.bind("<Shift-Tab>", self._focus_add)
        self.qty_entry.bind("<FocusIn>", lambda _e: self._set_active_entry(self.qty_entry))
        self.qty_entry.bind("<Return>", lambda _e: self.on_add_item())
        self.qty_entry.bind("<Tab>", self._focus_add)
        self.qty_entry.bind("<Shift-Tab>", self._focus_sku)
        self.add_item_button.bind("<Tab>", self._focus_sku)
        self.add_item_button.bind("<Shift-Tab>", self._focus_qty)

    def _build_keypad(self, parent):
        border, card = self._surface(parent, padding=16)
        border.grid(row=1, column=0, sticky="nsew")
        card.rowconfigure(1, weight=1)
        card.columnconfigure(0, weight=1)

        heading = ttk.Frame(card, style="Card.TFrame")
        heading.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(heading, text="Numeric keypad", style="CardTitle.TLabel").pack(
            side="left"
        )

        keypad = ttk.Frame(card, style="Card.TFrame")
        keypad.grid(row=1, column=0, sticky="nsew")
        keys = (
            ("7", "8", "9"),
            ("4", "5", "6"),
            ("1", "2", "3"),
            ("0", KEYPAD_BACK_LABEL, "C"),
        )
        for row_index, row in enumerate(keys):
            keypad.rowconfigure(row_index, weight=1)
            for column_index, key in enumerate(row):
                keypad.columnconfigure(column_index, weight=1)
                button = ttk.Button(
                    keypad,
                    text=key,
                    style="Keypad.TButton",
                    command=lambda value=key: self._keypad_press(value),
                )
                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=KEYPAD_BUTTON_GRID_PADX,
                    pady=KEYPAD_BUTTON_GRID_PADY,
                    sticky="nsew",
                )
                if key == KEYPAD_BACK_LABEL:
                    self.backspace_button = button

        self.keypad_enter_button = ttk.Button(
            card,
            text="ENTER ITEM",
            style="Success.TButton",
            command=lambda: self._keypad_press("Enter"),
        )
        self.keypad_enter_button.grid(row=2, column=0, sticky="ew", pady=(10, 0), ipady=3)

    def _build_cart(self, parent):
        border, card = self._surface(parent)
        border.grid(row=0, column=0, sticky="nsew")
        card.rowconfigure(1, weight=1)
        card.columnconfigure(0, weight=1)

        heading = ttk.Frame(card, style="Card.TFrame", padding=(20, 16))
        heading.grid(row=0, column=0, sticky="ew")
        title_group = ttk.Frame(heading, style="Card.TFrame")
        title_group.pack(side="left")
        ttk.Label(title_group, text="Current sale", style="CardTitle.TLabel").pack(
            anchor="w"
        )
        self.cart_count_label = ttk.Label(
            title_group,
            text="No items",
            style="CardMuted.TLabel",
        )
        self.cart_count_label.pack(anchor="w", pady=(3, 0))

        cart_actions = ttk.Frame(heading, style="Card.TFrame")
        cart_actions.pack(side="right")
        self.remove_button = ttk.Button(
            cart_actions,
            text="REMOVE SELECTED",
            style="DangerOutline.TButton",
            command=self.on_remove_item,
        )
        self.remove_button.pack(side="left")
        self.clear_button = ttk.Button(
            cart_actions,
            text="CLEAR CART",
            style="Secondary.TButton",
            command=self.on_clear_cart,
        )
        self.clear_button.pack(side="left", padx=(8, 0))

        table = ttk.Frame(card, style="Card.TFrame")
        table.grid(row=1, column=0, sticky="nsew")
        table.rowconfigure(0, weight=1)
        table.columnconfigure(0, weight=1)

        columns = ("name", "sku", "price", "stock", "qty", "total")
        self.cart_tree = ttk.Treeview(
            table, columns=columns, show="headings", selectmode="browse"
        )
        headings = {
            "name": "PRODUCT",
            "sku": "SKU",
            "price": "PRICE",
            "stock": "AVAILABLE",
            "qty": "QTY",
            "total": "TOTAL",
        }
        for column, label in headings.items():
            self.cart_tree.heading(column, text=label, anchor="center")

        self.cart_tree.column(
            "name", anchor="w", width=CART_COL_NAME_WIDTH,
            minwidth=CART_COL_NAME_MIN, stretch=True,
        )
        self.cart_tree.column(
            "sku", anchor="center", width=CART_COL_SKU_WIDTH,
            minwidth=CART_COL_SKU_MIN, stretch=False,
        )
        self.cart_tree.column(
            "price", anchor="e", width=CART_COL_PRICE_WIDTH,
            minwidth=CART_COL_PRICE_MIN, stretch=False,
        )
        self.cart_tree.column(
            "stock", anchor="center", width=CART_COL_STOCK_WIDTH,
            minwidth=CART_COL_STOCK_MIN, stretch=False,
        )
        self.cart_tree.column(
            "qty", anchor="center", width=CART_COL_QTY_WIDTH,
            minwidth=CART_COL_QTY_MIN, stretch=False,
        )
        self.cart_tree.column(
            "total", anchor="e", width=CART_COL_TOTAL_WIDTH,
            minwidth=CART_COL_TOTAL_MIN, stretch=False,
        )

        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        self.cart_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        footer = ttk.Frame(card, style="Card.TFrame", padding=(20, 16))
        footer.grid(row=2, column=0, sticky="ew")
        ttk.Separator(footer, orient="horizontal").pack(fill="x", pady=(0, 14))

        checkout_group = ttk.Frame(footer, style="Card.TFrame")
        checkout_group.pack(fill="x")
        amount = ttk.Frame(checkout_group, style="Card.TFrame")
        amount.pack(side="left")
        ttk.Label(amount, text="ORDER SUBTOTAL", style="CardMuted.TLabel").pack(
            anchor="w"
        )
        self.total_label = ttk.Label(
            amount, text=format_currency(0), style="CardMoney.TLabel"
        )
        self.total_label.pack(anchor="w", pady=(2, 0))

        self.checkout_button = ttk.Button(
            checkout_group,
            text="CHECKOUT / PAY",
            style="Success.TButton",
            command=self.on_checkout,
        )
        self.checkout_button.pack(side="right", ipadx=24, ipady=7)
        self.checkout_button.bind("<Return>", lambda _e: self.on_checkout())

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()

    def set_user_label(self, text):
        cleaned = text.replace("Logged in as:", "").strip()
        self.user_label.config(text=cleaned or "Signed in")

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
        item_count = 0
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
            item_count += item.quantity
        label = "No items" if item_count == 0 else f"{item_count} item(s)"
        self.cart_count_label.config(text=label)
        self.total_label.config(text=format_currency(total))

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

    def _focus_qty(self, _event):
        self.qty_entry.focus_set()
        return "break"

    def _focus_add(self, _event):
        self.add_item_button.focus_set()
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
            self._apply_backspace(self._get_backspace_target())
            return
        if key == "Enter":
            self.on_add_item()
            return
        entry.insert(tk.END, key)
