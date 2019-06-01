from StructDef import Student, Individual
import numpy as np

'''Function that creates the design variable matrix for all individuals in the given population.
    Mutates the population parameter, and returns it.'''
def create_design_var_matrix(population):
    # TODO: move this documentation
    '''The chrom field is a list of size num_students which holds which project the student is
    assigned. '''
    for individual in population:
        for j in range(individual.num_students):
            for k in range(individual.num_projects):
                if individual.chrom[j] == k:
                    individual.dv_matrix[j, k] = 1
                else:
                    individual.dv_matrix[j, k] = 0
    return population

'''Function that calculates number of students per projects
    for all individuals in the given population. Non-trivial, as some students
    can select a partner. Mutates the population parameter, and returns it.'''
def get_num_students_per_project(student_list, population):
    for individual in population:
        for i in range(individual.num_students):
            for j in range(individual.num_projects):
                if individual.dv_matrix[i, j] != 0:      # If student i has been assigned project j
                    if student_list[i].selected_partner: # If they selected a partner, add 2 to count
                        individual.num_student_per_project[j] += 2
                    else:                                # Otherwise, add 1
                        individual.num_student_per_project[j] += 1
    return population

'''Function that attempts to correct infeasibility in chromosomes across a population.
    Mutates the population parameter and returns it.'''
def repair_dv_matrix(population, max_per_project, student_pref_matrix, student_list):
    population = get_num_students_per_project(population)
    for individual in population:
        # Correct infeasibility in each individual

        for i in range(individual.num_projects):
            if individual.num_student_per_project[i] <= max_per_project: # if the project is feasible, continue
                continue
            crowded_proj = i
            for j in range(individual.num_students):
                # Find a student who picked the crowded project
                assigned_proj = individual.chrom[j]
                if assigned_proj == crowded_proj:
                    compatible_projs = np.argsort(student_pref_matrix[j, :]) # Sort the compatible projects based on student preference

                    # Compute how many students need to be moved around
                    if (student_list[j].selected_partner):
                        add = 2
                    else:
                        add = 1

                    # Now move the student(s) to a project based on preference
                    for k in range(individual.num_projects):
                        tentative_proj = compatible_projs[k]
                        if (individual.num_student_per_project[tentative_proj] <= max_per_project - add):
                            individual.chrom[j] = tentative_proj
                            individual.dv_matrix[j, assigned_proj] = 0
                            individual.dv_matrix[j, tentative_proj] = 1
                            individual.num_student_per_project[assigned_proj] -= add
                            individual.num_student_per_project[tentative_proj] += add
                            break

                # Back to j-loop
                if individual.num_student_per_project[i] <= max_per_project: # Leave the j loop if satisfied, else keep switching out students
                    break

            # i-loop
            if individual.num_student_per_project[i] > max_per_project:
                # raise Exception("Infeasible project: " + str(i))
                pass
    return population
