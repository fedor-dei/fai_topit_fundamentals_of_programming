"""
Программа для обработки данных эксперимента.
Запрашивает параметры у пользователя, вычисляет общее время,
комплексный коэффициент и выводит итоговую карточку.
"""

name = input("Имя пользователя: ")
experiment = input("Название эксперимента: ")
launches = int(input("Кол-во запусков: "))
launch_in_seconds = float(input("длительность запуска в секундах: "))
coefficient_real = float(input("действительная часть комплексного коэффициента: "))
coefficient_imag = float(input("мнимая часть комплексного коэффициента: "))
coefficient = complex(coefficient_real, coefficient_imag)
full_time_sec = launches * launch_in_seconds
full_time_min = full_time_sec / 60.0
has_runs = bool(launches)
coefficient_squared = coefficient_real ** 2 + coefficient_imag ** 2

print("========================================")
print(f"ЭКСПЕРИМЕНТ: {experiment}")
print(f"Исследователь: {name}")
print(f"Запуски: {launches}")
print(f"Общее время: {full_time_sec:.2f} с ({full_time_min:.2f} мин)")
print(f"Коэффициент: {coefficient}")
print(f"Квадрат модуля: {coefficient_squared}")
print(f"Есть выполненные запуски: {has_runs}")
print("========================================")

print(f"Типы данных: \n{type(name)},\n"
      f"{type(experiment)},\n"
      f"{type(launches)},\n"
      f"{type(launch_in_seconds)},\n"
      f"{type(coefficient_real)},\n"
      f"{type(coefficient_imag)}\n")