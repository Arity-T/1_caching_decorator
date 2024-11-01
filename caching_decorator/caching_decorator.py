"""Кэширующий декоратор.

Пара полезных ссылок:
1. Зачем нужен wraps?
https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
2. Декораторы с параметрами
https://stackoverflow.com/questions/5929107/decorators-with-parameters
"""

__all__ = ["cache"]

from collections import deque
from functools import wraps


def cache(depth=10, policy="LRU"):
    def decorator(func):
        cache = dict()
        access = deque()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (*args, *kwargs.items())

            if key in cache:
                if policy == "LRU":
                    access.remove(key)
                    access.append(key)
                return cache[key]

            result = func(*args, **kwargs)
            cache[key] = result
            access.append(key)

            if len(cache) > depth:
                if policy == "LRU":
                    oldest_key = access.popleft()

                del cache[oldest_key]

            return result

        return wrapper

    return decorator
