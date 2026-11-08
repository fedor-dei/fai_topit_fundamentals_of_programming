submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]



students = set()
labs = set()
attempts = {}
best = {}
counts = {}

for student, lab, res in submissions:
    students.add(student)
    labs.add(lab)

    if student not in attempts:
        attempts[student] = []
    attempts[student].append((lab, res))

    key = (student, lab)

    if key not in best or best[key] < res:
        best[key] = res

    counts[key] = counts.get(key, 0) + 1

# ---- добавляем новую запись инкрементально ----
new_submission = ("daria", "lab_02", 5)
student, lab, res = new_submission

students.add(student)
labs.add(lab)
attempts.setdefault(student, []).append((lab, res))

print("Студенты:", students)
print("Лабораторные работы:", labs)
print("Попытки:", attempts)
print("Лучшие результаты:", best)
print("Количество попыток:", counts)

lab1 = {student for student, lab, _ in submissions if lab == "lab_01"}
lab2 = {student for student, lab, _ in submissions if lab == "lab_02"}
both_labs =  lab1 & lab2
print(both_labs)


def Show(command):
    if not command:
        print("Пустая команда")

    elif command[0] == "student":
        if len(command) < 2:
            print("Ошибка: не указан студент")
        else:
            student = command[1]

            if student in attempts:
                print(f"Попытки студента {student}: {attempts[student]}")
            else:
                print(f"Студент {student} не найден")

    elif command[0] == "best":
        if len(command) < 3:
            print("Ошибка: не указаны студент или лабораторная работа")
        else:
            student, lab = command[1], command[2]
            key = (student, lab)

            if key in best:
                print(f"Лучший результат {student} по {lab}: {best[key]}")
            else:
                print("Данные не найдены")

    elif command[0] == "attempts":
        if len(command) < 3:
            print("Ошибка: не указаны студент или лабораторная работа")
        else:
            student, lab = command[1], command[2]
            key = (student, lab)

            if key in counts:
                print(f"Количество попыток {student} по {lab}: {counts[key]}")
            else:
                print("Данные не найдены")

    elif command[0] == "completed":
        if len(command) < 2:
            print("Ошибка: не указана лабораторная работа")
        else:
            lab = command[1]

            if lab not in labs:
                print(f"Лабораторная работа {lab} не найдена")
            else:
                completed = {
                    student
                    for student, current_lab, _ in submissions
                    if current_lab == lab
                }
                print(f"Выполнили {lab}: {completed}")

    else:
        print("Неизвестная команда:", command[0])



queries = [
    "student anna",
    "best anna lab_01",
    "attempts boris lab_02",
    "completed lab_01",
]

for query in queries:
    command = query.split()
    Show(command)