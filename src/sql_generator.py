"""Conservative natural-language-to-SQL generation."""

from __future__ import annotations

import re

import pandas as pd

from .schema import canonicalize_dataframe


def generate_sql(question: str, columns: list[str], table_name: str = "analysis_data") -> str:
    """Generate safe SQL for common business questions without an LLM."""
    text = question.lower()
    available = set(canonicalize_dataframe(pd.DataFrame(columns=columns))[0].columns)
    if "revenue" not in available:
        raise ValueError("This dataset has no revenue column to query.")
    if any(word in text for word in ("profit", "margin")) and "profit" not in available:
        raise ValueError("The available dataset does not contain profit data.")
    date_column = next((column for column in ("date", "invoice_date", "order_date") if column in available), None)
    if "monthly" in text or "month" in text:
        if not date_column:
            raise ValueError("No date column is available for a monthly analysis.")
        return (
            f"SELECT SUBSTR(CAST({date_column} AS CHAR), 1, 7) AS month, SUM(revenue) AS revenue "
            f"FROM {table_name} GROUP BY month ORDER BY month"
        )
    dimension = _find_dimension(text, available)
    if dimension:
        return f"SELECT {dimension}, SUM(revenue) AS revenue FROM {table_name} GROUP BY {dimension} ORDER BY revenue DESC"
    if "customer" in text and "customer_id" in available:
        return f"SELECT customer_id, SUM(revenue) AS revenue FROM {table_name} GROUP BY customer_id ORDER BY revenue DESC LIMIT 20"
    if re.search(r"(total|overall).*(revenue|sales)|revenue.*total", text):
        return f"SELECT SUM(revenue) AS total_revenue FROM {table_name}"
    return f"SELECT COUNT(*) AS rows, SUM(revenue) AS total_revenue FROM {table_name}"


def _find_dimension(question: str, columns: set[str]) -> str | None:
    ignored = {"revenue", "profit", "quantity", "unit_price", "date", "invoice_no", "customer_id"}
    words = set(re.findall(r"[a-z0-9_]+", question))
    for column in sorted(columns):
        if column in ignored:
            continue
        singular = column[:-1] if column.endswith("s") else column
        if column in words or singular in words or f"{column}s" in words:
            return column
    aliases = {"sales": "revenue", "countries": "country", "products": "product_name", "customers": "customer_id"}
    for word, column in aliases.items():
        if word in words and column in columns and column not in ignored:
            return column
    return None
