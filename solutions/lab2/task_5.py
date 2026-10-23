import sys
import tracemalloc

empty_list = []
list_of_ten = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tuple_of_ten = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
string_of_ten = "1234567890"
integer_obj = 10
none_obj = None

print(f"Пустой список: {sys.getsizeof(empty_list)} байт")
print(f"Список из десяти целых чисел: {sys.getsizeof(list_of_ten)} байт")
print(f"Кортеж с теми же значениями: {sys.getsizeof(tuple_of_ten)} байт")
print(f"Строка из десяти символов: {sys.getsizeof(string_of_ten)} байт")
print(f"Целое число: {sys.getsizeof(integer_obj)} байт")
print(f"Объект None: {sys.getsizeof(none_obj)} байт")

my_list = []
prev_size = sys.getsizeof(my_list)
for i in range(100):
    my_list.append(i)
    current_size = sys.getsizeof(my_list)
    if current_size != prev_size:
        print(f"Длина: {len(my_list):3d} | Размер: {current_size} байт")
        prev_size = current_size

tracemalloc.start()
numbers = list(range(100000))
current_mem, peak_mem = tracemalloc.get_traced_memory()

print("Вариант 1: list(range(100_000))")
print(f"Текущий объем памяти: {current_mem / 1024:.1f} KB")
print(f"Пиковый объем памяти: {peak_mem / 1024:.1f} KB")
tracemalloc.stop()

tracemalloc.start()
numbers_1 = range(100000)
current_mem, peak_mem = tracemalloc.get_traced_memory()
print("Вариант 2: range(100_000)")
print(f"Текущий объем памяти: {current_mem / 1024:.5f} KB")
print(f"Пиковый объем памяти: {peak_mem / 1024:.5f} KB")
tracemalloc.stop()