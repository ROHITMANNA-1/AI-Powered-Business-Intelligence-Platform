"""Evidence-backed descriptive insight generation."""

from __future__ import annotations

import pandas as pd

from .eda import grouped_summary, monthly_revenue
from .kpis import calculate_kpis


def generate_insights(dataframe: pd.DataFrame) -> list[dict[str, str]]:
    kpis = calculate_kpis(dataframe)
    insights: list[dict[str, str]] = []
    if kpis["total_revenue"] is not None:
        insights.append({
            "title": "Revenue baseline",
            "supporting_metric": f"Total revenue: {kpis['total_revenue']:,.2f}",
            "comparison": f"Across {kpis['orders']:,} orders" if kpis["orders"] else "Order count unavailable",
            "interpretation": "This is the measured revenue baseline for the loaded and cleaned data.",
            "next_step": "Compare the baseline across time, country, and product to locate concentration and change.",
        })
    monthly = monthly_revenue(dataframe)
    if len(monthly) >= 2:
        change = float(monthly.iloc[-1]["revenue"] - monthly.iloc[-2]["revenue"])
        direction = "increased" if change >= 0 else "decreased"
        insights.append({
            "title": "Latest monthly revenue movement",
            "supporting_metric": f"Change: {change:,.2f}",
            "comparison": f"{monthly.iloc[-2]['period']} to {monthly.iloc[-1]['period']}",
            "interpretation": f"Revenue {direction} between the two latest available months.",
            "next_step": "Investigate product and country contributions before attributing reasons.",
        })
    for dimension in ("country", "category", "region"):
        summary = grouped_summary(dataframe, dimension)
        if not summary.empty:
            top = summary.iloc[0]
            insights.append({
                "title": f"Top {dimension} by revenue",
                "supporting_metric": f"{top[dimension]}: {top['revenue']:,.2f}",
                "comparison": f"Compared with {len(summary) - 1} other {dimension} values",
                "interpretation": f"The leading {dimension} contributes the highest observed revenue.",
                "next_step": f"Review share, trend, and profitability for each {dimension} before making decisions.",
            })
            break
    return insights
