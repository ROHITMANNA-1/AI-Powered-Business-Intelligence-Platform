# Interview Questions and Answers

## Why is this not a prediction project?
It focuses on descriptive and diagnostic analytics: what happened, where it happened, how metrics changed, and which dimensions are associated with differences. No future outcome is predicted.

## How is SQL safety handled?
Generated SQL must be a single SELECT/WITH statement, may reference only the analysis table, and is rejected if it contains mutation or administrative keywords. Production access should use a read-only database user.

## How are AI answers grounded?
Python or SQL computes the result first. The explanation receives the measured result and states when the data is insufficient. It does not invent profit or causal explanations that are absent from the dataset.

## How would you evaluate generated SQL?
Run generated SQL against a fixture, compare selected totals and grouped results with independently calculated Pandas values, and reject unsafe or semantically unsupported queries.

## What would you improve for production?
Add schema-aware structured LLM output, query timeout and row limits, authentication, audit logs, richer data contracts, a semantic metric layer, and Power BI refresh governance.
