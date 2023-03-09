from flask import Flask, abort, request, redirect ,url_for ,render_template, flash, get_flashed_messages, session
from setup_db import execute_query
from email_validator import validate_email,EmailNotValidError
from sqlite3 import IntegrityError
from collections import namedtuple
from classes import Course,Student,Attendence
import datetime
app = Flask(__name__)

app.secret_key = "SA3202DSG;=4334/./322/1`1423DSVKGOTdsfdssdg"


def authenticate(email,password):
    role = [r[0] for r in  execute_query(f"SELECT role FROM users WHERE email='{email}' AND password='{password}'")]
    if role == []:
        return None
    else:
        return role[0]
    
@app.route('/login', methods = ['GET','POST'])
def user_login():
    if request.method == 'POST':
        role = authenticate(request.form["email"],request.form["password"])
        if role == None:
            return abort(403)
        else:
            session["role"] = role
            return redirect(url_for("homepage"))
    return render_template("login.html")

@app.route('/logout')
def user_logout():
    session.pop('role',None)
    return redirect(url_for("homepage"))

@app.route('/')
def homepage():
    course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query("SELECT * FROM courses")]
    return render_template("home.html",course=course)




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
    students = [Student(s_id,name,email) for s_id,name,email in execute_query("SELECT id,name,email FROM students")]
    
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

@app.route('/courses')
def show_courses():        
    course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query("SELECT * FROM courses")]
    return render_template("courses.html",course = course)


@app.route('/search',methods = ['GET','POST'])
def navbar_search():
    if request.method == 'POST':
        keyword = request.form["search-keyword"]
        if keyword != "":
            teachers = execute_query(f"SELECT name,email FROM teachers WHERE name LIKE '%{keyword}%' OR email LIKE '%{keyword}%'")
            courses = execute_query(f"SELECT name,description FROM courses WHERE name LIKE '%{keyword}%' OR description LIKE '%{keyword}%'")
            students = execute_query(f"SELECT name,email FROM students WHERE name LIKE '%{keyword}%' OR email LIKE '%{keyword}%'")
            return render_template("search.html",teachers=teachers,courses=courses,students=students)
        else:
            message = "No Keyword Entry"
            course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query("SELECT * FROM courses")]
            return render_template("home.html",message=message, course=course)
        
        
        
@app.route('/teachers', methods = ['GET','POST'])
def teachers():
    teachers = [teacher for teacher in execute_query("SELECT id,name FROM teachers")]
    return render_template("teachers.html",teachers = teachers)


@app.route('/teacher/<teacher_id>', methods = ['GET','POST'])
def teacher_page(teacher_id):
    if request.method == 'POST':
        s_grade = request.form["grade"]
        # execute_query(f"UPDATE students SET  grade='{s_grade}' WHERE name='{s_name}' ")
        return redirect(url_for("teachers"))
    else:
        t_name = [n[0] for n in execute_query(f"SELECT name FROM teachers WHERE id={teacher_id}")]
        course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query(f"SELECT * FROM courses WHERE teacher_id={teacher_id}")]
        return render_template("teacher_profile.html",t_name = t_name[0],course = course)
    
    
@app.route('/attendence', methods = ['GET','POST'])
def attend():
    course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query("SELECT * FROM courses")]
    return render_template('attendence.html',course = course)
    
    
def get_records(c_id):
        attendance_records = execute_query(f"SELECT student_id, attendence FROM attendances WHERE course_id = {c_id}")
        attendences = {}
        for s_id,attendence in attendance_records:
            attendences[s_id] = attendence
        return attendences     
    
@app.route('/attend/<course_id>', methods = ['GET','POST'])
def course_attend(course_id):
    if request.method == 'POST':
        course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query(f"SELECT * FROM courses WHERE id={course_id}")]
        date = "2023-03-10"
        choice = request.form['choice']
        s_id = request.form['s_id_']
        execute_query(f"UPDATE attendances SET attendence='{choice}'  WHERE student_id='{s_id}' AND course_id='{course_id}' AND date='{date}'")
        attendence = get_records(course_id)
        return redirect(url_for("course_attend",course_id = course_id))
    else:
        course = [Course(c_id,name,desc,t_id) for c_id,name,desc,t_id in execute_query(f"SELECT * FROM courses WHERE id={course_id}")]
        date = "2023-03-10"
        attendence = get_records(course_id)
        result = execute_query(f"SELECT COUNT(*) FROM attendances WHERE course_id={course_id} AND date='{date}'")
        if result[0][0] > 0:
            return render_template("attend.html",course = course, date = date,c_attend = attendence)
        else:
            student_ids = [ids[0] for ids in execute_query(f"SELECT student_id FROM students_courses WHERE course_id = {course_id}")]
            for s_id in student_ids:
                execute_query(f"INSERT INTO attendances (student_id,course_id,date) VALUES ('{s_id}','{course_id}','{date}')")
            attendence = get_records(course_id)
            return render_template("attend.html",course = course, date = date,c_attend = attendence)

        
        

   
    