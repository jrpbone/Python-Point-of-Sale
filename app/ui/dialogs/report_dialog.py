import tkinter as tk
from tkinter import ttk

from app.ui.config import FONT_FAMILY, get_palette
from app.ui.formatting import format_currency


class ReportDialog:
    def __init__(self, parent, summary, colors=None):
        self.colors = colors or get_palette()
        top = self.top = tk.Toplevel(parent)
        top.title("Sales Summary")
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Sales Summary", style="Header.TLabel").pack(anchor="w")

        totals = summary.get("totals", {})
        today = totals.get("today", {})
        week = totals.get("week", {})
        month = totals.get("month", {})

        summary_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        summary_card.pack(fill="x", pady=(10, 16))
        summary_card.columnconfigure(1, weight=1)

        ttk.Label(summary_card, text="Performance", style="Subheader.TLabel").grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 10),
        )

        rows = [
            ("Today", today),
            ("Last 7 Days", week),
            ("Last 30 Days", month),
        ]
        for idx, (label, data) in enumerate(rows, start=1):
            ttk.Label(summary_card, text=label, style="Card.TLabel").grid(
                row=idx, column=0, sticky="w", pady=4
            )
            total_text = format_currency(data.get("total", 0))
            count_text = f"{data.get('count', 0)} sale(s)"
            value = f"{total_text}  |  {count_text}"
            ttk.Label(
                summary_card,
                text=value,
                style="Card.TLabel",
                font=(FONT_FAMILY, 12, "bold"),
            ).grid(row=idx, column=1, sticky="e", pady=4)

        top_skus_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        top_skus_card.pack(fill="both", expand=True)

        ttk.Label(
            top_skus_card,
            text="Top SKUs (Last 30 Days)",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        top_rows = summary.get("top_skus", [])
        if not top_rows:
            ttk.Label(
                top_skus_card,
                text="No sales data available.",
                style="Card.TLabel",
                foreground=self.colors["text_light"],
            ).pack(anchor="w")
        else:
            columns = ("sku", "name", "quantity", "total")
            tree = ttk.Treeview(top_skus_card, columns=columns, show="headings", height=6)
            tree.heading("sku", text="SKU", anchor="center")
            tree.heading("name", text="Name", anchor="center")
            tree.heading("quantity", text="Qty", anchor="center")
            tree.heading("total", text="Total", anchor="center")
            tree.column("sku", anchor="center", width=120, minwidth=80)
            tree.column("name", anchor="w", width=240, minwidth=160)
            tree.column("quantity", anchor="center", width=80, minwidth=60)
            tree.column("total", anchor="e", width=120, minwidth=90)
            for row in top_rows:
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        row["sku"] or "",
                        row["name"],
                        row["quantity"],
                        format_currency(row["total"]),
                    ),
                )
            tree.pack(fill="both", expand=True)

        actions = ttk.Frame(container, style="Main.TFrame")
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Close", command=top.destroy).pack(anchor="e")

        self._center_to_parent(parent)

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
