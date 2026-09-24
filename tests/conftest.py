from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def retail_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "invoice_no": ["1001", "1001", "1002", "C1003", "1004", "1004"],
            "quantity": [2, 1, 3, 1, 4, 4],
            "unit_price": [10.0, 5.0, 8.0, 20.0, 2.5, 2.5],
            "invoice_date": pd.to_datetime(["2024-01-02", "2024-01-02", "2024-02-03", "2024-02-04", "2024-03-01", "2024-03-01"]),
            "customer_id": ["A", "A", "B", "C", "D", "D"],
            "country": ["UK", "UK", "FR", "UK", "DE", "DE"],
        }
    )
