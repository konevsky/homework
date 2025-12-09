import functools
from typing import Callable, Optional, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            def write(message: str) -> None:
                print(message)
                if filename is not None:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")

            write(f"{func.__name__} started. Inputs: {args}, {kwargs}")

            try:
                result = func(*args, **kwargs)
                write(f"{func.__name__} finished. Result: {result}")
                return result

            except Exception as e:
                error_name = type(e).__name__
                write(f"{func.__name__} error: {error_name}. " f"Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
