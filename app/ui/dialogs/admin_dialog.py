import tkinter as tk
from tkinter import messagebox, ttk

from app.ui.config import (
    ADMIN_ACTIONS_PADY,
    ADMIN_AUTHORIZE_PADX,
    ADMIN_CARD_OUTER_PAD,
    ADMIN_CARD_PADDING,
    ADMIN_CONTAINER_PADDING,
    ADMIN_ENTRY_PADY,
    ADMIN_ENTRY_WIDTH,
    ADMIN_HEADER_PADY,
    ADMIN_LABEL_PADY,
    ADMIN_SUBHEADER_PADY,
    apply_window_icon,
    get_palette,
)


class AdminAuthDialog:
    def __init__(self, parent, colors=None):
        self.colors = colors or get_palette()
        top = self.top = tk.Toplevel(parent)
        top.title("Admin Authorization")
        apply_window_icon(top)
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=ADMIN_CONTAINER_PADDING)
        container.pack(fill="both", expand=True)

        card = ttk.Frame(container, style="Card.TFrame", padding=ADMIN_CARD_PADDING)
        card.pack(fill="x", pady=ADMIN_CARD_OUTER_PAD)

        ttk.Label(card, text="Admin Access Required", style="Header.TLabel").pack(
            pady=ADMIN_HEADER_PADY
        )
        ttk.Label(
            card,
            text="Confirm an administrator PIN to continue.",
            style="Subheader.TLabel",
        ).pack(pady=ADMIN_SUBHEADER_PADY)

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(fill="x")

        ttk.Label(form, text="Admin PIN", style="Card.TLabel").grid(
            row=0, column=0, sticky="w", pady=ADMIN_LABEL_PADY
        )

        self.pin_var = tk.StringVar()

        entry_pin = ttk.Entry(
            form, textvariable=self.pin_var, width=ADMIN_ENTRY_WIDTH, show="*"
        )
        entry_pin.grid(row=1, column=0, pady=ADMIN_ENTRY_PADY)

        entry_pin.bind("<Return>", lambda _e: self._confirm())

        actions = ttk.Frame(container, style="Main.TFrame")
        actions.pack(fill="x", pady=ADMIN_ACTIONS_PADY)

        ttk.Button(
            actions, text="Authorize", style="Success.TButton", command=self._confirm
        ).pack(side="left", fill="x", expand=True, padx=ADMIN_AUTHORIZE_PADX)
        ttk.Button(
            actions,
            text="Cancel",
            style="Secondary.TButton",
            command=top.destroy,
        ).pack(side="right")

        self.result = None
        self._center_to_parent(parent)
        entry_pin.focus_set()

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
        pin = (self.pin_var.get() or "").strip()
        if not pin:
            messagebox.showerror("Missing info", "Enter the admin password.")
            return
        self.result = pin
        self.top.destroy()
