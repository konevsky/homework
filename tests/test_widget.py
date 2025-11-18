from datetime import datetime

import pytest

from src.widget import get_date, mask_account_card

# ----------------------------
# Tests for mask_account_card
# ----------------------------


@pytest.mark.parametrize(
    "input_str, expected_value, mock_func",
    [
        ("Visa Platinum 1234567812345678", "**** **** **** 5678", "card"),
        ("Visa Gold 5555666677778888", "**** **** **** 8888", "card"),
        ("MasterCard 2222333344445555", "**** **** **** 5555", "card"),
        ("Maestro 4000000011112222", "**** **** **** 2222", "card"),
        ("Счет 40817810099910004312", "**4312", "account"),
    ],
)
def test_mask_account_card_correct_branch(monkeypatch, input_str, expected_value, mock_func):
    """
    Проверяет, что функция выбирает правильную ветку
    маскировки карты или счёта.
    """

    if mock_func == "card":
        monkeypatch.setattr("src.widget.get_mask_card_number", lambda number: expected_value)
    else:
        monkeypatch.setattr("src.widget.get_mask_account", lambda number: expected_value)

    assert mask_account_card(input_str) == expected_value


@pytest.mark.parametrize(
    "invalid_data",
    [
        "UnknownType 12345678",
        "CardWithoutNumber",
        "Visa",  # нет номера
        "12345678",  # нет типа, только номер
        "",
        "   ",  # пустая строка
    ],
)
def test_mask_account_card_invalid(invalid_data):
    """
    Проверка, что функция выбрасывает ошибку при некорректном формате входных данных.
    """
    with pytest.raises(Exception):
        mask_account_card(invalid_data)


def test_mask_account_card_not_recognized():
    """
    Тест на неизвестный тип карты или счета.
    """
    with pytest.raises(ValueError):
        mask_account_card("American Express 1234567812345678")


# ----------------------------
# Tests for get_date
# ----------------------------


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2020-01-01T00:00:00", "01.01.2020"),
        ("1999-12-31T23:59:59", "31.12.1999"),
    ],
)
def test_get_date_basic(input_date, expected):
    """
    Проверка корректного перевода ISO даты в формат ДД.ММ.ГГГГ.
    """
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),  # valid
        ("2024-03-11 12:00:00", "11.03.2024"),  # valid
    ],
)
def test_get_date_valid_extended(input_date, expected):
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "input_date",
    [
        "2024/03/11",
        "March 11 2024",
        "11-03-2024",
        "",
        "   ",
        None,
    ],
)
def test_get_date_invalid(input_date):
    with pytest.raises(Exception):
        get_date(input_date)


def test_get_date_extreme_case():
    """
    Граничный случай — минимальная корректная ISO-дата.
    """
    iso = datetime.min.isoformat()
    expected = datetime.min.strftime("%d.%m.%Y")

    assert get_date(iso) == expected
