from src.data_cleaning import clean_dataframe
from src.data_profiling import profile_dataframe
from src.insight_engine import generate_insights
from src.kpis import calculate_kpis
from src.report_generator import build_markdown_report, build_pdf_report


def test_report_contains_measured_sections(retail_data):
    import pytest

    cleaned, _ = clean_dataframe(retail_data)
    markdown = build_markdown_report(profile_dataframe(cleaned), calculate_kpis(cleaned), generate_insights(cleaned))
    assert "Executive summary" in markdown
    assert "Evidence-backed insights" in markdown
    assert "Unavailable" in markdown
    pytest.importorskip("reportlab")
    assert build_pdf_report(markdown).startswith(b"%PDF")
