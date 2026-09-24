"""SQLAlchemy database helpers with SQLite fallback for local development."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def create_database_engine() -> Engine:
    """Create a configured MySQL engine or a local SQLite engine."""
    url = os.getenv("DATABASE_URL")
    if not url and os.getenv("MYSQL_HOST"):
        url = (
            f"mysql+pymysql://{os.getenv('MYSQL_USER', '')}:{os.getenv('MYSQL_PASSWORD', '')}"
            f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE', 'ai_analyst')}"
        )
    return create_engine(url or "sqlite:///data/ai_analyst.db", future=True)


def safe_table_name(name: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_]", "_", name.lower()).strip("_")
    if not value:
        raise ValueError("Table name cannot be empty.")
    return value


def load_dataframe_to_database(dataframe: pd.DataFrame, table_name: str = "analysis_data") -> str:
    table = safe_table_name(table_name)
    engine = create_database_engine()
    Path("data").mkdir(exist_ok=True)
    dataframe.to_sql(table, engine, if_exists="replace", index=False)
    return table


def execute_read_only(engine: Engine, query: str, limit: int = 1000) -> pd.DataFrame:
    """Execute a validated query with a defensive result limit."""
    statement = text(query)
    with engine.connect() as connection:
        return pd.read_sql(statement, connection).head(limit)
