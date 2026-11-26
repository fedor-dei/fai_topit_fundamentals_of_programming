from task_2 import StepRange


values = [10, 20, 30]
iterator = iter(values)

print(iterator is values)
print(iter(iterator) is iterator)
print(next(iterator))
print(next(iterator))
print(next(iterator))
# print(next(iterator))

def consume(iterable) -> list:
    """Собирает элементы iterable, вручную используя iter() и next()."""
    iterator = iter(iterable)
    result = []
    while True:
        try:
            item = next(iterator)
            result.append(item)
        except StopIteration:
            break
    return result

def my_enumerate(iterable, start=0):
    iterator = iter(iterable)
    index = start
    while True:
        try:
            item = next(iterator)
            yield (index, item)
            index += 1
        except StopIteration:
            break


def my_zip(first, second):
    first_iterator = iter(first)
    second_iterator = iter(second)
    while True:
        try:
            item_1 = next(first_iterator)
            item_2 = next(second_iterator)
            yield (item_1, item_2)
        except StopIteration:
            break


numbers = [10, 20, 30, 40]
enum_numbers = (x for x in range(1, 4))
enum_letters = (x for x in "ABC")
iterator = iter(numbers)
next(iterator)



if __name__ == "__main__":
    print(consume([1, 2, 3]))
    print(consume((4, 5, 6)))
    print(consume("Python"))
    print(consume(range(3)))
    print(consume(iterator))

    print(list(my_enumerate(["яблоко", "груша", "банан"])))
    print(list(my_enumerate("Python", start=1)))
    print(list(my_enumerate(enum_numbers, start=1)))

    print(list(my_zip([1, 2, 3], ["a", "b", "c"])))
    print(list(my_zip("ABC", "123")))
    print(list(my_zip([1, 2, 3, 4], ["a", "b"])))
    print(list(my_zip(enum_letters, range(3))))

    numbers = StepRange(2, 11, 3)
    print(list(my_enumerate(numbers)))

    numbers = StepRange(2, 11, 3)
    print(list(my_zip(numbers, ["a", "b", "c"])))