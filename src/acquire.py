from __future__ import annotations

import json
import shutil
from pathlib import Path

from .common import ensure_directories
from .config import RAW, REPORTS

DATASET = "olistbr/brazilian-ecommerce"
EXPECTED = {
    "olist_customers_dataset.csv", "olist_geolocation_dataset.csv", "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv", "olist_order_reviews_dataset.csv", "olist_orders_dataset.csv",
    "olist_products_dataset.csv", "olist_sellers_dataset.csv", "product_category_name_translation.csv",
}


def acquire() -> dict[str, object]:
    ensure_directories()
    REPORTS.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"dataset": DATASET, "status": "blocked", "files": []}
    try:
        import kagglehub
        source = Path(kagglehub.dataset_download(DATASET))
        candidates = list(source.rglob("*.csv"))
        for path in candidates:
            if path.name in EXPECTED:
                shutil.copy2(path, RAW / path.name)
        files = sorted(p.name for p in RAW.glob("*.csv"))
        report.update({"status": "acquired" if EXPECTED.issubset(files) else "partial", "files": files})
    except (ImportError, OSError, RuntimeError) as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    (REPORTS / "acquisition.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    acquire()
