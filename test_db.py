from setup_db import *
import requests

#pytest example

def test_db():
    students_num = int(execute_query("SELECT COUNT(id) FROM students")[0][0])
    assert students_num == 20

def test_teachers():
    teachers_num = int(execute_query("SELECT COUNT()id FROM teachers")[0][0])
    assert teachers_num == 4
       
def test_status():
    r = requests.get("http://127.0.0.1:5000/register/1/3")
    if r.status_code == 200:
        r=requests.get("http://127.0.0.1:5000/registrations/1")
        assert r.text.find("3") != -1