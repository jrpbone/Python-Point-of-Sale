from pathlib import Path
import tkinter as tk


FONT_FAMILY = "Segoe UI"  # Global UI font family used across all screens.
LOW_STOCK_THRESHOLD = 5  # Warn when stock is at or below this level.
APP_ICON_PATH = Path(__file__).resolve().parents[2] / "assets" / "pos.ico"

PALETTE = {
    "bg_main": "#f4f7fb",  # App window background behind all content.
    "bg_card": "#ffffff",  # Surface color for cards and dialogs.
    "bg_subtle": "#eef3f8",  # Secondary surfaces and table headings.
    "nav": "#0f172a",  # Main navigation and branded panels.
    "nav_light": "#1e293b",  # Hover state on dark surfaces.
    "nav_text": "#f8fafc",  # Text shown on dark surfaces.
    "primary": "#2563eb",  # Primary action buttons and highlights.
    "primary_dark": "#1d4ed8",  # Active/hover state for primary buttons.
    "primary_soft": "#e8f0ff",  # Low-emphasis primary surface.
    "success": "#059669",  # Success buttons and money emphasis.
    "success_dark": "#047857",  # Success hover state.
    "warning": "#d97706",  # Warning accents and callouts.
    "danger": "#dc2626",  # Destructive actions (remove/clear).
    "danger_dark": "#b91c1c",  # Destructive hover state.
    "border": "#dbe3ee",  # Card, entry, and table borders.
    "text": "#172033",  # Default text color.
    "text_light": "#64748b",  # Secondary text (subheaders, hints).
}

FOCUS_BORDER = "#2563eb"  # Focus ring/border color for inputs and buttons.

# Typography (applies across cards and dialogs)
FONT_LABEL = 12  # Standard label text size.
FONT_HEADER = 26  # Large card header size (e.g., "POS Login").
FONT_SUBHEADER = 13  # Subheader size (secondary titles).
FONT_MONEY = 26  # Subtotal/total money emphasis.
FONT_BUTTON = 10  # Button label size.
FONT_KEYPAD = 18  # Numpad key size.
FONT_TREE = 11  # Treeview row text size.
FONT_LABELLFRAME = 10  # Labelframe title size.

# Global widget chrome (applies to all cards and dialogs)
BORDER_WIDTH = 1  # Border width for entries and buttons.
FOCUS_THICKNESS = 0  # ttk focus thickness (focus uses border color).
ENTRY_PADDING = 10  # Entry inner padding for text fields.
BUTTON_PADDING = 10  # Default padding for standard buttons.
DANGER_BUTTON_PADDING = 10  # Padding for remove/clear buttons.
KEYPAD_BUTTON_PADDING = 15  # Padding inside keypad buttons.

# POS screen layout (top-level containers)
TOP_BAR_PADDING = 20  # Inner padding of the top bar (user + action buttons).
CONTENT_PADDING = 20  # Padding around the main two-column content area.
LEFT_COL_PADX = (0, 16)  # Gap between left column and center divider.
RIGHT_COL_PADX = (0, 0)  # Right column outer spacing.
LOAD_PRODUCTS_PADX = 8  # Spacing between toolbar buttons.
POS_USER_LABEL_FONT_SIZE = 12  # "Logged in as" text size on top bar.

# Enter Item card (left column)
ENTER_ITEM_PADDING = 20  # Inner padding for the "Enter Item" card.
POS_ENTRY_CARD_OUTER_PAD = (0, 16)  # Space below "Enter Item" card.
SKU_ENTRY_PADY = (5, 10)  # Vertical padding around the SKU entry field.
POS_ENTRY_FONT_SIZE = 14  # SKU entry font size.
QTY_ACTION_PADY = (10, 0)  # Spacing above the quantity/checkout row.
QTY_LABEL_PADX = (0, 6)  # Gap between "Quantity" label and entry.
QTY_ENTRY_WIDTH = 10  # Quantity entry width (characters).
POS_QTY_ENTRY_FONT_SIZE = 14  # Quantity entry font size.

# Keypad block (left column)
KEYPAD_SECTION_PADY = (0, 7)  # Padding around keypad block.
KEYPAD_BUTTON_GRID_PADX = 5  # Horizontal spacing between keypad buttons.
KEYPAD_BUTTON_GRID_PADY = 5  # Vertical spacing between keypad buttons.
KEYPAD_BACK_LABEL = "\u232b"  # Backspace symbol shown on keypad.

# Bottom action row (Enter + Remove/Clear + Subtotal)
ENTER_BUTTON_WIDTH = 80  # Width for the Enter button (characters).
DANGER_BUTTON_WIDTH = 10  # Width for Remove/Clear buttons (characters).
ADMIN_BUTTON_WIDTH = 12  # Width for admin action buttons (Load/Export/Backup/Reports).
#ACTION_BUTTON_SPACING_PADX = (10, 0) Spacing between Remove and Clear buttons.
TOTAL_LABEL_PADY = (0, 15)  # Vertical padding for the Subtotal label row.
TOTALS_BOTTOM_PAD = 15  # Padding under the shared bottom action row.

# Current Sale card (right column)
POS_CART_CARD_OUTER_PAD = (0, 10)  # Space below Current Sale card.
CART_CARD_PADDING = 0  # Padding between card border and table contents.

# Current Sale table (Treeview) columns and rows
CART_COL_NAME_WIDTH = 320  # Product Name column width.
CART_COL_NAME_MIN = 200  # Product Name minimum width.
CART_COL_SKU_WIDTH = 120  # SKU column width.
CART_COL_SKU_MIN = 90  # SKU minimum width.
CART_COL_PRICE_WIDTH = 120  # Price column width.
CART_COL_PRICE_MIN = 90  # Price minimum width.
CART_COL_QTY_WIDTH = 70  # Qty column width.
CART_COL_QTY_MIN = 60  # Qty minimum width.
CART_COL_TOTAL_WIDTH = 130  # Total column width.
CART_COL_TOTAL_MIN = 100  # Total minimum width.
CART_COL_STOCK_WIDTH = 120  # Stock column width; fits the full "AVAILABLE" heading.
CART_COL_STOCK_MIN = 110  # Prevent the inventory heading from being cropped.
TREE_ROW_HEIGHT = 42  # Height of each row in the Current Sale table.

# Payment dialog card
PAYMENT_CONTAINER_PADDING = 24  # Outer padding around payment dialog.
PAYMENT_CARD_PADDING = 24  # Inner padding inside payment card.
PAYMENT_CARD_OUTER_PAD = (0, 16)  # Space below payment card.
PAYMENT_HEADER_PADX = 6  # Horizontal padding for payment header row.
PAYMENT_HEADER_PADY = (0, 12)  # Vertical padding for payment header row.
PAYMENT_ROW_PADX = 10  # Horizontal padding for payment rows.
PAYMENT_ROW_PADY = 6  # Vertical padding for payment rows.
PAYMENT_SEPARATOR_PADX = 6  # Horizontal padding for payment separator line.
PAYMENT_SEPARATOR_PADY = 10  # Vertical padding for payment separator line.
PAYMENT_FOOTNOTE_PADY = (0, 8)  # Padding under "All amounts are in PHP".
PAYMENT_ACTIONS_PADY = (6, 0)  # Padding around payment action buttons.
PAYMENT_CONFIRM_PADX = (0, 10)  # Gap between Confirm and Cancel buttons.
CURRENCY_LABEL_PADX = (0, 4)  # Space before currency label "P".
MONEY_ENTRY_WIDTH = 16  # Width of amount entries (characters).
PAYMENT_METHOD_WIDTH = 16  # Width of payment method dropdown (characters).
PAYMENT_SUBTOTAL_FONT_SIZE = 12  # Subtotal row font size in dialog.
PAYMENT_TOTAL_FONT_SIZE = 14  # Total row font size in dialog.
PAYMENT_METHOD_FONT_SIZE = 11  # Font size for payment method dropdown.

# Admin auth dialog card
ADMIN_CONTAINER_PADDING = 20  # Outer padding around admin dialog.
ADMIN_CARD_PADDING = 20  # Inner padding inside admin card.
ADMIN_CARD_OUTER_PAD = (0, 20)  # Space below admin card.
ADMIN_HEADER_PADY = (0, 10)  # Padding under "Admin Access Required".
ADMIN_SUBHEADER_PADY = (0, 15)  # Padding under admin instruction text.
ADMIN_LABEL_PADY = 6  # Padding under "Admin PIN" label.
ADMIN_ENTRY_PADY = (0, 5)  # Padding under admin PIN entry.
ADMIN_ACTIONS_PADY = 5  # Padding around admin action buttons.
ADMIN_AUTHORIZE_PADX = (0, 10)  # Gap between Authorize and Cancel.
ADMIN_ENTRY_WIDTH = 28  # Admin PIN entry width (characters).

# Login card (login_view)
LOGIN_CARD_PADDING = 42  # Inner padding for login card.
LOGIN_CARD_OUTER_PAD = (0, 0)  # Outer padding around login card.
LOGIN_TITLE_PADY = (0, 20)  # Padding under "POS Login" title.
LOGIN_SUBTITLE_PADY = (0, 30)  # Padding under login subtitle text.
LOGIN_FORM_PADY = 10  # Padding around login form fields.
LOGIN_LABEL_PADY = 6  # Padding under each label in the login form.
LOGIN_ENTRY_USER_PADY = (0, 15)  # Padding under username entry.
LOGIN_ENTRY_PIN_PADY = (0, 25)  # Padding under PIN entry.
LOGIN_BUTTON_PADY = 10  # Padding above/below the login button.
LOGIN_ENTRY_WIDTH = 36  # Width of login input fields (characters).
LOGIN_BUTTON_WIDTH = 28  # Width of login button (characters).
LOGIN_BG_BORDER_WIDTH = 0  # Border width around login background image.
LOGIN_BG_SCALE_PERCENT = 200  # Background image scale percent.
SCALE_PERCENT_DEN = 100  # Background image scale denominator.


def get_palette():
    return dict(PALETTE)


def apply_window_icon(window):
    """Apply the shared application icon to a Tk or Toplevel window."""
    if not APP_ICON_PATH.exists():
        return False
    try:
        # The default icon is inherited by child windows and native Tk dialogs.
        window.iconbitmap(str(APP_ICON_PATH), default=str(APP_ICON_PATH))
    except (tk.TclError, OSError):
        return False
    return True


def apply_theme(style, colors):
    style.theme_use("clam")
    focus_border = FOCUS_BORDER

    style.configure("Main.TFrame", background=colors["bg_main"])
    style.configure("Card.TFrame", background=colors["bg_card"], relief="flat")
    style.configure("Subtle.TFrame", background=colors["bg_subtle"], relief="flat")
    style.configure("Topbar.TFrame", background=colors["nav"], relief="flat")
    style.configure("TopbarLight.TFrame", background=colors["nav_light"], relief="flat")

    style.configure(
        "TLabel",
        background=colors["bg_main"],
        foreground=colors["text"],
        font=(FONT_FAMILY, FONT_LABEL),
    )
    style.configure(
        "Card.TLabel",
        background=colors["bg_card"],
        foreground=colors["text"],
        font=(FONT_FAMILY, FONT_LABEL),
    )
    style.configure(
        "Header.TLabel",
        font=(FONT_FAMILY, FONT_HEADER, "bold"),
        background=colors["bg_card"],
        foreground=colors["text"],
    )
    style.configure(
        "Subheader.TLabel",
        font=(FONT_FAMILY, FONT_SUBHEADER, "bold"),
        background=colors["bg_card"],
        foreground=colors["text_light"],
    )
    style.configure(
        "PageTitle.TLabel",
        font=(FONT_FAMILY, 18, "bold"),
        background=colors["bg_main"],
        foreground=colors["text"],
    )
    style.configure(
        "CardTitle.TLabel",
        font=(FONT_FAMILY, 12, "bold"),
        background=colors["bg_card"],
        foreground=colors["text"],
    )
    style.configure(
        "Eyebrow.TLabel",
        font=(FONT_FAMILY, 9, "bold"),
        background=colors["bg_card"],
        foreground=colors["primary"],
    )
    style.configure(
        "Muted.TLabel",
        font=(FONT_FAMILY, 10),
        background=colors["bg_main"],
        foreground=colors["text_light"],
    )
    style.configure(
        "CardMuted.TLabel",
        font=(FONT_FAMILY, 10),
        background=colors["bg_card"],
        foreground=colors["text_light"],
    )
    style.configure(
        "TopbarTitle.TLabel",
        font=(FONT_FAMILY, 18, "bold"),
        background=colors["nav"],
        foreground=colors["nav_text"],
    )
    style.configure(
        "TopbarText.TLabel",
        font=(FONT_FAMILY, 10),
        background=colors["nav"],
        foreground="#cbd5e1",
    )
    style.configure(
        "TopbarPill.TLabel",
        font=(FONT_FAMILY, 10, "bold"),
        background=colors["nav_light"],
        foreground=colors["nav_text"],
        padding=(14, 9),
    )
    style.configure(
        "Money.TLabel",
        font=(FONT_FAMILY, FONT_MONEY, "bold"),
        foreground=colors["success"],
        background=colors["bg_main"],
    )
    style.configure(
        "CardMoney.TLabel",
        font=(FONT_FAMILY, FONT_MONEY, "bold"),
        foreground=colors["success"],
        background=colors["bg_card"],
    )

    style.configure(
        "TButton",
        font=(FONT_FAMILY, FONT_BUTTON, "bold"),
        padding=BUTTON_PADDING,
        borderwidth=BORDER_WIDTH,
        focusthickness=FOCUS_THICKNESS,
        focuscolor=focus_border,
    )
    style.map(
        "TButton",
        background=[
            ("disabled", "#cbd5e1"),
            ("pressed", colors["primary_dark"]),
            ("active", colors["primary_dark"]),
            ("!active", colors["primary"]),
        ],
        foreground=[("disabled", "#f8fafc"), ("!disabled", "white")],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure(
        "Secondary.TButton",
        background=colors["bg_card"],
        foreground=colors["text"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
    )
    style.map(
        "Secondary.TButton",
        background=[("pressed", colors["bg_subtle"]), ("active", colors["bg_subtle"])],
        foreground=[("disabled", colors["text_light"]), ("!disabled", colors["text"])],
        bordercolor=[("focus", focus_border), ("!focus", colors["border"])],
        lightcolor=[("focus", focus_border), ("!focus", colors["border"])],
        darkcolor=[("focus", focus_border), ("!focus", colors["border"])],
    )

    style.configure(
        "Topbar.TButton",
        background=colors["nav_light"],
        foreground=colors["nav_text"],
        bordercolor=colors["nav_light"],
        lightcolor=colors["nav_light"],
        darkcolor=colors["nav_light"],
        padding=(14, 8),
    )
    style.map(
        "Topbar.TButton",
        background=[("active", "#334155"), ("pressed", "#475569")],
        foreground=[("!disabled", colors["nav_text"])],
    )

    style.configure(
        "Keypad.TButton",
        font=(FONT_FAMILY, FONT_KEYPAD, "bold"),
        padding=KEYPAD_BUTTON_PADDING,
    )
    style.map(
        "Keypad.TButton",
        background=[("pressed", colors["primary_soft"]), ("active", colors["bg_subtle"]), ("!active", "white")],
        foreground=[("active", colors["primary"]), ("!active", colors["text"])],
        bordercolor=[("focus", focus_border), ("!focus", colors["border"])],
        lightcolor=[("focus", focus_border), ("!focus", colors["border"])],
        darkcolor=[("focus", focus_border), ("!focus", colors["border"])],
    )

    style.configure("Success.TButton", background=colors["success"])
    style.map(
        "Success.TButton",
        background=[("active", colors["success_dark"]), ("pressed", colors["success_dark"]), ("!active", colors["success"])],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure(
        "Danger.TButton",
        background=colors["danger"],
        padding=DANGER_BUTTON_PADDING,
    )
    style.map(
        "Danger.TButton",
        background=[("active", colors["danger_dark"]), ("pressed", colors["danger_dark"]), ("!active", colors["danger"])],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )
    style.configure(
        "DangerOutline.TButton",
        background=colors["bg_card"],
        foreground=colors["danger"],
        bordercolor="#fecaca",
        lightcolor="#fecaca",
        darkcolor="#fecaca",
    )
    style.map(
        "DangerOutline.TButton",
        background=[("active", "#fef2f2"), ("pressed", "#fee2e2")],
        foreground=[("!disabled", colors["danger_dark"])],
        bordercolor=[("focus", colors["danger"]), ("!focus", "#fecaca")],
        lightcolor=[("focus", colors["danger"]), ("!focus", "#fecaca")],
        darkcolor=[("focus", colors["danger"]), ("!focus", "#fecaca")],
    )

    style.configure(
        "TEntry",
        fieldbackground="white",
        padding=ENTRY_PADDING,
        font=(FONT_FAMILY, FONT_LABEL),
        borderwidth=BORDER_WIDTH,
        focusthickness=FOCUS_THICKNESS,
        focuscolor=focus_border,
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
    )
    style.map(
        "TEntry",
        bordercolor=[("focus", focus_border), ("!focus", colors["border"])],
        lightcolor=[("focus", focus_border), ("!focus", colors["border"])],
        darkcolor=[("focus", focus_border), ("!focus", colors["border"])],
    )
    style.configure(
        "TCombobox",
        fieldbackground=colors["bg_card"],
        background=colors["bg_card"],
        foreground=colors["text"],
        padding=8,
        arrowsize=14,
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
    )
    style.map(
        "TCombobox",
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        foreground=colors["text"],
        font=(FONT_FAMILY, FONT_TREE),
        rowheight=TREE_ROW_HEIGHT,
        borderwidth=0,
        relief="flat",
    )
    style.configure(
        "Treeview.Heading",
        font=(FONT_FAMILY, 10, "bold"),
        background=colors["bg_subtle"],
        foreground=colors["text_light"],
        padding=(10, 12),
        relief="flat",
    )
    style.map(
        "Treeview.Heading",
        background=[("active", colors["primary_soft"])],
        foreground=[("active", colors["primary"])],
    )
    style.map(
        "Treeview",
        background=[("selected", colors["primary_soft"])],
        foreground=[("selected", colors["primary_dark"])],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure(
        "TLabelframe",
        background=colors["bg_card"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "TLabelframe.Label",
        background=colors["bg_card"],
        font=(FONT_FAMILY, FONT_LABELLFRAME, "bold"),
        foreground=colors["text"],
    )
    style.configure("TSeparator", background=colors["border"])
    style.configure(
        "TProgressbar",
        background=colors["primary"],
        troughcolor=colors["bg_subtle"],
        bordercolor=colors["bg_subtle"],
        lightcolor=colors["primary"],
        darkcolor=colors["primary"],
        thickness=12,
    )
