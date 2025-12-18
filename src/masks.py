import logging
from pathlib import Path

# путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")

formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False


def get_mask_card_number(card_number: str) -> str:
    logger.debug(f"Получен номер карты: {card_number}")

    card_number = card_number.replace(" ", "")

    if not card_number.isdigit():
        logger.error("Номер карты содержит недопустимые символы")
        raise ValueError("Номер карты должен содержать только цифры")

    if len(card_number) != 16:
        logger.error("Неверная длина номера карты")
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked = card_number[:4] + " " + card_number[4:6] + "**" + " " + "****" + " " + card_number[-4:]

    logger.info("Номер карты успешно замаскирован")
    return masked


def get_mask_account(account_number: str) -> str:
    logger.debug(f"Получен номер счета: {account_number}")

    account_number = account_number.replace(" ", "")

    if len(account_number) < 4:
        logger.error("Слишком короткий номер счета")
        raise ValueError("Номер счета должен содержать хотя бы 4 цифры")

    masked = "**" + account_number[-4:]
    logger.info("Номер счета успешно замаскирован")
    return masked
