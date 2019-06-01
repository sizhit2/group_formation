import csv
import re
from StructDef import Student

import pandas as pd

"""
Reads the CSV file with student info to create a list of student objects
:param filename: csv file to read from
:return: student_list (list of student objects, class roster with partners)
"""
def read_from_csv(filename):
    student_list = []
    reader = pd.read_csv(filename,delimiter = ',')
    for row in range(reader.shape[0]):
        last_name = reader['Last Name'][row]
        first_name = reader['First Name'][row]
        gpa = reader['GPA'][row]
        selected_partner = reader['Selected Partner?'][row]
        student = Student(gpa, selected_partner, last_name, first_name)
        student_list.append(student)
        if selected_partner:
            partner_last = reader['Partner Last'][row]
            partner_first = reader['Partner First'][row]
            partner_gpa = reader['Partner GPA'][row]
            student.update_partner_info(partner_last, partner_first, partner_gpa)
    return student_list

def parse_input_data(in_filename):
    in_data_file = open(in_filename, 'r+')
    in_data_lines = in_data_file.readlines()
    print (in_data_lines)

    # For the design variable matrix
    data_filename = in_data_lines[0].rstrip('\n')
    num_students = int (in_data_lines[1].rstrip('\n'))
    num_projects = int (in_data_lines[2].rstrip('\n'))
    min_selected_projects = int (in_data_lines[3].rstrip('\n'))
    max_students_per_proj = int (in_data_lines[4].rstrip('\n'))

    # For the genetic algorithm
    population_size = int (in_data_lines[5].rstrip('\n'))
    crossover_prob = float (in_data_lines[6].rstrip('\n'))
    mutation_prob = float (in_data_lines[7].rstrip('\n'))
    n_keep = int (in_data_lines[8].rstrip('\n'))
    n_cross = int (in_data_lines[9].rstrip('\n'))
    reassign = int (in_data_lines[10].rstrip('\n'))

    # For the simulation
    max_iter = int (in_data_lines[11].rstrip('\n'))
    cost_tol = float (in_data_lines[12].rstrip('\n'))
    gamma = float (in_data_lines[13].rstrip('\n'))
    gamma_gpa = float(in_data_lines[14].rstrip('\n'))

    in_data = []
    for (i, line) in enumerate(in_data_lines):
        line = line.rstrip('\n')
        if i == 0:
            continue
        if i in [6, 7, 12, 13, 14]:
            line = float(line)
        else:
            line = int(line)
        in_data.append(line)
    print (in_data)
    return in_data



'''Void function to test functionality implemented in this file'''
def test_main():
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv")
    # print (len(student_list))
    in_data = parse_input_data('../data/input_data.txt')
    # individualList = []

if __name__ == '__main__':
    test_main()
