# Main for Genetic Algorithm simulation
from StructDef import Student, Individual
from OptimizationFunctions import *
from InputOutput import *
from Initialize import initialize_population
from GeneticAlgorithmFunctions import *
import copy

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
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv", (num_projects+1))
    student_pref_matrix = np.zeros((num_students, num_projects))
    max_satisfaction = 0
    for i, student in enumerate(student_list):
        student_pref_matrix[i, :] = student.project_preferences
        max_satisfaction += max(student_pref_matrix[i, :])

    class_avg_gpa = get_class_avg_gpa(student_list)
    avg_size_group = int(num_students / num_projects)

    population = initialize_population(population_size, num_students, num_projects, n_cross)
    print ("Initial population generated...")
    population = compute_and_fix(population, max_students_per_proj, student_list)
    population = evaluate_fitness(population, student_list, max_satisfaction, class_avg_gpa, avg_size_group, gamma_gpa, gamma)
    population.sort(key=lambda ind: ind.fitness, reverse=True)
    for ind in population:
        print (ind.fitness)
    best_chromosome = copy.deepcopy(population[0])
    best_cost = best_chromosome.fitness
    cost_val = best_cost

    iter = 0
    iter_check = 0
    change_cost_function = 10
    converged = False
    max_iter = 1
    while iter < max_iter:
        iter += 1

        # Form a new generation
        new_pop = crossover_with_random_offspring_generation(population, n_keep, crossover_prob)
        new_pop = apply_mutation(new_pop, mutation_prob, n_keep)
        new_pop = compute_and_fix(new_pop, max_students_per_proj, student_list)
        new_pop = evaluate_fitness(new_pop, student_list, max_satisfaction, class_avg_gpa, avg_size_group, gamma_gpa, gamma)

        # Sort by fitness, and grab most fit individual
        new_pop.sort(key= lambda ind: ind.fitness, reverse=True)
        new_cost_val = new_pop[0].fitness
        change_cost_function = abs(new_cost_val - cost_val) / new_cost_val
        # for (i, ind) in enumerate(population):
        #     print("Chromosome: ", str(i), "\n", ind.chrom, "\n", str(ind.num_student_per_project))

        # Update the best cost and chromosome if needed
        if (new_cost_val > best_cost):
            best_cost = new_cost_val
            best_chromosome = copy.deepcopy(new_pop[0])

        if change_cost_function < cost_tol:
            if not converged:
                iter_check = 0
                converged = True
            else:
                iter_check += 1
        else:
            converged = False
        if iter_check > 10 and converged and reassign == -1:
            reassign = 1
        if iter_check > 30 and converged:
            break

        # For the next iteration
        population = new_pop
        cost_val = new_cost_val
    print ("Final chromosome: \n", best_chromosome.chrom)
    print ("Final fitness: \n", best_chromosome.fitness)
    print ("Num students per project: \n", best_chromosome.num_student_per_project)
    # print ("Avg gpa per project: \n", best_chromosome.avg_gpa_per_project)

if __name__ == '__main__':
    main()
