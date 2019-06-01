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

    def update_partner_info(self, partner_last_name, partner_first_name, partner_gpa):
        self.partner_last_name = partner_last_name
        self.partner_first_name = partner_first_name
        self.partner_gpa = partner_gpa


'''Struct for individuals in the genetic algorithm simulation.'''
class Individual(object):
    def __init__(self):
        self.chrom = None                           # chromosome string for the individual
        self.fitness = 0.0                          # fitness of the individual - associated to cost function
        self.costfunctionvalue = 0.0                # cost function to be maximized
        self.selected_project_to_swap = None        # projects transferred from father to offspring
        self.parent = None                          # parents of the offspring
        self.dv_matrix = None                       # associated student preference matrix (Design Variable Matrix)
        self.num_projects = 0                       # number of projects
        self.num_students = 0                       # number of students
        self.avg_gpa_per_project = None             # list of num_projects elements
        self.num_student_per_project = None         # list of num_projects elements
