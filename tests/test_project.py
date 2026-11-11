

import tempfile
import unittest
from pathlib import Path
from database import RegistrationSystem
from models import Student, Course, Enrollment


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.service = RegistrationSystem(Path(self.tempdir.name) / "test.db")

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_and_show_everything(self):
        student_id = self.service.create_student(Student(None, "Maria", "Lopez", "maria@example.com"))
        course_id = self.service.create_course(Course(None, "Database Lab", "MAC250", 3))
        self.service.enroll_student(Enrollment(student_id, course_id))

        self.assertEqual(self.service.show_all_students()[0].full_name, "Maria Lopez")
        self.assertEqual(self.service.show_all_courses()[0].course_code, "MAC250")
        self.assertEqual(self.service.show_all_enrollments()[0].student_name, "Maria Lopez")

    def test_duplicate_enrollment_is_rejected(self):
        import sqlite3
        sid = self.service.create_student(Student(None, "Maria", "Lopez", "maria@example.com"))
        cid = self.service.create_course(Course(None, "Database Lab", "MAC250", 3))
        self.service.enroll_student(Enrollment(sid, cid))
        with self.assertRaises(sqlite3.IntegrityError):
            self.service.enroll_student(Enrollment(sid, cid))

    def test_missing_student_cannot_enroll(self):
        import sqlite3
        cid = self.service.create_course(Course(None, "Database Lab", "MAC250", 3))
        with self.assertRaises(sqlite3.IntegrityError):
            self.service.enroll_student(Enrollment(999, cid))


if __name__ == "__main__":
    unittest.main()
