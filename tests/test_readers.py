from typing import Any, Dict, List
from unittest.mock import patch

import pandas as pd

from src.readers import read_transactions_csv, read_transactions_excel


def test_read_transactions_csv() -> None:
    fake_df = pd.DataFrame(
        [
            {
                "date": "2024-01-01",
                "amount": 100,
                "category": "Food",
                "description": "Lunch",
            }
        ]
    )

    with patch("src.readers.pd.read_csv", return_value=fake_df) as mock_read_csv:
        result: List[Dict[str, Any]] = read_transactions_csv("fake.csv")

    mock_read_csv.assert_called_once_with("fake.csv")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["amount"] == 100
    assert result[0]["category"] == "Food"


def test_read_transactions_excel() -> None:
    fake_df = pd.DataFrame(
        [
            {
                "date": "2024-01-02",
                "amount": 250,
                "category": "Transport",
                "description": "Taxi",
            }
        ]
    )

    with patch("src.readers.pd.read_excel", return_value=fake_df) as mock_read_excel:
        result: List[Dict[str, Any]] = read_transactions_excel("fake.xlsx")

    mock_read_excel.assert_called_once_with("fake.xlsx")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["amount"] == 250
    assert result[0]["description"] == "Taxi"
