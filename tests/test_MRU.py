from caching_decorator import cache


def test_cache_eviction_MRU():
    """Проверяет, что кэш очищает старые значения при превышении глубины при политике LIFO."""

    @cache(depth=2, policy="MRU")
    def slow_function(x):
        slow_function.call_count += 1
        return x * x

    # Инициализируем счетчик вызовов
    slow_function.call_count = 0

    slow_function(1)
    slow_function(2)
    assert slow_function.call_count == 2

    slow_function(2)
    assert slow_function.call_count == 2

    slow_function(3)
    assert slow_function.call_count == 3

    slow_function(1)
    assert slow_function.call_count == 3
