import math
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from app.ui.config import (
    LOGIN_BG_SCALE_PERCENT,
    LOGIN_BG_BORDER_WIDTH,
    LOGIN_CARD_OUTER_PAD,
    LOGIN_CARD_PADDING,
    LOGIN_BUTTON_PADY,
    LOGIN_BUTTON_WIDTH,
    LOGIN_ENTRY_WIDTH,
    LOGIN_ENTRY_PIN_PADY,
    LOGIN_ENTRY_USER_PADY,
    LOGIN_FORM_PADY,
    LOGIN_LABEL_PADY,
    LOGIN_SUBTITLE_PADY,
    LOGIN_TITLE_PADY,
    SCALE_PERCENT_DEN,
)


class LoginView(ttk.Frame):
    def __init__(self, parent, on_login):
        super().__init__(parent, style="Main.TFrame")
        self.on_login = on_login
        self.username_var = tk.StringVar()
        self.pin_var = tk.StringVar()
        self._build()

    def _build(self):
        asset_path = Path(__file__).resolve().parents[3] / "assets" / "shop.png"
        bg_scale_percent = LOGIN_BG_SCALE_PERCENT
        scale_num = max(1, int(bg_scale_percent))
        scale_den = SCALE_PERCENT_DEN
        divisor = math.gcd(scale_num, scale_den)
        scale_num //= divisor
        scale_den //= divisor

        self._bg_image = tk.PhotoImage(file=str(asset_path))
        if scale_num > 1:
            self._bg_image = self._bg_image.zoom(scale_num, scale_num)
        if scale_den > 1:
            self._bg_image = self._bg_image.subsample(scale_den, scale_den)
        bg_label = tk.Label(
            self, image=self._bg_image, borderwidth=LOGIN_BG_BORDER_WIDTH
        )
        bg_label.place(relx=0.5, rely=0.5, anchor="center")
        bg_label.lower()

        center_frame = ttk.Frame(self, style="Main.TFrame")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        card = ttk.Frame(center_frame, style="Card.TFrame", padding=LOGIN_CARD_PADDING)
        card.pack(fill="both", expand=True, pady=LOGIN_CARD_OUTER_PAD)

        ttk.Label(card, text="POS Login", style="Header.TLabel").pack(
            pady=LOGIN_TITLE_PADY
        )
        ttk.Label(card, text="Please sign in to continue", style="Subheader.TLabel").pack(
            pady=LOGIN_SUBTITLE_PADY
        )

        form = ttk.Frame(card, style="Card.TFrame")
        form.pack(pady=LOGIN_FORM_PADY)

        ttk.Label(form, text="Username", style="Card.TLabel").grid(
            row=0, column=0, sticky="w", pady=LOGIN_LABEL_PADY
        )
        ttk.Label(form, text="PIN", style="Card.TLabel").grid(
            row=2, column=0, sticky="w", pady=LOGIN_LABEL_PADY
        )

        entry_user = ttk.Entry(
            form, textvariable=self.username_var, width=LOGIN_ENTRY_WIDTH
        )
        entry_user.grid(row=1, column=0, pady=LOGIN_ENTRY_USER_PADY)

        entry_pin = ttk.Entry(
            form, textvariable=self.pin_var, width=LOGIN_ENTRY_WIDTH, show="*"
        )
        entry_pin.grid(row=3, column=0, pady=LOGIN_ENTRY_PIN_PADY)

        entry_user.bind("<Return>", lambda _e: self._submit())
        entry_pin.bind("<Return>", lambda _e: self._submit())

        self.login_button = ttk.Button(
            card,
            text="Login",
            command=self._submit,
            width=LOGIN_BUTTON_WIDTH,
        )
        self.login_button.pack(pady=LOGIN_BUTTON_PADY)
        self.login_button.bind("<Return>", lambda _e: self._submit())

    def _submit(self):
        self.on_login(self.username_var.get(), self.pin_var.get())

    def clear_form(self):
        self.username_var.set("")
        self.pin_var.set("")

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()
