"""Transparent, reproducible data cleaning operations."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .schema import canonicalize_dataframe


@dataclass
class CleaningReport:
    rows_before: int
    rows_after: int
    duplicate_rows_removed: int = 0
    cancelled_rows_removed: int = 0
    missing_values_filled: int = 0
    parsed_date_columns: list[str] = field(default_factory=list)
    derived_columns: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def clean_dataframe(
    dataframe: pd.DataFrame,
    *,
    remove_duplicates: bool = True,
    remove_cancelled: bool = True,
    fill_numeric_missing: bool = False,
) -> tuple[pd.DataFrame, CleaningReport]:
    """Clean common retail issues without silently changing business meaning."""
    result, _ = canonicalize_dataframe(dataframe)
    report = CleaningReport(rows_before=len(result), rows_after=len(result))

    if remove_duplicates:
        before = len(result)
        result = result.drop_duplicates().copy()
        report.duplicate_rows_removed = before - len(result)

    invoice_column = "invoice_no" if "invoice_no" in result else None
    if remove_cancelled and invoice_column:
        cancelled = result[invoice_column].astype(str).str.upper().str.startswith("C")
        report.cancelled_rows_removed = int(cancelled.sum())
        result = result.loc[~cancelled].copy()

    for column in result.columns:
        if "date" in column or column == "timestamp":
            parsed = pd.to_datetime(result[column], errors="coerce")
            if parsed.notna().any():
                result[column] = parsed
                report.parsed_date_columns.append(column)

    for column in result.select_dtypes(include="number").columns:
        missing = int(result[column].isna().sum())
        if fill_numeric_missing and missing:
            result[column] = result[column].fillna(result[column].median())
            report.missing_values_filled += missing

    if {"quantity", "unit_price"}.issubset(result.columns) and "revenue" not in result.columns:
        result["revenue"] = result["quantity"] * result["unit_price"]
        report.derived_columns.append("revenue")

    if "customer_id" in result.columns:
        missing_customers = int(result["customer_id"].isna().sum())
        if missing_customers:
            report.warnings.append(f"{missing_customers:,} rows have no customer_id.")

    report.rows_after = len(result)
    return result.reset_index(drop=True), report
