# Hiring-readiness compliance audit

Audit basis: repository artifacts, Power BI Desktop validation, generated analytical outputs, and GitHub Actions evidence on 2026-09-04.

This file is the **current** readiness audit. The earlier pre-repair PARTIAL/MISSING checklist has been retired so recruiters do not encounter stale project status.

| Requirement | Current evidence | Status |
|---|---|---|
| Real Olist acquisition | `src/acquire.py`, `reports/acquisition.json`, source profiling | PASS |
| Explicit analytical grain | `data/published/fact_orders.csv`, model tests, metric documentation | PASS |
| SQL depth | `sql/00_schema.sql` through `sql/07_advanced_analytics.sql` | PASS |
| Reusable KPI layer | `data/published/kpis.json`, monthly/category/state/status KPI outputs | PASS |
| Cohorts and retention | `data/published/customer_cohorts.csv`, advanced SQL/tests | PASS |
| Data-driven RFM | `data/published/rfm_segments.csv`, advanced analytics/tests | PASS |
| Seller analysis | `data/published/seller_kpis.csv` and SQL analysis | PASS |
| Freight analysis | `data/published/freight_state.csv`, KPI outputs | PASS |
| Fulfillment analysis | state/category/status outputs and report page | PASS |
| Pareto concentration | `data/published/category_pareto.csv` and advanced analytics | PASS |
| Data-quality gate | validation pipeline, `docs/data_quality_report.md`, quality tests | PASS |
| Metric reconciliation | pytest coverage across metrics/model/advanced analysis | PASS |
| End-to-end fixture CI | transform → validate → analyse → dashboard → pytest workflow | PASS |
| Dependency integrity | `python -m pip check` in CI | PASS |
| Statistical analysis | SciPy-backed customer-experience analysis and documented findings | PASS |
| Recruiter dashboard | `dashboard/index.html`, GitHub Pages deployment | PASS |
| Power BI semantic model | Desktop-validated PBIP/PBIR/TMDL project | PASS |
| DAX measures | Explicit measures loaded and validated in Power BI Desktop | PASS |
| Power BI report | Three rendered pages with committed screenshots | PASS |
| PBIP reopen validation | Saved project reopened in Desktop with zero Problems | PASS |
| README accuracy | Metrics, GMV terminology, validation boundary, and links reconciled | PASS |
| Data licensing | Complete MIT code license plus `DATA_LICENSE.md` attribution boundary | PASS |
| Resume claims | Claims constrained to verified repository/Power BI evidence | PASS |

## Verified headline reconciliation

| KPI | Value |
|---|---:|
| GMV | R$13,591,643.70 |
| Orders | 99,441 |
| Customers | 96,096 |
| AOV | R$136.68 |
| Late-delivery rate | 8.11% |
| Repeat-customer rate | 3.04% |

No headline discrepancies were recorded between the final Python/SQL outputs and the Power BI report.

## Power BI boundary

Power BI Desktop is a Windows desktop dependency and is not executed inside the Linux GitHub Actions job. It was therefore verified separately in Power BI Desktop 2.157.1354.0: the TMDL semantic model loaded, measures validated, the PBIP saved, and the project reopened with zero Problems. The PBIP/PBIR/TMDL source and three report screenshots are committed for inspection.

## Automated verification boundary

GitHub Actions validates the reproducible fixture path on every push and pull request: dependency integrity, Ruff, transformation, validation, analysis, dashboard-data generation, dashboard generation, and pytest. The dashboard deployment is maintained separately through GitHub Pages.

## Completion assessment

**Portfolio-project scope: COMPLETE.**

There are no known analytical, Power BI, test, CI, dashboard, reconciliation, documentation, or licensing blockers in the committed deliverable. Future changes should be treated as enhancements rather than completion requirements.
