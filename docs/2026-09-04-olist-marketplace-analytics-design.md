# Olist Marketplace Analytics Design

## Goal

Create a reproducible analyst portfolio engagement answering marketplace GMV, fulfillment,
freight, satisfaction, and repeat-purchase questions using the public Olist dataset.

## Architecture

Raw CSV files remain ignored. Python acquisition and validation profile the inputs. DuckDB
loads normalized tables and executes substantive SQL over a star-style model. Python adds
statistical comparisons and figures. Aggregated, portfolio-safe outputs feed a static
recruiter dashboard and Power BI-ready semantic assets.

## Integrity rules

- Merchandise value is GMV, not recognized marketplace revenue.
- Fact grain is explicit before any aggregate is calculated.
- Payment and item facts are never joined without pre-aggregation.
- Findings use computed data only, with limitations disclosed.
- Raw source data and credentials never enter Git.

## Verification

Small deterministic fixtures test KPI calculations, joins, timestamps, late flags,
reconciliation, and RFM logic. Full-data validation runs locally after acquisition.

