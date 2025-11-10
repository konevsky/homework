from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


# Импортируем функции маскировки из модуля masks
def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Аргумент:
        account_info (str): строка с типом и номером карты или счета.

    Возвращает:
        str: строка с замаскированным номером.
    """
    # Разбиваем строку на части
    parts = account_info.split()

    # Номер карты или счета всегда будет в последней части строки
    account_number = parts[-1]

    # Тип карты или счета может быть в нескольких словах, поэтому объединяем всё до последнего элемента
    account_type = " ".join(parts[:-1])

    # Применяем маскировку в зависимости от типа
    if account_type in ["Visa Platinum", "Visa Gold", "Visa Classic", "MasterCard", "Maestro"]:
        # Добавим сюда все типы карт, если нужно
        return get_mask_card_number(account_number)
    elif account_type == "Счет":
        return get_mask_account(account_number)
    else:
        raise ValueError("Неизвестный тип карты или счета")


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате "2024-03-11T02:26:18.671407"
    в строку формата "ДД.ММ.ГГГГ".

    Аргумент:
        date_str (str): строка с датой в формате "YYYY-MM-DDTHH:MM:SS.ssssss".

    Возвращает:
        str: строка с датой в формате "ДД.ММ.ГГГГ".
    """
    # Парсим строку в объект datetime
    dt = datetime.fromisoformat(date_str)

    # Возвращаем строку в нужном формате "ДД.ММ.ГГГГ"
    return dt.strftime("%d.%m.%Y")
