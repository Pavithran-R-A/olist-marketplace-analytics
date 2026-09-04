import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path(os.environ.get("OLIST_DATA_DIR", ROOT / "data" / "raw"))
PROCESSED = Path(os.environ.get("OLIST_PROCESSED_DIR", ROOT / "data" / "processed"))
PUBLISHED = Path(os.environ.get("OLIST_PUBLISHED_DIR", ROOT / "data" / "published"))
REPORTS = ROOT / "reports"
DB_PATH = Path(os.environ.get("OLIST_DB_PATH", PROCESSED / "olist.duckdb"))
