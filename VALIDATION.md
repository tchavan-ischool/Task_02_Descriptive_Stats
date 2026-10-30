# Validation status

Test dataset: `2024_fb_ads_president_scored_anon.csv`, the 41-column Task 2 file.

## Completed in the authoring environment
- Pure Python script: **ran successfully** over all 246,745 records.
- Pandas script: **ran successfully** over all 246,745 records.
- Both report 41 columns, 4,475 page groups and 246,745 page/ad groups.
- The three selected numeric columns matched for count, mean, min, max, sample standard deviation and median.
- Missing-value counts matched, accounting for zero-valued keys omitted from one implementation's counter.
- `python verify_results.py`: **PASS** for pure Python and Pandas.

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
