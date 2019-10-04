from flask import Flask, escape, request
import json

from StructDef import *
from GGA_Server import *

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
	print ("hello")
	req_json = request.json
	print (req_json)
	f_name = req_json['first_name']
	l_name = req_json['last_name']
	uin = req_json['uin']
	gpa = req_json['gpa']
	partner_first_name = req_json['partner_first_name']
	partner_last_name = req_json['partner_last_name']
	partner_gpa = req_json['partner_gpa']
	prefs = req_json['prefs']
	selected_partner = False

	# if len(partner_first_name) > 0:
	#     selected_partner = True

	student = Student(gpa=gpa, selected_partner=selected_partner, last_name=l_name, first_name=f_name)
	student.update_partner_info(partner_last_name, partner_first_name, partner_gpa)
	student.update_project_preferences(prefs)
	print(student)
	student_list.append(student)
	return "Successful write\n"

@app.route('/StudentList')
def print_student_list():
    for stud in student_list:
        print (str(stud))
    if (len(student_list) == 0):
        print ("No data\n")
    return "Peace\n"

@app.route('/GA')
def drive_ga():
	num_students = len(student_list)
	num_projects = 3
	max_students_per_proj = 3
	run_ga(student_list, num_students, num_projects, max_students_per_proj)
	return "Success? You may or may not have the run the GA\n"
