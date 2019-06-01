import numpy as np

'''Struct to hold student-specific information.'''

class Student(object):

    def __init__(self, gpa=0.0, selected_partner=None, last_name='', first_name=''):
        self.uin = 0
        self.gpa = gpa
        self.selected_partner = selected_partner
        self.last_name = last_name
        self.first_name = first_name
        self.partner_last_name = ''
        self.partner_first_name = ''
        self.partner_gpa = 0.0
        self.project_preferences = None

    def update_partner_info(self, partner_last_name, partner_first_name, partner_gpa):
        self.partner_last_name = partner_last_name
        self.partner_first_name = partner_first_name
        self.partner_gpa = partner_gpa

    def update_project_preferences(self, prefs_array):
        self.project_preferences = prefs_array


'''Struct for individuals in the genetic algorithm simulation.'''
class Individual(object):
    def __init__(self, num_projects, num_students, n_cross, parent=None):
        self.num_projects = num_projects            # number of projects
        self.num_students = num_students            # number of students
        self.parent = parent                        # parents of the offspring

        self.chrom = np.zeros(num_projects + num_students)              # chromosome string for the individual
        self.dv_matrix = np.zeros((num_students, num_projects))         # associated student preference matrix (Design Variable Matrix)
        self.avg_gpa_per_project = np.zeros(num_projects)               # list of num_projects elements
        self.num_student_per_project = np.zeros(num_projects)           # list of num_projects elements
        self.selected_project_to_swap = np.zeros(n_cross)               # projects transferred from father to offspring

        self.fitness = 0.0                          # fitness of the individual - associated to cost function
        self.costfunctionvalue = 0.0                # cost function to be maximized
