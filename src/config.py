from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
PUBLISHED = ROOT / "data" / "published"
REPORTS = ROOT / "reports"
DB_PATH = PROCESSED / "olist.duckdb"

