# Data quality report

## Observed issues and treatment

| Observed issue | Business effect | Treatment | Rationale |
|---|---|---|---|
| Geolocation contains 261,831 duplicate rows | Naive geographic joins can multiply facts | Excluded from core model | Customer and seller state provide stable portfolio geography. |
| Reviews contain missing comment fields | Text completeness is limited | Keep review score; ignore comment text | Scores remain usable for satisfaction analysis. |
| Orders contain missing delivery timestamps | Delivery KPI denominator can be biased | Require both delivery dates | Avoid invented delivery duration or lateness. |
| Products contain missing attributes | Category and logistics detail can be incomplete | Category fallback to `Unknown` | Preserve merchandise totals while exposing missingness. |
| Item and payment tables have different grains | Joins can inflate GMV | Pre-aggregate items at order grain | Reconciliation protects KPI correctness. |

Full source counts are in `reports/source_profile.csv`. Validation checks include duplicate
rows, nulls, timestamp ordering, negative monetary values, and source-file presence.

