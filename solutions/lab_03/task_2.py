measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]
target = int(input())
def Solve(measurements, target):
    summ = 0
    gt_avg_count = 0
    min_ = measurements[0]
    even = 0
    max_ = measurements[0]
    for i in range(len(measurements)):
        summ += measurements[i]

    found_index = -1
    for i in range(len(measurements)):
        if measurements[i] == target:
            found_index = i
            break

    avg = summ / len(measurements)
    for i in range(len(measurements)):
        if measurements[i] < min_:
            min_ = measurements[i]
        if measurements[i] > max_:
            max_ = measurements[i]
        if measurements[i] % 2 == 0:
            even += 1
        if measurements[i] > avg:
            gt_avg_count += 1
    return summ, min_, max_,  even, gt_avg_count, found_index



def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d**2 <= n:
        if n % d == 0:
            return False
        d += 2
    return True


import random # исключение, чтобы не писать вручную список из 100 элементов


def selection_sort(arr):
    """Возвращает новый отсортированный список, исходный не меняет."""
    a = list(arr)
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def linear_search(arr, target):
    comparisons = 0
    for i, x in enumerate(arr):
        comparisons += 1
        if x == target:
            return i, comparisons
    return -1, comparisons


def binary_search(arr, target):
    """arr должен быть отсортирован. Возвращает (индекс, число сравнений)."""
    comparisons = 0
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comparisons


def show():
    print("=== Проверка простоты ===")
    for n in [0, 1, 2, 3, 4, 9, 17, 25, 29, 97, 100, 1001]:
        if is_prime(n):
            print(f"{n} простое")
        else:
            print(f"{n} не простое")

    print("\n=== Поиск элемента ===")
    print(f"n | {'линейный':>10} | {'бинарный':>10}")
    print("-" * 34)
    for n in [10, 100, 1000]:
        data = [random.randint(1, 10_000) for _ in range(n)]
        s = selection_sort(data)
        target = data[n // 2]
        _, lin = linear_search(data, target)
        _, bin_ = binary_search(s, target)
        print(f"{n:>5} | {lin:>10} | {bin_:>10}")

print(Solve(measurements, target))
show()