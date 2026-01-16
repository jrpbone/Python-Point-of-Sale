from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

from app.ui.view_models import CartRow


@dataclass
class MainWindowState:
    default_excel_path: Path
    colors: Dict[str, str]
    current_user: Optional[object] = None
    db_mtime: Optional[float] = None
    cart: Dict[int, CartRow] = field(default_factory=dict)
    products_loaded: bool = False
    low_stock_notified: set[int] = field(default_factory=set)

    def reset_session(self):
        self.current_user = None
        self.db_mtime = None
        self.cart.clear()
        self.low_stock_notified.clear()
