# Task 2 — Comparative reflection (review and personalize)

## Pure Python vs. Pandas vs. Polars
One important outcome of this task was successfully reproducing the same descriptive statistics using three different analytical approaches: Pure Python, Pandas, and Polars. Although each approach uses different programming techniques and data structures, the validation results confirmed agreement across the key metrics tested. Pure Python provided a better understanding of the underlying calculations, while Pandas and Polars demonstrated how DataFrame libraries simplify data manipulation and grouped analysis. This exercise strengthened my understanding of statistical consistency, data validation, and the importance of verifying results across different implementations.

## Why can three approaches disagree?
Differences can arise from missing-value rules, inferred types, standard-deviation conventions (`ddof=1` vs `ddof=0`), string normalization, numeric parsing, and whether a group retains missing keys. In this project, we standardized the main numeric fields and use sample standard deviation. The validation script checks shared metrics, but further manual review of grouped sums, categorical frequencies, and edge cases is still valuable.

## Structured fields and data quality
Some columns contain representations of lists or dictionaries, which basic CSV loading treats as strings. Raw string grouping is not the same as parsing and analyzing each nested item. The identifiers must remain strings; otherwise a generic type inference routine might incorrectly treat numeric-looking IDs as numeric measures. The mixed-currency field is another reason to distinguish technical aggregation from a meaningful economic claim.

## Recommendation to a junior analyst
I would introduce pure Python first to understand counting, numerical summaries, missing-value treatment, and grouping mechanics, then Pandas for efficient everyday analysis, and finally Polars for expression-based data workflows and additional performance-oriented techniques. That is a learning progression rather than a measured performance ranking.

## Further personal notes to add before submission
- What problems did **you** encounter while executing the Polars script?
- Did you measure execution times on the same computer, or are your performance comments based on ease of coding?
- Which differences were most surprising when you examined the raw data and the group-level outputs?
