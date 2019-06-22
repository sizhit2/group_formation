# Main for Genetic Algorithm simulation
from StructDef import Student, Individual
from OptimizationFunctions import OptimizationFunctions
from InputOutput import *
from GeneticAlgorithmFunctions import GeneticAlgorithmFunctions
import copy
import time

def run_ga(dir='../data/Run10_noGPAweight/'):
    in_data = parse_input_data(dir+'input_data.txt')

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

    # gamma_gpa = 0  # Comment out this line when considering GPA

    print ("Reading Excel data....")
    student_list = read_from_csv(dir+data_filename, num_projects)
    student_pref_matrix = np.zeros((num_students, num_projects))
    max_satisfaction = 0
    for i, student in enumerate(student_list):
        student_pref_matrix[i, :] = student.project_preferences
        max_satisfaction += max(student_pref_matrix[i, :])

    class_avg_gpa = OptimizationFunctions.get_class_avg_gpa(student_list)
    avg_size_group = int(num_students / num_projects)

    population = GeneticAlgorithmFunctions.initialize_population(population_size, num_students, num_projects, n_cross)
    print ("Initial population generated...")
    population = OptimizationFunctions.compute_and_fix(population, max_students_per_proj, student_list)
    population = OptimizationFunctions.evaluate_fitness(population, student_list, max_satisfaction, class_avg_gpa,
                                                        avg_size_group, gamma_gpa, gamma)
    population.sort(key=lambda ind: ind.fitness, reverse=True)
    # for ind in population:
    #     print (ind.fitness)
    best_chromosome = copy.deepcopy(population[0])
    best_cost = best_chromosome.fitness
    cost_val = best_cost

    iter = 0
    iter_check = 0
    change_cost_function = 10
    converged = False
    reassign_helped = 0         # To check effectiveness of reassign
    reassign_generations = []   # Generations wherein reassigning helped at least one individual
    most_satisfied = 0

    start = time.time()
    while iter < max_iter:
        iter += 1
        if iter % 100 == 0:
            print ("Generation #", iter)
        # Form a new generation
        new_pop = GeneticAlgorithmFunctions.crossover_with_random_offspring_generation(population, n_keep,
                                                                                       crossover_prob)
        new_pop = GeneticAlgorithmFunctions.apply_mutation(new_pop, mutation_prob, n_keep)
        new_pop = OptimizationFunctions.compute_and_fix(new_pop, max_students_per_proj, student_list)
        new_pop = OptimizationFunctions.evaluate_fitness(new_pop, student_list, max_satisfaction, class_avg_gpa,
                                                             avg_size_group, gamma_gpa, gamma)

        # Sort by fitness, and grab most fit individual
        new_pop.sort(key=lambda ind: ind.fitness, reverse=True)

        # To check if reassign increases fitness:
        # temp_cost_val = new_pop[0].fitness

        # Reassign and re-evaluate fitness
        # new_pop = reassign_students(new_pop, student_list, reassign, max_students_per_proj)
        # new_pop = evaluate_fitness(new_pop, student_list, max_satisfaction, class_avg_gpa, avg_size_group, gamma_gpa, gamma)
        # new_pop.sort(key= lambda ind: ind.fitness, reverse=True)

        new_cost_val = new_pop[0].fitness
        change_cost_function = abs(new_cost_val - cost_val) / new_cost_val

        # if new_cost_val > temp_cost_val:
        #     reassign_helped += 1
        #     reassign_generations.append(iter)

        # Update the best cost and chromosome if needed
        if new_cost_val > best_cost:
            best_cost = new_cost_val
            best_chromosome = copy.deepcopy(new_pop[0])
            most_satisfied = OptimizationFunctions.get_num_satisfied_students(best_chromosome, student_list)

        # If at the same cost, we have fewer students in unfavorable projects
        # make that the best chromosome
        elif new_cost_val == best_cost:
            satisfied = OptimizationFunctions.get_num_satisfied_students(new_pop[0], student_list)
            if satisfied > most_satisfied:
                most_satisfied = satisfied
                best_chromosome = copy.deepcopy(new_pop[0])

        # Convergence checks: Once cost function stops changing, make sure we stay converged for 30 iterations
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

    else:  # Loop else to check if termination was due to convergence or maximum iterations
        print("Max iter reached..")

    seconds_taken = time.time() - start
    print("Final chromosome: \n", best_chromosome.chrom)

    # Get some insights on achieved configuration
    total_satisfaction = 0
    num_students_picked_project = 0
    num_students_unfavorable = 0
    for stud in range(len(student_list)):
        student = student_list[stud]
        satisfaction = student.project_preferences[best_chromosome.chrom[stud]]
        total_satisfaction += satisfaction
        if satisfaction > 0:
            num_students_picked_project += 1
        else:
            num_students_unfavorable += 1

    print("Total satisfaction:\n", total_satisfaction)
    print("Max satisfaction:\n", max_satisfaction)
    print("# students in projects they picked:", num_students_picked_project)
    print("# students in projects they did not pick:", num_students_unfavorable)
    print("Final fitness: \n", best_chromosome.fitness)
    print("Num students per project: \n", best_chromosome.num_student_per_project)
    # print ("Reassigning students helped in %d generations" % reassign_helped)
    # print ("Generations benefitting from reassign:", reassign_generations)
    print("Number of generations to converge: %d" % iter)
    print("Execution time %dm %ds" % (int(seconds_taken) / 60, int(seconds_taken) % 60))
    # print ("Avg gpa per project: \n", best_chromosome.avg_gpa_per_project)
    export_individual_to_csv(best_chromosome, student_list)
    return (total_satisfaction, most_satisfied, best_chromosome.fitness, best_chromosome.num_student_per_project,
            iter, seconds_taken)


# Temporary to run on new data
def t_main():
    run_ga()

def main():
    num_iter = 5
    ga_results = []
    best_fitness = 0
    fit_index = 0
    most_satisfied = 0
    msat_index = 0
    best_satisfaction = 0
    bsat_index = 0
    for i in range(num_iter):
        print("\nRun #%d" % (i+1))
        result = run_ga()
        if len(ga_results) == 0:
            best_fitness = result[2]
            best_satisfaction = result[0]
            most_satisfied = result[1]
        else:
            if result[2] > best_fitness:
                fit_index = i
                best_fitness = result[2]
            if result[0] > best_satisfaction:
                bsat_index = i
                best_satisfaction = result[0]
            if result[1] == most_satisfied:
                if result[0] == best_satisfaction:
                    msat_index = i
                    most_satisfied = result[1]
            if result[1] > most_satisfied:
                msat_index = i
                most_satisfied = result[1]
        ga_results.append(result)

    print("Best run for fitness: %d" % (fit_index+1))
    print("Best run for total satisfaction: %d" % (bsat_index+1))
    print("Best run for # students satisfied: %d" % (msat_index+1))


if __name__ == '__main__':
    t_main()
