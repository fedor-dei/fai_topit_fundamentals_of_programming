from collections.abc import Iterable, Iterator
from collections import deque
import tracemalloc
from typing import TypeVar, Callable

def sum_with_list(n):
    values = [float(i) for i in range(n)]
    return sum(values)


def sum_with_generator(n):
    values = (float(i) for i in range(n))
    return sum(values)

def measure_memory(func: Callable[[int], float], n: int) -> tuple[float, int]:
    """Измеряет результат работы функции и пиковую память."""
    tracemalloc.start()

    try:
        result = func(n)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return result, peak


def read_measurements(lines: Iterable[str]) -> Iterator[float]:
    """Преобразует непустые строки в вещественные числа."""
    for line in lines:
        line = line.strip()
        if line:
            yield float(line)


def filter_range(values: Iterable[float], minimum: float, maximum: float ) -> Iterator[float]:
    """Пропускает только значения из закрытого диапазона."""
    for value in values:
        if minimum <= value <= maximum:
            yield value


def moving_average(values: Iterable[float], window_size: int) -> Iterator[float]:
    """Выдает скользящее среднее для заданного размера окна."""
    if window_size <= 0:
        raise ValueError("Размер окна должен быть положительным")

    window = deque(maxlen=window_size)
    total = 0.0

    for value in values:
        if len(window) == window_size:
            total -= window[0]

        window.append(value)
        total += value

        if len(window) == window_size:
            yield total / window_size


def process_measurements(
    lines: Iterable[str],
    minimum: float,
    maximum: float,
    window_size: int
) -> Iterator[float]:
    measurements = read_measurements(lines)
    filtered = filter_range(measurements, minimum, maximum)
    averages = moving_average(filtered, window_size)

    yield from averages


def lazy_pipeline_sum(n: int) -> float:
    """Обрабатывает n измерений через ленивый конвейер."""
    lines = (str(i % 100) for i in range(n))

    return sum(
        process_measurements(
            lines,
            minimum=10.0,
            maximum=50.0,
            window_size=5
        )
    )


def eager_pipeline_sum(n: int) -> float:
    """Обрабатывает n измерений, создавая списки на каждом этапе."""
    lines = (str(i % 100) for i in range(n))

    # Первый этап: список чисел
    numbers = [float(line) for line in lines]

    # Второй этап: новый список после фильтрации
    filtered = [
        value for value in numbers
        if 10.0 <= value <= 50.0
    ]

    # Третий этап: список скользящих средних
    window = deque(maxlen=5)
    total = 0.0
    averages = []

    for value in filtered:
        if len(window) == 5:
            total -= window[0]

        window.append(value)
        total += value

        if len(window) == 5:
            averages.append(total / 5)

    return sum(averages)


T = TypeVar("T")


def take(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Возвращает не более n первых элементов итерируемого объекта."""
    if n <= 0:
        return

    iterator = iter(iterable)
    count = 0

    while count < n:
        try:
            value = next(iterator)
        except StopIteration:
            return

        yield value
        count += 1


def drop(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Пропускает первые n элементов и выдает остальные."""
    iterator = iter(iterable)
    skipped = 0

    while skipped < n:
        try:
            next(iterator)
        except StopIteration:
            return

        skipped += 1

    yield from iterator


def batch(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Разбивает итерируемый объект на пакеты заданного размера."""
    if size <= 0:
        raise ValueError("Размер пакета должен быть положительным")

    current_batch = []

    for value in iterable:
        current_batch.append(value)

        if len(current_batch) == size:
            yield current_batch
            current_batch = []

    if current_batch:
        yield current_batch


if __name__ == "__main__":
    raw_lines = ["10.0", "", "12.5", "100.0", "11.5", "13.0", "9.5"]
    measurements = read_measurements(raw_lines)
    for value in measurements:
        print(value)

    #check for generator type
    measurements = read_measurements(raw_lines)
    print(type(measurements))

    #filter values
    filtered = filter_range(measurements, 10.0, 15.0)

    print(list(filtered))

    # checking moving_average
    measurements = [10.0, 12.0, 14.0, 16.0, 18.0]
    averages = moving_average(measurements, 3)

    print(list(averages))
    print(list(moving_average([10, 20, 30, 40], 2)))

    lines = ["10", "20", "100", "30", "", "40", "5", "50"]

    result = process_measurements(
        lines,
        minimum=10,
        maximum=50,
        window_size=2
    )

    print(list(result))

    # tracemalloc checks
    n = 100000

    list_result, list_peak = measure_memory(sum_with_list, n)
    generator_result, generator_peak = measure_memory(sum_with_generator, n)

    print("Сумма списка:", list_result)
    print("Пиковая память списка:", list_peak / 1024, "КБ")

    print("Сумма генератора:", generator_result)
    print("Пиковая память генератора:", generator_peak / 1024, "КБ")

    #final test
    lines = [
        "10",
        "20",
        "100",
        "30",
        "",
        "40",
        "5",
        "50"
    ]

    result = process_measurements(
        lines,
        minimum=10,
        maximum=50,
        window_size=2
    )

    for value in result:
        print(value)
    # empty
    print(list(process_measurements([], 10, 50, 2)))
    # every filtered
    print(list(process_measurements(["100", "200"], 10, 50, 2)))
    # less, than window size
    print(list(process_measurements(["10", "20"], 10, 50, 3)))

    # generator exhaustion
    raw_lines = ["10.0", "", "12.5", "100.0", "11.5", "13.0", "9.5"]

    pipeline = process_measurements(
        raw_lines,
        minimum=10.0,
        maximum=50.0,
        window_size=2
    )
    print(next(pipeline))
    print(next(pipeline))
    remaining = list(pipeline)
    print(remaining)
    print(list(pipeline))

    new_pipeline = process_measurements(
        raw_lines,
        minimum=10.0,
        maximum=50.0,
        window_size=2
    )
    print(list(new_pipeline))


    even_squares = [
        number ** 2 for number in range(1, 21) if number % 2 == 0
    ]

    print(even_squares)

    # set comprehension
    words = ["Python", "", "iterator", "code", "Python"]
    lengths = {len(word) for word in words if word}
    print(lengths)

    # dict comprehension
    squares_dict = {
        number: number ** 2
        for number in range(1, 11)
    }
    print(squares_dict)

    # generator expression
    sum_of_squares = sum(
        number ** 2 for number in range(1, 1_000_001)
    )
    print(sum_of_squares)

    # take
    numbers = [10, 20, 30, 40, 50]

    print(list(take(3, numbers)))
    print(list(take(10, numbers)))
    print(list(take(0, numbers)))

    squares = (number ** 2 for number in range(10))
    print(list(take(4, squares)))

    # drop
    numbers = [10, 20, 30, 40, 50]

    print(list(drop(2, numbers)))
    print(list(drop(0, numbers)))
    print(list(drop(10, numbers)))

    squares = (number ** 2 for number in range(6))
    print(list(drop(3, squares)))

    # batch
    numbers = [10, 20, 30, 40, 50]

    print(list(batch(numbers, 2)))
    print(list(batch(numbers, 3)))
    print(list(batch(numbers, 10)))

    squares = (number ** 2 for number in range(7))
    print(list(batch(squares, 3)))


    extended_lines = [
        "10.0",
        "",
        "12.5",
        "100.0",
        "11.5",
        "13.0",
        "9.5",
        "14.0",
        "15.5",
        "8.0",
        "16.0"
    ]


    pipeline = process_measurements(
        extended_lines,
        minimum=10.0,
        maximum=50.0,
        window_size=2
    )

    selected = take(4, drop(1, pipeline))

    packages = batch(selected, 2)

    print(list(packages))

    # memory comparison
    n = 100_000

    lazy_result, lazy_peak = measure_memory(lazy_pipeline_sum, n)
    eager_result, eager_peak = measure_memory(eager_pipeline_sum, n)

    print("Результат ленивого конвейера:", lazy_result)
    print("Память ленивого конвейера:", lazy_peak / 1024, "КБ")

    print("Результат конвейера со списками:", eager_result)
    print("Память конвейера со списками:", eager_peak / 1024, "КБ")

    print("Результаты совпадают:", lazy_result == eager_result)