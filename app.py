"""Run the interactive Campus Portal (Flask web interface)."""

from pathlib import Path
import sqlite3
from flask import Flask, redirect, render_template, request, url_for
from database import RegistrationSystem
from models import Student, Course, Enrollment

app = Flask(__name__)
registration = RegistrationSystem(Path(__file__).with_name("courses.db"))


@app.route("/", methods=["GET"])
def home():
    students = registration.show_all_students()
    courses = registration.show_all_courses()
    enrollments = registration.show_all_enrollments()
    show = request.args.get("show", "all")
    if show not in {"all", "students", "courses", "enrollments"}:
        show = "all"
    return render_template(
        "index.html",
        students=students,
        courses=courses,
        enrollments=enrollments,
        show=show,
        notice=request.args.get("notice", ""),
        error=request.args.get("error", ""),
    )


@app.post("/student")
def add_student():
    try:
        student = Student(
            student_id=None,
            first_name=request.form["first_name"].strip(),
            last_name=request.form["last_name"].strip(),
            email=request.form["email"].strip(),
        )
        registration.create_student(student)
        return redirect(url_for("home", notice="Student added!", show="students"))
    except (ValueError, sqlite3.IntegrityError, KeyError) as exc:
        return redirect(url_for("home", error=f"Couldn't add student: {exc}", show="students"))


@app.post("/course")
def add_course():
    try:
        course = Course(
            course_id=None,
            course_name=request.form["course_name"].strip(),
            course_code=request.form["course_code"].strip().upper(),
            credits=int(request.form["credits"]),
        )
        registration.create_course(course)
        return redirect(url_for("home", notice="Course added!", show="courses"))
    except (ValueError, sqlite3.IntegrityError, KeyError) as exc:
        return redirect(url_for("home", error=f"Couldn't add course: {exc}", show="courses"))


@app.post("/enroll")
def add_enrollment():
    try:
        enrollment = Enrollment(
            student_id=int(request.form["student_id"]),
            course_id=int(request.form["course_id"]),
        )
        registration.enroll_student(enrollment)
        return redirect(url_for("home", notice="Student enrolled!", show="enrollments"))
    except (ValueError, sqlite3.IntegrityError, KeyError) as exc:
        return redirect(url_for("home", error=f"Couldn't enroll student: {exc}", show="enrollments"))


if __name__ == "__main__":
    app.run(port=5001)
