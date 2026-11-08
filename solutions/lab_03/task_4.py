def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое непустого списка."""
    if not values:
        return 0.0

    return sum(values) / len(values)


def normalize_name(name: str) -> str:
    """Удаляет лишние пробелы и приводит каждую часть имени к нужному регистру."""
    if isinstance(name, str) and name.strip():
        return " ".join(part.capitalize() for part in name.split())
    return ""


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    """Формирует строковый отчет о результатах студента."""
    if not student.strip() or not results:
        return ""

    if precision < 0:
        return ""

    mean = arithmetic_mean(results)

    return (
        f"{prefix}: {normalize_name(student)}. "
        f"Средний балл: {mean:.{precision}f}"
    )


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    if not tags:
        return ()

    result = []

    for tag in tags:
        cleaned = tag.strip()

        if lowercase:
            cleaned = cleaned.lower()

        if cleaned and cleaned not in result:
            result.append(cleaned)

    return tuple(result)


assert arithmetic_mean([2, 4, 6]) == 4.0
assert arithmetic_mean([5]) == 5.0
assert arithmetic_mean([]) == 0.0


assert normalize_name("  иВАН   пЕТРОВ  ") == "Иван Петров"
assert normalize_name("АННА СМИРНОВА") == "Анна Смирнова"
assert normalize_name("петр") == "Петр"
assert normalize_name("   ") == ""


assert build_report("иван петров", [4, 5, 3]) == (
    "Результат: Иван Петров. Средний балл: 4.00"
)

assert build_report(
    "анна иванова",
    [5, 4, 5],
    precision=1
) == "Результат: Анна Иванова. Средний балл: 4.7"

assert build_report(
    "петр сидоров",
    [3, 4, 5],
    prefix="Отчет",
    precision=0
) == "Отчет: Петр Сидоров. Средний балл: 4"

assert build_report("Иван", []) == ""


assert collect_tags("Python", "Java", "Python") == (
    "python", "java"
)

assert collect_tags("  Python ", "", " Java ") == (
    "python", "java"
)

assert collect_tags() == ()


print(arithmetic_mean([4, 5, 3]))
print(normalize_name("  иВАН   пЕТРОВ "))
print(build_report("Иван Петров", [5, 4, 5]))
print(collect_tags("Python", "Java", "Python"))


print(build_report(
    student="Анна Смирнова",
    results=[5, 5, 4],
    precision=1,
    prefix="Итог"
))

print(collect_tags(
    "Python",
    "Java",
    lowercase=False
))


report_data = {
    "student": "Мария Иванова",
    "results": [5, 4, 5],
    "precision": 1,
    "prefix": "Успеваемость"
}

print(build_report(**report_data))




course = "глобальный" # глобальная область видимости


def outer_func():
    course_name = "внешний" # объемлющая область видимости

    def inner_func():
        nonlocal course_name

        course_name = "внутренний"
        print("Внутренняя функция:", course_name)

    inner_func()

    print("Внешняя функция:", course_name)


outer_func()

print("Глобальная переменная:", course)


def add_result(value, results=None):
    if results is None:
        results = []
    results.append(value)
    return results


def apply_to_results(operation, values):
    return [operation(value) for value in values]


def add_five(result):
    return result + 5


def make_threshold_checker(threshold):
    def check_result(result):
        return result >= threshold

    return check_result


results = [40, 60, 80]

print(apply_to_results(add_five, results)) # передаётся сама функция, а не результат

print(apply_to_results(lambda result: result * 2, results))

check_50 = make_threshold_checker(50)
check_80 = make_threshold_checker(80)

print([check_50(value) for value in results])
print([check_80(value) for value in results])