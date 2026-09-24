import pandas as pd
import pytest

from src.ai_analyst import answer_question
from src.sql_generator import generate_sql
from src.sql_validator import validate_read_only_sql


def test_sql_validator_allows_select_and_blocks_mutation():
    assert validate_read_only_sql("SELECT SUM(revenue) FROM analysis_data")[0]
    assert not validate_read_only_sql("DELETE FROM analysis_data")[0]
    assert not validate_read_only_sql("SELECT * FROM other_table")[0]
    assert not validate_read_only_sql("SELECT 1; SELECT 2")[0]


def test_question_result_is_grounded_in_dataframe(retail_data):
    from src.data_cleaning import clean_dataframe
    cleaned, _ = clean_dataframe(retail_data)
    response = answer_question("What was the total revenue?", cleaned)
    assert response["result"].iloc[0]["total_revenue"] == 59.0
    assert "59.0" in response["explanation"]
    assert response["llm_used"] is False


def test_missing_business_measure_is_rejected(retail_data):
    from src.data_cleaning import clean_dataframe
    cleaned, _ = clean_dataframe(retail_data)
    with pytest.raises(ValueError, match="profit"):
        answer_question("Which category had the highest profit?", cleaned)


def test_monthly_sql_executes_in_local_fallback(retail_data):
    from src.data_cleaning import clean_dataframe
    cleaned, _ = clean_dataframe(retail_data)
    response = answer_question("How did monthly revenue change?", cleaned)
    assert len(response["result"]) == 3
    assert "SUBSTR" in response["sql"]
