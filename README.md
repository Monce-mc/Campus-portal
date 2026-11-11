# Campus Portal: Student, Course & Enrollment System

A Flask + SQLite web application for a university registration system, implemented with object-oriented Python.

## Features
- Interactive web interface for student and course entry.
- Enroll students in courses.
- Show all students, courses, enrollments, or all records together.
- OOP models: `Student`, `Course`, `Enrollment` in `models.py`.
- `RegistrationSystem` service in `database.py` provides SQLite persistence.
- Duplicate student email, course code, and student-course enrollment are rejected.

## Files
- `app.py`: Flask routes and website
- `models.py`: OOP class definitions
- `database.py`: SQLite service, database schema, create/read operations
- `templates/index.html`: HTML and CSS front end
- `tests/test_project.py`: automated tests
- `requirements.txt`: Python dependency
- `.gitignore`: excludes local database files
- `README.md`: setup instructions

## Setup
1. Install Python 3.10 or later.
2. Download this repository and open a terminal in the folder containing `app.py`.
3. Install requirements: `python -m pip install -r requirements.txt`
4. Run the web app: `python app.py`
5. Open http://127.0.0.1:5001 in your browser.
6. Press Ctrl+C to stop the app.

On macOS/Linux, use `python3` instead of `python` if required.

## Using the app
1. Create a student with a first name, last name, and email.
2. Create a course with a name, code (e.g. MAC250), and credits.
3. Select the student and course, then click Enroll Student.
4. Use Show All / Show All Students / Show All Courses / Show All Enrollments.

## Database
The application automatically creates a local `instagram.db` SQLite database on the first run. You do not need to upload any personal student records to GitHub. The database is excluded by `.gitignore`.

## Testing
Run `python -m unittest discover -s tests -v`.

## Technology
Python, Flask, SQLite, HTML/CSS, Jinja.

For class submission, compare the OOP fields with your instructor's original class specifications. This version uses the schema and composite enrollment key from the working Campus Portal project.