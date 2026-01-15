import re
from datetime import datetime
from typing import Dict, List


def filter_by_state(data: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: список словарей
    :param state: значение поля 'state', по умолчанию 'EXECUTED'
    :return: новый список словарей, у которых data['state'] == state
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list, reverse: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date'.

    :param data: список словарей
    :param reverse: порядок сортировки (True — по убыванию, False — по возрастанию)
                    по умолчанию сортируется по убыванию (сначала новые даты)
    :return: новый отсортированный список словарей
    """
    return sorted(data, key=lambda item: datetime.fromisoformat(item["date"]), reverse=reverse)


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список банковских операций по строке поиска в описании.

    :param data: список словарей с данными о банковских операциях
    :param search: строка для поиска
    :return: список операций, в описании которых есть строка поиска
    """
    if not search:
        return []

    pattern = re.compile(search, re.IGNORECASE)

    result = []
    for operation in data:
        description = operation.get("description", "")
        if pattern.search(description):
            result.append(operation)

    return result


def count_operations_by_category(
    data: List[Dict],
    categories: List[str],
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    :param data: список словарей с операциями
    :param categories: список категорий операций
    :return: словарь {категория: количество операций}
    """
    result = {category: 0 for category in categories}

    for operation in data:
        description = operation.get("description")
        if description in result:
            result[description] += 1

    return result
