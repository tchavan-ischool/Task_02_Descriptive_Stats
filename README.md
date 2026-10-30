# Task 02 — Descriptive Statistics (Milestone A)

## Research objective
Analyze the **2024 Facebook Political Ads** dataset using three independent approaches: the Python standard library, Pandas, and Polars. Compare dataset-level descriptive statistics and grouped analysis by `page_id` and by `page_id` + `ad_id`.

## Dataset
**Source:** Professor Strome's course Google Drive collection, **2024 Facebook Political Ads**, specifically the Task 2 / Milestone A dataset. **Insert the verified course dataset sharing URL here before submission.** The correct file is named `2024_fb_ads_president_scored_anon.csv` (41 columns). **Do not substitute the Task 1 dataset** `fb_ads_president_scored_anon.csv` (40 columns).

The raw CSV is intentionally excluded from this repository. Download it from the course-provided source and place it at `data/2024_fb_ads_president_scored_anon.csv`.

## Setup and execution
Python 3.10+ recommended. On Windows PowerShell or macOS/Linux:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
mkdir data
mkdir outputs
```

Place the downloaded CSV in `data/` and run from the repository root:

```bash
python pure_python_stats.py data/2024_fb_ads_president_scored_anon.csv
python pandas_stats.py data/2024_fb_ads_president_scored_anon.csv
python polars_stats.py data/2024_fb_ads_president_scored_anon.csv
python verify_results.py
```

The three scripts write JSON results under `outputs/` (excluded from Git), including column summaries and the top 10 groups ranked by summed nominal estimated spend. The checker compares dataset dimensions, key numerical statistics, missing-value counts, and group counts; it does *not* prove full equivalence of every categorical frequency or grouped total. Inspect those details as well before submission.

## First findings from the correct Task 2 CSV
- 246,745 records and 41 columns.
- 4,475 distinct `page_id` groups, and 246,745 distinct (`page_id`, `ad_id`) combinations.
- `estimated_spend` has median 49 and mean 1,061.29 in its **source currency units**. This is a right-skewed distribution; these are not all unconditionally USD.
- 246,599 records have currency `USD`; others have different currency codes. Any combined monetary totals **must be separated by currency or converted appropriately** before being interpreted as one monetary total.
- `bylines` is missing for 1,009 records.

See [FINDINGS.md](FINDINGS.md) for interpretation and [REFLECTION.md](REFLECTION.md) for method comparison and limitations.

## Technical methodology
- Numeric: `estimated_audience_size`, `estimated_impressions`, and `estimated_spend` are parsed as numbers. Binary score indicators are retained as categorical flags in this version of the analysis; this decision should be documented rather than silently treating binary categories as continuous variables.
- The scripts calculate count, mean, min/max, **sample** standard deviation (`ddof=1`), and median for numeric columns; categorical count, number of unique values, mode, and top five values for other columns.
- Missing strings (`NA`, `N/A`, `none`, `null`, empty, etc.) are normalized. Structured fields (e.g. serialized lists/dictionaries) are analyzed as raw categorical strings; do not interpret those frequencies as parsed demographic or geographic statistics.
- Grouped analysis counts ad records and sums nominal `estimated_spend`. The grouped reporting is **not currency-normalized**. Do not interpret totals as USD when multiple currencies are present. `page_id` and `ad_id` are identifiers, not quantities.

## Validation status
All three implementations—Pure Python, Pandas, and Polars—were executed successfully on the complete Task 2 dataset. The validation script confirmed matching dataset dimensions, numeric statistics, missing-value counts, and grouped record counts. See VALIDATION.md for details.

## Repository files
- `pure_python_stats.py`: standard-library baseline
- `pandas_stats.py`: chunked Pandas analysis
- `polars_stats.py`: Polars lazy-expression analysis
- `verify_results.py`: cross-implementation checks
- `FINDINGS.md`: narrative findings
- `REFLECTION.md`: comparative analysis and research questions
- `VALIDATION.md`: execution and validation status
- `requirements.txt`, `.gitignore`

## AI-assistance disclosure
AI was used to prepare script scaffolding and documentation. The researcher must independently inspect and test the scripts, confirm the dataset source, complete the Polars run, and revise the reflection to accurately describe their own observations.
