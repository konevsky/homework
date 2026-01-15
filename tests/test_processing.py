import pytest

from src.processing import filter_by_state, process_bank_search, sort_by_date

# -----------------------
# FIXTURES
# -----------------------


@pytest.fixture
def sample_data():
    """Основной набор данных для тестов."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2024-01-01T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-12-31T23:59:59"},
        {"id": 4, "state": "CANCELED", "date": "2022-05-05T08:30:00"},
    ]


@pytest.fixture
def data_with_equal_dates():
    """Данные, в которых даты совпадают."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T00:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T00:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T00:00:00"},
    ]


@pytest.fixture
def data_with_invalid_date():
    """Данные с некорректным форматом даты."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024/01/01"},  # неправильный формат
        {"id": 2, "state": "EXECUTED", "date": "not-a-date"},  # вообще не дата
        {"id": 3, "state": "EXECUTED", "date": ""},
    ]


@pytest.fixture
def data_with_descriptions():
    """Данные с описаниями операций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг связи"},
        {"id": 3, "description": "Перевод частному лицу"},
        {"id": 4, "description": "Снятие наличных"},
    ]


# -----------------------
# TESTS FOR filter_by_state
# -----------------------


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
        ("UNKNOWN", []),  # нет совпадений
    ],
)
def test_filter_by_state(sample_data, state, expected_ids):
    result = filter_by_state(sample_data, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_empty():
    """Пустой вход → пустой выход."""
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_default(sample_data):
    """Проверка значения по умолчанию state='EXECUTED'."""
    result = filter_by_state(sample_data)
    assert [item["id"] for item in result] == [1, 3]


# -----------------------
# TESTS FOR sort_by_date
# -----------------------


def test_sort_by_date_desc(sample_data):
    """Сортировка по убыванию (reverse=True). Новые даты первыми."""
    result = sort_by_date(sample_data)
    assert [item["id"] for item in result] == [1, 2, 3, 4]


def test_sort_by_date_asc(sample_data):
    """Сортировка по возрастанию (reverse=False). Старые даты первыми."""
    result = sort_by_date(sample_data, reverse=False)
    assert [item["id"] for item in result] == [4, 3, 2, 1]


def test_sort_by_date_equal_dates(data_with_equal_dates):
    """Одинаковые даты → порядок не меняется."""
    result = sort_by_date(data_with_equal_dates)
    assert result == data_with_equal_dates  # stable sort


@pytest.mark.parametrize(
    "bad_entry",
    [
        {"date": "2024/01/01"},
        {"date": "not-a-date"},
        {"date": ""},
        {"date": None},
    ],
)
def test_sort_by_date_invalid_format(bad_entry):
    """Некорректная дата должна вызвать исключение."""
    with pytest.raises(Exception):
        sort_by_date([bad_entry])


def test_sort_by_date_missing_key():
    """Отсутствует ключ date → KeyError."""
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1}])


# -----------------------
# COMPLEX COMBINED TEST
# -----------------------


def test_filter_and_sort_together(sample_data):
    """Проверка типичной последовательности: фильтрация + сортировка."""
    executed = filter_by_state(sample_data, "EXECUTED")
    sorted_data = sort_by_date(executed)

    assert [item["id"] for item in sorted_data] == [1, 3]


# -----------------------
# TESTS FOR process_bank_search
# -----------------------


@pytest.mark.parametrize(
    "search, expected_ids",
    [
        ("перевод", [1, 3]),
        ("Перевод", [1, 3]),  # проверка IGNORECASE
        ("услуг", [2]),
        ("наличных", [4]),
        ("кредит", []),  # нет совпадений
    ],
)
def test_process_bank_search(data_with_descriptions, search, expected_ids):
    result = process_bank_search(data_with_descriptions, search)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_search_empty_search(data_with_descriptions):
    """Пустая строка поиска → пустой результат."""
    result = process_bank_search(data_with_descriptions, "")
    assert result == []


def test_process_bank_search_empty_data():
    """Пустой список операций → пустой результат."""
    result = process_bank_search([], "перевод")
    assert result == []


def test_process_bank_search_missing_description_key():
    """Отсутствует ключ description → операция игнорируется."""
    data = [
        {"id": 1, "description": "Перевод"},
        {"id": 2},  # нет description
    ]
    result = process_bank_search(data, "перевод")
    assert [item["id"] for item in result] == [1]
