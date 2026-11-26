def sequential_search(iterable, target):
    """Ищет значение последовательным перебором."""
    checks = 0

    for value in iterable:
        checks += 1

        if value == target:
            return True, checks

    return False, checks



class StepRange:
    def __init__(self, start: int, stop: int, step: int):
        if step == 0:
            raise ValueError("шаг не должен быть равен нулю")
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self) -> "StepRangeIterator":
        return StepRangeIterator(self.start, self.stop, self.step)

    def __len__(self):
        if self.step > 0:
            if self.start >= self.stop:
                return 0
            return (self.stop - self.start + self.step - 1) // self.step
        else:
            if self.start <= self.stop:
                return 0
            return (self.start - self.stop - self.step - 1) // (-self.step)

    def __contains__(self, value: int) -> bool:
        """Проверяет принадлежность числа последовательности."""

        if not isinstance(value, int):
            return False

        if self.step > 0:
            return self.start <= value < self.stop and (value - self.start) % self.step == 0

        return self.stop < value <= self.start and (value - self.start) % self.step == 0

    def __repr__(self) -> str:
        """Возвращает однозначное представление объекта."""
        return f"StepRange({self.start}, {self.stop}, {self.step})"




class StepRangeIterator:
    """Выполняет последовательный обход StepRange."""
    def __init__(self, start: int, stop: int, step: int):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration
        elif self.step < 0 and self.current <= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value



if __name__ == "__main__":
    # 2 iterators
    numbers = StepRange(2, 11, 3)
    print(list(numbers))
    iterator_a = iter(numbers)
    iterator_b = iter(numbers)

    numbers = StepRange(2, 11, 3)
    print(len(numbers))

    print(next(iterator_a))
    print(next(iterator_b))
    print(next(iterator_a))
    print(next(iterator_b))
    print(next(iterator_a))
    print(next(iterator_b))

    print("A:", iterator_a.current)
    print("B:", iterator_b.current)
    print(iterator_a is iterator_b)

    # creating a list through __iter__
    numbers = StepRange(2, 11, 3)
    print(list(StepRange(0, 5, 1)))
    print(list(StepRange(5, 0, -1)))
    print(list(StepRange(0, 0, 1)))
    print(list(StepRange(0, 5, -1)))

    # length of a list through __len__
    print(len(StepRange(2, 11, 3)))
    print(len(StepRange(0, 5, 1)))
    print(len(StepRange(5, 0, -1)))
    print(len(StepRange(0, 0, 1)))

    # using __contains__ to find numbers
    numbers = StepRange(2, 11, 3)

    print(2 in numbers)
    print(5 in numbers)
    print(8 in numbers)
    print(6 in numbers)
    print(11 in numbers) # expected False

    # using __repr__ to represent itself
    print(repr(numbers))
    print([numbers])




    numbers = StepRange(0, 1000000, 1)

    target = 999999

    print(target in numbers) # True

    print(target in numbers)

    print(sequential_search(numbers, target))