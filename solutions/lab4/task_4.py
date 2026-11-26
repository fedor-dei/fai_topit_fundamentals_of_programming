from dataclasses import dataclass
from collections.abc import Iterable, Iterator

@dataclass
class Submission:
    """Представляет попытку сдачи лабораторной работы студентом."""

    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ""

    def __post_init__(self) -> None:
        """Проверяет корректность данных после создания объекта."""

        if not self.student_id.strip():
            raise ValueError("Идентификатор студента не может быть пустым")

        if not self.laboratory_id.strip():
            raise ValueError("Идентификатор лабораторной работы не может быть пустым")

        if self.attempt <= 0:
            raise ValueError("Номер попытки должен быть положительным")

        if not 0 <= self.score <= 100:
            raise ValueError("Оценка должна находиться в диапазоне от 0 до 100")


class Student:
    """Представляет студента и его сданные лабораторные работы."""

    def __init__(self, student_id: str, full_name: str) -> None:
        """Создаёт студента с идентификатором и полным именем."""

        if not self.is_valid_student_id(student_id):
            raise ValueError("Некорректный идентификатор студента")

        if not full_name.strip():
            raise ValueError("Имя студента не может быть пустым")

        self.student_id = student_id.strip()
        self.full_name = full_name.strip()
        self._submissions: list[Submission] = []

    def add_submission(self, submission: Submission) -> None:
        """Добавляет работу студента."""
        if submission.student_id != self.student_id:
            raise ValueError("Работа принадлежит другому студенту")

        self._submissions.append(submission)

    @property
    def submissions(self) -> tuple[Submission, ...]:
        """Возвращает работы в виде неизменяемого кортежа."""
        return tuple(self._submissions)

    @property
    def average_score(self) -> float:
        """Возвращает средний балл по всем попыткам."""
        if not self._submissions:
            return 0.0

        total = sum(
            submission.score for submission in self._submissions
        )
        return total / len(self._submissions)

    def best_score(self, laboratory_id: str) -> float | None:
        """Возвращает лучший результат по указанной лабораторной."""
        scores = [
            submission.score
            for submission in self._submissions
            if submission.laboratory_id == laboratory_id
        ]

        if not scores:
            return None

        return max(scores)

    def __len__(self) -> int:
        """Возвращает количество попыток сдачи."""
        return len(self._submissions)

    def __iter__(self) -> Iterator[Submission]:
        """Возвращает итератор по работам студента."""
        return iter(self._submissions)

    def __str__(self) -> str:
        """Возвращает понятное человеку описание студента."""
        return (
            f"Студент: {self.full_name}, "
            f"ID: {self.student_id}, "
            f"попыток: {len(self)}"
        )

    def __repr__(self) -> str:
        """Возвращает подробное отладочное представление студента."""
        return (
            f"Student(student_id={self.student_id!r}, "
            f"full_name={self.full_name!r}, "
            f"submissions={self._submissions!r})"
        )

    @staticmethod
    def is_valid_student_id(student_id: str) -> bool:
        """Проверяет, что идентификатор не пустой."""
        return isinstance(student_id, str) and bool(student_id.strip())

    @classmethod
    def from_full_name(cls, student_id: str, full_name: str) -> "Student":
        """Создаёт студента по идентификатору и полному имени."""
        return cls(student_id, full_name)

    def get_sorted_submissions(self) -> tuple[Submission, ...]:
        """Возвращает работы, отсортированные по попытке и оценке."""
        return tuple(
            sorted(
                self._submissions,
                key=lambda submission: (
                    submission.attempt,
                    submission.score
                )
            )
        )


class Course:
    """Представляет учебный курс и зарегистрированных студентов."""

    def __init__(self) -> None:
        """Создаёт курс с пустым списком студентов."""
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        """Добавляет студента на курс."""
        if student.student_id in self._students:
            raise ValueError("Студент уже зарегистрирован")

        self._students[student.student_id] = student

    def get_student(self, student_id: str) -> Student:
        """Возвращает студента по идентификатору."""
        return self._students[student_id]

    def submit(self, submission: Submission) -> None:
        """Добавляет работу зарегистрированному студенту."""
        student = self.get_student(submission.student_id)
        student.add_submission(submission)

    def top_students(self, limit: int = 3) -> list[Student]:
        """Возвращает студентов с наибольшим средним баллом."""
        if limit < 0:
            raise ValueError("Количество студентов не может быть отрицательным")

        sorted_students = sorted(
            self._students.values(),
            key=lambda student: student.average_score,
            reverse=True
        )

        return sorted_students[:limit]

    def __contains__(self, student_id: object) -> bool:
        """Проверяет наличие студента на курсе по идентификатору."""
        return student_id in self._students

    def __len__(self) -> int:
        """Возвращает количество зарегистрированных студентов."""
        return len(self._students)

    def __iter__(self) -> Iterator[Student]:
        """Возвращает итератор по зарегистрированным студентам."""
        return iter(self._students.values())


if __name__ == "__main__":
    submission = Submission(
        student_id="ST001",
        laboratory_id="LAB04",
        attempt=1,
        score=95.0,
        comment="Хорошая работа"
    )

    print(submission)
    print(repr(submission))

    # bad_submission = Submission(
    #     student_id="ST001",
    #     laboratory_id="LAB04",
    #     attempt=1,
    #     score=120.0
    # )

    student = Student("ST001", "Иван Иванов")

    student.add_submission(
        Submission("ST001", "LAB04", 1, 75.0)
    )

    student.add_submission(
        Submission("ST001", "LAB04", 2, 95.0)
    )

    student.add_submission(
        Submission("ST001", "LAB03", 1, 85.0)
    )

    print(student)
    print(repr(student))

    print("Количество попыток:", len(student))
    print("Средний балл:", student.average_score)
    print("Лучший балл LAB04:", student.best_score("LAB04"))

    print("Работы студента:")
    for submission in student:
        print(submission)

    print("Кортеж работ:", student.submissions)

    # create student
    student = Student.from_full_name(
        "ST002",
        "Пётр Петров"
    )

    print(student)
    print(Student.is_valid_student_id("ST002"))
    print(Student.is_valid_student_id(""))

    try:
        invalid_student = Student("", "Иван Иванов")
    except ValueError as error:
        print(error)

    student = Student("ST001", "Иван Иванов")

    student.add_submission(
        Submission("ST001", "LAB04", 2, 95.0)
    )

    student.add_submission(
        Submission("ST001", "LAB04", 1, 75.0)
    )

    student.add_submission(
        Submission("ST001", "LAB03", 1, 85.0)
    )

    print("Исходный порядок:")
    for submission in student:
        print(submission)

    print("\nОтсортированный порядок:")
    for submission in student.get_sorted_submissions():
        print(submission)

    print("\nПовторно исходный порядок:")
    for submission in student:
        print(submission)


    # Course
    if __name__ == "__main__":
        course = Course()

        # Создаём студентов
        student1 = Student("ST001", "Иван Иванов")
        student2 = Student("ST002", "Пётр Петров")
        student3 = Student("ST003", "Анна Смирнова")

        # Регистрируем студентов
        course.add_student(student1)
        course.add_student(student2)
        course.add_student(student3)

        # Добавляем работы через Course
        course.submit(
            Submission("ST001", "LAB04", 1, 80.0)
        )

        course.submit(
            Submission("ST002", "LAB04", 1, 95.0)
        )

        course.submit(
            Submission("ST003", "LAB04", 1, 100.0)
        )

        # Проверяем количество студентов
        print("Количество студентов:", len(course))

        # Проверяем наличие студента
        print("ST001 зарегистрирован:", "ST001" in course)
        print("ST005 зарегистрирован:", "ST005" in course)

        # Получаем студента
        print(course.get_student("ST002"))

        # Обходим всех студентов
        print("\nВсе студенты:")
        for student in course:
            print(student)

        # Выводим лучших студентов
        print("\nЛучшие студенты:")
        for student in course.top_students(limit=2):
            print(student, "Средний балл:", student.average_score)

        try:
            course.add_student(student1)
        except ValueError as error:
            print("Ошибка регистрации:", error)

        try:
            course.submit(
                Submission("ST999", "LAB04", 1, 90.0)
            )
        except KeyError:
            print("Ошибка: студент не зарегистрирован")

        try:
            student1.add_submission(
                Submission("ST002", "LAB04", 1, 90.0)
            )
        except ValueError as error:
            print("Ошибка добавления:", error)

        empty_course = Course()

        print("Количество студентов:", len(empty_course))
        print("Лучшие студенты:", empty_course.top_students())

        try:
            course.top_students(-1)
        except ValueError as error:
            print("Ошибка:", error)