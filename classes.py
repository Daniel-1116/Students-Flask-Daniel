from setup_db import execute_query


class Course():
    def __init__(self,c_id,name,desc,teacher_id) -> None:
        self.c_id = c_id
        self.name = name
        self.desc = desc
    
        self.t_name = self.teacher_name(teacher_id)
        self.students = self.assigned_students()
        
    def teacher_name(self,teacher_id):
        name = [name[0] for name in execute_query(f"SELECT name FROM teachers WHERE id='{teacher_id}'")]
        return name[0]
    
    def assigned_students(self):
        student_ids = [c_id[0] for c_id in execute_query(f"SELECT student_id FROM students_courses WHERE course_id='{self.c_id}'")]
        student_names_ids = []
        for i in student_ids:
            name = [n[0] for n in execute_query(f"SELECT name FROM students WHERE id={i}")]
            student_names_ids.append([i,name[0]])
        return student_names_ids
    
    def __str__(self) -> str:
        return self.name,self.t_name,self.students
    
class Student():
    def __init__(self,s_id,name,email,grade=0) -> None:
        self.s_id = s_id
        self.name = name
        self.email = email
        self.grade = grade
        self.courses = self.assigned_course()
        
    def assigned_course(self):
        course_ids = [c_id[0] for c_id in execute_query(f"SELECT course_id FROM students_courses WHERE student_id='{self.s_id}'")]
        course_name = []
        for i in course_ids:
            name = [n[0] for n in execute_query(f"SELECT name FROM courses WHERE id={i}")]
            course_name.append(name[0])
        courses = (' '.join(course_name))
        return courses
        
        
class Attendence():
    def __init__(self) -> None:
        self.records = self.get_records(self)
        
    def get_records(self,c_id):
        attendance_records = execute_query(f"SELECT student_id, attendence FROM students_courses WHERE course_id = {c_id}")
        attendences = {}
        for s_id,attendence in attendance_records:
            attendences[s_id] = attendence
        return attendences 