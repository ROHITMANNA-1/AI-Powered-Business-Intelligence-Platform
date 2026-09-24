from src.data_cleaning import clean_dataframe
from src.kpis import calculate_kpis


def test_kpis_match_independent_calculation(retail_data):
    cleaned, _ = clean_dataframe(retail_data)
    kpis = calculate_kpis(cleaned)
    assert kpis["total_revenue"] == 59.0
    assert kpis["orders"] == 3
    assert kpis["customers"] == 3
    assert kpis["average_order_value"] == 59.0 / 3
    assert kpis["total_profit"] is None
