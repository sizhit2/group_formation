import csv
import re
from StructDef import Student
from StructDef import Individual

import pandas as pd
import numpy as np

def read_from_csv(filename, num_projects):
    """
    Reads the CSV file with student info to create a list of student objects. Ensure that projects are numbered
    contiguously, else parsing correctness is not assured.
    :param filename: csv file to read. format for CSV must be followed
    :param num_projects: number of projects in simulation
    :return: list of Student objects for the class
    """
    student_list = []
    with open(filename, 'r+') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for ind, row in enumerate(reader):
            if ind == 0:
                continue
            last_name = row[0]
            first_name = row[1]
            if row[2]:
                gpa = float(row[2])
            else:
                gpa = 0.0
            selected_partner = int(row[3])

            project_preferences = np.zeros(num_projects)
            for i in range(num_projects):
                project_preferences[i] = int(row[4+i])

            student = Student(gpa, selected_partner, last_name, first_name)
            student.update_project_preferences(project_preferences)
            if selected_partner:
                partner_last = row[-5]
                partner_first = row[-4]
                if row[-3]:
                    partner_gpa = row[-3]
                else:
                    partner_gpa = 0.0
                student.update_partner_info(partner_last, partner_first, partner_gpa)
            student_list.append(student)
    return student_list


def parse_input_data(in_filename):
    """
    Grabs input parameters to the GA simulation from a text file.
    :param in_filename: file to read for values
    :return: list of values to initialize the GA simulation.
    """
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

def export_individual_to_csv(ind, student_list, dir='../data/output/',
                            filename='final_teams.csv'):
    """
    Exports a configuration of students in teams to a given file.
    :param ind: chromosome with data to be written
    :param student_list: list with student data for reference
    :param filename: file to write to
    :return: True if successful write.
    """
    header = ['Project', 'Average GPA', 'Group satisfaction', 'Student names']
    print ("Writing to output file: " + dir + filename)
    with open(dir+filename, 'w+') as out_file:
        data_writer = csv.writer(out_file, delimiter=',')
        data_writer.writerow(header)

        # Track data while traversing file
        unsatisfied_students = []
        num_unsatisfied = 0
        total_satisfaction = 0

        for row in range(ind.num_projects):
            # Finding teams for each project
            student_names = []
            group_satisfaction = 0
            for stud in range(ind.num_students):
                if ind.chrom[stud] == row:
                    student = student_list[stud]
                    name = student.first_name.capitalize() + ' ' + student.last_name.capitalize()
                    student_names.append(name)
                    if student.selected_partner:
                        p_name = str(student.partner_first_name).capitalize()
                        p_name += ' ' + str(student.partner_last_name).capitalize()
                        p_name += '*'
                        student_names.append(p_name)

                    sat = student.project_preferences[row]
                    group_satisfaction += sat
                    total_satisfaction += sat
                    if sat == 0:
                        num_unsatisfied += 1
                        unsatisfied_students.append(name)
            write_row = [row+1, None, group_satisfaction] + student_names
            data_writer.writerow(write_row)

        # Write empty row
        data_writer.writerow([])
        data_writer.writerow(['Total satisfaction', total_satisfaction])
        data_writer.writerow(['Num unsatisfied', num_unsatisfied])
        data_writer.writerow(['Unsatisfied students'] + unsatisfied_students)
        data_writer.writerow(['* - student is a partner of student to the left'])

    print ('Data written to ' + dir + filename)
    return True

# Void function to test functionality implemented here
def test_main():
    student_list = read_from_csv("../data/Run10_noGPAweight/StudentPreferenceSpring2018.csv", num_projects=23)
    # print (len(student_list))
    print(student_list[2].project_preferences)
    print(len(student_list[2].project_preferences))
    in_data = parse_input_data("../data/Run10_noGPAweight/input_data.txt")
    print(len(in_data))
    print(in_data)
    # individualList = []


if __name__ == '__main__':
    test_main()
