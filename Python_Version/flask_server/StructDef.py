import numpy as np

class Student(object):
    """ Student objects hold data about the students. Data relevant for the simulation is the gpa, whether they
    selected a partner, and the preference list for the student."""

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

    def to_string(self):
        return "Student object:\nuin: {}, gpa: {}, first_name: {}, \
        last_name: {}, partner_first_name: {}, partner_last_name {}, \
        prefs: {}".format(self.uin, self.gpa, self.first_name, self.last_name,
                    self.partner_first_name, self.partner_last_name, self.project_preferences)

    def __str__(self):
        return "Student object:\nuin: {}, gpa: {}, first_name: {}, \
        last_name: {}, partner_first_name: {}, partner_last_name {}, \
        prefs: {}".format(self.uin, self.gpa, self.first_name, self.last_name,
                    self.partner_first_name, self.partner_last_name, self.project_preferences)


class Individual(object):
    """Class for individuals of the genetic algorithm simulation. """
    def __init__(self, num_projects, num_students, n_cross, parent=None):
        self.num_projects = num_projects  # number of projects
        self.num_students = num_students  # number of students
        self.parent = parent              # parents of the offspring
        self.n_cross = n_cross            # number of positions of crossover

        # Chromosome string for the individual
        # indices 0-num_students-1 hold the data for which project is assigned to the corresponding student
        # the last num_projects indices simply hold the project index.
        self.chrom = np.zeros(num_projects + num_students, dtype=int)

        # Sparse matrix, entries are 1 in row i column j if student i is assigned project j
        self.dv_matrix = np.zeros((num_students, num_projects), dtype=int)

        self.avg_gpa_per_project = np.zeros(num_projects)                 # list of num_projects elements
        self.num_student_per_project = np.zeros(num_projects, dtype=int)  # list of num_projects elements
        self.selected_project_to_swap = np.zeros(n_cross)                 # projects inherited from father

        self.fitness = 0.0                                 # fitness of the individual - associated to cost function
        self.cost_function_value = 0.0                     # cost function to be maximized, note: might be redundant
