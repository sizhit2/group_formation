from StructDef import Student, Individual
from InputOutput import *
import numpy as np


'''Function that creates the design variable matrix for all individuals in the given population.
    Mutates the population parameter, and returns it.'''
def fill_dv_matrix(population):
    '''The chrom field is a list of size num_students which holds which project the student is
    assigned. '''
    for individual in population:
        individual = fill_ind_dv_matrix(individual)
    return population

'''Fills design variable matrix based on projects assigned by the chromosome.'''
def fill_ind_dv_matrix(individual):
    for j in range(individual.num_students):
        k = individual.chrom[j]
        individual.dv_matrix[j, k] = 1
    return individual


'''Function that calculates number of students per projects
    for all individuals in the given population. Non-trivial, as some students
    can select a partner. Mutates the population parameter, and returns it.'''
def get_num_students_per_project(population, student_list):
    for individual in population:
        individual = get_ind_students_per_project_ind(individual, student_list)
    return population

'''Calculates number of students per project for an individual. Non-trivial, as
students can select a partner.'''
def get_ind_students_per_project_ind(individual, student_list):
    for j in range(individual.num_students):
        if student_list[j].selected_partner:
            add = 2
        else:
            add = 1
        individual.num_student_per_project[individual.chrom[j]] += add
    return individual


'''Function that attempts to correct infeasibility in chromosomes across a population.
    Mutates the population parameter and returns it.'''
def repair_dv_matrix(population, max_per_project, student_list):
    population = get_num_students_per_project(population, student_list)
    for individual in population:
        # Correct infeasibility in each individual
        individual = repair_ind_dv_matrix(individual, max_per_project, student_list)
    return population

'''Attempts to fix infeasibility (more than max_per_project students assigned to a project),
does not stop for infeasible projects. Mutates the individual, and returns'''
def repair_ind_dv_matrix(individual, max_per_project, student_list):
    for proj in range(individual.num_projects):
        if individual.num_student_per_project[proj] <= max_per_project:
            continue
        crowded_proj = proj
        for stud in range(individual.num_students):
            if individual.chrom[stud] == crowded_proj:
                if student_list[stud].selected_partner:
                    add = 2
                else:
                    add = 1
                compatible_projs = np.argsort(student_list[stud].project_preferences)[::-1]
                for tentative_proj in compatible_projs:
                    # If we can fit this student into the project of their preference do it
                    if individual.num_student_per_project[tentative_proj] <= (max_per_project - add):
                        individual.chrom[stud] = tentative_proj
                        individual.dv_matrix[stud, tentative_proj] = 1
                        individual.dv_matrix[stud, crowded_proj] = 0
                        individual.num_student_per_project[tentative_proj] += add
                        individual.num_student_per_project[crowded_proj] -= add
                        break
                if individual.num_student_per_project[crowded_proj] <= max_per_project:
                    break  # break out of student loop
        if individual.num_student_per_project[crowded_proj] > max_per_project:
            # print("infeasible project: " + str(crowded_proj))
            pass
    return individual

'''Fills the design variable matrix for each individual in a population and attempts
to fix for infeasibility. With certain chromosomes it may be impossible, but the
algorithm will not stop for this. Mutates and returns the population parameter.'''
def compute_and_fix(population, max_per_project, student_list):
    population = fill_dv_matrix(population)
    population = repair_dv_matrix(population, max_per_project, student_list)
    return population

'''Evaluates the fitness of a given individual in a population. The fitness is
a combination of student satisfaction, variance of number of students in each project,
and the variance of the average gpa per project. Tries to minimize the variances,
and maximize the student satisfaction.'''
def evaluate_ind_fitness(individual, student_list, max_satisfaction, class_avg_gpa, avg_size_group = 5, gamma_gpa=0.0, gamma=0.0):
    satisfaction_score = 0
    for (i, proj) in enumerate(individual.chrom[:individual.num_students]):
        # Student i was assigned project proj
        student = student_list[i]
        satisfaction_score += student.project_preferences[proj]
    # Normalize the satisfaction_score based on max_satisfaction
    satisfaction_score = satisfaction_score / max_satisfaction

    # Cost associated with number of students per group
    sigma = 0
    if abs(gamma) > 0.0:
        for i in range(individual.num_projects):
            sigma += (((individual.num_student_per_project[i]) - avg_size_group) / avg_size_group)**2
        sigma = sigma / individual.num_projects

    # Cost associated with average GPA per project
    sigma_gpa = 0
    if abs(gamma_gpa) > 0.0:
        fictitious_num_students = np.zeros(individual.num_projects)
        for stud in range(individual.num_students):
            # Account for partners
            pair_gpa = student_list[stud].gpa
            if (student_list[stud].selected_partner):
                pair_gpa += student_list[stud].partner_gpa
                pair_gpa = pair_gpa / 2

            # Add all GPAs per project
            for proj in range(individual.num_projects):
                fictitious_num_students[proj] += individual.dv_matrix[stud, proj]
                individual.avg_gpa_per_project[proj] += pair_gpa * individual.dv_matrix[stud, proj]

        # Getting variance of average GPA per project
        for proj in range(individual.num_projects):
            if fictitious_num_students[proj] != 0:
                individual.avg_gpa_per_project[proj] /= fictitious_num_students[proj]
                sigma_gpa += (individual.avg_gpa_per_project[proj] - class_avg_gpa) ** 2
        sigma_gpa /= individual.num_projects

    # Combine the 3 costs to get the final fitness
    individual.fitness = satisfaction_score
    if sigma > 0:
        individual.fitness += gamma * (1.0 - sigma)
    if sigma_gpa > 0:
        individual.fitness += gamma_gpa * (1.0 - sigma_gpa)

    individual.cost_function_value = individual.fitness
    return individual

'''Evaluates fitness of each individual of a population, updates and returns it.'''
def evaluate_fitness(population, student_list, max_satisfaction, class_avg_gpa, avg_size_group = 5, gamma_gpa=0.0, gamma=0.0):
    for individual in population:
        individual = evaluate_ind_fitness(individual, student_list, max_satisfaction, class_avg_gpa, avg_size_group, gamma_gpa, gamma)
    return population

'''Calculates average gpa of the class. '''
def get_class_avg_gpa(student_list):
    sigma_gpa = 0.0
    num_students = 0
    for student in student_list:
        if student.selected_partner:
            sigma_gpa += (student.gpa + student.partner_gpa) / 2.0
            num_students += 2
        else:
            sigma_gpa += student.gpa
            num_students += 1
    return sigma_gpa / num_students

'''Reassigns students in the top 5 percent of fit individuals. Assumes that the population
comes in sorted by fitness. Only does the reassign if it increases the fitness.
Evaluate fitness once again after reassign. '''
def reassign_students(population, student_list, reassign_prob, max_per_project):
    for i in range(len(population) // 20):
        ind = population[i]
        for j in range(ind.num_students):
            student = student_list[j]
            assigned_proj = ind.chrom[j]
            found = False
            reassign_student = True

            # Account for partners
            if (student.selected_partner):
                add = 2
            else:
                add = 1

            if reassign_prob < 1:
                flip = np.random.rand()
                if flip > reassign_prob: # Reassign students with probability reassign_prob
                     reassign_student = False

            # If the student is assigned an unfavorable project, and reassign is true
            if student.project_preferences[assigned_proj] == 0 and reassign_student:
                tentative_projs = np.argsort(student.project_preferences)[::-1]
                for tentative_proj in tentative_projs:
                    # If we only have unfavorable projects, skip and don't reassign
                    if student.project_preferences[tentative_proj] == 0:
                        break

                    # We are assured that the student prefers tentaive project,
                    # so this should increase fitness
                    if ind.num_student_per_project[tentative_proj] <= (max_per_project - add):
                        ind.chrom[j] = tentative_proj
                        ind.dv_matrix[j, tentative_proj] = 1
                        ind.dv_matrix[j, assigned_proj] = 0
                        ind.num_student_per_project[tentative_proj] += add
                        ind.num_student_per_project[assigned_proj] -= add
                        found = True
                        break
    return population

def get_num_satisfied_students(individual, student_list):
    num_students_picked_project = 0
    for stud in range(len(student_list)):
        student = student_list[stud]
        satisfaction = student.project_preferences[individual.chrom[stud]]
        if satisfaction > 0:
            num_students_picked_project += 1
    return num_students_picked_project

def test_main():
    num_projects = 27
    num_students = 100
    ind = Individual(num_projects, num_students, 2)

    # Get student list and preference matrix
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv", 28)
    student_pref_matrix = np.zeros((100, 27))
    for i, student in enumerate(student_list):
        student_pref_matrix[i, :] = student.project_preferences

    for j in range(num_students):
        ind.chrom[j] = np.random.randint(0, high=num_projects)
    for j in range(num_projects):
        ind.chrom[num_students + j] = j

    # print (ind.chrom)
    # ind = get_ind_students_per_project_ind(student_list, ind)
    # print (ind.num_student_per_project)
    # ind = fill_ind_dv_matrix(ind)
    ind = repair_ind_dv_matrix(ind, 5, student_list)
    print("After:")
    print(ind.chrom)
    print(sum(ind.num_student_per_project))

    print(len([stud for stud in student_list if stud.selected_partner]))

if __name__ == '__main__':
    test_main()
