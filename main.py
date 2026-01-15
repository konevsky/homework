from typing import Dict, List

from src.external_api import get_transaction_amount_rub
from src.processing import filter_by_state, sort_by_date
from src.readers import read_transactions_csv, read_transactions_excel
from src.utils import load_operations
from src.widget import get_date, mask_account_card


def yes_no_input(prompt: str) -> bool:
    """Возвращает True/False на основе ответа пользователя Да/Нет"""
    while True:
        answer = input(prompt + " ").strip().lower()
        if answer in ["да", "yes", "y"]:
            return True
        elif answer in ["нет", "no", "n"]:
            return False
        else:
            print("Пожалуйста, введите 'Да' или 'Нет'.")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = input("Введите путь к JSON-файлу: ").strip()
        transactions: List[Dict] = load_operations(file_path)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ").strip()
        transactions = read_transactions_csv(file_path)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ").strip()
        transactions = read_transactions_excel(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Файл пустой или произошла ошибка при загрузке.")
        return

    # --------------------------
    # Выбор статуса для фильтрации
    # --------------------------
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    status = ""
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        user_input = input("Ваш выбор: ").strip()
        status_upper = user_input.upper()
        if status_upper in valid_statuses:
            status = status_upper
            print(f'Операции отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'Статус операции "{user_input}" недоступен.')

    # --------------------------
    # Фильтрация по выбранному статусу
    # --------------------------
    filtered_transactions = filter_by_state(transactions, state=status)
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # --------------------------
    # Конвертация в RUB
    # --------------------------
    for tx in filtered_transactions:
        tx["operationAmount"]["amount_rub"] = get_transaction_amount_rub(tx)

    # --------------------------
    # Сортировка по дате
    # --------------------------
    if yes_no_input("Отсортировать операции по дате? Да/Нет"):
        while True:
            order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
            if order in ["по возрастанию", "возрастание", "asc"]:
                reverse = False
                break
            elif order in ["по убыванию", "убывание", "desc"]:
                reverse = True
                break
            else:
                print("Введите корректный вариант: 'по возрастанию' или 'по убыванию'.")
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

    # --------------------------
    # Фильтрация только рублевых транзакций
    # --------------------------
    if yes_no_input("Выводить только рублевые транзакции? Да/Нет"):
        filtered_transactions = [
            tx for tx in filtered_transactions if tx["operationAmount"]["currency"]["code"] == "RUB"
        ]

    # --------------------------
    # Фильтрация по слову в description
    # --------------------------
    if yes_no_input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        keyword = input("Введите слово для поиска в описании: ").strip().lower()
        filtered_transactions = [tx for tx in filtered_transactions if keyword in tx.get("description", "").lower()]

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # --------------------------
    # Вывод итогового списка
    # --------------------------
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for tx in filtered_transactions:
        # Дата
        date_fmt = get_date(tx.get("date", "")) if tx.get("date") else "Нет даты"

        # Описание
        desc = tx.get("description", "Нет описания")

        # Сумма и валюта
        amount_info = tx.get("operationAmount", {})
        amount = amount_info.get("amount", 0)
        currency = amount_info.get("currency", {}).get("code", "")
        amount_rub = amount_info.get("amount_rub", 0.0)

        # Маскировка карт/счетов
        from_info = tx.get("from")
        to_info = tx.get("to")
        masked_from = mask_account_card(from_info) if from_info else ""
        masked_to = mask_account_card(to_info) if to_info else ""

        # Вывод суммы с рублями, если есть
        if currency == "RUB":
            print(f"{date_fmt} {desc}\nСумма: {amount:.2f} руб.")
        else:
            print(f"{date_fmt} {desc}\nСумма: {amount:.2f} {currency} ({amount_rub:.2f} руб.)")

        if masked_from or masked_to:
            print(f"{masked_from} -> {masked_to}")

        print("-" * 50)


if __name__ == "__main__":
    main()
