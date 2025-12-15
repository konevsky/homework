from unittest.mock import patch

from src.external_api import get_transaction_amount_rub


# ----------------------------
# 1. Транзакция в RUB — возвращаем сумму без API
# ----------------------------
def test_rub_transaction():
    transaction = {"operationAmount": {"amount": "1000", "currency": {"code": "RUB"}}}

    result = get_transaction_amount_rub(transaction)
    assert result == 1000.0


# ----------------------------
# 2. Транзакция в USD — используем мок для курса
# ----------------------------
def test_usd_transaction():
    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}

    # Мокаем _get_rate_to_rub, чтобы вернуть курс 90
    with patch("external_api._get_rate_to_rub", return_value=90):
        result = get_transaction_amount_rub(transaction)

    # 10 * 90 = 900
    assert result == 900.0


# ----------------------------
# 3. Транзакция в EUR — используем мок для курса
# ----------------------------
def test_eur_transaction():
    transaction = {"operationAmount": {"amount": "20", "currency": {"code": "EUR"}}}

    with patch("external_api._get_rate_to_rub", return_value=100):
        result = get_transaction_amount_rub(transaction)

    # 20 * 100 = 2000
    assert result == 2000.0


# ----------------------------
# 4. Некорректная транзакция — отсутствуют ключи
# ----------------------------
def test_invalid_transaction():
    transaction = {"wrong": "data"}

    result = get_transaction_amount_rub(transaction)
    assert result == 0.0


# ----------------------------
# 5. Неизвестная валюта — возвращаем 0
# ----------------------------
def test_unknown_currency():
    transaction = {"operationAmount": {"amount": "50", "currency": {"code": "GBP"}}}

    result = get_transaction_amount_rub(transaction)
    assert result == 0.0
