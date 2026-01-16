import tkinter as tk
from tkinter import ttk

from app.ui.config import get_palette
from app.ui.formatting import format_currency


class ErrorListDialog:
    def __init__(self, parent, title, errors, colors=None):
        self.colors = colors or get_palette()
        top = self.top = tk.Toplevel(parent)
        top.title(title)
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=title, style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            container,
            text=f"{len(errors)} issue(s) found.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        text_frame = ttk.Frame(container, style="Main.TFrame")
        text_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(
            text_frame,
            height=12,
            wrap="none",
            yscrollcommand=scrollbar.set,
            background="white",
            relief="solid",
            borderwidth=1,
        )
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)

        for error in errors:
            text.insert("end", f"{error}\n")
        text.config(state="disabled")

        ttk.Button(container, text="Close", command=top.destroy).pack(
            pady=(10, 0), anchor="e"
        )

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


class ProgressDialog:
    def __init__(self, parent, title, total, colors=None):
        self.colors = colors or get_palette()
        top = self.top = tk.Toplevel(parent)
        top.title(title)
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=title, style="Subheader.TLabel").pack(anchor="w")
        self.progress_label = ttk.Label(container, text="0 / 0", style="Card.TLabel")
        self.progress_label.pack(anchor="w", pady=(0, 8))

        self.progress = ttk.Progressbar(
            container,
            mode="determinate",
            maximum=max(total, 1),
            value=0,
        )
        self.progress.pack(fill="x")
        self._center_to_parent(parent)

    def update_progress(self, current, total):
        self.progress["maximum"] = max(total, 1)
        self.progress["value"] = current
        self.progress_label.config(text=f"{current} / {total}")
        self.top.update_idletasks()

    def close(self):
        self.top.destroy()

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


class ImportPreviewDialog:
    def __init__(self, parent, columns, rows, summary, errors, colors=None):
        self.colors = colors or get_palette()
        top = self.top = tk.Toplevel(parent)
        top.title("Import Preview")
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Import Preview", style="Header.TLabel").pack(
            anchor="w"
        )
        stats_text = (
            f"Rows: {summary.get('total', 0)} total, "
            f"{summary.get('valid', 0)} valid, "
            f"{summary.get('invalid', 0)} invalid. "
            f"New: {summary.get('add', 0)}, Updates: {summary.get('update', 0)}."
        )
        ttk.Label(container, text=stats_text, style="Subheader.TLabel").pack(
            anchor="w", pady=(0, 10)
        )

        if errors:
            ttk.Label(
                container,
                text="Invalid rows will be skipped.",
                style="Card.TLabel",
                foreground=self.colors["warning"],
            ).pack(anchor="w", pady=(0, 6))

        columns_keys = [key for key, _label in columns]
        tree = ttk.Treeview(container, columns=columns_keys, show="headings", height=8)
        for key, label in columns:
            tree.heading(key, text=label, anchor="center")
            tree.column(key, anchor="center", width=120, minwidth=80, stretch=True)
        for row in rows:
            values = []
            for key in columns_keys:
                value = row.get(key, "")
                if key == "price" and isinstance(value, (int, float)):
                    value = format_currency(value)
                if key == "__action":
                    value = str(value or "").upper()
                values.append(value if value is not None else "")
            tree.insert("", tk.END, values=values)
        tree.pack(fill="both", expand=True)

        if summary.get("valid", 0) > len(rows):
            ttk.Label(
                container,
                text=f"Showing first {len(rows)} valid rows.",
                style="Card.TLabel",
            ).pack(anchor="w", pady=(6, 0))

        actions = ttk.Frame(container, style="Main.TFrame")
        actions.pack(fill="x", pady=(10, 0))

        self.result = False

        if errors:
            ttk.Button(
                actions,
                text="View Errors",
                command=lambda: ErrorListDialog(parent, "Import Errors", errors, self.colors),
            ).pack(side="left")

        ttk.Button(actions, text="Cancel", command=top.destroy).pack(side="right")

        import_button = ttk.Button(
            actions,
            text="Import",
            style="Success.TButton",
            command=self._confirm,
        )
        import_button.pack(side="right", padx=(0, 8))
        if not summary.get("valid"):
            import_button.config(state="disabled")

        self._center_to_parent(parent)

    def _confirm(self):
        self.result = True
        self.top.destroy()

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
