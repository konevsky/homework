def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате:
    XXXX XX** **** XXXX
    Видны первые 6 и последние 4 цифры, остальные заменены '*'.

    Пример:
    '7000792289606361' -> '7000 79** **** 6361'
    """
    # Убираем пробелы на случай, если они есть
    card_number = card_number.replace(" ", "")

    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Формируем маску
    masked = (
        card_number[:4]
        + " "
        + card_number[4:6]  # первые 4 цифры
        + "**"
        + " "
        + "****"  # 5-6 цифры + **
        + " "
        + card_number[-4:]  # полностью маскируем 7-10 цифры  # последние 4 цифры
    )
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета в формате: **XXXX
    Видны только последние 4 цифры, перед ними две '*'.

    Пример:
    '73654108430135874305' -> '**4305'
    """
    account_number = account_number.replace(" ", "")

    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать хотя бы 4 цифры")

    masked = "**" + account_number[-4:]
    return masked
