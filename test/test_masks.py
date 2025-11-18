import pytest

from src.masks import get_mask_account, get_mask_card_number

# -----------------------------
# ТЕСТЫ ДЛЯ get_mask_card_number
# -----------------------------


def test_get_mask_card_number_valid():
    """Проверка корректного маскирования валидного номера карты."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "value",
    [
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
        "",  # пустая строка
        "1234",  # слишком короткий
    ],
)
def test_get_mask_card_number_invalid_length(value):
    """Функция должна выбрасывать ValueError при неверной длине входных данных."""
    with pytest.raises(ValueError):
        get_mask_card_number(value)


def test_get_mask_card_number_with_spaces():
    """Пробелы должны игнорироваться перед обработкой."""
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


def test_get_mask_card_number_non_digits():
    """Нестандартный случай — функция не проверяет цифры, но длина должна совпасть."""
    with pytest.raises(ValueError):
        get_mask_card_number("abcd1234abcd1234")  # длина 16, но не цифры — допускаем ValueError


# -----------------------------
# ТЕСТЫ ДЛЯ get_mask_account
# -----------------------------


def test_get_mask_account_valid():
    """Проверяем маскировку корректного номера."""
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_with_spaces():
    """Пробелы должны устраняться."""
    assert get_mask_account("7365410843 0135874305") == "**4305"


@pytest.mark.parametrize(
    "value",
    [
        "123",  # меньше 4 символов
        "",  # пусто
    ],
)
def test_get_mask_account_invalid_length(value):
    """Функция должна бросать ValueError при слишком коротком номере."""
    with pytest.raises(ValueError):
        get_mask_account(value)


def test_get_mask_account_non_digits():
    """Функция не проверяет тип символов, но должна корректно работать с любой строкой достаточной длины."""
    assert get_mask_account("abcdXYZ1234") == "**1234"
