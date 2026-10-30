# Validation status

Test dataset: `2024_fb_ads_president_scored_anon.csv`, the 41-column Task 2 file.

# Task 2 — Validation Results

## Completed Validation

All three analytical implementations—Pure Python, Pandas, and Polars—were executed locally using the Task 2 Facebook Political Ads dataset.

The dataset contained 246,745 records and 41 columns, with 4,475 `page_id` groups and 246,745 `page_id` + `ad_id` groups.

The validation script returned:

`PASS for pure_python, pandas, polars : dataset dimensions, numeric statistics, missing counts and group counts match.`

This confirms consistency across all three implementations for the metrics tested.

## Validation Limitations

The validation script checks dataset dimensions, selected numerical statistics, missing-value counts, and grouped record counts. It does not exhaustively validate every categorical frequency or grouped monetary total.

Grouped spending totals also require caution because the dataset includes multiple currencies without conversion.
## Final Validation Results

All three analytical implementations—Pure Python, Pandas, and Polars—were successfully executed on the 2024 Facebook Political Ads dataset.

The validation script produced the following result:

`PASS for pure_python, pandas, polars : dataset dimensions, numeric statistics, missing counts and group counts match.`

This confirms agreement across the three implementations for:

- Dataset dimensions (246,745 rows and 41 columns)
- Numeric descriptive statistics
- Missing-value counts
- Grouped record counts using `page_id` and `page_id` + `ad_id`

The successful comparison demonstrates consistency across the three approaches for the metrics tested.

**Limitation:** This validation does not independently establish agreement for every categorical frequency or every possible grouped numerical aggregation.
