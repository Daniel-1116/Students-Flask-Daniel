import sqlite3
from faker import Faker
import random


def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql)
    return cur.fetchall()


def table_exists(table_name):
    result = execute_query(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return len(result) > 0

def create_table():
    if not table_exists('teachers'):
        execute_query("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )""")

    if not table_exists('courses'):
        execute_query("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                description TEXT,
                teacher_id INTEGER NOT NULL,
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )""")

    if not table_exists('students'):
        execute_query("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                photo_filename TEXT
            )""")

    if not table_exists('students_courses'):
        execute_query("""
            CREATE TABLE IF NOT EXISTS students_courses (
                id INTEGER PRIMARY KEY, 
                student_id INTEGER,
                course_id INTEGER,
                grade INTEGER DEFAULT(0),
                FOREIGN KEY (course_id) REFERENCES courses (id),
                FOREIGN KEY (student_id) REFERENCES students (id),
                UNIQUE(student_id, course_id)
            )""")

    if not table_exists('users'):
        execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )""")

    if not table_exists('attendances'):
        execute_query("""
            CREATE TABLE IF NOT EXISTS attendances (
                id INTEGER PRIMARY KEY, 
                student_id INTEGER,
                course_id INTEGER,
                attendance TEXT,
                date TEXT,
                FOREIGN KEY (course_id) REFERENCES courses (id),
                FOREIGN KEY (student_id) REFERENCES students (id),
                UNIQUE(student_id, course_id, date)
            )""")

def create_fake_data(students_num=40, teachers_num=4):
    fake = Faker()

    courses = ["Python", "Java", "Django", "JavaScript"]
    default_password = 12345

    existing_combinations = set()

    for i in range(students_num):
        student_data = {'name': fake.name(), 'email': fake.email()}
        student_id = i + 1

        while True:
            course_id = random.randint(1, 4)
            combination = (student_id, course_id)

            if combination not in existing_combinations:
                existing_combinations.add(combination)
                break

        execute_query(
            f"INSERT INTO students (name, email) VALUES ('{student_data['name']}', '{student_data['email']}')")
        execute_query(
            f"INSERT OR IGNORE INTO students_courses (student_id, course_id, grade) VALUES ({student_id}, {course_id}, 0)")

        execute_query(
            f"INSERT INTO users (email, password, role) VALUES ('{student_data['email']}', '{default_password}', 'student')")

    for teacher in range(teachers_num):
        teacher = {"name": fake.name(), "email": fake.email()}
        execute_query(
            f"INSERT INTO teachers (name,email) VALUES ('{teacher['name']}','{teacher['email']}')")
        execute_query(
            f"INSERT INTO users (email,password,role) VALUES ('{teacher['email']}','{default_password}','teacher')")

    for course_name in courses:
        teacher_ids = [tup[0]
                       for tup in execute_query("SELECT id FROM teachers")]
        execute_query(
            f"INSERT INTO courses (name, description, teacher_id) VALUES ('{course_name}','A Very Nice Course','{random.choice(teacher_ids)}')")
    execute_query(
        "INSERT INTO users VALUES (NULL,'admin@admin.com','admin','admin')")

if __name__ == "__main__":
    create_table()
    create_fake_data()
