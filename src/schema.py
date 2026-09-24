"""Detect business fields from arbitrary normalized CSV headings."""

from __future__ import annotations

import re

import pandas as pd

ALIASES: dict[str, tuple[str, ...]] = {
    "invoice_no": ("invoice_no", "invoice", "order_id", "order_number", "order_no", "transaction_id", "transaction_number"),
    "quantity": ("quantity", "qty", "units", "unit_count", "items_sold"),
    "unit_price": ("unit_price", "price", "unit_cost", "selling_price", "item_price"),
    "revenue": ("revenue", "sales", "sales_amount", "total_sales", "total_revenue", "amount", "net_sales"),
    "profit": ("profit", "profit_amount", "net_profit", "gross_profit"),
    "customer_id": ("customer_id", "customer", "customer_number", "client", "client_id", "buyer_id"),
    "date": ("invoice_date", "order_date", "transaction_date", "purchase_date", "date", "timestamp"),
    "discount": ("discount", "discount_rate", "discount_percent", "discount_amount"),
    "product_name": ("product_name", "product", "item", "item_name", "description", "product_description"),
}


def _compact(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def detect_schema(columns: list[str]) -> dict[str, str]:
    """Return canonical field names mapped to the actual source headings."""
    compact_columns = {_compact(column): column for column in columns}
    detected: dict[str, str] = {}
    for canonical, aliases in ALIASES.items():
        for alias in aliases:
            match = compact_columns.get(_compact(alias))
            if match:
                detected[canonical] = match
                break
    return detected


def canonicalize_dataframe(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    """Rename detected fields to stable internal names and return the mapping."""
    result = dataframe.copy()
    detected = detect_schema(list(result.columns))
    rename_map: dict[str, str] = {}
    for canonical, source in detected.items():
        if canonical not in result.columns and source != canonical:
            rename_map[source] = canonical
    result = result.rename(columns=rename_map)
    return result, {canonical: rename_map.get(source, source) for canonical, source in detected.items()}
