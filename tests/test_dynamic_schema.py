import pandas as pd

from src.ai_analyst import answer_question
from src.data_cleaning import clean_dataframe
from src.data_loader import normalize_columns
from src.kpis import calculate_kpis
from src.schema import canonicalize_dataframe, detect_schema


def test_nonstandard_headings_are_detected_and_analyzed():
    source = pd.DataFrame(
        {
            "Order Number": ["A-1", "A-2", "A-3"],
            "Sales Amount": [100.0, 50.0, 25.0],
            "Qty": [2, 1, 5],
            "Transaction Date": ["2024-01-01", "2024-02-01", "2024-02-15"],
            "Client": ["C1", "C2", "C1"],
            "State": ["NY", "CA", "NY"],
        }
    )
    normalized = normalize_columns(source)
    canonical, mapping = canonicalize_dataframe(normalized)
    cleaned, _ = clean_dataframe(normalized)

    assert detect_schema(list(normalized.columns))["revenue"] == "sales_amount"
    assert mapping["invoice_no"] == "invoice_no"
    assert {"revenue", "quantity", "date", "customer_id"}.issubset(cleaned.columns)
    assert calculate_kpis(cleaned)["total_revenue"] == 175.0

    response = answer_question("What were sales by state?", cleaned)
    assert "state" in response["sql"]
    assert set(response["result"]["state"]) == {"NY", "CA"}
