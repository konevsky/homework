import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_transaction_amount_rub(transaction: Dict) -> float:
    """
    Возвращает сумму транзакции в рублях (float).
    Для USD и EUR выполняется конвертация через внешний API.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, TypeError, ValueError):
        return 0.0

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        rate = _get_rate_to_rub(currency)
        return round(amount * rate, 2)

    return 0.0


def _get_rate_to_rub(currency: str) -> float:
    """
    Получает текущий курс валюты к RUB через Exchange Rates Data API
    """
    headers = {"apikey": API_KEY}

    params = {"base": currency, "symbols": "RUB"}

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return float(data["rates"]["RUB"])
