# Task 2 — Findings and interpretation

## Overview
I examined the Task 2 Facebook political advertising CSV, which includes 246,745 ad records across 41 columns. The dataset contains identifiers, creation timestamps, bylines, estimated audience size, estimated impressions, estimated spend, publication platforms, and a collection of content classification fields. This is the **Task 2 dataset**, not the separate CSV used for Task 1.

## Distribution of estimated spend
The recorded `estimated_spend` field has a median of 49 and a mean of approximately 1,061.29 in the source currency units, with a maximum of 474,999 and a sample standard deviation of approximately 4,992.56. The mean is substantially higher than the median, suggesting a right-skewed distribution: many records report low estimated spend, while a smaller group has substantially higher values. An average without the median would therefore be a misleading description of the typical record.

**Currency warning:** Although 246,599 records use `USD`, the dataset also contains other currencies. The `estimated_spend` statistics above summarize the raw numeric field without conversion and are therefore primarily exploratory, **not a validated single-currency spending estimate**. A more defensible financial comparison would filter to `currency == 'USD'` or normalize other currencies using a documented conversion methodology.

## Grouping reveals concentration and data structure
Grouping by `page_id` yielded 4,475 groups. Grouping by both `page_id` and `ad_id` yielded 246,745 combinations, the same as the record count. In this particular dataset, the pair uniquely identifies each ad record. Grouped analysis therefore reveals a more informative distribution of activity by page than by the unique page/ad combination. This is a structural finding about the data, not a judgment about the organizations or people represented.

The five largest nominal group totals and their counts are visible in the generated `outputs/pure_python_results.json` after running the script. Note that reported group totals aggregate **nominal** amounts without currency conversion; they must not be compared as dollar totals across currencies.

## Missingness and data preparation
The `bylines` field was missing on 1,009 records. This matters because analyses by paying entity or organization can undercount unattributed records or bias rankings if missing values are discarded without explanation. The scripts report missing values and preserve all rows for overall record counts. Date fields and serialized structures are treated as strings, with a separate normalization step needed for any time-series, geographic, or demographic analysis.

Several data fields contain list-like or dictionary-like text. Their raw string frequencies can be counted, but interpreting them as individual mentions or regions would require parsing into structured values. That should be distinguished from what this milestone's basic descriptive scripts actually compute.

## Conclusions
The clearest defensible takeaway is methodological: medians, distributions, missingness, and grouping provide a more nuanced understanding than a single overall average. Grouping demonstrates the value of choosing meaningful keys, while the mixed-currency and structured-text issues show why type detection and data cleaning decisions must be made explicitly. These observations form the foundation for Task 3's more generalized cross-dataset system.
