import copy
import numpy as np
from InputOutput import *
from StructDef import *
from OptimizationFunctions import *
from Initialize import *

def roulette_wheel(population):
    size = len(population)
    temp_s = 0.0
    pick = np.random.rand()
    i = 0
    while i < size and temp_s < pick:
        temp_s += np.random.rand() / 4
        i += 1

    if i > 0:
        return (i-1)
    return i


'''Assumes that population is sorted by fitness/cost value in descending order'''
def crossover_with_random_offspring_generation(population, n_keep, crossover_prob):
    population_size = len(population)
    new_population = []
    for i in range(n_keep):
        ind = copy.copy(population[i])
        ind.parent = [i, i]
        new_population.append(ind)

    temp_ind = population[0]
    num_projects = temp_ind.num_projects
    num_students = temp_ind.num_students
    n_cross = temp_ind.n_cross

    while len(new_population) < population_size:
        flip = np.random.rand()
        if flip < crossover_prob:
            father_index = roulette_wheel(population)
            mother_index = roulette_wheel(population)
            while mother_index == father_index:
                mother_index = roulette_wheel(population)
            parents = [mother_index, father_index]
            ind = Individual(num_projects, num_students, n_cross, parent=parents)
            ind.chrom = np.array(population[mother_index].chrom)
            for k in range(n_cross):
                select_project = np.random.randint(0, high=num_projects)
                if k > 0 and select_project in ind.selected_project_to_swap: # don't repeat swaps
                    continue
                for stud in range(num_students):
                    if population[father_index].chrom[stud] == select_project:
                        ind.chrom[stud] = select_project
                ind.selected_project_to_swap[k] = select_project
        else: # if flip > crossover prob, generate at random
            parent = len(new_population) - 1
            ind = Individual(num_projects, num_students, n_cross, parent=[parent, parent])
            for i in range(num_students):
                ind.chrom[i] = np.random.randint(0, high=num_projects)

        new_population.append(ind)
    return new_population

def test_main():
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv", 28)
    population = initialize_population(population_size=10, num_students=100, num_projects=27, n_cross=2)
    new_pop = crossover_with_random_offspring_generation(population, 2, 0.95)
    print (len(new_pop))
    for ind in new_pop:
        if ind.parent[0] != ind.parent[1]:
            print (population[ind.parent[0]].chrom, population[ind.parent[1]].chrom, ind.chrom)
            break

if __name__ == '__main__':
    test_main()
