import copy
import numpy as np
from InputOutput import *
from StructDef import *
from OptimizationFunctions import *

class GeneticAlgorithmFunctions(object):

    @staticmethod
    def initialize_population(population_size, num_students, num_projects, n_cross):
        """
        Sets up the initial population, with random chromosomes.
        :param n_cross: Number of points of crossover, needed by constructor
        :return: list of individuals of size population_size
        """
        population = []
        for i in range(population_size):
            ind = Individual(num_projects, num_students, n_cross, parent=None)
            for j in range(num_students):
                ind.chrom[j] = np.random.randint(0, high=num_projects)
            for j in range(num_projects):
                ind.chrom[num_students + j] = j
            population.append(ind)
        return population

    @staticmethod
    def roulette_wheel(population):
        """
        Roulette wheel to pseudo-randomize choice of parents.
        :param population: list of individuals
        :return: index of parent chosen
        """
        size = len(population)
        temp_s = 0.0
        pick = np.random.rand() * 10

        i = 0
        while i < size and temp_s < pick:
            temp_s += population[i].fitness
            i += 1

        if i > 0:
            return (i-1)
        return i

    @staticmethod
    def crossover_with_random_offspring_generation(population, n_keep, crossover_prob):
        """Uses individuals from the current population to spawn a new generation.
        Assumes that population is sorted by fitness/cost value in descending order.
        :param population: old population to use for breeding
        :param n_keep: number of individuals to keep from previous generation
        :param crossover_prob: probability of crossover taking place (~0.95)
        :return: a new population based on breeding of the old population.
        """

        population_size = len(population)
        new_population = []

        # Keep the best n_keep individuals from the last generation
        for i in range(n_keep):
            ind = copy.copy(population[i])
            ind.parent = [i, i]
            new_population.append(ind)

        # Just to gather variables
        temp_ind = population[0]
        num_projects = temp_ind.num_projects
        num_students = temp_ind.num_students
        n_cross = temp_ind.n_cross

        # Add individuals to the new population. If crossover occurs, then an
        # individual will share parts of its chromosome with 2 individuals from
        # the old population. Else, the chromosome is randomly generated.
        while len(new_population) < population_size:
            flip = np.random.rand()
            if flip < crossover_prob:
                father_index = GeneticAlgorithmFunctions.roulette_wheel(population)
                mother_index = GeneticAlgorithmFunctions.roulette_wheel(population)

                # Try to ensure to inherit from different parents
                # May not be possible when the fitnesses are lower, hence we try to inherit
                # from different parents, unless it is not possible
                fail_safe = 5
                iter = 0
                while mother_index == father_index and iter < fail_safe: # Ensure to inherit from different parents
                    mother_index = GeneticAlgorithmFunctions.roulette_wheel(population)
                    iter += 1

                parents = [mother_index, father_index]
                ind = Individual(num_projects, num_students, n_cross, parent=parents)
                ind.chrom = np.array(population[mother_index].chrom)

                swapped_projects = []
                # For the n_cross points of crossover
                for k in range(n_cross):
                    select_project = np.random.randint(0, high=num_projects)

                    if select_project in swapped_projects:  # don't repeat swaps
                        continue
                    for stud in range(num_students):
                        if population[father_index].chrom[stud] == select_project:
                            ind.chrom[stud] = select_project

                    ind.selected_project_to_swap[k] = select_project
                    swapped_projects.append(select_project)
            else: # if flip > crossover prob, generate at random
                parent = len(new_population) - 1
                ind = Individual(num_projects, num_students, n_cross, parent=[parent, parent])
                for i in range(num_students):
                    ind.chrom[i] = np.random.randint(0, high=num_projects)

            new_population.append(ind)
        return new_population

    @staticmethod
    def apply_mutation(population, mutation_prob, n_keep):
        """
        Applies mutation to a population. The mutation works on all the individuals not kept from the previous
        generation. Works by picking 2 random students and swapping their projects. Thus, mutation maintains the
        feasibility of projects, while also introducing new configurations that may not be possible from crossover.
        :param population: population to mutate
        :param mutation_prob: probability with which mutation occurs
        :param n_keep: number of individuals kept from previous generation
        :return: mutated population
        """
        for k in range(n_keep, len(population)):
            flip = np.random.rand()
            if flip < mutation_prob:
                ind = population[k]
                stud1, stud2 = np.random.randint(0, high=ind.num_students, size=2)

                # Python swapping using ind.chrom[stud1], ind.chrom[stud2] = ind.chrom[stud2], ind.chrom[stud1]
                # does not successfully swap the data, hence we swap with a temporary
                temp = ind.chrom[stud1]
                ind.chrom[stud1] = ind.chrom[stud2]
                ind.chrom[stud2] = temp
        return population

# Void function to test functionality implemented here
def test_main():
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv", 28)
    population = GeneticAlgorithmFunctions.initialize_population(population_size=10, num_students=100,
                                                                 num_projects=27, n_cross=2)
    new_pop = GeneticAlgorithmFunctions.crossover_with_random_offspring_generation(population, 2, 0.95)
    print(len(new_pop))
    mf, mm, mn, mb = 0, 0, 0, 0
    for ind in new_pop:
        if ind.parent[0] != ind.parent[1]:
            # print (population[ind.parent[0]].chrom, population[ind.parent[1]].chrom, ind.chrom)
            for i in range(population[0].num_students):
                if population[ind.parent[1]].chrom[i] == ind.chrom[i]:
                    if population[ind.parent[0]].chrom[i] == ind.chrom[i]:
                        mb += 1
                    else:
                        mf += 1
                elif population[ind.parent[0]].chrom[i] == ind.chrom[i]:
                    mm += 1
                else:
                    mn += 1
            break
    print (mf, mm, mn, mb)
    temp_pop = list(new_pop)
    new_pop = GeneticAlgorithmFunctions.apply_mutation(new_pop, 0.1, 2)


if __name__ == '__main__':
    test_main()
