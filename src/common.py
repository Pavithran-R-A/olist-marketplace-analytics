from pathlib import Path

import duckdb

from .config import DB_PATH, PROCESSED, PUBLISHED, RAW


def ensure_directories() -> None:
    for path in (RAW, PROCESSED, PUBLISHED):
        path.mkdir(parents=True, exist_ok=True)


def connection() -> duckdb.DuckDBPyConnection:
    ensure_directories()
    return duckdb.connect(str(DB_PATH))


def csv_files() -> list[Path]:
    return sorted(RAW.glob("*.csv"))

