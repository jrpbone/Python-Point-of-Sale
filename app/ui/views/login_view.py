import tkinter as tk
from pathlib import Path
from tkinter import ttk

from app.ui.config import FONT_FAMILY, get_palette


class LoginView(ttk.Frame):
    """Branded, keyboard-friendly authentication screen."""

    CARD_WIDTH = 420
    CARD_HEIGHT = 580

    def __init__(self, parent, on_login):
        super().__init__(parent, style="Main.TFrame")
        self.on_login = on_login
        self.colors = get_palette()
        self.username_var = tk.StringVar()
        self.pin_var = tk.StringVar()
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=11)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)

        self._build_brand_panel()
        self._build_sign_in_panel()

    def _build_brand_panel(self):
        panel = tk.Canvas(
            self,
            background=self.colors["nav"],
            borderwidth=0,
            highlightthickness=0,
        )
        panel.grid(row=0, column=0, sticky="nsew")
        panel.bind("<Configure>", lambda event: self._draw_brand_background(panel, event))

        content = tk.Frame(panel, bg=self.colors["nav"])
        content.place(relx=0.5, rely=0.49, anchor="center")

        logo_path = Path(__file__).resolve().parents[3] / "assets" / "pos_login.png"
        try:
            self._brand_image = tk.PhotoImage(file=str(logo_path)).subsample(2, 2)
            tk.Label(
                content,
                image=self._brand_image,
                bg=self.colors["nav"],
                borderwidth=0,
                highlightthickness=0,
            ).pack(anchor="w", pady=(0, 18))
        except tk.TclError:
            self._brand_image = None

        brand_name = tk.Frame(content, bg=self.colors["nav"])
        brand_name.pack(anchor="w")
        tk.Label(
            brand_name,
            text="Py",
            bg=self.colors["nav"],
            fg="#f8fafc",
            font=(FONT_FAMILY, 44, "bold"),
        ).pack(side="left")
        tk.Label(
            brand_name,
            text="POS",
            bg=self.colors["nav"],
            fg="#3b82f6",
            font=(FONT_FAMILY, 44, "bold"),
        ).pack(side="left")

        tk.Label(
            content,
            text="POINT OF SALE SYSTEM",
            bg=self.colors["nav"],
            fg="#94a3b8",
            font=(FONT_FAMILY, 12, "bold"),
        ).pack(anchor="w", pady=(8, 20))

        divider = tk.Frame(content, bg=self.colors["nav"])
        divider.pack(fill="x", pady=(0, 20))
        tk.Frame(divider, bg=self.colors["primary"], height=2, width=70).pack(
            side="left"
        )
        tk.Frame(divider, bg="#26364f", height=1, width=285).pack(
            side="left", pady=(1, 0)
        )

        modules = tk.Frame(content, bg=self.colors["nav"])
        modules.pack(anchor="w")
        module_specs = (
            ("S", "SALES"),
            ("I", "INVENTORY"),
            ("R", "REPORTS"),
        )
        for index, (symbol, label) in enumerate(module_specs):
            tile = tk.Frame(
                modules,
                bg=self.colors["nav_light"],
                padx=14,
                pady=11,
            )
            tile.pack(side="left", padx=((0 if index == 0 else 9), 0))
            tk.Label(
                tile,
                text=symbol,
                width=2,
                bg=self.colors["nav_light"],
                fg="#93c5fd",
                font=(FONT_FAMILY, 10, "bold"),
            ).pack(side="left")
            tk.Label(
                tile,
                text=label,
                bg=self.colors["nav_light"],
                fg="#f1f5f9",
                font=(FONT_FAMILY, 9, "bold"),
            ).pack(side="left", padx=(5, 0))

        status = tk.Frame(panel, bg=self.colors["nav"])
        status.place(relx=0.5, rely=0.86, anchor="center")
        tk.Label(
            status,
            text="◆",
            bg=self.colors["nav"],
            fg="#60a5fa",
            font=(FONT_FAMILY, 13),
        ).pack(side="left", padx=(0, 10))
        tk.Label(
            status,
            text="LOCAL DATABASE  |  AUTHORIZED ACCESS",
            bg=self.colors["nav"],
            fg="#94a3b8",
            font=(FONT_FAMILY, 9, "bold"),
        ).pack(side="left")

    def _build_sign_in_panel(self):
        panel = tk.Canvas(
            self,
            background=self.colors["bg_main"],
            borderwidth=0,
            highlightthickness=0,
        )
        panel.grid(row=0, column=1, sticky="nsew")
        panel.bind("<Configure>", lambda event: self._draw_form_background(panel, event))

        shadow = tk.Frame(
            panel,
            background="#dce4ef",
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
        )
        shadow.place(relx=0.5, rely=0.5, anchor="center", x=8, y=10)
        shadow.pack_propagate(False)

        shell = tk.Frame(
            panel,
            background=self.colors["border"],
            width=self.CARD_WIDTH,
            height=self.CARD_HEIGHT,
            padx=1,
            pady=1,
        )
        shell.place(relx=0.5, rely=0.5, anchor="center")
        shell.pack_propagate(False)

        tk.Frame(shell, background=self.colors["primary"], height=5).pack(fill="x")
        card = ttk.Frame(shell, style="Card.TFrame", padding=(36, 28))
        card.pack(fill="both", expand=True)

        header = ttk.Frame(card, style="Card.TFrame")
        header.pack(fill="x")
        tk.Label(
            header,
            text="P",
            width=2,
            bg=self.colors["primary_soft"],
            fg=self.colors["primary"],
            font=(FONT_FAMILY, 15, "bold"),
            padx=7,
            pady=7,
        ).pack(side="left", padx=(0, 13))

        header_copy = ttk.Frame(header, style="Card.TFrame")
        header_copy.pack(side="left")
        ttk.Label(header_copy, text="USER ACCESS", style="Eyebrow.TLabel").pack(
            anchor="w"
        )
        ttk.Label(header_copy, text="PyPOS", style="CardTitle.TLabel").pack(
            anchor="w", pady=(2, 0)
        )

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=(22, 22))

        ttk.Label(card, text="Welcome back", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Sign in to continue to your account",
            style="CardMuted.TLabel",
        ).pack(anchor="w", pady=(4, 22))

        ttk.Label(card, text="Username", style="Card.TLabel").pack(
            anchor="w", pady=(0, 6)
        )
        self.username_entry = self._build_input(
            card,
            variable=self.username_var,
            symbol="U",
        )
        self.username_entry.bind("<Return>", lambda _e: self.pin_entry.focus_set())

        ttk.Label(card, text="PIN", style="Card.TLabel").pack(
            anchor="w", pady=(18, 6)
        )
        self.pin_entry = self._build_input(
            card,
            variable=self.pin_var,
            symbol="#",
            show="*",
        )
        self.pin_entry.bind("<Return>", lambda _e: self._submit())

        self.login_button = ttk.Button(
            card,
            text="SIGN IN",
            style="Success.TButton",
            command=self._submit,
        )
        self.login_button.pack(fill="x", pady=(24, 0), ipady=5)
        self.login_button.bind("<Return>", lambda _e: self._submit())

        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=(22, 16))

        access_border = tk.Frame(card, bg=self.colors["border"], padx=1, pady=1)
        access_border.pack(fill="x")
        tk.Label(
            access_border,
            text="AUTHORIZED USER ACCESS",
            bg="#f8fafc",
            fg=self.colors["primary"],
            font=(FONT_FAMILY, 9, "bold"),
            pady=10,
        ).pack(fill="x")

    def _build_input(self, parent, variable, symbol, show=""):
        border = tk.Frame(parent, bg=self.colors["border"], padx=1, pady=1)
        border.pack(fill="x")
        field = tk.Frame(border, bg="#ffffff")
        field.pack(fill="both")

        tk.Label(
            field,
            text=symbol,
            width=3,
            bg="#ffffff",
            fg=self.colors["primary"],
            font=(FONT_FAMILY, 10, "bold"),
        ).pack(side="left", padx=(8, 2))
        entry = tk.Entry(
            field,
            textvariable=variable,
            show=show,
            bg="#ffffff",
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            selectbackground=self.colors["primary_soft"],
            selectforeground=self.colors["primary_dark"],
            font=(FONT_FAMILY, 11),
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 12), ipady=13)
        entry.bind("<FocusIn>", lambda _e: border.configure(bg=self.colors["primary"]))
        entry.bind("<FocusOut>", lambda _e: border.configure(bg=self.colors["border"]))
        return entry

    def _draw_brand_background(self, canvas, event):
        canvas.delete("decoration")
        width, height = event.width, event.height
        line_color = "#17335d"
        canvas.create_oval(
            -260,
            height * 0.05,
            width * 0.25,
            height * 0.55,
            outline=line_color,
            width=1,
            tags="decoration",
        )
        canvas.create_oval(
            width * 0.72,
            height * 0.72,
            width * 1.08,
            height * 1.10,
            outline=line_color,
            width=1,
            tags="decoration",
        )
        dot_color = "#12305a"
        for row in range(7):
            for column in range(11):
                x = width * 0.68 + column * 16
                y = 26 + row * 16
                canvas.create_oval(
                    x,
                    y,
                    x + 4,
                    y + 4,
                    fill=dot_color,
                    outline="",
                    tags="decoration",
                )

    def _draw_form_background(self, canvas, event):
        canvas.delete("decoration")
        width, height = event.width, event.height
        canvas.create_oval(
            width * 0.45,
            -height * 0.55,
            width * 1.55,
            height * 0.45,
            fill="#edf2f8",
            outline="",
            tags="decoration",
        )
        canvas.create_oval(
            width * 0.70,
            height * 0.32,
            width * 1.45,
            height * 1.08,
            outline="#e5ecf5",
            width=18,
            tags="decoration",
        )
        for row in range(6):
            for column in range(8):
                x = width - 115 + column * 13
                y = height - 105 + row * 13
                canvas.create_oval(
                    x,
                    y,
                    x + 3,
                    y + 3,
                    fill="#dbe7f6",
                    outline="",
                    tags="decoration",
                )

    def _submit(self):
        self.on_login(self.username_var.get(), self.pin_var.get())

    def clear_form(self):
        self.username_var.set("")
        self.pin_var.set("")
        self.username_entry.focus_set()

    def show(self):
        self.pack(fill="both", expand=True)
        self.after_idle(self.username_entry.focus_set)

    def hide(self):
        self.pack_forget()
