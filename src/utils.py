import json
from typing import List, Dict


def load_operations(path: str) -> List[Dict]:
    """
    Загружает финансовые транзакции из JSON-файла.

    :param path: путь до JSON-файла
    :return: список словарей с транзакциями или пустой список
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
