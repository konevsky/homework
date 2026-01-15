from typing import Any, Dict, List, cast

import pandas as pd


def read_transactions_csv(path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    :param path: путь к CSV-файлу
    :return: список словарей с транзакциями
    """
    df: pd.DataFrame = pd.read_csv(path)

    records: Any = df.to_dict(orient="records")

    return cast(List[Dict[str, Any]], records)


def read_transactions_excel(path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    :param path: путь к Excel-файлу
    :return: список словарей с транзакциями
    """
    df: pd.DataFrame = pd.read_excel(path)

    records: Any = df.to_dict(orient="records")

    return cast(List[Dict[str, Any]], records)
