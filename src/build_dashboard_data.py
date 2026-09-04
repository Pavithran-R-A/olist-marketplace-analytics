from __future__ import annotations

import json
import shutil

from .config import PUBLISHED, REPORTS


def build() -> None:
    PUBLISHED.mkdir(parents=True, exist_ok=True)
    for path in list(PUBLISHED.glob("*.csv")) + list(PUBLISHED.glob("*.json")):
        path.unlink()
    for path in REPORTS.glob("*.csv"):
        shutil.copy2(path, PUBLISHED / path.name)
    kpis = json.loads((REPORTS / "kpis.json").read_text(encoding="utf-8"))
    (PUBLISHED / "kpis.json").write_text(json.dumps(kpis, indent=2), encoding="utf-8")
    print(f"Published {len(list(PUBLISHED.glob('*')))} dashboard-safe files")


if __name__ == "__main__":
    build()
