"""Read-only SQL validation for analyst-generated queries."""

from __future__ import annotations

import re

FORBIDDEN = re.compile(r"\b(insert|update|delete|drop|alter|truncate|create|replace|grant|revoke|call|execute)\b", re.I)


def validate_read_only_sql(query: str, allowed_table: str = "analysis_data") -> tuple[bool, str]:
    normalized = query.strip().rstrip(";").strip()
    if not normalized:
        return False, "Query is empty."
    if ";" in normalized:
        return False, "Only one SQL statement is allowed."
    if FORBIDDEN.search(normalized):
        return False, "Only read-only SELECT queries are allowed."
    if not re.match(r"^(select|with)\b", normalized, re.I):
        return False, "Query must begin with SELECT or WITH."
    referenced = re.findall(r"\b(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)", normalized, re.I)
    if referenced and any(table.lower() != allowed_table.lower() for table in referenced):
        return False, f"Query may only reference the {allowed_table} table."
    return True, normalized
