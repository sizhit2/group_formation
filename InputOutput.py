import csv
from StructDef import MyStudent
# from StructDef import updatePartnerInfo

import pandas as pd
'''
int NumberOfProjects, struct MyStudent *Student, arma::mat& StudentPreferenceMatrix, std::string filename)
'''
studentList = []
'''
def readFromCsv(NumberOfProject,studentList,StudentPreferenceMatrix,filename):
    csv_reader = csv.reader(filename,delimiter = ',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            if line_count == 1:
                print(f'\t{row["Lastname"]}')
                #print(lastname)
            #print(row)
        line_count += 1
readFromCsv(0,0,0,"StudentPreferenceSpring2019_PredetTeamRemoved.csv")
'''     
def readFromCsv(NumberOfProject,studentList,StudentPreferenceMatrix,filename):
    reader = pd.read_csv(filename,delimiter = ',')
    for row in range(reader.shape[0]):
        lastname = reader['Last Name'][row]
        firstname = reader['First Name'][row]
        GPA = reader['GPA'][row]
        selectedPartner = reader['Selected Partner?'][row]
        stu = MyStudent(GPA,selectedPartner,lastname,firstname)
        studentList.append(stu)
        if selectedPartner:
            partnerlast = reader['Partner Last'][row]
            partnerfirst = reader['Partner First'][row]
            partnerGPA = reader['Partner GPA'][row]
            stu.updatePartnerInfo(partnerlast,partnerfirst,partnerGPA)
            
        

        

readFromCsv(0,studentList,0,"StudentPreferenceSpring2019_PredetTeamRemoved.csv")
print(len(studentList))


