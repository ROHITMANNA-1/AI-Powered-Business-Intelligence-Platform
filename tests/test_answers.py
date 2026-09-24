from src.ai_analyst import answer_question
from src.data_cleaning import clean_dataframe


def test_grouped_business_question_returns_answer_and_dimension(retail_data):
    cleaned, _ = clean_dataframe(retail_data)
    response = answer_question("Which countries generated the highest sales?", cleaned)
    assert "country" in response["sql"]
    assert len(response["result"]) == 3
    assert "Top results" in response["answer"]
