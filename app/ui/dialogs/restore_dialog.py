import tkinter as tk
from tkinter import ttk

from app.ui.config import apply_window_icon, get_palette


class RestoreBackupDialog:
    def __init__(self, parent, backups, colors=None):
        self.colors = colors or get_palette()
        self.backups = list(backups)
        top = self.top = tk.Toplevel(parent)
        top.title("Restore Backup")
        apply_window_icon(top)
        top.grab_set()
        top.transient(parent)

        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Restore a backup", style="PageTitle.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            container,
            text=f"Select from {len(self.backups)} available backup(s).",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        list_frame = ttk.Frame(container, style="Main.TFrame")
        list_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            height=10,
            activestyle="none",
            background=self.colors["bg_card"],
            foreground=self.colors["text"],
            selectbackground=self.colors["primary_soft"],
            selectforeground=self.colors["primary_dark"],
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            highlightthickness=1,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 11),
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        for backup in self.backups:
            self.listbox.insert("end", backup.name)

        actions = ttk.Frame(container, style="Main.TFrame")
        actions.pack(fill="x", pady=(10, 0))

        self.result = None
        self.restore_button = ttk.Button(
            actions,
            text="Restore",
            style="Success.TButton",
            command=self._confirm,
            state="disabled",
        )
        self.restore_button.pack(side="right", padx=(0, 8))
        ttk.Button(
            actions,
            text="Cancel",
            style="Secondary.TButton",
            command=top.destroy,
        ).pack(side="right")

        self.listbox.bind("<<ListboxSelect>>", self._on_select)
        self.listbox.bind("<Double-Button-1>", lambda _e: self._confirm())

        self._center_to_parent(parent)

    def _on_select(self, _event=None):
        selection = self.listbox.curselection()
        if selection:
            self.restore_button.config(state="normal")
        else:
            self.restore_button.config(state="disabled")

    def _confirm(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.result = self.backups[index]
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
