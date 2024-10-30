from caching_decorator import cache


def test_cache_eviction_LRU():
    """Проверяет, что кэш очищает старые значения при превышении глубины  при политике LRU."""

    @cache(depth=2)
    def slow_function(x):
        slow_function.call_count += 1
        return x * x

    # Инициализируем счетчик вызовов
    slow_function.call_count = 0

    slow_function(1)
    slow_function(2)
    assert slow_function.call_count == 2  # Должно быть 2 вызова

    slow_function(2)
    assert slow_function.call_count == 2
    # Вызов с новым значением вытесняет менее используемое значение (1)
    slow_function(3)
    assert slow_function.call_count == 3  # Еще один вызов

    # Повторный вызов для 1 должен пересчитаться, так как он вытеснен
    slow_function(1)
    assert slow_function.call_count == 4  # Пересчитывается заново
