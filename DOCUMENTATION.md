# POS System Documentation

## 1. Project Overview

- Purpose: Desktop point-of-sale system for product lookup, cart management, checkout, inventory adjustments, admin import/export, user management (create users, reset PINs, activate/deactivate cashiers), automated logout backups, restore, and audit tracking.
- High-level architecture: Tkinter UI (views and dialogs), controller layer (PosController), business logic layer (PosService and CartService), persistence via SQLite repositories, and UI constants in `app/ui/config.py`.
- Target use case: Small retail or kiosk operations that need an offline-capable POS with basic inventory management and lightweight reporting.

## 2. Application Architecture

### Structure

- `main.py` configures logging, bootstraps the database, constructs `PosService`, and starts the Tkinter UI.
- `app/db.py` encapsulates SQLite setup, schema creation, seed data, and backup/restore utilities.
- Repository classes in `app/repositories/` implement table-level CRUD and reporting queries.
- `app/services/pos_service.py` orchestrates POS workflows (checkout, import/export, reporting) with transactions and connection recovery.
- `app/ui/importers.py` runs import/export work in background threads and posts UI updates via `after()`.
- UI is split into views (`app/ui/views/`), dialogs (`app/ui/dialogs/`), and a controller (`app/ui/controllers/pos_controller.py`).

### Role of Tkinter

- Tkinter provides the main window, frames, dialogs, and widgets (Treeview, buttons, entries).
- Event handling uses Tkinter callbacks and key bindings (`<Return>`, `<Tab>`, `<F1>`, `<F2>`), with layout managed by `pack`, `grid`, and `place`.
- Long-running import/export tasks run in background threads and update the UI through `after()` callbacks.
- User feedback relies on `tkinter.messagebox` for modal errors, warnings, confirmations, and info.
- Tkinter callback exceptions are logged via `report_callback_exception`.

### Configuration and Constants

- Configuration is code-driven via `app/ui/config.py` (UI look-and-feel) and `app/settings.py` (tax settings).
- Styles are applied centrally in `apply_theme`, and constants are imported by UI components.
- There is no active `.ini` configuration file loaded by the codebase.

## 3. File-by-File Breakdown

### Root Files

#### `.gitignore`

- Purpose: Git ignore rules for local artifacts and data files.
- Responsibilities: Prevents generated files and local data from being committed.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `main.py`

- Purpose: Application entry point.
- Responsibilities: Configures rotating application logging and exception hooks; initializes DB schema and seed data; creates SQLite connection; constructs `PosService`; starts Tkinter main loop.
- Key imports:
  - `logging`, `RotatingFileHandler`, `threading`, `sys` for log setup and exception hooks.
  - `app.db` for DB lifecycle functions and log location.
  - `PosService` for business logic.
  - `run_app` to launch the UI.
- Public functions/classes:
  - `main()`: Bootstraps the application.

#### `DOCUMENTATION.md`

- Purpose: Project documentation.
- Responsibilities: Describes architecture, usage, and maintenance for developers.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `products.xlsx`

- Purpose: Default product import file referenced by UI state.
- Responsibilities: Provides product rows for import.
- Key imports: N/A (read by `openpyxl` in `app/ui/importers.py`).
- Public functions/classes: N/A.

#### `dbProducts.xlsx`

- Purpose: Product export output file.
- Responsibilities: Stores exported database products in Excel format.
- Key imports: N/A (written by `openpyxl` in `app/ui/importers.py`).
- Public functions/classes: N/A.

#### `sales.xlsx`

- Purpose: Sales export log (Excel).
- Responsibilities: Appended to on each checkout in `PosService._export_sale`.
- Key imports: N/A (written by `openpyxl`).
- Public functions/classes: N/A.

#### `assets/shop.png`

- Purpose: Login screen background image.
- Responsibilities: Rendered by `LoginView` via `tk.PhotoImage`.
- Key imports: N/A.
- Public functions/classes: N/A.

### Tests: `tests/`

#### `tests/test_smoke.py`

- Purpose: Lightweight regression coverage for critical flows.
- Responsibilities: Verifies import/update, export, and backup/restore behavior against a temporary SQLite DB.
- Key imports:
  - `app.db` to initialize a temporary database.
  - `PosService` to drive import logic.
  - `app.ui.importers` for export worker coverage.
- Public functions/classes: `SmokeTests` (unittest.TestCase).

### Core Package: `app/`

#### `app/__init__.py`

- Purpose: Package marker for `app`.
- Responsibilities: Enables package imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/db.py`

- Purpose: SQLite connection and schema management.
- Responsibilities: Creates tables and indexes; seeds default data; ensures required columns; provides backup/restore helpers; sets audit log timestamps to UTC+8 by default.
- Key imports:
  - `sqlite3` for database access.
  - `shutil`, `datetime`, `pathlib.Path` for backup/restore paths.
  - `app.security.hash_pin` to seed hashed PINs.
- Public functions/classes:
  - `get_connection()`: Returns a configured SQLite connection.
  - `init_db()`: Creates schema and indexes.
  - `seed_data()`: Inserts default users and categories when missing.
  - `backup_database()`: Copies `pos.db` to a timestamped backup.
  - `restore_database()`: Replaces `pos.db` from a selected backup, optionally creating a safety backup.

#### `app/models.py`

- Purpose: Data model definitions.
- Responsibilities: Defines `Product` and `User` dataclasses used across layers.
- Key imports: `dataclasses.dataclass` for lightweight model types.
- Public functions/classes:
  - `Product`: Product record with pricing and inventory.
  - `User`: User record with role and name.

#### `app/security.py`

- Purpose: PIN hashing and verification utilities.
- Responsibilities: Hashes PINs and verifies them for authentication.
- Key imports: `hashlib`, `hmac`, `os`, `base64` for PBKDF2 hashing.
- Public functions/classes:
  - `hash_pin()`, `verify_pin()`, `is_hashed()`.

#### `app/settings.py`

- Purpose: Tax configuration for checkout.
- Responsibilities: Defines `TAX_RATE` and `TAX_ROUNDING` used by checkout and payment totals.
- Key imports: N/A.
- Public functions/classes: N/A.

### Services: `app/services/`

#### `app/services/__init__.py`

- Purpose: Package marker.
- Responsibilities: Enables service imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/services/pos_service.py`

- Purpose: Central POS business logic.
- Responsibilities: Authentication, user provisioning and activation state, import validation, batch import updates, checkout transactions, stock updates, audit logging, reporting, and connection recovery.
- Key imports:
  - Repository classes for data access.
  - `csv` and `openpyxl` for exports.
- Public functions/classes:
  - `PosService`: Main service class.
  - `CartItem`: Dataclass for checkout items.
  - `preview_import()`, `import_products()`, `checkout()`, `get_sales_summary()`, `log_admin_action()`.
  - `list_users()`, `create_user()`, `set_user_active()`.

### Repositories: `app/repositories/`

#### `app/repositories/__init__.py`

- Purpose: Package marker.
- Responsibilities: Enables repository imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/repositories/audit_repository.py`

- Purpose: Audit log persistence.
- Responsibilities: Writes audit entries to `audit_logs` with UTC+8 timestamps.
- Key imports: N/A.
- Public functions/classes:
  - `AuditRepository.add_entry()`, `AuditRepository.add_entries()`.

#### `app/repositories/category_repository.py`

- Purpose: Category lookup and creation.
- Responsibilities: Returns existing category IDs or inserts new ones.
- Key imports: N/A.
- Public functions/classes:
  - `CategoryRepository.get_or_create()`.

#### `app/repositories/payment_repository.py`

- Purpose: Payment persistence.
- Responsibilities: Inserts payment records per sale.
- Key imports: N/A.
- Public functions/classes:
  - `PaymentRepository.add_payment()`.

#### `app/repositories/product_repository.py`

- Purpose: Product CRUD and lookup.
- Responsibilities: Query by SKU/barcode, update quantities (single and bulk), upsert products, list catalog, and map existing SKUs for import.
- Key imports: `app.models.Product` for typed results.
- Public functions/classes:
  - `list_products()`, `get_by_sku()`, `get_by_exact_sku()`, `get_sku_map()`.
  - `update_quantity()`, `update_quantities_bulk()`, `insert_many()`.

#### `app/repositories/sale_repository.py`

- Purpose: Sales persistence and reporting queries.
- Responsibilities: Inserts sales and line items; provides summary and top-SKU queries.
- Key imports: N/A.
- Public functions/classes:
  - `create_sale()`, `add_line_item()`, `totals_since()`, `top_skus_since()`.

#### `app/repositories/stock_repository.py`

- Purpose: Stock movement logging.
- Responsibilities: Records inventory changes with movement type.
- Key imports: N/A.
- Public functions/classes:
  - `add_movement()`.

#### `app/repositories/user_repository.py`

- Purpose: User authentication and PIN verification.
- Responsibilities: Validates credentials, lists users, creates users, updates usernames, resets PINs, and toggles active status.
- Key imports: `app.security` for hash verification; `app.models.User` for return types.
- Public functions/classes:
  - `authenticate()`, `authenticate_admin()`, `list_users()`, `create_user()`.
  - `update_username()`, `reset_pin()`, `get_user_by_id()`, `set_active()`.

### UI Core: `app/ui/`

#### `app/ui/__init__.py`

- Purpose: Package marker.
- Responsibilities: Enables UI imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/ui/config.py`

- Purpose: UI constants and ttk theme configuration.
- Responsibilities: Defines palette, fonts, spacing, and widget sizing; configures ttk styles.
- Key imports: N/A.
- Public functions/classes:
  - `get_palette()`: Returns palette dict.
  - `apply_theme()`: Applies ttk styles to the root theme.

#### `app/ui/formatting.py`

- Purpose: Formatting helpers.
- Responsibilities: Formats currency strings for display.
- Key imports: N/A.
- Public functions/classes:
  - `format_currency()`.

#### `app/ui/importers.py`

- Purpose: Product import/export helpers and file parsing.
- Responsibilities: Reads XLSX/CSV files, validates and previews data, runs import/export in background threads, and updates the UI with progress.
- Key imports:
  - `openpyxl` for Excel read/write.
  - `csv` for CSV parsing.
  - `threading` and `logging` for background work and error reporting.
  - Dialogs for preview, progress, and error display.
- Public functions/classes:
  - `load_products_from_excel()`, `export_products_to_excel()`.

#### `app/ui/main_window.py`

- Purpose: Root window creation and view wiring.
- Responsibilities: Builds `LoginView` and `PosView`, applies theme, binds controller callbacks, and installs Tk callback exception logging.
- Key imports:
  - `PosController` to coordinate UI actions.
  - Views (`LoginView`, `PosView`).
- Public functions/classes:
  - `MainWindow`: Top-level UI composition.
  - `run_app()`: Starts the Tkinter main loop.

#### `app/ui/state.py`

- Purpose: Shared UI state container.
- Responsibilities: Tracks current user, cart items, default import path, and low-stock warnings.
- Key imports: `dataclasses`, `typing`.
- Public functions/classes:
  - `MainWindowState`.

#### `app/ui/view_models.py`

- Purpose: UI model for cart rows.
- Responsibilities: Provides computed line totals and stock availability.
- Key imports: `dataclasses.dataclass`.
- Public functions/classes:
  - `CartRow`.

### UI Controller: `app/ui/controllers/`

#### `app/ui/controllers/__init__.py`

- Purpose: Package marker.
- Responsibilities: Enables controller imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/ui/controllers/pos_controller.py`

- Purpose: Controller layer between UI and services.
- Responsibilities: Handles login/logout, cart actions, gated admin actions, user management (create and activate/deactivate users), import/export, automatic logout backups, restore workflows, and report dialogs.
- Key imports:
  - Dialogs for payment, admin auth, restore, and report.
  - `PosService` methods via injected service instance.
- Public functions/classes:
  - `PosController` with handlers such as `login()`, `logout()`, `checkout()`.

### UI Services: `app/ui/services/`

#### `app/ui/services/__init__.py`

- Purpose: Package marker.
- Responsibilities: Enables UI service imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/ui/services/cart_service.py`

- Purpose: In-memory cart management.
- Responsibilities: Adds/removes items, computes subtotal, returns checkout items.
- Key imports: `CartRow` from view models.
- Public functions/classes:
  - `CartService`.

### UI Views: `app/ui/views/`

#### `app/ui/views/__init__.py`

- Purpose: Package marker.
- Responsibilities: Enables view imports.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/ui/views/login_view.py`

- Purpose: Login screen UI.
- Responsibilities: Renders login form and background image; collects credentials.
- Key imports:
  - `tkinter` widgets and layout.
  - UI config constants for sizing and spacing.
- Public functions/classes:
  - `LoginView`.

#### `app/ui/views/pos_view.py`

- Purpose: Main POS screen UI.
- Responsibilities: Renders cart, keypad, action buttons, item entry fields, and available stock per cart row.
- Key imports:
  - UI config constants for layout and sizes.
  - `format_currency` for totals.
- Public functions/classes:
  - `PosView`.

### UI Dialogs: `app/ui/dialogs/`

#### `app/ui/dialogs/__init__.py`

- Purpose: Dialog export surface for simplified imports.
- Responsibilities: Re-exports dialog classes from submodules.
- Key imports: Dialog classes from local modules.
- Public functions/classes: N/A.

#### `app/ui/dialogs/admin_dialog.py`

- Purpose: Admin authorization prompt.
- Responsibilities: Collects admin PIN and returns it via `result`.
- Key imports: Tkinter and UI config constants.
- Public functions/classes:
  - `AdminAuthDialog`.

#### `app/ui/dialogs/payment_dialog.py`

- Purpose: Checkout payment dialog.
- Responsibilities: Captures payment method, discount, and received amount; validates inputs.
- Key imports: Tkinter widgets; `format_currency`; UI constants.
- Public functions/classes:
  - `PaymentDialog`.

#### `app/ui/dialogs/import_dialogs.py`

- Purpose: Import workflow dialogs.
- Responsibilities: Shows import preview, progress, and detailed error lists.
- Key imports: Tkinter widgets; `format_currency`; UI constants.
- Public functions/classes:
  - `ErrorListDialog`, `ProgressDialog`, `ImportPreviewDialog`.

#### `app/ui/dialogs/report_dialog.py`

- Purpose: Sales summary UI.
- Responsibilities: Displays totals for time windows and top SKU table.
- Key imports: Tkinter widgets; `format_currency`; UI constants.
- Public functions/classes:
  - `ReportDialog`.

#### `app/ui/dialogs/restore_dialog.py`

- Purpose: Restore backup selection UI.
- Responsibilities: Lists backup DB files and returns selected path.
- Key imports: Tkinter widgets; UI palette.
- Public functions/classes:
  - `RestoreBackupDialog`.

#### `app/ui/dialogs/manage_users_dialog.py`

- Purpose: User management UI.
- Responsibilities: Lists active users by default, adds new users, updates usernames, resets PINs, and toggles users between active and inactive lists.
- Key imports: Tkinter widgets; UI palette.
- Public functions/classes:
  - `ManageUsersDialog`.

### Data and Runtime Files: `app/data/`

#### `app/data/pos.db`

- Purpose: Primary SQLite database for users, products, sales, payments, and logs.
- Responsibilities: Persistent storage for the application.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/pos.log`

- Purpose: Runtime log file for unexpected exceptions.
- Responsibilities: Stores rotated logs produced by `main.py` and Tkinter callback logging.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/backups/pos_backup_20260115_195449_213441.db`

- Purpose: Auto-generated logout backup.
- Responsibilities: Restore source for the Restore dialog.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/backups/pos_backup_20260115_195644_343838.db`

- Purpose: Auto-generated logout backup.
- Responsibilities: Restore source for the Restore dialog.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/backups/pos_backup_20260115_195725_010123.db`

- Purpose: Auto-generated logout backup.
- Responsibilities: Restore source for the Restore dialog.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/backups/pos_backup_20260115_195847_693221.db`

- Purpose: Auto-generated logout backup.
- Responsibilities: Restore source for the Restore dialog.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/backups/pos_backup_20260115_195920_194890.db`

- Purpose: Auto-generated logout backup.
- Responsibilities: Restore source for the Restore dialog.
- Key imports: N/A.
- Public functions/classes: N/A.

#### `app/data/backups/pos_backup_20260115_201306_585016.db`

- Purpose: Auto-generated logout backup.
- Responsibilities: Restore source for the Restore dialog.
- Key imports: N/A.
- Public functions/classes: N/A.

## 4. Configuration and Constants

- UI constants are imported directly from `app/ui/config.py`. There is no runtime config loader.
- Tax calculation is controlled by `app/settings.py` via `TAX_RATE` and `TAX_ROUNDING`.
- `apply_theme()` centralizes ttk styling so UI components only reference constants and styles.
- `LOW_STOCK_THRESHOLD` affects low-stock warnings in the POS view flow.
- `.ini configuration`: There is no active `.ini` file in the project, and the code does not read one. Any future `.ini` should mirror values in `app/ui/config.py` and be parsed explicitly (no loader exists today).

## 5. UI Components

- Main window: `MainWindow` builds the root frame, applies theme, and binds keyboard shortcuts.
- Login view: `LoginView` renders username/PIN inputs and a background image; uses `place` and `grid` for layout.
- POS view: `PosView` provides SKU entry, keypad, cart table, and top action buttons; uses `pack` and `grid`.
- Dialogs:
  - `PaymentDialog` handles checkout inputs and validation.
  - `AdminAuthDialog` enforces admin access for gated actions (cashier users only).
  - `ImportPreviewDialog`, `ProgressDialog`, and `ErrorListDialog` support the import workflow.
  - `ReportDialog` summarizes sales totals and top SKUs.
  - `RestoreBackupDialog` lists backup files for restore.
  - `ManageUsersDialog` allows admins to add users, update usernames, reset PINs, and activate/deactivate cashier accounts with an inactive list view.

## 6. Data Flow and Application Logic

- Login flow:
  - `LoginView` submits credentials to `PosController.login()`.
  - `PosService.login()` delegates to `UserRepository.authenticate()`.
- Adding items:
  - POS view submits SKU and quantity to `PosController.add_item_from_entry()`.
  - The service looks up SKU/barcode, cart service tracks quantity, and UI updates the cart list.
- Checkout:
  - `PaymentDialog` returns payment details.
  - `PosService.checkout()` validates stock, writes sales and payment records, updates inventory, logs audit, and exports sales XLSX.
- Import:
  - User triggers import; file dialog selects XLSX/CSV.
  - `ImportPreviewDialog` shows validated rows, counts, and error summaries; import runs in a worker thread with progress updates.
  - `import_products()` updates quantities or inserts new products inside a single transaction.
- Export:
  - `export_products_to_excel()` writes catalog to `dbProducts.xlsx` in a background thread.
- Backup and restore:
  - On logout, the controller copies `pos.db` to `app/data/backups/` with a timestamped filename.
  - Restore lists existing backups, creates a pre-restore safety copy, overwrites `pos.db`, and closes the app to ensure clean re-open.
- Audit logging:
  - Admin actions and sales write to `audit_logs` with UTC+8 timestamps.
- Reporting:
  - Sales summary aggregates totals for today, last 7 days, and last 30 days; top SKUs are queried from sales data.
- User management:
  - Admins can add users, update usernames, reset PINs, deactivate cashier users (archived from the active list), and reactivate users from the inactive list.

## 7. Error Handling and Validation

- UI validation:
  - SKU required, quantity must be a positive integer.
  - Payment dialog validates discount and received amount, and enforces max change for cash.
- Service validation:
  - Checkout rejects empty carts and insufficient stock.
  - Import validation rejects missing SKU, invalid quantity, or invalid price.
- Error handling strategy:
  - Exceptions are caught and displayed via `messagebox` with user-friendly messages.
  - Import workflow collects per-row errors and presents them in a dedicated error dialog.
  - Unhandled exceptions are logged to `app/data/pos.log` (including Tkinter callback failures).

## 8. Development and Maintenance Notes

- Keep the UI -> controller -> service -> repository separation when extending features.
- Avoid accessing the database directly from views; use `PosService` and repositories.
- Backup and restore close or replace the database; ensure connection state is consistent.
- `openpyxl` is required for XLSX import/export; the app already guards missing dependencies with user-facing errors.
- Use `tests/test_smoke.py` for quick regression checks on import/export/restore flows.
- Review `app/data/pos.log` when troubleshooting unexpected exceptions.
- Generated artifacts (`app/data/backups`, `sales.xlsx`, `dbProducts.xlsx`) should not be treated as source of truth in version control.
- `__pycache__` and `.pyc` files are generated by Python and can be ignored or cleaned when packaging.

## 9. Quick Start

- Prerequisites:
  - Python 3.11+ (tested with modern CPython).
  - `openpyxl` is required only for XLSX import/export.
- Run locally:
  - From the project root: `python main.py`.
  - The app will initialize the SQLite database and open the login screen.
- Logs:
  - Runtime errors are written to `app/data/pos.log`.
- First login:
  - Use the seeded accounts in `app/db.py` (e.g., `admin` for admin access).
  - Import products via the **Import** button as needed.

## 10. Developer Onboarding

- Entry points:
  - Start with `main.py` to see application bootstrapping.
  - Follow into `app/ui/main_window.py` to understand view wiring.
  - Review `app/ui/controllers/pos_controller.py` to see user flows and handlers.
- Data model and persistence:
  - Schema and seed data live in `app/db.py`.
  - Table access is isolated to `app/repositories/`.
  - Business logic and transactions live in `app/services/pos_service.py`.
- UI structure:
  - Views are in `app/ui/views/` and dialogs in `app/ui/dialogs/`.
  - Layout and styling are controlled by constants in `app/ui/config.py`.
- Common tasks:
  - Adding a screen: create a view, wire it in `MainWindow`, and route events through `PosController`.
  - Adding data access: create a repository method and call it from `PosService`.
  - Adding UI constants: define in `app/ui/config.py` and reuse consistently.
  - Running smoke tests: `python -m unittest tests.test_smoke`.
- Operational artifacts:
  - SQLite DB: `app/data/pos.db`.
  - Backups: `app/data/backups/` (created on logout).
  - Exports: `sales.xlsx`, `dbProducts.xlsx`.
  - Logs: `app/data/pos.log`.
- Pitfalls:
  - Do not write directly to the DB from views or dialogs.
  - Ensure the DB connection is valid after restore operations.
  - Keep imports localized in dialogs to avoid circular dependencies.
