import copy

original = [
    ["Python", 5],
    ["Algorithms", 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

print(original)
print(alias)
print(shallow)
print(deep)

def show(stage):
    print(f"{stage}")
    print("original: ", original, "| id:", id(original))
    print("alias: ", alias, "| id:", id(alias))
    print("shallow: ", shallow, "| id:", id(shallow))
    print("deep: ", deep, "| id:", id(deep))
    print()

    print("id(original[0]): ", id(original[0]))
    print("id(alias[0]): ", id(alias[0]))
    print("id(shallow[0]): ", id(shallow[0]))
    print("id(deep[0]): ", id(deep[0]))
    print()

    print("id(original[0][1]):", id(original[0][1]))
    print("id(alias[0][1]): ", id(alias[0][1]))
    print("id(shallow[0][1]): ", id(shallow[0][1]))
    print("id(deep[0][1]): ", id(deep[0][1]))
    print()


show("Начальное состояние")

original.append(["Databases", 5])
show("После original.append(['Databases', 5])")

original[0][1] = 3
show("После original[0][1] = 3")

wrong_matrix = [[0] * 3] * 3
wrong_matrix[0][0] = 1
print(wrong_matrix)
print("id строк:", id(wrong_matrix[0]), id(wrong_matrix[1]), id(wrong_matrix[2]))

correct_matrix = [[0] * 3 for _ in range(3)]
print(correct_matrix)
correct_matrix[0][0] = 1
print(correct_matrix)