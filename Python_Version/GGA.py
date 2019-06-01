# Main for Genetic Algorithm simulation
from StructDef import Student, Individual
from OptimizationFunctions import *
from InputOutput import *
from Initialize import initialize_population

def main():
    in_data = parse_input_data('../data/input_data.txt')

    # For the design variable matrix
    data_filename = in_data[0]
    num_students = in_data[1]
    num_projects = in_data[2]
    min_selected_projects = in_data[3]
    max_students_per_proj = in_data[4]

    # For the genetic algorithm
    population_size = in_data[5]
    crossover_prob = in_data[6]
    mutation_prob = in_data[7]
    n_keep = in_data[8]
    n_cross = in_data[9]
    reassign = in_data[10]

    # For the simulation
    max_iter = in_data[11]
    cost_tol = in_data[12]
    gamma = in_data[13]
    gamma_gpa = in_data[14]

    print ("Reading Excel data....")
    print (num_projects)
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv", (num_projects+1))
    student_pref_matrix = np.zeros((num_students, num_projects))
    for i, student in enumerate(student_list):
        student_pref_matrix[i, :] = student.project_preferences
    # TODO: evaluate max_cost
    print (student_pref_matrix[2, :])

    population = initialize_population(population_size, num_students, num_projects, n_cross)
    print ("Initial population generated...")

    iter = 0
    iter_check = 0
    change_cost_function = 10
    converged = False
    max_iter = 1
    while (iter < max_iter):
        population = create_design_var_matrix(population)
        population = repair_dv_matrix(population, max_students_per_proj, student_pref_matrix, student_list)




if __name__ == '__main__':
    main()
