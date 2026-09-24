# Evaluation and Limitations

## Current automated checks

- Cleaning removes duplicates and cancellations and derives revenue.
- Profiling reports shape, types, missingness, duplicates, and non-positive values.
- KPI tests compare results with independently known fixture values.
- SQL tests block mutation, multiple statements, and unauthorized tables.
- AI question tests verify result values come from the dataframe and reject unavailable measures.
- Report tests verify Markdown sections and PDF output.

Run `pytest -q` from the repository root.

## Known limitations

- The starter source has no profit, cost, category, shipping, or delivery fields.
- The current offline analyst supports a conservative set of question patterns; unrecognized questions receive a safe aggregate or a clear unsupported-data error.
- Optional LLM integration is not enabled by default and should use structured output, a read-only database user, query timeouts, and result-size limits before production deployment.
- Currency is treated as the source's sterling unit; no currency conversion is performed.
- Retention is not calculated unless order dates and customer identifiers support a defined cohort method.
- Power BI is documented as a separate consumer of cleaned data/MySQL; Streamlit does not automate Power BI refresh or embedding.
