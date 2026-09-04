# Data quality report

## Observed issues and treatment

| Observed issue | Business effect | Treatment | Rationale |
|---|---|---|---|
| Geolocation contains 261,831 duplicate rows | Naive geographic joins can multiply facts | Excluded from core model | Customer and seller state provide stable portfolio geography. |
| Reviews contain missing comment fields | Text completeness is limited | Keep review score; ignore comment text | Scores remain usable for satisfaction analysis. |
| Orders contain missing delivery timestamps | Delivery KPI denominator can be biased | Require both delivery dates | Avoid invented delivery duration or lateness. |
| Products contain missing attributes | Category and logistics detail can be incomplete | Category fallback to `Unknown` | Preserve merchandise totals while exposing missingness. |
| Item and payment tables have different grains | Joins can inflate GMV | Pre-aggregate items at order grain | Reconciliation protects KPI correctness. |

The executable gate writes `reports/quality_gate.json`. It records rule name, severity,
observed value, expected condition, status, and business implication. Current execution
contains 18 checks: 17 pass and one warning for delivered orders missing timestamps. No
critical failures occurred. Full source counts are
in `reports/source_profile.csv`. Critical failures raise an exception and stop the pipeline.
