import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "operationAmount": {"amount": "100", "currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 2,
            "description": "Перевод со счета на счет",
            "operationAmount": {"amount": "200", "currency": {"name": "EUR", "code": "EUR"}},
        },
        {
            "id": 3,
            "description": "Перевод с карты на карту",
            "operationAmount": {"amount": "300", "currency": {"name": "USD", "code": "USD"}},
        },
    ]


def test_filter_by_currency(sample_transactions):
    usd = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd) == 2
    assert usd[0]["id"] == 1
    assert usd[1]["id"] == 3


def test_transaction_descriptions(sample_transactions):
    gen = transaction_descriptions(sample_transactions)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод с карты на карту"


def test_card_number_generator_basic():
    gen = card_number_generator(1, 3)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"

    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_formatting():
    gen = card_number_generator(9999, 10001)
    results = list(gen)
    assert results[0] == "0000 0000 0000 9999"
    assert results[1] == "0000 0000 0001 0000"
    assert results[2] == "0000 0000 0001 0001"
