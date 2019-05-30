import csv
from StructDef import MyStudent
# from StructDef import updatePartnerInfo

import pandas as pd


'''
int NumberOfProjects, struct MyStudent *Student, arma::mat& StudentPreferenceMatrix, std::string filename)
'''

'''Reads data from the csv file containing students' project preferences. Returns a list of MyStudent objects, encapsulating
    the relevant data. '''
def readFromCsv(NumberOfProject,studentList,StudentPreferenceMatrix,filename):
    student_list = []
    reader = pd.read_csv(filename,delimiter = ',')
    for row in range(reader.shape[0]):
        last_name = reader['Last Name'][row]
        first_name = reader['First Name'][row]
        gpa = reader['GPA'][row]
        selected_partner = reader['Selected Partner?'][row]
        student = MyStudent(gpa,selected_partner,last_name,first_name)
        student_list.append(student)
        if selected_partner:
            partner_last = reader['Partner Last'][row]
            partner_first = reader['Partner First'][row]
            partner_gpa = reader['Partner GPA'][row]
            student.updatePartnerInfo(partner_last, partner_first, partner_gpa)
    return student_list

def ReadInputData(in_filename):
    pass


'''Void function to test functionality implemented in this file'''
def test_main():
    student_list = readFromCsv(0,studentList,0,"StudentPreferenceSpring2019_PredetTeamRemoved.csv")
    individualList = []

if __name__ == '__main__':
    test_main()
