import tkinter as tk
from tkinter import messagebox, ttk

from app.settings import TAX_RATE, TAX_ROUNDING
from app.ui.config import (
    CURRENCY_LABEL_PADX,
    MONEY_ENTRY_WIDTH,
    PAYMENT_ACTIONS_PADY,
    PAYMENT_CARD_OUTER_PAD,
    PAYMENT_CARD_PADDING,
    PAYMENT_CONFIRM_PADX,
    PAYMENT_CONTAINER_PADDING,
    PAYMENT_FOOTNOTE_PADY,
    PAYMENT_HEADER_PADX,
    PAYMENT_HEADER_PADY,
    PAYMENT_METHOD_FONT_SIZE,
    PAYMENT_METHOD_WIDTH,
    PAYMENT_ROW_PADX,
    PAYMENT_ROW_PADY,
    PAYMENT_SEPARATOR_PADX,
    PAYMENT_SEPARATOR_PADY,
    PAYMENT_SUBTOTAL_FONT_SIZE,
    PAYMENT_TOTAL_FONT_SIZE,
    FONT_FAMILY,
    get_palette,
)
from app.ui.formatting import format_currency


class PaymentDialog:
    MAX_CASH_CHANGE = 1000.0

    def __init__(self, parent, subtotal, colors=None):
        self.colors = colors or get_palette()
        top = self.top = tk.Toplevel(parent)
        top.title("Payment")
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        self.subtotal = subtotal
        self.total_due = subtotal

        container = ttk.Frame(top, style="Main.TFrame", padding=PAYMENT_CONTAINER_PADDING)
        container.pack(fill="both", expand=True)

        card = ttk.Frame(container, style="Card.TFrame", padding=PAYMENT_CARD_PADDING)
        card.pack(fill="x", pady=PAYMENT_CARD_OUTER_PAD)
        card.columnconfigure(1, weight=1)

        ttk.Label(card, text="Payment Details", style="Subheader.TLabel").grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=PAYMENT_HEADER_PADX,
            pady=PAYMENT_HEADER_PADY,
        )

        row = 1
        ttk.Label(card, text="Subtotal", style="Card.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )
        self.subtotal_label = ttk.Label(
            card,
            text=format_currency(subtotal),
            style="Card.TLabel",
            font=(FONT_FAMILY, PAYMENT_SUBTOTAL_FONT_SIZE, "bold"),
        )
        self.subtotal_label.grid(
            row=row,
            column=1,
            sticky="e",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )

        row += 1
        ttk.Label(card, text="Discount", style="Card.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )
        self.discount_var = tk.StringVar(value="0")
        discount_frame, _discount_entry = self._money_entry(card, self.discount_var)
        discount_frame.grid(
            row=row,
            column=1,
            sticky="e",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )

        row += 1
        ttk.Separator(card, orient="horizontal").grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=PAYMENT_SEPARATOR_PADX,
            pady=PAYMENT_SEPARATOR_PADY,
        )

        row += 1
        ttk.Label(card, text="Total Due", style="Card.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )
        self.total_label = ttk.Label(
            card,
            text=format_currency(self.total_due),
            style="Card.TLabel",
            font=(FONT_FAMILY, PAYMENT_TOTAL_FONT_SIZE, "bold"),
            foreground=self.colors["primary"],
        )
        self.total_label.grid(
            row=row,
            column=1,
            sticky="e",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )

        row += 1
        ttk.Label(card, text="Payment Method", style="Card.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )
        self.method_var = tk.StringVar(value="CASH")
        ttk.Combobox(
            card,
            textvariable=self.method_var,
            values=["CASH", "CARD", "E-WALLET"],
            state="readonly",
            width=PAYMENT_METHOD_WIDTH,
            font=(FONT_FAMILY, PAYMENT_METHOD_FONT_SIZE),
        ).grid(
            row=row,
            column=1,
            sticky="e",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )

        row += 1
        ttk.Label(card, text="Amount Received", style="Card.TLabel").grid(
            row=row,
            column=0,
            sticky="w",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )
        self.received_var = tk.StringVar()
        received_frame, self.received_entry = self._money_entry(card, self.received_var)
        received_frame.grid(
            row=row,
            column=1,
            sticky="e",
            padx=PAYMENT_ROW_PADX,
            pady=PAYMENT_ROW_PADY,
        )
        self.received_entry.bind("<Return>", lambda _e: self._confirm())

        ttk.Label(
            container,
            text="All amounts are in PHP.",
            style="TLabel",
            foreground=self.colors["text_light"],
        ).pack(anchor="w", pady=PAYMENT_FOOTNOTE_PADY)

        actions = ttk.Frame(container, style="Main.TFrame")
        actions.pack(fill="x", pady=PAYMENT_ACTIONS_PADY)

        style = ttk.Style()
        style.configure("MutedSuccess.TButton", background="#047857")
        style.map(
            "MutedSuccess.TButton",
            background=[("disabled", "#065f46"), ("active", "#047857"), ("!active", "#047857")],
            foreground=[("disabled", "white"), ("!active", "white")],
        )

        self.confirm_button = ttk.Button(
            actions,
            text="CONFIRM PAYMENT",
            style="Success.TButton",
            command=self._confirm,
            state="disabled",
        )
        self.confirm_button.pack(
            side="left", fill="x", expand=True, padx=PAYMENT_CONFIRM_PADX
        )
        ttk.Button(actions, text="Cancel", command=top.destroy).pack(side="right")

        self.result = None
        self.discount_var.trace_add("write", lambda *_: self._update_totals())
        self.received_var.trace_add("write", lambda *_: self._update_confirm_state())
        self.method_var.trace_add("write", lambda *_: self._update_confirm_state())
        self._update_totals()
        self._center_to_parent(parent)
        self.received_entry.focus_set()

    def _money_entry(self, parent, variable):
        frame = ttk.Frame(parent, style="Card.TFrame")
        ttk.Label(frame, text="P", style="Card.TLabel").pack(
            side="left", padx=CURRENCY_LABEL_PADX
        )
        entry = ttk.Entry(
            frame, textvariable=variable, width=MONEY_ENTRY_WIDTH, justify="right"
        )
        entry.pack(side="left", fill="x", expand=True)
        return frame, entry

    @staticmethod
    def _parse_money(value, default=None):
        text = (value or "").strip()
        if not text:
            return default
        text = text.replace(",", "")
        if text[:1] in ("P", "p"):
            text = text[1:]
        try:
            return float(text)
        except ValueError:
            return None

    def _center_to_parent(self, parent):
        self.top.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        win_w = self.top.winfo_width()
        win_h = self.top.winfo_height()
        x = parent_x + (parent_w - win_w) // 2
        y = parent_y + (parent_h - win_h) // 2
        self.top.geometry(f"+{x}+{y}")

    def _confirm(self):
        discount = self._parse_money(self.discount_var.get(), default=0.0)
        if discount is None:
            messagebox.showerror("Invalid input", "Enter valid numbers.")
            return
        received = self._parse_money(self.received_var.get())
        if received is None:
            messagebox.showerror("Invalid amount", "Amount received is not valid.")
            return
        total_due = self._calculate_total(discount)
        if received < total_due:
            messagebox.showerror(
                "Invalid amount",
                f"Amount received must be at least {format_currency(total_due)}.",
            )
            return
        if self.method_var.get() == "CASH":
            change_due = received - total_due
            if change_due >= self.MAX_CASH_CHANGE:
                messagebox.showerror(
                    "Invalid amount",
                    f"Change exceeds {format_currency(self.MAX_CASH_CHANGE)}. "
                    "Please re-enter the amount received.",
                )
                return
        self.result = (self.method_var.get(), received, discount)
        self.top.destroy()

    def _calculate_total(self, discount):
        taxable = max(self.subtotal - discount, 0)
        tax = round(taxable * TAX_RATE, TAX_ROUNDING)
        return round(taxable + tax, TAX_ROUNDING)

    def _update_totals(self):
        discount = self._parse_money(self.discount_var.get(), default=0.0)
        invalid_discount = discount is None or discount < 0
        if invalid_discount:
            discount = 0.0
        self.total_due = self._calculate_total(discount)
        self.total_label.config(text=format_currency(self.total_due))
        self._update_confirm_state(invalid_discount=invalid_discount)

    def _update_confirm_state(self, invalid_discount=False):
        if invalid_discount:
            self.confirm_button.config(state="disabled", style="MutedSuccess.TButton")
            return
        received = self._parse_money(self.received_var.get())
        is_valid = received is not None and received >= self.total_due
        if is_valid and self.method_var.get() == "CASH":
            change_due = received - self.total_due
            if change_due >= self.MAX_CASH_CHANGE:
                is_valid = False
        if is_valid:
            self.confirm_button.config(state="normal", style="Success.TButton")
        else:
            self.confirm_button.config(state="disabled", style="MutedSuccess.TButton")
