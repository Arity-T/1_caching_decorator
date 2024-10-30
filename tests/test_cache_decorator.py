from caching_decorator import cache


def test_caching():
    """Проверяет, что результат кэшируется и функция не выполняется повторно."""

    @cache(depth=3)
    def slow_function(x):
        slow_function.call_count += 1
        return x * x

    # Инициализируем счетчик вызовов
    slow_function.call_count = 0

    result1 = slow_function(2)
    result2 = slow_function(2)

    assert result1 == result2  # Ожидаем одинаковый результат
    assert slow_function.call_count == 1  # Функция должна быть вызвана только один раз


def test_multiple_functions():
    """Проверяет, что кэш работает независимо для нескольких функций."""

    @cache(depth=2)
    def square(x):
        square.call_count += 1
        return x * x

    @cache(depth=2)
    def double(x):
        double.call_count += 1
        return x * 2

    # Инициализируем счетчики вызовов
    square.call_count = 0
    double.call_count = 0

    # Вызываем обе функции с одинаковыми аргументами
    square(3)
    square(3)
    assert square.call_count == 1  # Должен быть один вызов функции square

    double(3)
    double(3)
    assert double.call_count == 1  # Должен быть один вызов функции double

    # Проверка независимости кэша
    assert square.call_count == 1
    assert double.call_count == 1


def test_cache_with_kwargs():
    """Проверяет, что кэширование работает корректно с аргументами-ключевыми словами."""

    @cache(depth=2)
    def slow_function(x, power=2):
        slow_function.call_count += 1
        return x**power

    # Инициализируем счетчик вызовов
    slow_function.call_count = 0

    assert slow_function(3, power=2) == 9
    assert slow_function(3, power=2) == 9
    assert slow_function.call_count == 1  # Второй вызов должен использовать кэш

    # Новый вызов с другим значением ключевого аргумента
    assert slow_function(3, power=3) == 27
    assert slow_function.call_count == 2  # Должен быть вызов функции
