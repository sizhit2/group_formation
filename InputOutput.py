import csv
from StructDef import MyStudent
# from StructDef import updatePartnerInfo

import pandas as pd
'''
int NumberOfProjects, struct MyStudent *Student, arma::mat& StudentPreferenceMatrix, std::string filename)
'''
studentList = []
individualList = []
    
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



