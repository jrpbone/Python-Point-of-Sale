import tkinter as tk
from tkinter import messagebox, ttk

from app.ui.config import FONT_FAMILY, get_palette


class ManageUsersDialog:
    def __init__(
        self,
        parent,
        users,
        on_update_username,
        on_reset_pin,
        on_create_user=None,
        on_set_active=None,
        colors=None,
    ):
        self.colors = colors or get_palette()
        self.on_update_username = on_update_username
        self.on_reset_pin = on_reset_pin
        self.on_create_user = on_create_user
        self.on_set_active = on_set_active
        self.users = {
            row["id"]: {key: row[key] for key in row.keys()} for row in users
        }
        self.selected_user_id = None
        self.view_mode = "active"

        top = self.top = tk.Toplevel(parent)
        top.title("Manage Users")
        top.grab_set()
        top.transient(parent)
        top.configure(background=self.colors["bg_main"])

        container = ttk.Frame(top, style="Main.TFrame", padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Manage Users", style="Header.TLabel").pack(anchor="w")

        table_controls = ttk.Frame(container, style="Main.TFrame")
        table_controls.pack(fill="x", pady=(6, 0))
        self.view_button = ttk.Button(
            table_controls,
            text="Inactive Users",
            command=self._toggle_view,
        )
        self.view_button.pack(side="right")

        table_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        table_card.pack(fill="both", expand=True, pady=(12, 16))

        columns = ("username", "name", "role", "status")
        self.tree = ttk.Treeview(table_card, columns=columns, show="headings", height=8)
        self.tree.heading("username", text="Username", anchor="w")
        self.tree.heading("name", text="Name", anchor="w")
        self.tree.heading("role", text="Role", anchor="center")
        self.tree.heading("status", text="Status", anchor="center")
        self.tree.column("username", anchor="w", width=160, minwidth=120)
        self.tree.column("name", anchor="w", width=200, minwidth=140)
        self.tree.column("role", anchor="center", width=90, minwidth=80)
        self.tree.column("status", anchor="center", width=90, minwidth=80)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        form_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        form_card.pack(fill="x")
        form_card.columnconfigure(1, weight=1)

        self.selected_label = ttk.Label(
            form_card,
            text="Select a user to edit.",
            style="Card.TLabel",
            font=(FONT_FAMILY, 11, "bold"),
        )
        self.selected_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(form_card, text="Username", style="Card.TLabel").grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            form_card, textvariable=self.username_var, width=28
        )
        self.username_entry.grid(row=1, column=1, sticky="ew", pady=4, padx=(8, 0))

        ttk.Label(form_card, text="New PIN", style="Card.TLabel").grid(
            row=2, column=0, sticky="w", pady=4
        )
        self.pin_var = tk.StringVar()
        self.pin_entry = ttk.Entry(
            form_card, textvariable=self.pin_var, width=28, show="*"
        )
        self.pin_entry.grid(row=2, column=1, sticky="ew", pady=4, padx=(8, 0))

        add_card = ttk.Frame(container, style="Card.TFrame", padding=16)
        add_card.pack(fill="x", pady=(12, 0))
        add_card.columnconfigure(1, weight=1)

        ttk.Label(
            add_card,
            text="Add User",
            style="Card.TLabel",
            font=(FONT_FAMILY, 11, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ttk.Label(add_card, text="Username", style="Card.TLabel").grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.add_username_var = tk.StringVar()
        self.add_username_entry = ttk.Entry(
            add_card, textvariable=self.add_username_var, width=28
        )
        self.add_username_entry.grid(row=1, column=1, sticky="ew", pady=4, padx=(8, 0))

        ttk.Label(add_card, text="Name", style="Card.TLabel").grid(
            row=2, column=0, sticky="w", pady=4
        )
        self.add_name_var = tk.StringVar()
        self.add_name_entry = ttk.Entry(
            add_card, textvariable=self.add_name_var, width=28
        )
        self.add_name_entry.grid(row=2, column=1, sticky="ew", pady=4, padx=(8, 0))

        ttk.Label(add_card, text="Role", style="Card.TLabel").grid(
            row=3, column=0, sticky="w", pady=4
        )
        self.add_role_var = tk.StringVar(value="cashier")
        self.add_role_entry = ttk.Combobox(
            add_card,
            textvariable=self.add_role_var,
            values=("cashier", "admin"),
            state="readonly",
            width=26,
        )
        self.add_role_entry.grid(row=3, column=1, sticky="ew", pady=4, padx=(8, 0))

        ttk.Label(add_card, text="PIN", style="Card.TLabel").grid(
            row=4, column=0, sticky="w", pady=4
        )
        self.add_pin_var = tk.StringVar()
        self.add_pin_entry = ttk.Entry(
            add_card, textvariable=self.add_pin_var, width=28, show="*"
        )
        self.add_pin_entry.grid(row=4, column=1, sticky="ew", pady=4, padx=(8, 0))
        self._bind_enter(self.add_pin_entry, self._add_user)

        add_user_button = ttk.Button(
            add_card,
            text="Add User",
            style="Success.TButton",
            command=self._add_user,
        )
        add_user_button.grid(row=5, column=0, columnspan=2, sticky="e", pady=(10, 0))
        self._bind_enter(add_user_button, add_user_button.invoke)

        actions = ttk.Frame(container, style="Main.TFrame")
        actions.pack(fill="x", pady=(12, 0))

        self.toggle_active_button = ttk.Button(
            actions,
            text="Make Inactive",
            command=self._toggle_active,
        )
        self.toggle_active_button.pack(side="left", padx=(0, 10))

        ttk.Button(
            actions,
            text="Update Username",
            style="Success.TButton",
            command=self._update_username,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            actions,
            text="Set PIN",
            command=self._reset_pin,
        ).pack(side="left")

        ttk.Button(actions, text="Close", command=top.destroy).pack(side="right")

        self._load_users()
        self._center_to_parent(parent)

    def _load_users(self):
        self.tree.delete(*self.tree.get_children())
        ordered_users = sorted(
            self.users.items(),
            key=lambda item: ((item[1]["username"] or "").lower(), item[0]),
        )
        for user_id, row in ordered_users:
            if self.view_mode == "active" and not row["active"]:
                continue
            if self.view_mode == "inactive" and row["active"]:
                continue
            status = "Active" if row["active"] else "Inactive"
            name = row["first_name"] or ""
            self.tree.insert(
                "",
                tk.END,
                iid=str(user_id),
                values=(row["username"], name, row["role"], status),
            )
        self._clear_selection()

    def _on_select(self, _event):
        selection = self.tree.selection()
        if not selection:
            return
        user_id = int(selection[0])
        self.selected_user_id = user_id
        row = self.users.get(user_id)
        if not row:
            return
        name = row["first_name"] or row["username"]
        self.selected_label.config(
            text=f"Selected: {name} ({row['role']})",
            foreground=self.colors["text"],
        )
        self.username_var.set(row["username"])
        self.pin_var.set("")

    def _update_username(self):
        user_id = self._require_selection()
        if user_id is None:
            return
        new_username = (self.username_var.get() or "").strip()
        if not new_username:
            messagebox.showerror("Update failed", "Enter a username.")
            return
        try:
            self.on_update_username(user_id, new_username)
        except Exception as exc:
            messagebox.showerror("Update failed", str(exc))
            return
        row = self.users[user_id]
        row["username"] = new_username
        name = row["first_name"] or ""
        status = "Active" if row["active"] else "Inactive"
        self.tree.item(
            str(user_id),
            values=(new_username, name, row["role"], status),
        )
        display_name = row["first_name"] or new_username
        self.selected_label.config(
            text=f"Selected: {display_name} ({row['role']})",
            foreground=self.colors["text"],
        )
        messagebox.showinfo("User updated", "Username updated successfully.")

    def _reset_pin(self):
        user_id = self._require_selection()
        if user_id is None:
            return
        new_pin = (self.pin_var.get() or "").strip()
        if not new_pin:
            messagebox.showerror("Reset failed", "Enter a new PIN.")
            return
        try:
            self.on_reset_pin(user_id, new_pin)
        except Exception as exc:
            messagebox.showerror("Reset failed", str(exc))
            return
        self.pin_var.set("")
        messagebox.showinfo("PIN reset", "PIN reset successfully.")

    def _add_user(self):
        if not self.on_create_user:
            messagebox.showerror("Add user failed", "User creation is not available.")
            return
        username = (self.add_username_var.get() or "").strip()
        name = (self.add_name_var.get() or "").strip()
        role = (self.add_role_var.get() or "").strip().lower()
        pin = (self.add_pin_var.get() or "").strip()
        if not username:
            messagebox.showerror("Add user failed", "Enter a username.")
            return
        if not pin:
            messagebox.showerror("Add user failed", "Enter a PIN.")
            return
        try:
            new_user = self.on_create_user(username, pin, name or None, role)
        except Exception as exc:
            messagebox.showerror("Add user failed", str(exc))
            return
        if not new_user:
            messagebox.showerror("Add user failed", "User could not be created.")
            return
        user_id = new_user["id"]
        self.users[user_id] = {key: new_user[key] for key in new_user.keys()}
        if self.view_mode == "inactive":
            self.view_mode = "active"
            self.view_button.config(text="Inactive Users")
            self.toggle_active_button.config(text="Make Inactive")
        self._load_users()
        if self.tree.exists(str(user_id)):
            self.tree.selection_set(str(user_id))
            self.tree.see(str(user_id))
            self._on_select(None)
        self.add_username_var.set("")
        self.add_name_var.set("")
        self.add_pin_var.set("")
        self.add_role_var.set("cashier")
        messagebox.showinfo("User added", "User created successfully.")

    def _toggle_view(self):
        self.view_mode = "inactive" if self.view_mode == "active" else "active"
        label = "Inactive Users" if self.view_mode == "active" else "Active Users"
        self.view_button.config(text=label)
        if self.view_mode == "active":
            self.toggle_active_button.config(text="Make Inactive")
        else:
            self.toggle_active_button.config(text="Make Active")
        self._load_users()

    def _toggle_active(self):
        if not self.on_set_active:
            messagebox.showerror("Update failed", "User status update is unavailable.")
            return
        user_id = self._require_selection()
        if user_id is None:
            return
        row = self.users.get(user_id)
        if not row:
            messagebox.showerror("Update failed", "User not found.")
            return
        name = row["first_name"] or row["username"]
        if self.view_mode == "active":
            if row["role"] != "cashier":
                messagebox.showerror(
                    "Deactivate failed",
                    "Only cashier users can be made inactive.",
                )
                return
            confirm = messagebox.askyesno(
                "Confirm deactivation",
                f"Make {name} inactive?",
            )
            if not confirm:
                return
            active = False
        else:
            confirm = messagebox.askyesno(
                "Confirm activation",
                f"Make {name} active?",
            )
            if not confirm:
                return
            active = True
        try:
            updated = self.on_set_active(user_id, active)
        except Exception as exc:
            messagebox.showerror("Update failed", str(exc))
            return
        if updated:
            self.users[user_id] = {key: updated[key] for key in updated.keys()}
        else:
            self.users[user_id]["active"] = 1 if active else 0
        self._load_users()
        message = "User activated." if active else "User made inactive."
        messagebox.showinfo("User updated", message)

    def _require_selection(self):
        if self.selected_user_id is None:
            messagebox.showwarning("Select user", "Select a user first.")
            return None
        return self.selected_user_id

    def _clear_selection(self):
        self.selected_user_id = None
        self.tree.selection_remove(self.tree.selection())
        self.selected_label.config(
            text="Select a user to edit.",
            foreground=self.colors["text_light"],
        )
        self.username_var.set("")
        self.pin_var.set("")

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

    @staticmethod
    def _bind_enter(widget, handler):
        def _on_enter(_event):
            handler()
            return "break"

        widget.bind("<Return>", _on_enter)
        widget.bind("<KP_Enter>", _on_enter)
