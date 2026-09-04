# Olist Marketplace Analytics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a reproducible Olist analytics portfolio for marketplace leadership decisions.

**Architecture:** Ignored raw CSVs feed DuckDB tables. Order facts pre-aggregate item values
before joins. SQL generates analytical outputs, Python adds statistics and dashboard exports,
and static HTML plus Power BI-ready assets communicate the results.

**Tech Stack:** Python 3.13, pandas, DuckDB, SQL, SciPy, Plotly, pytest, Ruff, DAX, GitHub Actions.

**Spec:** `docs/2026-09-04-olist-marketplace-analytics-design.md`

## Global Constraints

- GMV is merchandise value, not recognized marketplace revenue.
- Raw data remains ignored and credentials remain outside Git.
- Findings use computed values only.
- Power BI Desktop validation is reported only if available.

### Task 1: Foundation and acquisition

**Files:** `pyproject.toml`, `.gitignore`, `src/acquire.py`, `reports/acquisition.json`

- [x] Initialize Git and create package structure.
- [x] Install reproducible runtime and development dependencies.
- [x] Download and verify all nine Olist source files.

### Task 2: Quality and model

**Files:** `src/validate.py`, `src/transform.py`, `sql/`, `docs/data_quality_report.md`

- [x] Profile rows, columns, duplicates, and missing values.
- [x] Implement timestamp, monetary, key, and review checks.
- [x] Build order and item facts with explicit grain.
- [x] Reconcile model orders and GMV against source totals.

### Task 3: Analysis and communication

**Files:** `src/analyse.py`, `src/build_dashboard_data.py`, `src/dashboard.py`, `reports/`

- [x] Calculate monthly, category, regional, fulfillment, review, and customer outputs.
- [x] Compare late and on-time reviews statistically.
- [x] Build a recruiter-viewable static dashboard.

### Task 4: Portfolio assets and verification

**Files:** `docs/`, `powerbi/`, `tests/`, `.github/workflows/ci.yml`

- [x] Add metric, methodology, requirements, insights, resume, and interview documentation.
- [x] Add DAX measures, TMDL model specification, and build instructions.
- [x] Run unit, integration, lint, and full-data pipeline checks.

