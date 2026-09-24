"""Grounded analyst responses built from validated query results."""

from __future__ import annotations

import os
import re

import pandas as pd

from .sql_generator import generate_sql
from .sql_validator import validate_read_only_sql
from .schema import canonicalize_dataframe


def answer_question(question: str, dataframe: pd.DataFrame) -> dict[str, object]:
    """Return SQL, measured results, and a non-causal explanation."""
    dataframe, schema = canonicalize_dataframe(dataframe)
    llm_used = False
    if llm_is_configured():
        try:
            query = generate_sql_with_llm(question, list(dataframe.columns))
            llm_used = True
        except Exception:
            query = generate_sql(question, list(dataframe.columns))
    else:
        query = generate_sql(question, list(dataframe.columns))
    valid, validated = validate_read_only_sql(query)
    if not valid:
        raise ValueError(validated)
    result = _execute_in_memory(validated, dataframe)
    explanation = explain_result(question, result)
    return {"question": question, "sql": validated, "result": result, "answer": explanation, "explanation": explanation, "llm_used": llm_used, "schema": schema}


def generate_sql_with_llm(question: str, columns: list[str], table_name: str = "analysis_data") -> str:
    """Ask the configured model for SQL, then let the validator decide whether it is usable."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    f"Generate exactly one read-only SQL query for table {table_name}. "
                    f"Available columns: {', '.join(columns)}. Return SQL only. "
                    "Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or multiple statements."
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    content = response.choices[0].message.content or ""
    return re.sub(r"^```(?:sql)?\s*|\s*```$", "", content.strip(), flags=re.I)


def _execute_in_memory(query: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    import sqlite3
    with sqlite3.connect(":memory:") as connection:
        dataframe.to_sql("analysis_data", connection, index=False)
        return pd.read_sql_query(query, connection)


def explain_result(question: str, result: pd.DataFrame) -> str:
    if result.empty:
        return "The query returned no rows, so the available data does not support a finding for this question."
    if len(result) == 1:
        details = ", ".join(f"{key}={value}" for key, value in result.iloc[0].to_dict().items())
        return f"Measured answer: {details}. This is a descriptive observation; the data does not establish causation."
    preview = result.head(5).to_dict(orient="records")
    return f"Measured answer: the query returned {len(result):,} rows. Top results: {preview}. This is a descriptive observation; the data does not establish causation."


def llm_is_configured() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))
