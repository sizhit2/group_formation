from StructDef import *
import InputOutput
import numpy as np

def initialize_population(population_size, num_students, num_projects, n_cross):
    population = []
    for i in range(population_size):
        ind = Individual(num_projects, num_students, n_cross, parent=None)
        for j in range(num_students):
            ind.chrom[j] = np.random.randint(0, high=num_projects)
        for j in range(num_projects):
            ind.chrom[num_students + j] = j
        population.append(ind)
    return population

def test_main():
    pop = initialize_population(10, 50, 10, 2)
    print (pop[0].chrom)
    print (pop[4].chrom)
    print (len(pop))

if __name__ == '__main__':
    test_main()
