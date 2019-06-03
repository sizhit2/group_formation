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
                    if individual.num_student_per_project[tentative_proj] <= max_per_project - add:
                        individual.chrom[stud] = tentative_proj
                        individual.dv_matrix[stud, tentative_proj] = 1
                        individual.dv_matrix[stud, crowded_proj] = 0
                        individual.num_student_per_project[tentative_proj] += add
                        individual.num_student_per_project[crowded_proj] -= add
                        break
                if individual.num_student_per_project[crowded_proj] <= max_per_project:
                    break  # break out of student loop
        if individual.num_student_per_project[crowded_proj] > max_per_project:
            print("infeasible project: " + str(crowded_proj))
    return individual

def compute_and_fix(population, max_per_project, student_list):
    population = fill_dv_matrix(population)
    population = repair_dv_matrix(population, max_per_project, student_list)
    return population



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
