import pytest

from src.decorators import log


def test_log_console_success(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)

    # Проверяем результат функции
    assert result == 5

    # Проверяем вывод в консоль
    captured = capsys.readouterr().out.splitlines()
    assert captured[0] == "add started. Inputs: (2, 3), {}"
    assert captured[1] == "add finished. Result: 5"


def test_log_console_error(capsys):
    @log()
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    captured = capsys.readouterr().out.splitlines()
    assert captured[0] == "div started. Inputs: (1, 0), {}"
    assert captured[1].startswith("div error: ZeroDivisionError. Inputs: (1, 0), {}")


def test_log_file_and_console_success(tmp_path, capsys):
    logfile = tmp_path / "log.txt"

    @log(filename=str(logfile))
    def mul(a, b):
        return a * b

    mul(3, 4)

    # Проверяем консоль
    captured = capsys.readouterr().out.splitlines()
    assert captured[0] == "mul started. Inputs: (3, 4), {}"
    assert captured[1] == "mul finished. Result: 12"

    # Проверяем файл
    lines = logfile.read_text().splitlines()
    assert lines[0] == "mul started. Inputs: (3, 4), {}"
    assert lines[1] == "mul finished. Result: 12"


def test_log_file_and_console_error(tmp_path, capsys):
    logfile = tmp_path / "log.txt"

    @log(filename=str(logfile))
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(10, 0)

    captured = capsys.readouterr().out.splitlines()
    assert captured[0] == "div started. Inputs: (10, 0), {}"
    assert captured[1].startswith("div error: ZeroDivisionError. Inputs: (10, 0), {}")

    lines = logfile.read_text().splitlines()
    assert lines[0] == "div started. Inputs: (10, 0), {}"
    assert lines[1].startswith("div error: ZeroDivisionError. Inputs: (10, 0), {}")
