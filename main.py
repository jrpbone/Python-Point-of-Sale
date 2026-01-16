import logging
import sys
import threading
from logging.handlers import RotatingFileHandler

from app.db import DB_PATH, init_db, get_connection, seed_data
from app.services.pos_service import PosService
from app.ui.main_window import run_app


def _configure_logging():
    log_dir = DB_PATH.parent
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "pos.log"
    handler = RotatingFileHandler(
        log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(handler)

    def _handle_exception(exc_type, exc, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            return
        logging.exception("Unhandled exception", exc_info=(exc_type, exc, tb))
        sys.__excepthook__(exc_type, exc, tb)

    def _handle_thread_exception(args):
        logging.exception(
            "Unhandled thread exception",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    sys.excepthook = _handle_exception
    threading.excepthook = _handle_thread_exception


def main():
    _configure_logging()
    init_db()
    seed_data()
    conn = get_connection()
    try:
        service = PosService(conn)
        run_app(service)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
