from typing import Any, Dict, Generator, Iterable


def filter_by_currency(
    transactions: Iterable[Dict[str, Any]], currency_code: str
) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует список транзакций по коду валюты.

    Генератор проходит по списку словарей с транзакциями и
    поочередно возвращает только те транзакции, в которых
    валюта операции соответствует переданному коду.

    Args:
        transactions (list): Список словарей с транзакциями.
        currency_code (str): Код валюты для фильтрации (например, "USD").

    Yields:
        dict: Транзакция, содержащая указанную валюту.
    """
    for tx in transactions:
        # Проверяем, что у транзакции есть поле operationAmount → currency → code
        if (
            "operationAmount" in tx
            and "currency" in tx["operationAmount"]
            and tx["operationAmount"]["currency"].get("code") == currency_code
        ):
            yield tx


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор, возвращающий описание каждой транзакции.

    Проходит по списку транзакций и поочередно возвращает
    значение поля "description".

    Args:
        transactions (list): Список словарей с транзакциями.

    Yields:
        str: Описание операции.
    """
    for tx in transactions:
        # Берём поле "description", если оно есть
        if "description" in tx:
            yield tx["description"]


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Принимает начальное и конечное значения диапазона и
    поочередно возвращает каждое число, преобразованное
    в строку длиной 16 цифр с пробелами каждые 4 символа.

    Args:
        start (int): Начальное значение диапазона (включительно).
        end (int): Конечное значение диапазона (включительно).

    Yields:
        str: Номер карты в формате 'XXXX XXXX XXXX XXXX'.
    """
    for number in range(start, end + 1):
        # Преобразуем число в 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Форматируем как XXXX XXXX XXXX XXXX
        formatted = f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted
