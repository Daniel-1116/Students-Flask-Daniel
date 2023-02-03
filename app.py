from flask import Flask, request, redirect ,url_for ,render_template
from setup_db import execute_query
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Registrations.html')

@app.route('/register/<student_id>/<course_id>')
def register(student_id,course_id):
    execute_query(f"INSERT INTO students_courses (student_id,course_id) VALUES ('{student_id}','{course_id}')")
    return redirect(url_for('registrations',student_id=student_id))
    
@app.route('/registrations/<student_id>')
def registrations(student_id):
    course_ids = [c[0] for c in execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")] 
    course_names = [execute_query(f"SELECT name FROM courses WHERE id = {course}") for course in course_ids]  
    student_name = execute_query(f"SELECT name FROM students WHERE id= '{student_id}'")
    return render_template('registrations.html',courses = course_names)
