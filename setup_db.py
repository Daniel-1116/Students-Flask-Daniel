import sqlite3
from faker import Faker
import random
def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql)      
    return cur.fetchall()
    
def create_table():
    execute_query("""
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                    ) """)
                    
    execute_query("""CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
                    )""")
                    
    execute_query("""
                  CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY, 
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                    )""")
    
    execute_query("""
                  CREATE TABLE IF NOT EXISTS students_courses (
                    id INTEGER PRIMARY KEY, 
                    student_id INTEGER,
                    course_id INTEGER UNIQUE,
                    FOREIGN KEY (course_id) REFERENCES courses (id),
                    FOREIGN KEY (student_id) REFERENCES students (id)
                    )""")                
    
    
def create_fake_data(students_num=40, teachers_num=4):
    fake = Faker()
    for student in range(students_num):
        execute_query(f"INSERT INTO students (name,email) VALUES ('{fake.name()}','{fake.email()}')")
    
    for teacher in range(teachers_num):
        execute_query(f"INSERT INTO teachers (name,email) VALUES ('{fake.name()}','{fake.email()}')")
        
    courses = ["Python","Java","HTML","CSS"]
    
    for course in courses:
        teacher_ids =[tup[0] for tup in execute_query("SELECT id FROM teachers")]
        execute_query(F"INSERT INTO courses (name,teacher_id) VALUES ('{course}','{random.choice(teacher_ids)}') ")
