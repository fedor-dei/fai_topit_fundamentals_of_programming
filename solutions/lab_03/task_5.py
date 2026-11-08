
students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}


def mean(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def min_(values):
    if not values:
        return None

    result = values[0]

    for value in values:
        if value < result:
            result = value

    return result


def max_(values):
    if not values:
        return None

    result = values[0]

    for value in values:
        if value > result:
            result = value

    return result


def classify(score):
    if score is None:
        return "Нет результатов"
    elif score >= 90:
        return "Отлично"
    elif score >= 75:
        return "Хорошо"
    elif score >= 60:
        return "Удовлетворительно"
    else:
        return "Недостаточно"


def student_summary(name, results):
    average = mean(results)

    return {
        "name": name,
        "results": list(results),
        "count": len(results),
        "mean": average,
        "minimum": min_(results),
        "maximum": max_(results),
        "category": classify(average if results else None),
    }


def group_summary(students):
    all_results = []

    categories = {
        "Отлично": 0,
        "Хорошо": 0,
        "Удовлетворительно": 0,
        "Недостаточно": 0,
        "Нет результатов": 0,
    }

    for name, results in students.items():
        all_results.extend(results)

        summary = student_summary(name, results)
        category = summary["category"]
        categories[category] += 1

    return {
        "students_count": len(students),
        "results_count": len(all_results),
        "mean": mean(all_results),
        "minimum": min_(all_results),
        "maximum": max_(all_results),
        "category_counts": categories,
    }


def find_top_students(students):
    averages = {}

    for name, results in students.items():
        if results:
            averages[name] = mean(results)

    if not averages:
        return []

    highest = max_(list(averages.values()))

    return [name for name, average in averages.items() if average == highest]


def format_report(student_data, group_data):
    lines = []


    lines.append("РЕЗУЛЬТАТЫ СТУДЕНТОВ:")

    for student in student_data:
        lines.append(f"\nСтудент: {student['name']}")
        lines.append(f"  Результаты: {student['results']}")
        lines.append(f"  Количество: {student['count']}")
        lines.append(f"  Среднее: {student['mean']:.2f}")
        lines.append(f"  Минимум: {student['minimum']}")
        lines.append(f"  Максимум: {student['maximum']}")
        lines.append(f"  Категория: {student['category']}")

    lines.append("\nСТАТИСТИКА ГРУППЫ:")
    lines.append(f"  Количество студентов: {group_data['students_count']}")
    lines.append(f"  Количество результатов: {group_data['results_count']}")
    lines.append(f"  Среднее по группе: {group_data['mean']:.2f}")
    lines.append(f"  Минимум: {group_data['minimum']}")
    lines.append(f"  Максимум: {group_data['maximum']}")

    lines.append("\nКОЛИЧЕСТВО СТУДЕНТОВ ПО КАТЕГОРИЯМ:")

    for category, count in group_data["category_counts"].items():
        lines.append(f"  {category}: {count}")

    students = {
        student["name"]: student["results"]
        for student in student_data
    }

    top_students = find_top_students(students)

    lines.append("\nЛИДЕРЫ ГРУППЫ:")
    lines.append(", ".join(top_students) if top_students else "Нет лидеров")

    rating = sorted(
        student_data,
        key=lambda student: (
            student["count"] > 0,
            student["mean"]
        ),
        reverse=True
    )

    lines.append("\nРЕЙТИНГ СТУДЕНТОВ:")

    for position, student in enumerate(rating, start=1):
        if student["count"] > 0:
            lines.append(
                f"  {position}. {student['name']} "
                f"— {student['mean']:.2f}"
            )
        else:
            lines.append(
                f"  {position}. {student['name']} — нет результатов"
            )

    return "\n".join(lines)


student_data = []

for name, results in students.items():
    student_data.append(
        student_summary(name, results)
    )

group_data = group_summary(students)

report = format_report(student_data, group_data)

print(report)



def test_scenarios():
    # Сценарий 1. Обычный набор данных
    data = {
        "Анна": [78, 91, 84, 88],
        "Борис": [60, 72, 68],
        "Дарья": [95, 93, 97, 90],
        "Илья": [55, 61],
    }

    original = {
        name: results.copy()
        for name, results in data.items()
    }

    summaries = [
        student_summary(name, results)
        for name, results in data.items()
    ]

    group = group_summary(data)

    assert len(summaries) == 4
    assert summaries[0]["mean"] == 85.25
    assert group["students_count"] == 4
    assert group["results_count"] == 13
    assert round(group["mean"], 2) == 79.38
    assert find_top_students(data) == ["Дарья"]

    assert data == original

    # Сценарий 2. Один студент
    one_student = {
        "Оля": [80, 100]
    }

    assert find_top_students(one_student) == ["Оля"]
    assert group_summary(one_student)["mean"] == 90.0

    # Сценарий 3. Несколько лидеров
    several_leaders = {
        "Анна": [80, 100],
        "Борис": [90],
        "Дарья": [70, 80],
    }

    assert set(find_top_students(several_leaders)) == {
        "Анна", "Борис"
    }

    # Сценарий 4. Пустая группа
    empty_group = {}

    empty_stats = group_summary(empty_group)

    assert empty_stats["students_count"] == 0
    assert empty_stats["results_count"] == 0
    assert empty_stats["mean"] == 0.0
    assert empty_stats["minimum"] is None
    assert empty_stats["maximum"] is None
    assert find_top_students(empty_group) == []

    # Сценарий 5. Студент без результатов
    data_with_empty = {
        "Анна": [],
        "Борис": [70, 80],
    }

    empty_student = student_summary("Анна", [])

    assert empty_student["mean"] == 0.0
    assert empty_student["minimum"] is None
    assert empty_student["maximum"] is None
    assert empty_student["category"] == "Нет результатов"

    assert find_top_students(data_with_empty) == ["Борис"]

    categories = group_summary(data_with_empty)["category_counts"]
    assert categories["Нет результатов"] == 1

    # Сценарий 6. Граничные значения категорий
    assert classify(59.99) == "Недостаточно"
    assert classify(60) == "Удовлетворительно"
    assert classify(74.99) == "Удовлетворительно"
    assert classify(75) == "Хорошо"
    assert classify(89.99) == "Хорошо"
    assert classify(90) == "Отлично"
    assert classify(None) == "Нет результатов"

    print("Все сценарии пройдены")

test_scenarios()


