import sys
import weakref

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))


class Record:
    pass


record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())


class Record:
    """Простой класс для демонстрации объектов в реестре."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Record('{self.name}')"


def check_registry(registry, step_name):
    """Вспомогательная функция для вывода текущего состояния реестра."""
    print(f"[{step_name}]")
    if registry:
        print(f"Записи в реестре: {list(registry.items())}")
    else:
        print("Реестр пуст.")


registry = weakref.WeakValueDictionary()

print("=== ЭТАП 1: Создание объектов и регистрация ===")
r1 = Record("Объект 1")
r2 = Record("Объект 2")

registry['rec1'] = r1
registry['rec2'] = r2
registry['rec3'] = Record("Объект 3")

check_registry(registry, "Сразу после регистрации")

print("\n=== ЭТАП 2: Удаление сильной ссылки ===")
del r2

check_registry(registry, "После удаления r2")

print("\n=== ЭТАП 3: Удаление последней сильной ссылки ===")
del r1

check_registry(registry, "После удаления r1")