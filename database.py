import sqlite3
from pathlib import Path
from models import Student, Course, Enrollment


class RegistrationSystem:

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self.initialize_database()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize_database(self):
      
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS Students (
                    student_id INTEGER PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS Courses (
                    course_id INTEGER PRIMARY KEY,
                    course_name VARCHAR(100) NOT NULL UNIQUE,
                    course_code VARCHAR(10) NOT NULL UNIQUE,
                    credits INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS Enrollments (
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    PRIMARY KEY (student_id, course_id),
                    FOREIGN KEY (student_id) REFERENCES Students(student_id),
                    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
                );
            """)

    def create_student(self, student: Student) -> int:
        with self._connect() as conn:
            result = conn.execute(
                "INSERT INTO Students (first_name, last_name, email) VALUES (?, ?, ?)",
                (student.first_name.strip(), student.last_name.strip(), student.email.strip()),
            )
            return result.lastrowid

    def create_course(self, course: Course) -> int:
        with self._connect() as conn:
            result = conn.execute(
                "INSERT INTO Courses (course_name, course_code, credits) VALUES (?, ?, ?)",
                (course.course_name.strip(), course.course_code.strip().upper(), course.credits),
            )
            return result.lastrowid

    def enroll_student(self, enrollment: Enrollment) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)",
                (enrollment.student_id, enrollment.course_id),
            )

    def show_all_students(self) -> list[Student]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT student_id, first_name, last_name, email
                FROM Students ORDER BY first_name, last_name
            """).fetchall()
        return [Student(**dict(row)) for row in rows]

    def show_all_courses(self) -> list[Course]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT course_id, course_name, course_code, credits
                FROM Courses ORDER BY course_code
            """).fetchall()
        return [Course(**dict(row)) for row in rows]

    def show_all_enrollments(self) -> list[Enrollment]:
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT e.student_id, e.course_id,
                       s.first_name || ' ' || s.last_name AS student_name,
                       c.course_code, c.course_name
                FROM Enrollments e
                JOIN Students s ON s.student_id = e.student_id
                JOIN Courses c ON c.course_id = e.course_id
                ORDER BY s.first_name, s.last_name, c.course_code
            """).fetchall()
        return [Enrollment(**dict(row)) for row in rows]
