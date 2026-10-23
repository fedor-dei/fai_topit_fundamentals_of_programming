import gc
import weakref
first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)
print("Включён ли сборщик мусора? -", gc.isenabled())
print("Пороги поколений (поколение 0, 1, 2):")
thresholds = gc.get_threshold()
print(thresholds)
stats = gc.get_stats()
print("Статистика сборки мусора по поколениям:")
print(stats, "\n")

id_first = id(first)
id_second = id(second)
print(f"Идентификатор first: {id_first}")
print(f"Идентификатор second: {id_second}")
del first, second
collected_count = gc.collect()
print(f"Сборщик мусора нашел и удалил объектов: {collected_count}\n")

gc.disable()
print("Включён ли сборщик мусора? -", gc.isenabled())

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None

# Структура 1: Два объекта, ссылающихся друг на друга
node1 = Node("A")
node2 = Node("B")
node1.link = node2
node2.link = node1
wr1 = weakref.ref(node1)
wr2 = weakref.ref(node2)

# Структура 2: Кольцо из трех объектов
node3 = Node("C")
node4 = Node("D")
node5 = Node("E")
node3.link = node4
node4.link = node5
node5.link = node3
wr3 = weakref.ref(node3)

# Структура 3: Объект, ссылающийся сам на себя
node6 = Node("F")
node6.link = node6
wr6 = weakref.ref(node6)

print("Создано 3 циклические структуры из объектов пользовательского класса.\n")

del node1, node2, node3, node4, node5, node6
print("Внешние переменные удалены (del).\n")

print("Проверка памяти ДО gc.collect():")
print(f"  Структура 1 (пара) в памяти? {wr1() is not None and wr2() is not None}")
print(f"  Структура 2 (кольцо) в памяти? {wr3() is not None}")
print(f"  Структура 3 (самоссылка) в памяти? {wr6() is not None}")

print("Запуск gc.collect()")
collected_count = gc.collect()
print(f"Удалено объектов: {collected_count}\n")

print("Проверка памяти ПОСЛЕ gc.collect():")
print(f"  Структура 1 (пара) в памяти? {wr1() is not None and wr2() is not None}")
print(f"  Структура 2 (кольцо) в памяти? {wr3() is not None}")
print(f"  Структура 3 (самоссылка) в памяти? {wr6() is not None}\n")

gc.collect()
gc.enable()


gc.disable()

count_before = len(gc.get_objects())
print(f"[1] Объектов в памяти до создания графа: {count_before}\n")

node1 = {'id': 1, 'data': [10, 20]}
node2 = {'id': 2, 'data': [30, 40]}
node3 = {'id': 3, 'data': [50, 60]}
node4 = {'id': 4, 'data': [70, 80], 'MARKER': 'independent'}

node1['next'] = [node2]
node2['next'] = [node3]
node3['next'] = [node1]

# 3. Выводим связи графа
print("[2] Связи графа:")
print(f"  node1 (id={node1['id']}) -> node2 (id={node2['id']})")
print(f"  node2 (id={node2['id']}) -> node3 (id={node3['id']})")
print(f"  node3 (id={node3['id']}) -> node1 (id={node1['id']})")
print(f"  node4 (id={node4['id']}) -> нет связей\n")

# Сохраняем id независимого узла для последующей проверки
independent_node_id = id(node4)

# 4. Удаляем внешние имена ТОЛЬКО циклических узлов
# node4 намеренно НЕ трогаем — он должен остаться доступным
del node1, node2, node3

# 5. Считаем объекты перед ручной сборкой
count_after_del = len(gc.get_objects())
print(f"[3] Объектов в памяти после del (до gc.collect): {count_after_del}")

# 6. Выполняем ручную сборку мусора
collected = gc.collect()
print(f"[4] gc.collect() собрал объектов: {collected}\n")

# 7. Считаем объекты после сборки
count_after_gc = len(gc.get_objects())
print(f"[5] Объектов в памяти после gc.collect(): {count_after_gc}")

# 8. Сравниваем число объектов до создания графа и после его удаления
diff = count_after_gc - count_before
print(f"\n[6] Разница (до - после): {diff}")
if abs(diff) <= 2:
    print("    -> циклы удалены.")
else:
    print("    -> Остались 'хвосты'.")

print("\n[7] Проверка независимого узла node4:")
found = False
for obj in gc.get_objects():
    if isinstance(obj, dict) and obj.get('MARKER') == 'independent':
        found = True
        print(f"    -> node4 жив, id={id(obj)} (сохранённый id: {independent_node_id})")
        print(f"    -> Содержимое: {obj}")
        break
if not found:
    print("    -> ОШИБКА: node4 не найден")

gc.enable()