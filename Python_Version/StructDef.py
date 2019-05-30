import numpy as np
class MyStudent(object):
    def __init__(self,GPA,SelectedPartner,LastName,FirstName):
        '''
    char LastName[40]; 
	char FirstName[40];
	char PartnerLastName[40]; 
	char PartnerFirstName[40];

    maybe change the representation later 
        '''
        self.uin = 0
        self.GPA = 0.0
        self.SelectedPartner = 0
        self.LastName = None 
        self.FirstName = None
        self.PartnerLastName = None
        self.PartnerFirstName = None
        self.PartnerGPA = 0.0
    
    def updatePartnerInfo(self,partnerlastname,partnerfirstname,partnergpa):
        self.PartnerLastName = partnerlastname
        self.PartnerFirstName = partnerfirstname
        self.PartnerGPA = partnergpa



class Individual(object):
    def __init__(self):
        '''
    arma::ivec chrom;                   /* chromosome string for the individual */
    double     fitness;                 /* fitness of the individual  - associatated to cost function */
	double     costfunctionvalue;       /* cost function to be maximized */
    arma::ivec SelectedProjectToSwap;   /* projects transferred from father to offspring */
    arma::ivec parent;                  /* parents of the offspring */
	arma::imat DesignVariableMatrix;    // associated with the StudentPreference matrix 
	arma::vec  AverageGPAPerProject;    
	arma::ivec NumberOfStudentPerProject;
        '''
        self.chrom = None
        self.fitness = 0.0
        self.costfunctionvalue = 0.0
        self.SelectedProjectToSwap = None
        self.parent = None
        self.DesignVariableMatrix = None
        self.AverageGPAPerProject = None
        self.NumberOfStudentPerProject = None




