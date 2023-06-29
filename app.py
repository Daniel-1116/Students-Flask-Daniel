import os
from werkzeug.utils import secure_filename
from flask import Flask, abort, jsonify, request, redirect, url_for, render_template, flash, get_flashed_messages, session
from setup_db import execute_query
from sqlite3 import IntegrityError
from collections import namedtuple
from classes import Course, Student, Attendence
import datetime

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "SA3202DSG;=4334/./322/1`1423DSVKGOTdsfdssdg"


def authenticate(email, password):
    role = [r[0] for r in execute_query(
        f"SELECT role FROM users WHERE email='{email}' AND password='{password}'")]
    if role == []:
        return None
    else:
        return role[0]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_image_filename(course_name):
    for ext in ALLOWED_EXTENSIONS:
        filename = f"{course_name}.{ext}"
        file_path = os.path.join(app.static_folder, 'images', filename)

        if os.path.isfile(file_path):
            image_filename = filename
            break
    return image_filename


def get_records(c_id, date):
    attendance_records = execute_query(
        f"SELECT student_id, COALESCE(attendance, 'N/A') AS attendance FROM attendances WHERE course_id={c_id} AND date='{date}'")
    attendances = {}
    for record in attendance_records:
        s_id, attendance = record
        attendances[s_id] = attendance
    return attendances


def get_courses_info(teacher_id=None, course_id=None):
    if teacher_id is not None:
        if course_id is not None:
            query = f"""
                SELECT courses.id, courses.name, courses.description, teachers.name
                FROM courses
                JOIN teachers ON courses.teacher_id = teachers.id
                WHERE courses.teacher_id = {teacher_id} AND courses.id = {course_id}
            """
        else:
            query = f"""
                SELECT courses.id, courses.name, courses.description, teachers.name
                FROM courses
                JOIN teachers ON courses.teacher_id = teachers.id
                WHERE courses.teacher_id = {teacher_id}
            """
    else:
        query = """
            SELECT courses.id, courses.name, courses.description, teachers.name
            FROM courses
            JOIN teachers ON courses.teacher_id = teachers.id
        """
    course_details = execute_query(query)
    courses = []
    for c_id, name, desc, t_name in course_details:
        image_filename = get_image_filename(name)
        course = {
            'id': c_id,
            'name': name,
            'desc': desc,
            't_name': t_name,
            'image_filename': image_filename
        }
        courses.append(course)
    return courses


@app.route('/admin')
def admin_page():
    return render_template("admin.html")


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        role = authenticate(request.form["email"], request.form["password"])
        if role == None:
            return abort(403)
        else:
            session["role"] = role
            return redirect(url_for("homepage"))
    return render_template("login.html")


@app.route('/logout')
def user_logout():
    session.pop('role', None)
    return redirect(url_for("homepage"))


@app.route('/', methods=['GET', 'POST'])
def homepage():
    course_details = execute_query("""SELECT courses.name, teachers.name FROM courses 
                                    JOIN teachers ON courses.teacher_id = teachers.id """)
    course_names = [names[0] for names in course_details]
    teacher_names = [names[1] for names in course_details]
    courses = {}
    for c_name, t_name in zip(course_names[-2:], teacher_names[-2:]):
        image_filename = get_image_filename(c_name)
        courses[c_name] = {
            'image_filename': image_filename,
            'teacher_name': t_name
        }
    return render_template("home.html", courses=courses)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form["s_id"]
        course_id = request.form["c_id"]
        student_name = [s[0] for s in execute_query(
            f"SELECT name FROM students WHERE id='{student_id}'")]
        course_name = [s[0] for s in execute_query(
            f"SELECT name FROM courses WHERE id='{course_id}'")]
        try:
            execute_query(
                f"INSERT INTO students_courses (student_id,course_id) VALUES ('{student_id}','{course_id}')")
        except IntegrityError:
            student_name = [s[0] for s in execute_query(
                f"SELECT name FROM students WHERE id='{student_id}'")]
            course_name = [s[0] for s in execute_query(
                f"SELECT name FROM courses WHERE id='{course_id}'")]
            response = {
                'message': f"{student_name} is already registered to {course_name}"}
            return jsonify(response)
        execute_query(
            f"INSERT INTO students_courses (student_id,course_id) VALUES ('{student_id}','{course_id}')")
        response = {
            'message': f'Successfully Added {student_name} to {course_name}'}
        return jsonify(response)
    else:
        courses = get_courses_info()
        students = [i for i in execute_query("SELECT id,name FROM students")]
        return render_template('register.html', students=students, courses=courses)


@app.route('/add_student', methods=['GET', 'POST'])
def add_new_student():
    if request.method == 'POST':
        full_name = request.form["full_name"]
        email = request.form["email"]
        execute_query(
            f"INSERT INTO students (name,email) VALUES ('{full_name}','{email}')")
        response = {'message': f'Successfully Added {full_name}'}
        return jsonify(response)
    else:
        return render_template('add_student.html')


@app.route('/students')
def all_students():
    students = [Student(s_id, name, email) for s_id, name, email in execute_query(
        "SELECT id,name,email FROM students")]
    return render_template('students.html', students=students)


@app.route('/student/<s_id>', methods=['GET', 'POST'])
def student_page(s_id):
    for s_id, name, email, phone, photo in execute_query(f"SELECT * FROM students WHERE id={s_id}"):
        s_details = {"s_id": s_id, "name": name,
                     "email": email, "phone": phone, "photo": photo}
    course_ids = [c_id[0] for c_id in execute_query(
        f"SELECT course_id FROM students_courses WHERE student_id='{s_id}'")]
    c_names = []
    for i in course_ids:
        name = [n[0] for n in execute_query(
            f"SELECT name FROM courses WHERE id={i}")]
        c_names.append(name[0])
    s_details["grades"] = {c_names[i]: grade[0] for i, grade in enumerate(execute_query(
        f"SELECT grade FROM students_courses WHERE student_id={s_id} AND course_id IN ({','.join(map(str, course_ids))})"))}
    s_details["average_attendance"] = {}
    for course_id, course_name in zip(course_ids, c_names):
        attendance_data = execute_query(f"SELECT date, attendance FROM attendances WHERE course_id={course_id} AND student_id={s_id}")
        attendance_count = len(attendance_data)
        yes_count = sum(1 for data in attendance_data if data[1] == 'yes')
        average_attendance = round((yes_count / attendance_count) * 100) if attendance_count > 0 else 0
        s_details["average_attendance"][course_name] = average_attendance
        print(s_details)
    return render_template("student_profile.html", s_details=s_details, c_names=c_names, course_ids=course_ids)


@app.route('/update/<s_id>', methods=['GET', 'POST'])
def update_info(s_id):
    if request.method == 'GET':
        for s_id, name, email, phone, photo in execute_query(f"SELECT * FROM students WHERE id={s_id}"):
            s_details = {"s_id": s_id, "name": name,
                         "email": email, "phone": phone, "photo": photo}
        course_ids = [c_id[0] for c_id in execute_query(
            f"SELECT course_id FROM students_courses WHERE student_id='{s_id}'")]
        c_names = []
        for i in course_ids:
            name = [n[0] for n in execute_query(
                f"SELECT name FROM courses WHERE id={i}")]
            c_names.append(name[0])
        return render_template("update_profile.html", s_details=s_details, c_names=c_names, course_ids=course_ids)
    else:
        email = request.form["email"]
        phone = request.form["phone"]
        if (email == '') and (phone != ''):
            execute_query(
                f"UPDATE students SET phone='{phone}' WHERE id={s_id}")
        if (phone == '') and (email != ''):
            execute_query(
                f"UPDATE students SET email='{email}' WHERE id={s_id}")
        if email and phone:
            execute_query(
                f"UPDATE students SET email='{email}',phone='{phone}' WHERE id={s_id}")
        if (email == '') and (phone == ''):
            pass
        return redirect(url_for("student_page", s_id=s_id))


@app.route('/upload_photo/<s_id>', methods=['POST'])
def upload_photo(s_id):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('student_page', s_id=s_id))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('student_page', s_id=s_id))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        execute_query(
            f"UPDATE students SET photo_filename='{filename}' WHERE id={s_id}")
    return redirect(url_for('student_page', s_id=s_id))


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form["course_name"]
        course_desc = request.form["course_desc"]
        teacher = request.form["teacher"]
        teacher_id = [i[0] for i in execute_query(
            f"SELECT id FROM teachers WHERE name='{teacher}'")]
        execute_query(
            f"INSERT INTO courses (name,description,teacher_id) VALUES ('{course_name}','{course_desc}','{teacher_id[0]}')")
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        response = {'message': f'Successfully Added {course_name} to DB'}
        return jsonify(response)
    else:
        teachers = [t[0] for t in execute_query("SELECT name FROM teachers")]
        return render_template("add_course.html", teachers=teachers)


@app.route('/courses')
def show_courses():
    courses = get_courses_info()
    return render_template("courses.html", courses=courses)


@app.route('/search', methods=['GET', 'POST'])
def navbar_search():
    if request.method == 'POST':
        keyword = request.form["search-keyword"]
        if keyword != "":
            teachers = execute_query(
                f"SELECT name,email FROM teachers WHERE name LIKE '%{keyword}%' OR email LIKE '%{keyword}%'")
            courses = execute_query(
                f"SELECT name,description FROM courses WHERE name LIKE '%{keyword}%' OR description LIKE '%{keyword}%'")
            students = execute_query(
                f"SELECT name,email FROM students WHERE name LIKE '%{keyword}%' OR email LIKE '%{keyword}%'")
            return render_template("search.html", teachers=teachers, courses=courses, students=students)
        else:
            message = "No Keyword Entry"
            course = [Course(c_id, name, desc, t_id) for c_id, name,
                      desc, t_id in execute_query("SELECT * FROM courses")]
            return render_template("home.html", message=message, course=course)


@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    teachers = [teacher for teacher in execute_query(
        "SELECT id,name FROM teachers")]
    return render_template("teachers.html", teachers=teachers)


@app.route('/teacher/<teacher_id>', methods=['GET', 'POST'])
def teacher_page(teacher_id):
    if request.method == 'POST':
        s_grade = request.form["grade"]
        s_id = request.form["s_id"]
        c_id = request.form["c_id"]
        execute_query(
            f"UPDATE students_courses SET grade='{s_grade}' WHERE student_id={s_id} AND course_id={c_id}")
        return redirect(url_for("teacher_page", teacher_id=teacher_id))
    else:
        c_ids = [c[0] for c in execute_query(
            f"SELECT id FROM courses WHERE teacher_id={teacher_id}")]
        student_ids = [s[0] for s in execute_query(
            f"SELECT student_id FROM students_courses WHERE course_id IN ({','.join(map(str, c_ids))})")]
        course = [Course(c_id, name, desc, t_id) for c_id, name, desc, t_id in execute_query(
            f"SELECT * FROM courses WHERE teacher_id={teacher_id}")]
        t_name = [n[0] for n in execute_query(
            f"SELECT name from teachers WHERE id={teacher_id}")]
        grades = {}
        for student_id in student_ids:
            grades_info = execute_query(
                f"SELECT course_id,grade FROM students_courses WHERE student_id={student_id} AND course_id IN ({','.join(map(str, c_ids))})")
            grades[student_id] = {c_id: grade for c_id, grade in grades_info}
        return render_template("teacher_profile.html", t_name=t_name[0], course=course, grades=grades, t_id=teacher_id)


@app.route('/teacher/<teacher_id>/attendance', methods=['GET', 'POST'])
def attendance(teacher_id):
    courses = get_courses_info(teacher_id)
    return render_template('attendance.html', courses=courses, teacher_id=teacher_id)


@app.route('/teacher/<teacher_id>/attend/<course_id>', methods=['GET', 'POST'])
def course_attend(course_id, teacher_id):
    courses = [Course(c_id, name, desc, t_id) for c_id, name, desc, t_id in execute_query(
            f"SELECT * FROM courses WHERE teacher_id={teacher_id} AND id= {course_id}")]
    selected_date = request.args.get('selected_date')

    if request.method == 'POST':
        choice = request.form['choice']
        s_id = request.form['s_id_']
        selected_date = request.form['selected_date']
        execute_query(
            f"UPDATE attendances SET attendance='{choice}' WHERE student_id='{s_id}' AND course_id='{course_id}' AND date='{selected_date}'")
        attendance = get_records(course_id, selected_date)
    else:
        if selected_date:
            attendance = get_records(course_id, selected_date)
        else:
            selected_date = datetime.date.today().strftime('%Y-%m-%d')
            attendance = get_records(course_id, selected_date)

    available_dates = [date[0] for date in execute_query(
        f"SELECT DISTINCT date FROM attendances WHERE course_id={course_id}")]
    student_ids = [ids[0] for ids in execute_query(
        f"SELECT student_id FROM students_courses WHERE course_id={course_id}")]

    d = [d[0] for d in execute_query(
        f"SELECT COUNT(*) FROM attendances WHERE course_id={course_id} AND date='{selected_date}'")]

    if d[0] > 0:
        return render_template("attend.html", course=courses, date=selected_date, c_attend=attendance, t_id=teacher_id, available_dates=available_dates, student_ids=student_ids)

    for s_id in student_ids:
        execute_query(
            f"INSERT INTO attendances (student_id, course_id, date) VALUES ('{s_id}','{course_id}','{selected_date}')")

    return render_template("attend.html", course=courses, date=selected_date, c_attend=attendance, t_id=teacher_id, available_dates=available_dates, student_ids=student_ids)
