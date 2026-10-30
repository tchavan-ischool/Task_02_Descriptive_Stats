# Validation status

Test dataset: `2024_fb_ads_president_scored_anon.csv`, the 41-column Task 2 file.

## Completed in the authoring environment
- Pure Python script: **ran successfully** over all 246,745 records.
- Pandas script: **ran successfully** over all 246,745 records.
- Both report 41 columns, 4,475 page groups and 246,745 page/ad groups.
- The three selected numeric columns matched for count, mean, min, max, sample standard deviation and median.
- Missing-value counts matched, accounting for zero-valued keys omitted from one implementation's counter.
- `python verify_results.py`: **PASS** for pure Python and Pandas.

## Not yet completed
- The Polars package could not be installed in the authoring environment, so `polars_stats.py` **has not been executed or validated**. Install the dependencies locally and run the third script; then run the validator again and correct any differences before claiming complete three-way equivalence.
- The validator compares key metrics, not every top-five frequency, sorted top-group listing, or full group monetary sum. Manually spot-check those before submitting.
- A direct course-provided Google Drive dataset URL has not yet been verified and must be inserted in the README.

## Known analytical limitations
- Grouped monetary totals are *nominal sums across source currencies*, not a properly currency-normalized spending analysis.
- Numeric flags and text-encoded list/dictionary columns are summarized as categories, not expanded into semantic subfields.
