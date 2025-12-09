import functools

def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def write(msg):
                # Всегда выводим в консоль
                print(msg)
                # Если filename задан — пишем и в файл
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")

            # Логируем начало
            write(f"{func.__name__} started. Inputs: {args}, {kwargs}")

            try:
                result = func(*args, **kwargs)
                write(f"{func.__name__} finished. Result: {result}")
                return result

            except Exception as e:
                error_name = type(e).__name__
                # Логирование ошибки + входные параметры
                write(
                    f"{func.__name__} error: {error_name}. "
                    f"Inputs: {args}, {kwargs}"
                )
                raise  # не скрываем ошибку

        return wrapper
    return decorator
