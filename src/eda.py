"""Descriptive analysis tables and Plotly figures."""

from __future__ import annotations

import pandas as pd


def monthly_revenue(dataframe: pd.DataFrame) -> pd.DataFrame:
    date_column = next((c for c in ("date", "invoice_date", "order_date") if c in dataframe), None)
    if not date_column or "revenue" not in dataframe:
        return pd.DataFrame(columns=["period", "revenue"])
    result = dataframe.assign(period=pd.to_datetime(dataframe[date_column], errors="coerce")).dropna(subset=["period"])
    return result.assign(period=result["period"].dt.to_period("M").astype(str)).groupby("period", as_index=False)["revenue"].sum()


def grouped_summary(dataframe: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dimension not in dataframe or "revenue" not in dataframe:
        return pd.DataFrame()
    aggregations: dict[str, tuple[str, str]] = {"revenue": ("revenue", "sum")}
    if "profit" in dataframe:
        aggregations["profit"] = ("profit", "sum")
    return dataframe.groupby(dimension, dropna=False).agg(**aggregations).sort_values("revenue", ascending=False).reset_index()


def revenue_trend_figure(dataframe: pd.DataFrame):
    import plotly.express as px

    summary = monthly_revenue(dataframe)
    return px.line(summary, x="period", y="revenue", markers=True, title="Monthly revenue")
