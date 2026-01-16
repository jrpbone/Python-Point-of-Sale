FONT_FAMILY = "Segoe UI"  # Global UI font family used across all screens.
LOW_STOCK_THRESHOLD = 5  # Warn when stock is at or below this level.

PALETTE = {
    "bg_main": "#f3f4f6",  # App window background behind all content.
    "bg_card": "#ffffff",  # Surface color for cards and dialogs.
    "primary": "#3b82f6",  # Primary action buttons and highlights.
    "primary_dark": "#2563eb",  # Active/hover state for primary buttons.
    "success": "#10b981",  # Success buttons and money emphasis.
    "warning": "#f59e0b",  # Warning accents and callouts.
    "danger": "#ef4444",  # Destructive actions (remove/clear).
    "text": "#1f2937",  # Default text color.
    "text_light": "#6b7280",  # Secondary text (subheaders, hints).
}

FOCUS_BORDER = "#111827"  # Focus ring/border color for inputs and buttons.

# Typography (applies across cards and dialogs)
FONT_LABEL = 12  # Standard label text size.
FONT_HEADER = 24  # Large card header size (e.g., "POS Login").
FONT_SUBHEADER = 14  # Subheader size (secondary titles).
FONT_MONEY = 20  # Subtotal/total money emphasis.
FONT_BUTTON = 11  # Button label size.
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
TOP_BAR_PADDING = 10  # Inner padding of the top bar (user + action buttons).
CONTENT_PADDING = 10  # Padding around the main two-column content area.
LEFT_COL_PADX = (0, 10)  # Gap between left column and center divider.
RIGHT_COL_PADX = (10, 0)  # Gap between right column and center divider.
LOAD_PRODUCTS_PADX = 10  # Spacing between Load Products and Logout buttons.
POS_USER_LABEL_FONT_SIZE = 12  # "Logged in as" text size on top bar.

# Enter Item card (left column)
ENTER_ITEM_PADDING = 15  # Inner padding for the "Enter Item" card.
POS_ENTRY_CARD_OUTER_PAD = (0, 15)  # Space below "Enter Item" card.
SKU_ENTRY_PADY = (5, 10)  # Vertical padding around the SKU entry field.
POS_ENTRY_FONT_SIZE = 14  # SKU entry font size.
QTY_ACTION_PADY = (10, 0)  # Spacing above the quantity/checkout row.
QTY_LABEL_PADX = (0, 6)  # Gap between "Quantity" label and entry.
QTY_ENTRY_WIDTH = 10  # Quantity entry width (characters).
POS_QTY_ENTRY_FONT_SIZE = 14  # Quantity entry font size.

# Keypad block (left column)
KEYPAD_SECTION_PADY = (0, 7)  # Padding around keypad block.
KEYPAD_BUTTON_GRID_PADX = 4  # Horizontal spacing between keypad buttons.
KEYPAD_BUTTON_GRID_PADY = 4  # Vertical spacing between keypad buttons.
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
CART_COL_STOCK_WIDTH = 90  # Stock column width.
CART_COL_STOCK_MIN = 70  # Stock minimum width.
TREE_ROW_HEIGHT = 35  # Height of each row in the Current Sale table.

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
LOGIN_CARD_PADDING = 50  # Inner padding for login card.
LOGIN_CARD_OUTER_PAD = (0, 0)  # Outer padding around login card.
LOGIN_TITLE_PADY = (0, 20)  # Padding under "POS Login" title.
LOGIN_SUBTITLE_PADY = (0, 30)  # Padding under login subtitle text.
LOGIN_FORM_PADY = 10  # Padding around login form fields.
LOGIN_LABEL_PADY = 6  # Padding under each label in the login form.
LOGIN_ENTRY_USER_PADY = (0, 15)  # Padding under username entry.
LOGIN_ENTRY_PIN_PADY = (0, 25)  # Padding under PIN entry.
LOGIN_BUTTON_PADY = 10  # Padding above/below the login button.
LOGIN_ENTRY_WIDTH = 50  # Width of login input fields (characters).
LOGIN_BUTTON_WIDTH = 20  # Width of login button (characters).
LOGIN_BG_BORDER_WIDTH = 0  # Border width around login background image.
LOGIN_BG_SCALE_PERCENT = 200  # Background image scale percent.
SCALE_PERCENT_DEN = 100  # Background image scale denominator.


def get_palette():
    return dict(PALETTE)


def apply_theme(style, colors):
    style.theme_use("clam")
    focus_border = FOCUS_BORDER

    style.configure("Main.TFrame", background=colors["bg_main"])
    style.configure("Card.TFrame", background=colors["bg_card"], relief="flat")

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
        foreground=colors["primary"],
    )
    style.configure(
        "Subheader.TLabel",
        font=(FONT_FAMILY, FONT_SUBHEADER, "bold"),
        background=colors["bg_card"],
        foreground=colors["text_light"],
    )
    style.configure(
        "Money.TLabel",
        font=(FONT_FAMILY, FONT_MONEY, "bold"),
        foreground=colors["success"],
        background=colors["bg_main"],
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
        background=[("active", colors["primary_dark"]), ("!active", colors["primary"])],
        foreground=[("active", "white"), ("!active", "white")],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure(
        "Keypad.TButton",
        font=(FONT_FAMILY, FONT_KEYPAD, "bold"),
        padding=KEYPAD_BUTTON_PADDING,
    )
    style.map(
        "Keypad.TButton",
        background=[("active", "#e5e7eb"), ("!active", "white")],
        foreground=[("active", colors["primary"]), ("!active", colors["text"])],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure("Success.TButton", background=colors["success"])
    style.map(
        "Success.TButton",
        background=[("active", "#059669"), ("!active", colors["success"])],
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
        background=[("active", "#dc2626"), ("!active", colors["danger"])],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure(
        "TEntry",
        fieldbackground="white",
        padding=ENTRY_PADDING,
        font=(FONT_FAMILY, FONT_LABEL),
        borderwidth=BORDER_WIDTH,
        focusthickness=FOCUS_THICKNESS,
        focuscolor=focus_border,
    )
    style.map(
        "TEntry",
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
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
    )
    style.configure(
        "Treeview.Heading",
        font=(FONT_FAMILY, FONT_TREE, "bold"),
        background=colors["bg_main"],
        foreground=colors["text"],
    )
    style.map(
        "Treeview",
        background=[("selected", colors["primary"])],
        foreground=[("selected", "white")],
        bordercolor=[("focus", focus_border)],
        lightcolor=[("focus", focus_border)],
        darkcolor=[("focus", focus_border)],
    )

    style.configure("TLabelframe", background=colors["bg_main"])
    style.configure(
        "TLabelframe.Label",
        background=colors["bg_main"],
        font=(FONT_FAMILY, FONT_LABELLFRAME, "bold"),
        foreground=colors["text_light"],
    )
