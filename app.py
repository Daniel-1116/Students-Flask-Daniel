from flask import Flask, request, redirect ,url_for ,render_template, flash, get_flashed_messages
from setup_db import execute_query
from email_validator import validate_email,EmailNotValidError
from sqlite3 import IntegrityError
from collections import namedtuple

app = Flask(__name__)

app.secret_key = "SA3202DSG;=4334/./322/1`1423DSVKGOT"



@app.route('/register/<student_id>/<course_id>')
def register(student_id,course_id):
    try:
        execute_query(f"INSERT INTO students_courses (student_id,course_id) VALUES ('{student_id}','{course_id}')")
    except IntegrityError:
        student_name = [s[0] for s in execute_query(f"SELECT name FROM students WHERE id='{student_id}'")]
        course_name = [s[0] for s in execute_query(f"SELECT name FROM courses WHERE id='{course_id}'")]
        return f"{student_name} is already registered to {course_name}"
        
    return redirect(url_for('registrations',student_id=student_id))
    
@app.route('/registrations/<student_id>')
def registrations(student_id):
    course_ids = [c[0] for c in execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")] 
    course_names = [execute_query(f"SELECT name FROM courses WHERE id = {course}") for course in course_ids]  
    student_name = execute_query(f"SELECT name FROM students WHERE id = '{student_id}'")
    return render_template('registrations.html',courses = course_names,student = student_name)



@app.route('/add_student', methods = ['GET','POST'])
def add_new_student():
    if request.method == 'POST':
        full_name = request.form["full_name"]
        email = request.form["email"]
        execute_query(f"INSERT INTO students (name,email) VALUES ('{full_name}','{email}')")
        flash(f"Successfully Added {full_name}")
        return redirect(url_for('all_students')) 
    else:
        courses = [c[0] for c in execute_query("SELECT name FROM courses")]
        return render_template('add_student.html',courses = courses)


@app.route('/students')
def all_students():
    students = [s[0] for s in execute_query("SELECT name FROM students")]
    return render_template('students.html',students = students)  


@app.route('/add_course',methods = ['GET','POST'])  
def add_course():
    if request.method == 'POST':
        course_name = request.form["course_name"]
        course_desc = request.form["course_desc"]
        teacher = request.form["teacher"]
        teacher_id = [i[0] for i in execute_query(f"SELECT id FROM teachers WHERE name='{teacher}'")]
        execute_query(f"INSERT INTO courses (name,description,teacher_id) VALUES ('{course_name}','{course_desc}','{teacher_id[0]}')")
        flash(f"Successfully Added {course_name} To DB")
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        return render_template("add_course.html",teachers = teachers)
    else:
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        return render_template("add_course.html",teachers = teachers)


# @app.route('/')
# def something(student_id):
#     course_names = execute_query(f"SELECT courses.name FROM courses JOIN students_courses.course_id=course_id WHERE students_courses.student_id={student_id}")
#     # courses = []
    # for course_tuple in course_names:
    #     course=namedtuple("Course",["name","teacher"])
    #     course.name = course_tuple[0]
    #     courses.append(course)
   
  