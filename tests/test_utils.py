import json

from src.utils import load_operations


# ----------------------------
# 1. Тест корректного файла JSON
# ----------------------------
def test_load_operations_correct(tmp_path):
    data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_operations(str(file_path))
    assert result == data


# ----------------------------
# 2. Тест пустого файла
# ----------------------------
def test_load_operations_empty_file(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text("", encoding="utf-8")

    result = load_operations(str(file_path))
    assert result == []


# ----------------------------
# 3. Тест файла с некорректным JSON
# ----------------------------
def test_load_operations_invalid_json(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text("not a json", encoding="utf-8")

    result = load_operations(str(file_path))
    assert result == []


# ----------------------------
# 4. Тест файла, где JSON не список
# ----------------------------
def test_load_operations_not_list(tmp_path):
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps({"id": 1}), encoding="utf-8")

    result = load_operations(str(file_path))
    assert result == []


# ----------------------------
# 5. Тест отсутствующего файла
# ----------------------------
def test_load_operations_file_not_found():
    result = load_operations("non_existent_file.json")
    assert result == []
