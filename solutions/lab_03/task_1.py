records = [
    (0,   "exam",     0),
    (59,  "exam",     0),
    (60,  "exam",     0),
    (74,  "exam",     0),
    (75,  "exam",     0),
    (89,  "exam",     0),
    (90,  "exam",     0),
    (100, "exam",     0),
    (90,  "exam",     4),
    (0,   "practice", 5),
    (80,  "unknown",  0),
]


def Process(score, work_type, absences):
    if score < 0 or score > 100:
        return "неправильный ввод", None

    if absences < 0 or absences > 5:
        return "неправильный ввод", None

    # Определение типа работы
    match work_type:
        case "exam":
            work_name = "экзаменационная работа"
        case "project":
            work_name = "проектная работа"
        case "practice":
            work_name = "практическая работа"
        case _:
            work_name = "неизвестный тип работы"

    # Определение уровня по score
    if 90 <= score <= 100:
        level = 4
    elif 75 <= score <= 89:
        level = 3
    elif 60 <= score <= 74:
        level = 2
    else:
        level = 0

    if absences > 3:
        level -= 1

    # Название уровня
    if level == 4:
        level = "отличный"
    elif level == 3:
        level = "хороший"
    elif level == 2:
        level = "удовлетворительный"
    else:
        level = "недостаточный"

    result = (work_name, "; уровень: ", level)
    return result, level


counts = {
    "отличный": 0,
    "хороший": 0,
    "удовлетворительный": 0,
    "недостаточный": 0,
}

result_lines = []

for i, (score, work_type, absences) in enumerate(records, start=1):
    result, level = Process(score, work_type, absences)

    line = (
        f"{i}) score={score}, work_type={work_type}, "
        f"absences={absences} -> {result}"
    )
    result_lines.append(line)

    if level:
        counts[level] += 1

print("\n".join(result_lines))

print("\nИтоговая сводка:")
for level in ["отличный", "хороший", "удовлетворительный", "недостаточный"]:
    print(level, ": ",counts[level])