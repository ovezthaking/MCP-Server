import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "app.db"

db_path_raw = os.getenv("DB_PATH")
db_path = Path(db_path_raw).expanduser() if db_path_raw else DEFAULT_DB_PATH

if not db_path.is_absolute():
    db_path = (PROJECT_ROOT / db_path).resolve()

db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{db_path.as_posix()}", future=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)
