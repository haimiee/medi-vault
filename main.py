from nicegui import app
from db.lib import init_db
from ui.ui import run_ui

if __name__ in {"__main__", "__mp_main__"}:
    app.on_startup(init_db)  # Initialize DB
    run_ui()