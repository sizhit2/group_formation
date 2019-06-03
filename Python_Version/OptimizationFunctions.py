from StructDef import Student, Individual
from InputOutput import *
import numpy as np

'''Function that creates the design variable matrix for all individuals in the given population.
    Mutates the population parameter, and returns it.'''
def create_design_var_matrix(population):
    '''The chrom field is a list of size num_students which holds which project the student is
    assigned. '''
    for individual in population:
        for j in range(individual.num_students):
            k = individual.chrom[j]
            individual.dv_matrix[j, k] = 1
    return population

def create_dv_matrix_ind(individual):
    for j in range(individual.num_students):
        k = individual.chrom[j]
        individual.dv_matrix[j, k] = 1
    return individual

'''Function that calculates number of students per projects
    for all individuals in the given population. Non-trivial, as some students
    can select a partner. Mutates the population parameter, and returns it.'''
def get_num_students_per_project(student_list, population):
    for individual in population:
        for j in range(individual.num_students):
            if (student_list[j].selected_partner):
                add = 2
            else:
                add = 1
        individual.num_student_per_project[individual.chrom[j]] += add
    return population

def get_num_students_per_project_ind(individual, student_list):
    for j in range(individual.num_students):
        if (student_list[j].selected_partner):
            add = 2
        else:
            add = 1
        individual.num_student_per_project[individual.chrom[j]] += add
    return individual

'''Function that attempts to correct infeasibility in chromosomes across a population.
    Mutates the population parameter and returns it.'''
def repair_dv_matrix(population, max_per_project, student_pref_matrix, student_list):
    population = get_num_students_per_project(student_list, population)
    population = create_design_var_matrix(population)
    for individual in population:
        # Correct infeasibility in each individual

        for i in range(individual.num_projects):
            if individual.num_student_per_project[i] <= max_per_project: # if the project is feasible, continue
                continue
            crowded_proj = i
            # print ("found crowded project:" + str(i))
            for j in range(individual.num_students):
                # Find a student who picked the crowded project
                assigned_proj = int(individual.chrom[j])
                if assigned_proj == crowded_proj:
                    compatible_projs = np.argsort(student_pref_matrix[j, :])[::-1] # Sort the compatible projects based on student preference
                    # print (len(compatible_projs))
                    # print (compatible_projs)
                    # Compute how many students need to be moved around
                    if (student_list[j].selected_partner):
                        add = 2
                    else:
                        add = 1

                    # Now move the student(s) to a project based on preference
                    for k in range(individual.num_projects):
                        tentative_proj = compatible_projs[k]
                        if (individual.num_student_per_project[tentative_proj] < max_per_project):
                            individual.chrom[j] = tentative_proj
                            individual.dv_matrix[j, assigned_proj] = 0
                            individual.dv_matrix[j, tentative_proj] = 1
                            individual.num_student_per_project[assigned_proj] -= add
                            print (individual.num_student_per_project[assigned_proj])
                            individual.num_student_per_project[tentative_proj] += add
                            break

                # Back to j-loop
                if individual.num_student_per_project[i] <= max_per_project: # Leave the j loop if satisfied, else keep switching out students
                    print ("Resolved project: " + str(i))
                    break

            # i-loop
            if individual.num_student_per_project[i] > max_per_project:
                # raise Exception("Infeasible project: " + str(i))
                # print ("skipped over project " + str(i))
                pass
    return population

def repair_dv_matrix_individual(individual, max_per_project, student_pref_matrix, student_list):
    individual = get_num_students_per_project_ind(individual, student_list)
    individual = create_dv_matrix_ind(individual)

    print ("Before:")
    print (individual.chrom)
    print (individual.num_student_per_project)

    for proj in range(individual.num_projects):
        if individual.num_student_per_project[proj] <= max_per_project:
            continue
        crowded_proj = proj
        for stud in range(individual.num_students):
            if (individual.chrom[stud] == crowded_proj):
                if student_list[stud].selected_partner:
                    add = 2
                else:
                    add = 1
                compatible_projs = np.argsort(student_list[stud].project_preferences)[::-1]
                for tentative_proj in compatible_projs:
                    # If we can fit this student into the project of their preference do it
                    if (individual.num_student_per_project[tentative_proj] <= max_per_project - add):
                        individual.chrom[stud] = tentative_proj
                        individual.dv_matrix[stud, tentative_proj] = 1
                        individual.dv_matrix[stud, crowded_proj] = 0
                        individual.num_student_per_project[tentative_proj] += add
                        individual.num_student_per_project[crowded_proj] -= add
                        break
                if (individual.num_student_per_project[crowded_proj] <= max_per_project):
                    break # break out of student loop
        if (individual.num_student_per_project[crowded_proj] > max_per_project):
            print ("infeasible project: " + str(crowded_proj))
    return individual

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
    # ind = get_num_students_per_project_ind(student_list, ind)
    # print (ind.num_student_per_project)
    # ind = create_dv_matrix_ind(ind)
    ind = repair_dv_matrix_individual(ind, 5, student_pref_matrix, student_list)
    print ("After:")
    print (ind.chrom)
    print (sum(ind.num_student_per_project))

    print (len([stud for stud in student_list if stud.selected_partner]))


if __name__ == '__main__':
    test_main()
