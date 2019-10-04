from flask import Flask, escape, request
import json

from StructDef import *

app = Flask(__name__)
student_list = []

@app.route('/')
def hello():
	name = request.args.get("name", "the worst data")
# 	print (name)
	req_json = request.json
# 	print (req_json['name'])
	name = req_json['name']


	return "Got data {}\n\n".format(name)

@app.route('/StudentPreferenceData')
def get_student_data():
    f_name = request.args.get("first_name")
    l_name = request.args.get("last_name")
    uin = request.args.get("uin")
    gpa = request.args.get("gpa")
    partner_first_name = request.args.get("partner_first_name")
    partner_last_name = request.args.get("partner_first_name")
    partner_gpa = request.args.get("partner_gpa")
    prefs = request.args.get("project_preferences")
    selected_partner = False

    # if len(partner_first_name) > 0:
    #     selected_partner = True

    student = Student(gpa=gpa, selected_partner=selected_partner, last_name=l_name, first_name=f_name)
    student.update_partner_info(partner_last_name, partner_first_name, partner_gpa)
    student.update_project_preferences(prefs)
    print(student)
    student_list.append(student)
    return "Successful write"

@app.route('/StudentList')
def print_student_list():
    for stud in student_list:
        print (str(stud))
    if (len(student_list) == 0):
        print ("No data")
    return "Peace"
