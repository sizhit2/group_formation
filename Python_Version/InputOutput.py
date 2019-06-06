import csv
import re
from StructDef import Student

import pandas as pd
import numpy as np

"""
Reads the CSV file with student info to create a list of student objects
:param filename: csv file to read from
:return: student_list (list of student objects, class roster with partners)
"""
def read_from_csv(filename, num_projects):
    student_list = []
    reader = pd.read_csv(filename,delimiter = ',')
    for row in range(reader.shape[0]):
        last_name = reader['Last Name'][row]
        first_name = reader['First Name'][row]
        gpa = reader['GPA'][row]
        selected_partner = reader['Selected Partner?'][row]

        project_preferences = np.zeros(num_projects)
        ind = 0
        for i in range(num_projects):
            # if i == 4:              # Temporary, because Project 5 does not exist
            #     continue
            project_preferences[ind] = reader['Project ' + str(i+1)][row]
            ind += 1
        # project_preferences = project_preferences[:-1] # To fix an off-by-one error

        student = Student(gpa, selected_partner, last_name, first_name)
        student.update_project_preferences(project_preferences)
        if selected_partner:
            partner_last = reader['Partner Last'][row]
            partner_first = reader['Partner First'][row]
            partner_gpa = reader['Partner GPA'][row]
            student.update_partner_info(partner_last, partner_first, partner_gpa)
        student_list.append(student)
    return student_list

def parse_input_data(in_filename):
    in_data_file = open(in_filename, 'r+')
    in_data_lines = in_data_file.readlines()

    # Get the files in lines, then convert the elements to correct type
    in_data = []
    for (i, line) in enumerate(in_data_lines):
        line = line.rstrip('\n')
        if i == 0:
            pass
        elif i in [6, 7, 10, 12, 13, 14]:
            line = float(line)
        else:
            line = int(line)
        in_data.append(line)
    return in_data



'''Void function to test functionality implemented in this file'''
def test_main():
    student_list = read_from_csv("../data/Run10_noGPAweight/StudentPreferenceSpring2018.csv", num_projects=23)
    # print (len(student_list))
    print (student_list[2].project_preferences)
    print (len(student_list[2].project_preferences))
    in_data = parse_input_data("../data/Run10_noGPAweight/input_data.txt")
    print (len(in_data))
    print (in_data)
    # individualList = []

if __name__ == '__main__':
    test_main()
