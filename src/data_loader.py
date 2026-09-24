"""Dataset loading and column normalization utilities."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import re
from typing import BinaryIO

import pandas as pd

from .schema import canonicalize_dataframe


def normalize_column_name(name: object) -> str:
    """Convert a source column into a stable snake_case identifier."""
    value = re.sub(r"[^a-zA-Z0-9]+", "_", str(name).strip().lower()).strip("_")
    return value or "unnamed_column"


def normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with unique, stable column names."""
    result = dataframe.copy()
    names: list[str] = []
    counts: dict[str, int] = {}
    for column in result.columns:
        base = normalize_column_name(column)
        counts[base] = counts.get(base, 0) + 1
        names.append(base if counts[base] == 1 else f"{base}_{counts[base]}")
    result.columns = names
    return result


def load_dataframe(source: str | Path | BinaryIO | bytes, filename: str | None = None) -> pd.DataFrame:
    """Load CSV or Excel content and normalize its columns."""
    name = filename or str(source)
    suffix = Path(name).suffix.lower()
    if isinstance(source, bytes):
        source = BytesIO(source)
    if suffix == ".csv":
        dataframe = pd.read_csv(source)
    elif suffix in {".xlsx", ".xls"}:
        dataframe = pd.read_excel(source)
    else:
        raise ValueError("Supported file types are CSV, XLSX, and XLS.")
    if dataframe.empty:
        raise ValueError("The uploaded dataset contains no rows.")
    normalized = normalize_columns(dataframe)
    canonical, _ = canonicalize_dataframe(normalized)
    return canonical
