import json
import logging
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "utils.log", mode="w", encoding="utf-8")

formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False


def load_operations(path: str) -> List[Dict]:
    logger.debug(f"Попытка загрузки файла: {path}")

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                logger.info(f"Загружено операций: {len(data)}")
                return data

            logger.warning("JSON не является списком")
            return []

    except FileNotFoundError:
        logger.error("Файл не найден")
        return []

    except json.JSONDecodeError:
        logger.error("Ошибка декодирования JSON")
        return []
