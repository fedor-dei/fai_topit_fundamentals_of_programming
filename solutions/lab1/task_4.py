student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10
print(student[0], student[-1])
print(student[:4], student[5:])
print(student.upper(), student.lower())
print(student[0] + "." + student[5] + ".")
print(course[::-1])
print(f"{student} - {course}: {completed}/{total} ({completed / total * 100:.1f}%)")
print("%s — %s: %d/%d (%.1f%%)" % (student, course, completed, total, completed / total * 100))
print("{} — {}: {}/{} ({}%)".format(student, course, completed, total, completed / total * 100))

symbol = "Я"
print(symbol)
print(ord(symbol))
print(chr(ord(symbol)))
print(symbol.encode("utf-8"))
print(len(symbol.encode("utf-8")))
# student[0] = "x"