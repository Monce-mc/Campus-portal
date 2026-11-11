

from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    student_id: int | None
    first_name: str
    last_name: str
    email: str

    def __post_init__(self):
        if not self.first_name.strip() or not self.last_name.strip():
            raise ValueError("First and last name are required.")
        if not self.email.strip() or "@" not in self.email:
            raise ValueError("Enter a valid email address.")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass(frozen=True)
class Course:
    course_id: int | None
    course_name: str
    course_code: str
    credits: int

    def __post_init__(self):
        if not self.course_name.strip() or not self.course_code.strip():
            raise ValueError("Course name and course code are required.")
        if not 0 <= self.credits <= 30:
            raise ValueError("Credits must be between 0 and 30.")


@dataclass(frozen=True)
class Enrollment:
    student_id: int
    course_id: int
    student_name: str = ""
    course_code: str = ""
    course_name: str = ""

    def __post_init__(self):
        if self.student_id <= 0 or self.course_id <= 0:
            raise ValueError("Select a valid student and course.")
