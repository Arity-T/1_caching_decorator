from caching_decorator import cache


def test_cache_eviction_FIFO():
    """Проверяет, что кэш очищает старые значения при превышении глубины при политике FIFO."""

    @cache(depth=2, policy="FIFO")
    def slow_function(x):
        slow_function.call_count += 1
        return x * x

    slow_function.call_count = 0

    slow_function(1)
    slow_function(2)
    assert slow_function.call_count == 2

    slow_function(2)
    assert slow_function.call_count == 2

    slow_function(3)
    assert slow_function.call_count == 3

    slow_function(1)
    assert slow_function.call_count == 4

    slow_function(2)
    assert slow_function.call_count == 5
