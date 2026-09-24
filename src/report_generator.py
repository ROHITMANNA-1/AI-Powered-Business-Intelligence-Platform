"""Markdown and PDF report generation."""

from __future__ import annotations

from typing import Any


def build_markdown_report(profile: dict[str, Any], kpis: dict[str, Any], insights: list[dict[str, str]]) -> str:
    lines = ["# AI Analyst Business Report", "", "## Executive summary", ""]
    lines.append(f"The dataset contains {profile['rows']:,} rows and {profile['columns']:,} columns.")
    lines.append("Findings below are descriptive and based only on the loaded data.")
    lines.extend(["", "## Dataset overview", "", f"- Rows: {profile['rows']:,}", f"- Columns: {profile['columns']:,}", f"- Duplicate rows: {profile['duplicate_rows']:,}"])
    lines.extend(["", "## KPI performance", ""])
    for name, value in kpis.items():
        lines.append(f"- {name.replace('_', ' ').title()}: {value if value is not None else 'Unavailable'}")
    lines.extend(["", "## Evidence-backed insights", ""])
    for insight in insights:
        lines.extend([f"### {insight['title']}", f"- Supporting metric: {insight['supporting_metric']}", f"- Comparison: {insight['comparison']}", f"- Interpretation: {insight['interpretation']}", f"- Further investigation: {insight['next_step']}", ""])
    lines.extend(["## Data quality observations", ""])
    lines.extend(f"- {issue}" for issue in profile["quality_issues"] or ["No configured quality checks found issues."])
    lines.extend(["", "## Limitations and next steps", "", "The source does not include profit, category, shipping, or delivery fields. Do not infer causation from these descriptive results."])
    return "\n".join(lines)


def build_pdf_report(markdown: str) -> bytes:
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    output = BytesIO()
    document = canvas.Canvas(output, pagesize=letter)
    _, height = letter
    y = height - 48
    for line in markdown.splitlines():
        if y < 48:
            document.showPage()
            y = height - 48
        document.drawString(48, y, line[:110])
        y -= 14
    document.save()
    return output.getvalue()
