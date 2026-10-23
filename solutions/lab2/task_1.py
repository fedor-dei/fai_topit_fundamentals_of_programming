a = 10
b = a

print(a, b)
print(id(a), id(b))

a += 1

print(a, b)
print(id(a), id(b))

first = [10, 20]
second = first

print(first, second)
print(id(first), id(second))

second.append(30)

print(first, second)
print(id(first), id(second))

second = list(first)
print(first == second)
print(first is second)
second.append(40)
print(first == second)
print(first is second)
print(first, second)

import copy


config_1 = {
    "название": "Проект 'Анализ данных'",
    "участники": ["Алиса", "Борис"],
    "параметры_запуска": [["--verbose", "--log-level=INFO"], ["--port=8080"]]
}

print("\n нежелательное совместное изменение")

config_2 = config_1

print("\nДо изменений")
print(f"Конфигурация 1: {config_1}")
print(f"Конфигурация 2: {config_2}")
print(f"Это один и тот же объект?: {config_1 is config_2}")

config_2["участники"].append("Виктор")
config_2["параметры_запуска"][0].append("--debug")

print("\n После изменений в Конфигурации 2")
print(f"Конфигурация 1: {config_1}")
print(f"Конфигурация 2: {config_2}")
print("Изменилась и первая, и вторая конфигурация")


print("\n действительно независимая конфигурация")

config_2 = copy.deepcopy(config_1)

print("\nДо изменений")
print(f"Конфигурация 1: {config_1}")
print(f"Конфигурация 2: {config_2}")
print(f"Это один и тот же объект? (is): {config_1 is config_2}")

config_2["участники"].append("Галина")
config_2["параметры_запуска"][1].append("--timeout=60")

print("\nПосле изменений в Конфигурации 2")
print(f"Конфигурация 1: {config_1}")
print(f"Конфигурация 2: {config_2}")

assert config_1["участники"] != config_2["участники"], "Ошибка: списки участников не должны совпадать"
assert id(config_1["параметры_запуска"]) != id(config_2["параметры_запуска"]), "Ошибка: ID вложенных списков должны различаться"
assert config_1 is not config_2, "Ошибка: сами словари не должны быть одним объектом"

print("\n Конфигурации полностью независимы")


print("""
1. При простом присваивании (=):
   - Общие: сама конфигурация, список участников 
     и вложенные списки параметров запуска. 
   - Python скопировал только «ссылку» на объект. Все элементы 
     остались теми же самыми объектами в памяти, поэтому изменение 
     в одной переменной затрагивало другую.

2. При использовании copy.deepcopy():
   - Независимые: сконфигурация и все вложенные 
     в него объекты.
   - Функция обошла всю структуру и создала новые копии 
     для каждого элемента, разорвав связи с исходными объектами в памяти.
""")