"""Validated SQL execution boundary."""

from __future__ import annotations

import pandas as pd
from sqlalchemy.engine import Engine

from .database import execute_read_only
from .sql_validator import validate_read_only_sql


def run_query(engine: Engine, query: str, table_name: str = "analysis_data") -> pd.DataFrame:
    valid, result = validate_read_only_sql(query, table_name)
    if not valid:
        raise ValueError(result)
    return execute_read_only(engine, result)
