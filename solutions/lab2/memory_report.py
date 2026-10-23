import sys
import tracemalloc


def main():
    report_data = []

    def measure(name, n_elements, factory):
        """Измеряет размер внешнего объекта и память, выделяемую при его создании."""
        obj = factory()
        ext_size = sys.getsizeof(obj)

        tracemalloc.start()
        obj2 = factory()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        report_data.append({
            "scenario": name,
            "elements": n_elements,
            "ext_size": ext_size,
            "current_mem": current_mem,
            "peak_mem": peak_mem
        })

    # 1. Измерения для базовых типов и небольших коллекций
    measure("Пустой список", 0, lambda: [])
    measure("Список из 10 целых чисел", 10, lambda: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    measure("Кортеж из 10 целых чисел", 10, lambda: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    measure("Строка из 10 символов", 10, lambda: "1234567890")
    measure("Целое число", 1, lambda: 10)
    measure("Объект None", 1, lambda: None)

    # 2. Измерение динамического роста списка (добавление 100 элементов)
    my_list = []
    prev_size = sys.getsizeof(my_list)
    tracemalloc.start()
    for i in range(100):
        my_list.append(i)
        current_size = sys.getsizeof(my_list)
        if current_size != prev_size:
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            report_data.append({
                "scenario": f"Рост списка (длина {len(my_list)})",
                "elements": len(my_list),
                "ext_size": current_size,
                "current_mem": current_mem,
                "peak_mem": peak_mem
            })
            prev_size = current_size
    tracemalloc.stop()

    # 3. Сравнение сценариев для большого количества элементов (100_000)
    # Вариант 1: list(range(100_000))
    tracemalloc.start()
    numbers = list(range(100000))
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    report_data.append({
        "scenario": "list(range(100_000))",
        "elements": 100000,
        "ext_size": sys.getsizeof(numbers),
        "current_mem": current_mem,
        "peak_mem": peak_mem
    })
    peak_list = peak_mem

    # Вариант 2: range(100_000)
    tracemalloc.start()
    numbers_1 = range(100000)
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    report_data.append({
        "scenario": "range(100_000)",
        "elements": 100000,
        "ext_size": sys.getsizeof(numbers_1),
        "current_mem": current_mem,
        "peak_mem": peak_mem
    })
    peak_range = peak_mem

    if peak_range > 0:
        peak_ratio = peak_list / peak_range
    else:
        peak_ratio = float('inf')


    header = (
        f"{'Название сценария':<35} | "
        f"{'Элементов':>9} | "
        f"{'Размер объекта (байт)':>21} | "
        f"{'Текущая (KB)':>12} | "
        f"{'Пиковая (KB)':>12}"
    )

    print(header)
    print("-" * len(header))

    for row in report_data:
        print(
            f"{row['scenario']:<35} | "
            f"{row['elements']:>9} | "
            f"{row['ext_size']:>21} | "
            f"{row['current_mem'] / 1024:>12.2f} | "
            f"{row['peak_mem'] / 1024:>12.2f}"
        )

    print("-" * len(header))
    print(f"Отношение пикового объема (list vs range): {peak_ratio:.2f}")


if __name__ == "__main__":
    main()