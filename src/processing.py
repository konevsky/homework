from datetime import datetime


def filter_by_state(data: list, state: str = 'EXECUTED') -> list:
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param data: список словарей
    :param state: значение поля 'state', по умолчанию 'EXECUTED'
    :return: новый список словарей, у которых data['state'] == state
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: list, reverse: bool = True) -> list:
    """
    Сортирует список словарей по ключу 'date'.

    :param data: список словарей
    :param reverse: порядок сортировки (True — по убыванию, False — по возрастанию)
                    по умолчанию сортируется по убыванию (сначала новые даты)
    :return: новый отсортированный список словарей
    """
    return sorted(
        data,
        key=lambda item: datetime.fromisoformat(item['date']),
        reverse=reverse
    )