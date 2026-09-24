"""Dataset profiling and data-quality checks."""

from __future__ import annotations

from typing import Any

import pandas as pd


def profile_dataframe(dataframe: pd.DataFrame) -> dict[str, Any]:
    """Return JSON-friendly structural, missingness, and summary metadata."""
    missing = dataframe.isna().sum()
    numeric = dataframe.select_dtypes(include="number")
    summary = numeric.describe().transpose().reset_index(names="column")
    return {
        "rows": int(len(dataframe)),
        "columns": int(len(dataframe.columns)),
        "column_names": list(map(str, dataframe.columns)),
        "dtypes": {str(column): str(dtype) for column, dtype in dataframe.dtypes.items()},
        "missing_values": {str(column): int(value) for column, value in missing.items() if value},
        "duplicate_rows": int(dataframe.duplicated().sum()),
        "numeric_summary": summary,
        "quality_issues": quality_issues(dataframe),
    }


def quality_issues(dataframe: pd.DataFrame) -> list[str]:
    """Identify issues worth reviewing without deciding business policy."""
    issues: list[str] = []
    for column, count in dataframe.isna().sum().items():
        if count:
            issues.append(f"{column}: {int(count):,} missing values")
    duplicates = int(dataframe.duplicated().sum())
    if duplicates:
        issues.append(f"{duplicates:,} duplicate rows")
    if "quantity" in dataframe:
        count = int((pd.to_numeric(dataframe["quantity"], errors="coerce") <= 0).sum())
        if count:
            issues.append(f"quantity: {count:,} non-positive values")
    if "unit_price" in dataframe:
        count = int((pd.to_numeric(dataframe["unit_price"], errors="coerce") <= 0).sum())
        if count:
            issues.append(f"unit_price: {count:,} non-positive values")
    return issues
