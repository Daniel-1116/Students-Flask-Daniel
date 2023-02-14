from setup_db import execute_query


class Course():
    def __init__(self,c_id,name,desc,teacher_id) -> None:
        self.c_id = c_id
        self.name = name
        self.desc = desc
        self.t_name = self.teacher_name(teacher_id)
        
    def teacher_name(self,teacher_id):
        name = [name[0] for name in execute_query(f"SELECT name FROM teachers WHERE id='{teacher_id}'")]
        return name[0]
    
    
class Student():
    def __init__(self,s_id,name,email) -> None:
        self.s_id = s_id
        self.name = name
        self.email = email
        self.course = self.assigned_course()
        
    def assigned_course(self):
        course_ids = [c_id[0] for c_id in execute_query(f"SELECT course_id FROM students_courses WHERE student_id='{self.s_id}'")]
        course_name = []
        for i in course_ids:
            name = [n[0] for n in execute_query(f"SELECT name FROM courses WHERE id={i}")]
            course_name.append(name[0])
        courses = (' '.join(course_name))
        return courses
        