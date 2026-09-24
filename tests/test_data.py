from src.data_cleaning import clean_dataframe
from src.data_profiling import profile_dataframe


def test_cleaning_removes_cancelled_and_derives_revenue(retail_data):
    cleaned, report = clean_dataframe(retail_data)
    assert len(cleaned) == 4
    assert "revenue" in cleaned
    assert cleaned["revenue"].sum() == 59.0
    assert report.cancelled_rows_removed == 1


def test_profile_reports_shape_and_quality(retail_data):
    profile = profile_dataframe(retail_data)
    assert profile["rows"] == 6
    assert profile["columns"] == 6
    assert profile["duplicate_rows"] == 1
    assert any("duplicate" in issue for issue in profile["quality_issues"])
