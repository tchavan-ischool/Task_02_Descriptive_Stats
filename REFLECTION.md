# Task 2 — Comparative reflection (review and personalize)

## Pure Python vs. Pandas vs. Polars
Pure Python made each part of the analysis explicit: reading the CSV, classifying fields, tracking missing values, maintaining frequency dictionaries, and implementing grouped counters. The approach is educational because it exposes assumptions that dataframe APIs can conceal, but it requires more manual code and careful treatment of edge cases.

Pandas shortened the grouping and frequency logic with `groupby`, `value_counts`, and numeric aggregation operations. In the supplied implementation, chunking helps limit memory requirements for the large CSV, but requires counters to be combined carefully across chunks. The complete dataset's key numeric results and group counts were verified against the pure Python results.

Polars expresses transformations through typed expressions and lazy scans, which may help manage larger files. **Its implementation is included but not yet tested in the supplied environment.** After installing Polars locally, run the script and record any fixes, actual runtime, and observed differences. Do not present an unrun script as validated.

## Why can three approaches disagree?
Differences can arise from missing-value rules, inferred types, standard-deviation conventions (`ddof=1` vs `ddof=0`), string normalization, numeric parsing, and whether a group retains missing keys. In this project, we standardized the main numeric fields and use sample standard deviation. The validation script checks shared metrics, but further manual review of grouped sums, categorical frequencies, and edge cases is still valuable.

## Structured fields and data quality
Some columns contain representations of lists or dictionaries, which basic CSV loading treats as strings. Raw string grouping is not the same as parsing and analyzing each nested item. The identifiers must remain strings; otherwise a generic type inference routine might incorrectly treat numeric-looking IDs as numeric measures. The mixed-currency field is another reason to distinguish technical aggregation from a meaningful economic claim.

## Recommendation to a junior analyst
I would introduce pure Python first to understand counting, numerical summaries, missing-value treatment, and grouping mechanics, then Pandas for efficient everyday analysis, and finally Polars for expression-based data workflows and additional performance-oriented techniques. That is a learning progression rather than a measured performance ranking.

## AI-assisted starter code
AI assistance was used to draft these scripts and supporting documents. The most useful aspect was rapidly producing a structured starting point. The risk is that generated code can contain subtle logic, API, or statistical assumptions; it must therefore be run, validated, and checked against the assignment rather than accepted simply because it appears plausible.

## Further personal notes to add before submission
- What problems did **you** encounter while executing the Polars script?
- Did you measure execution times on the same computer, or are your performance comments based on ease of coding?
- Which differences were most surprising when you examined the raw data and the group-level outputs?
