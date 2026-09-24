"""Shared KPI definitions used by Python, SQL, and documentation."""

from __future__ import annotations

import pandas as pd

from .schema import canonicalize_dataframe


def calculate_kpis(dataframe: pd.DataFrame) -> dict[str, float | int | None]:
    """Calculate only KPIs supported by the available columns."""
    dataframe, _ = canonicalize_dataframe(dataframe)
    revenue = float(dataframe["revenue"].sum()) if "revenue" in dataframe else None
    orders = int(dataframe["invoice_no"].nunique()) if "invoice_no" in dataframe else None
    customers = int(dataframe["customer_id"].nunique()) if "customer_id" in dataframe else None
    return {
        "total_revenue": revenue,
        "total_profit": float(dataframe["profit"].sum()) if "profit" in dataframe else None,
        "profit_margin": (
            float(dataframe["profit"].sum() / revenue) if revenue and "profit" in dataframe else None
        ),
        "orders": orders,
        "average_order_value": revenue / orders if revenue is not None and orders else None,
        "customers": customers,
        "average_discount": float(dataframe["discount"].mean()) if "discount" in dataframe else None,
        "on_time_delivery_rate": None,
    }
