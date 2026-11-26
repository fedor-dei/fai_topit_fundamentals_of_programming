from abc import ABC, abstractmethod
from datetime import datetime
from task_4 import Submission, Student
from collections.abc import Iterable, Iterator, Callable


class CourseEvent(ABC):
    """Базовый абстрактный класс события учебного курса."""

    def __init__(self, created_at: datetime | None = None) -> None:
        """Сохраняет время создания события."""
        self._created_at = created_at or datetime.now()

    @property
    def created_at(self) -> datetime:
        """Возвращает время создания события."""
        return self._created_at

    @property
    @abstractmethod
    def student_id(self) -> str:
        """Возвращает идентификатор студента."""
        pass

    @abstractmethod
    def describe(self) -> str:
        """Возвращает текстовое описание события."""
        pass


class SubmissionEvent(CourseEvent):
    """Событие сдачи лабораторной работы студентом."""

    def __init__(
        self,
        submission: Submission,
        created_at: datetime | None = None
    ) -> None:
        """Создаёт событие сдачи лабораторной работы."""
        super().__init__(created_at)
        self.submission = submission

    @property
    def student_id(self) -> str:
        """Возвращает идентификатор студента."""
        return self.submission.student_id

    def describe(self) -> str:
        """Возвращает описание события сдачи работы."""
        return (
            f"Студент {self.student_id} сдал "
            f"{self.submission.laboratory_id}, "
            f"попытка №{self.submission.attempt}, "
            f"оценка: {self.submission.score}"
        )


class AttendanceEvent(CourseEvent):
    """Событие посещения занятия студентом."""

    def __init__(
        self,
        student_id: str,
        lesson_name: str,
        present: bool,
        created_at: datetime | None = None
    ) -> None:
        """Создаёт событие посещения занятия."""
        super().__init__(created_at)
        self._student_id = student_id
        self.lesson_name = lesson_name
        self.present = present

    @property
    def student_id(self) -> str:
        """Возвращает идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Возвращает описание посещения занятия."""
        status = "присутствовал" if self.present else "отсутствовал"

        return (
            f"Студент {self.student_id} {status} "
            f"на занятии «{self.lesson_name}»"
        )


class CommentEvent(CourseEvent):
    """Событие текстовой обратной связи студенту."""

    def __init__(
        self,
        student_id: str,
        comment: str,
        created_at: datetime | None = None
    ) -> None:
        """Создаёт событие с комментарием."""
        super().__init__(created_at)
        self._student_id = student_id
        self.comment = comment

    @property
    def student_id(self) -> str:
        """Возвращает идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Возвращает описание события с комментарием."""
        return (
            f"Комментарий для студента {self.student_id}: "
            f"{self.comment}"
        )


class CourseJournal:
    """Хранит события учебного курса."""

    def __init__(self) -> None:
        """Создаёт пустой журнал."""
        self._events: list[CourseEvent] = []

    def add_event(self, event: CourseEvent) -> None:
        """Добавляет событие в журнал."""
        self._events.append(event)

    def __len__(self) -> int:
        """Возвращает количество событий."""
        return len(self._events)

    def __iter__(self) -> Iterator[CourseEvent]:
        """Возвращает итератор по событиям."""
        return iter(self._events)

    def __getitem__(
        self,
        index: int | slice
    ) -> CourseEvent | list[CourseEvent]:
        """Возвращает событие по индексу или список событий по срезу."""
        return self._events[index]

    def __str__(self) -> str:
        """Возвращает человекочитаемое содержимое журнала."""
        return "\n".join(
            event.describe() for event in self._events
        )

    def __repr__(self) -> str:
        """Возвращает отладочное представление журнала."""
        return f"CourseJournal(events={len(self._events)})"

    def events_for_student(self, student_id: str) -> Iterator[CourseEvent]:
        """Возвращает события указанного студента."""
        for event in self._events:
            if event.student_id == student_id:
                yield event

    def events_by_type(self, event_type: type[CourseEvent]) -> Iterator[CourseEvent]:
        """Возвращает события указанного класса."""
        for event in self._events:
            if isinstance(event, event_type):
                yield event

    def summary(self) -> dict[str, object]:
        """Возвращает сводную статистику журнала."""

        by_type: dict[str, int] = {}
        by_student: dict[str, int] = {}

        for event in self._events:
            # Считаем события каждого типа
            event_name = type(event).__name__
            by_type[event_name] = by_type.get(event_name, 0) + 1

            # Считаем события каждого студента
            student_id = event.student_id
            by_student[student_id] = by_student.get(student_id, 0) + 1

        return {
            "total_events": len(self._events),
            "by_type": by_type,
            "by_student": by_student
        }


class ScoreView:
    """Предоставляет ленивый просмотр оценок из журнала."""

    def __init__(self, journal: CourseJournal) -> None:
        """Сохраняет ссылку на журнал."""
        self._journal = journal

    def __iter__(self) -> Iterator[float]:
        """Возвращает оценки из событий сдачи лабораторных."""
        for event in self._journal:
            if isinstance(event, SubmissionEvent):
                yield event.submission.score

def render_timeline(events) -> str:
    """Формирует временную шкалу, вызывая describe() у каждого события."""
    ordered_events = sorted(events, key=lambda event: event.created_at)

    return "\n".join(
        f"{event.created_at:%Y-%m-%d %H:%M:%S} | {event.describe()}" for event in ordered_events
    )

class DeadlineEvent(CourseEvent):
    """Событие, обозначающее срок сдачи лабораторной работы."""

    def __init__(
        self,
        student_id: str,
        laboratory_id: str,
        deadline: datetime,
        created_at: datetime | None = None
    ) -> None:
        """Создаёт событие с информацией о сроке сдачи."""
        super().__init__(created_at)
        self._student_id = student_id
        self.laboratory_id = laboratory_id
        self.deadline = deadline

    @property
    def student_id(self) -> str:
        """Возвращает идентификатор студента."""
        return self._student_id

    def describe(self) -> str:
        """Возвращает описание срока сдачи лабораторной."""
        return (
            f"Для студента {self.student_id} установлен срок сдачи "
            f"{self.laboratory_id}: "
            f"{self.deadline:%Y-%m-%d %H:%M}"
        )

class FilteredJournalView:
    """Ленивое представление журнала с фильтрацией событий."""

    def __init__(
        self,
        journal: CourseJournal,
        predicate: Callable[[CourseEvent], bool]
    ) -> None:
        """Сохраняет журнал и функцию-фильтр."""
        self._journal = journal
        self._predicate = predicate

    def __iter__(self) -> Iterator[CourseEvent]:
        """Возвращает события, прошедшие фильтрацию."""
        for event in self._journal:
            if self._predicate(event):
                yield event


if __name__ == "__main__":
    #Submission
    submission = Submission(
        student_id="ST001",
        laboratory_id="LAB04",
        attempt=1,
        score=95.0,
        comment="Хорошая работа"
    )

    event = SubmissionEvent(submission)

    print(event.student_id)
    print(event.created_at)
    print(event.describe())

    #Attendance
    attendance = AttendanceEvent(
        student_id="ST001",
        lesson_name="Python: генераторы",
        present=True
    )

    absence = AttendanceEvent(
        student_id="ST002",
        lesson_name="Python: генераторы",
        present=False
    )

    print(attendance.student_id)
    print(attendance.created_at)
    print(attendance.describe())
    print(absence.describe())

    #Comment
    comment = CommentEvent(
        student_id="ST001",
        comment="Хорошая работа!"
    )

    print(comment.student_id)
    print(comment.created_at)
    print(comment.describe())


    #CourseJournal
    journal = CourseJournal()

    submission = Submission("ST001", "LAB04", 1, 95.0)

    event1 = SubmissionEvent(submission)

    event2 = AttendanceEvent(
        "ST001",
        "Python: генераторы",
        True
    )

    event3 = CommentEvent("ST001","Хорошая работа!")



    # Добавляем события
    journal.add_event(event1)
    journal.add_event(event2)
    journal.add_event(event3)

    journal.add_event(
        AttendanceEvent("ST002", "Python", True)
    )

    journal.add_event(
        CommentEvent("ST003", "Хорошее выполнение!")
    )

    journal.add_event(
        SubmissionEvent(
            Submission("ST002", "LAB03", 1, 80.0)
        )
    )

    # Проверяем количество
    print("Количество событий:", len(journal))

    # Проверяем доступ по индексу
    print("\nПервое событие:")
    print(journal[0].describe())

    # Проверяем срез
    print("\nПервые два события:")
    for event in journal[0:2]:
        print(event.describe())

    # Проверяем обход журнала
    print("\nВсе события:")
    for event in journal:
        print(event.describe())

    # Проверяем представления
    print("\nstr:")
    print(str(journal))

    print("\nrepr:")
    print(repr(journal))

    #summary
    print("\nСтатистика журнала:")

    statistics = journal.summary()

    print("Всего событий:", statistics["total_events"])
    print("По типам:", statistics["by_type"])
    print("По студентам:", statistics["by_student"])

    #render_timeline
    journal = CourseJournal()

    journal.add_event(
        SubmissionEvent(
            Submission("ST001", "LAB04", 1, 95.0)
        )
    )

    journal.add_event(
        AttendanceEvent(
            "ST002",
            "Python",
            True
        )
    )

    journal.add_event(
        CommentEvent(
            "ST001",
            "Хорошая работа!"
        )
    )

    print(render_timeline(journal))


    #Score_view
    journal = CourseJournal()

    journal.add_event(
        SubmissionEvent(
            Submission("ST001", "LAB04", 1, 75.0)
        )
    )

    journal.add_event(
        AttendanceEvent("ST001", "Python", True)
    )

    journal.add_event(
        SubmissionEvent(
            Submission("ST001", "LAB04", 2, 95.0)
        )
    )

    journal.add_event(
        CommentEvent("ST001", "Хорошая работа!")
    )

    journal.add_event(
        SubmissionEvent(
            Submission("ST002", "LAB04", 1, 85.0)
        )
    )

    # Создаём представление оценок
    scores = ScoreView(journal)

    # Первый обход
    print("Первый обход:", list(scores))

    # Второй обход
    print("Второй обход:", list(scores))

    # Вычисляем средний балл
    all_scores = list(scores)

    average = sum(all_scores) / len(all_scores)

    print("Средняя оценка:", average)



    #Demonstration:
    print()
    # Создаём трёх студентов
    students = [
        Student("ST001", "Иван Иванов"),
        Student("ST002", "Пётр Петров"),
        Student("ST003", "Анна Смирнова")
    ]

    print("Студенты курса:")
    for student in students:
        print(student)

    # Создаём журнал
    journal = CourseJournal()

    # Создаём десять событий
    events: list[CourseEvent] = [

        # Первый студент
        SubmissionEvent(
            Submission("ST001", "LAB04", 1, 75.0),
            created_at=datetime(2026, 11, 1, 9, 0)
        ),

        AttendanceEvent(
            "ST001", "Python", True,
            created_at=datetime(2026, 11, 1, 10, 0)
        ),

        CommentEvent(
            "ST001", "Хорошее начало!",
            created_at=datetime(2026, 11, 1, 11, 0)
        ),

        # Вторая попытка той же лабораторной
        SubmissionEvent(
            Submission("ST001", "LAB04", 2, 95.0),
            created_at=datetime(2026, 11, 2, 9, 0)
        ),

        # Второй студент
        AttendanceEvent(
            "ST002", "Python", True,
            created_at=datetime(2026, 11, 2, 10, 0)
        ),

        SubmissionEvent(
            Submission("ST002", "LAB03", 1, 82.0),
            created_at=datetime(2026, 11, 2, 11, 0)
        ),

        CommentEvent(
            "ST002", "Можно улучшить оформление.",
            created_at=datetime(2026, 11, 2, 12, 0)
        ),

        # Третий студент
        AttendanceEvent(
            "ST003", "Python", False,
            created_at=datetime(2026, 11, 3, 9, 0)
        ),

        SubmissionEvent(
            Submission("ST003", "LAB04", 1, 91.0),
            created_at=datetime(2026, 11, 3, 10, 0)
        ),

        CommentEvent(
            "ST003", "Отличный результат!",
            created_at=datetime(2026, 11, 3, 11, 0)
        )
    ]

    # Добавляем все события в журнал
    for event in events:
        journal.add_event(event)

    # Проверяем количество событий
    print("\nВсего событий:", len(journal))

    # События конкретного студента
    print("\nСобытия студента ST001:")
    for event in journal.events_for_student("ST001"):
        print(event.describe())

    # События определённого типа
    print("\nСобытия сдачи лабораторных:")
    for event in journal.events_by_type(SubmissionEvent):
        print(event.describe())

    # Срез журнала
    print("\nПервые три события:")
    for event in journal[0:3]:
        print(event.describe())

    # Временная шкала
    print("\nВременная шкала:")
    print(render_timeline(journal))

    # Статистика журнала
    print("\nСтатистика:")
    print(journal.summary())

    # Работа с оценками
    score_view = ScoreView(journal)
    scores = list(score_view)

    print("\nОценки:", scores)
    print("Количество оценок:", len(scores))
    print("Средняя оценка:", sum(scores) / len(scores))

    # Проверяем повторный обход ScoreView
    print("Повторный обход:", list(score_view))

    #Deadline
    deadline_event = DeadlineEvent(
        student_id="ST001",
        laboratory_id="LAB05",
        deadline=datetime(2026, 12, 10, 23, 59),
        created_at=datetime(2026, 11, 27, 12, 0)
    )

    journal.add_event(deadline_event)

    print(render_timeline(journal))
    print(deadline_event.student_id)
    print(deadline_event.describe())

    # FilteredJournalView
    submission_view = FilteredJournalView(
        journal,
        lambda event: isinstance(event, SubmissionEvent)
    )
    #only lab
    print("\nТолько события сдачи:")

    for event in submission_view:
        print(event.describe())

    student_view = FilteredJournalView(
        journal,
        lambda event: event.student_id == "ST001"
    )
    #only one student
    print("\nВсе события студента ST001:")

    for event in student_view:
        print(event.describe())

    print("\nПервый обход:")
    print([event.describe() for event in student_view])

    print("\nВторой обход:")
    print([event.describe() for event in student_view])