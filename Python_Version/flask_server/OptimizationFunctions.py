from StructDef import Student, Individual
# from InputOutput import *
import numpy as np


class OptimizationFunctions(object):

    @staticmethod
    def fill_dv_matrix(population):
        """
        Function that creates the design variable matrix for all individuals in the given population.
        :return: population with design variable matrices updated
        """
        for individual in population:
            individual = OptimizationFunctions.fill_ind_dv_matrix(individual)
        return population

    @staticmethod
    def fill_ind_dv_matrix(individual):
        """
        Fills design variable matrix by mapping student # to project #
        :return: individual with design variable matrix updated
        """
        for j in range(individual.num_students):
            k = individual.chrom[j]
            individual.dv_matrix[j, k] = 1
        return individual

    @staticmethod
    def get_num_students_per_project(population, student_list):
        """
        Function that calculates number of students per projects for all individuals in the given population.
        Since students can choose partners, a student_list with relevant data is referenced.
        :param student_list: list of Student objects for the class
        :return: population with num_students_per_project updated.
        """

        for individual in population:
            individual = OptimizationFunctions.get_ind_students_per_project_ind(individual, student_list)
        return population

    @staticmethod
    def get_ind_students_per_project_ind(individual, student_list):
        """
        Function that calculates number of students per projects for a given individual. Since students can choose
        partners, a student_list with relevant data is referenced.
        :param student_list: list of Student objects for the class
        :return: individual with the num_student_per_project field updated
        """
        for j in range(individual.num_students):
            if student_list[j].selected_partner:
                add = 2
            else:
                add = 1
            individual.num_student_per_project[individual.chrom[j]] += add
        return individual

    @staticmethod
    def repair_dv_matrix(population, max_per_project, student_list):
        """
        Function that attempts to correct infeasibility in chromosomes across a population.
        :param max_per_project: maximum number of students that can be assigned to any single project
        :param student_list: list of Student objects for the class
        :return: population with repaired design variable matrices
        """
        population = OptimizationFunctions.get_num_students_per_project(population, student_list)
        for individual in population:
            # Correct infeasibility in each individual
            individual = OptimizationFunctions.repair_ind_dv_matrix(individual, max_per_project, student_list)
        return population

    @staticmethod
    def repair_ind_dv_matrix(individual, max_per_project, student_list):
        """
        Function that attempts to correct infeasibility in chromosomes of a given individual.
        :param max_per_project: maximum number of students that can be assigned to any single project
        :param student_list: list of Student objects for the class
        :return: individual with repaired design variable matrix
        """
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

                    # To move a student, try and move into a project of their picking
                    # Sort project indices based on student's preference
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
                # TODO: Add debug file parameter to see infeasibilities
                pass
        return individual

    @staticmethod
    def compute_and_fix(population, max_per_project, student_list):
        """
        Fills the design variable matrix for each individual in a population and attempts
        to fix for infeasibility. With certain chromosomes it may be impossible, but the
        algorithm will not stop for this.
        :param max_per_project: maximum number of students that can be assigned to any single project
        :param student_list: list of Student objects for the class
        :return: population with updated design variable matrices
        """
        population = OptimizationFunctions.fill_dv_matrix(population)
        population = OptimizationFunctions.repair_dv_matrix(population, max_per_project, student_list)
        return population

    @staticmethod
    def evaluate_ind_fitness(individual, student_list, max_satisfaction, class_avg_gpa, avg_size_group=5,
                             gamma_gpa=0.0, gamma=0.0):
        """
        Evaluates the fitness of a given individual in a population. The fitness is a combination of student
        satisfaction, variance of number of students in each project, and the variance of the average gpa per project.
        Tries to minimize the variances, and maximize the student satisfaction.
        :param student_list: list of Student objects for the class
        :param max_satisfaction: value of maximum theoretical satisfaction (pre-computed)
        :param class_avg_gpa: value of class average gpa, needed for variance
        :param avg_size_group: size of the average group, needed for variance
        :param gamma_gpa: weight of gpa part of fitness function
        :param gamma: weight of group size part of fitness function
        :return: individual with fitness field updated
        """
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
        individual.avg_gpa_per_project = np.zeros(individual.num_projects)
        sigma_gpa = 0.0
        if abs(gamma_gpa) > 0.0:
            fictitious_num_students = np.zeros(individual.num_projects)
            for stud in range(individual.num_students):
                # Account for partners
                pair_gpa = student_list[stud].gpa
                if student_list[stud].selected_partner:
                    pair_gpa += student_list[stud].partner_gpa
                    pair_gpa = pair_gpa / 2

                proj = individual.chrom[stud]
                fictitious_num_students[proj] += 1
                individual.avg_gpa_per_project[proj] += pair_gpa

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

    @staticmethod
    def evaluate_fitness(population, student_list, max_satisfaction, class_avg_gpa, avg_size_group=5,
                         gamma_gpa=0.0, gamma=0.0):
        """
        Evaluates fitness of each individual of a population
        :param student_list: list of Student objects for the class
        :param max_satisfaction: value of maximum theoretical satisfaction (pre-computed)
        :param class_avg_gpa: value of class average gpa, needed for variance
        :param avg_size_group: size of the average group, needed for variance
        :param gamma_gpa: weight of gpa part of fitness function
        :param gamma: weight of group size part of fitness function
        :return: population updated with fitnesses
        """
        for individual in population:
            individual = OptimizationFunctions.evaluate_ind_fitness(individual, student_list, max_satisfaction,
                                                                    class_avg_gpa, avg_size_group, gamma_gpa, gamma)
        return population

    @staticmethod
    def get_class_avg_gpa(student_list):
        """
        Calculates average gpa of the class. Use only once, and use this pre-computed result.
        :param student_list: list of Student objects for the class
        :return: average GPA for the class
        """
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

    @staticmethod
    def reassign_students(population, student_list, reassign_prob, max_per_project):
        """
        Reassigns students in the top 5 percent of fit individuals. Reassigning is done when a student is placed in an
        unfavorable project (i.e satisfaction value of 0). Reassign only occurs within the bounds of max_per_project,
        i.e students will be moved if and only if the destination project has slots open. Assumes that the population
        comes in sorted by fitness. Only does the reassign if it increases the fitness. Reassign done based on
        reassign_prob parameter.
        :param student_list: list of Student objects for the class
        :param reassign_prob: probability of getting re-assigned
        :param max_per_project: maximum number of students that can be assigned to any single project
        :return: population with students re-assigned if possible
        """
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
                    # Sort project indices based on student's preference
                    tentative_projs = np.argsort(student.project_preferences)[::-1]

                    for tentative_proj in tentative_projs:
                        # If we only have unfavorable projects, skip and don't reassign
                        if student.project_preferences[tentative_proj] == 0:
                            break

                        # We are assured that the student prefers tentative project,
                        # so this should increase fitness
                        if ind.num_student_per_project[tentative_proj] <= (max_per_project - add):
                            ind.chrom[j] = tentative_proj
                            ind.dv_matrix[j, tentative_proj] = 1
                            ind.dv_matrix[j, assigned_proj] = 0
                            ind.num_student_per_project[tentative_proj] += add
                            ind.num_student_per_project[assigned_proj] -= add
                            break
        return population

    @staticmethod
    def check_viable_swap(ind, tentative_proj, assigned_proj, add, t_add, max_per_project):
        """
        Viable swaps are when the new number of students per project stays within constraints post-swap.
        This function returns True if the swap is viable, False otherwise.
        """
        if ind.num_student_per_project[tentative_proj] - t_add + add <= max_per_project:
            if ind.num_student_per_project[assigned_proj] - add + t_add <= max_per_project:
                return True
        return False


    @staticmethod
    def reassign_students_alternative(population, student_list, reassign_prob, max_per_project):
        """
        Reassigns students in the top 5 percent of fit individuals. Reassigning is done when a student is placed in an
        unfavorable project (i.e satisfaction value of 0). Swaps students, if amicable to both, to ensure that all students
        are placed in favorable projects. Assumes that the population comes in sorted by fitness. Reassign done based on
        reassign_prob parameter.
        :param student_list: list of Student objects for the class
        :param reassign_prob: probability of getting re-assigned
        :param max_per_project: maximum number of students that can be assigned to any single project
        :return: population with students re-assigned if possible
        """
        for i in range(len(population) // 20):
            ind = population[i]
            for j in range(ind.num_students):
                student = student_list[j]
                assigned_proj = ind.chrom[j]
                reassign_student = True     # Determines whether or not to reassign based on reassign_prob

                if student.selected_partner:
                    add = 2
                else:
                    add = 1

                if reassign_prob < 1:
                    flip = np.random.rand()
                    if flip > reassign_prob:
                        reassign_student = False

                if student.project_preferences[assigned_proj] == 0 and reassign_student:
                    # First get preferences for student, most preferred first
                    tentative_projs = np.argsort(student.project_preferences)[::-1]
                    for tentative_proj in tentative_projs:
                        if student.project_preferences[tentative_proj] == 0: # If we reach unfavorable projects, skip
                            break

                        for row in range(ind.num_students):
                            if ind.dv_matrix[row, tentative_proj] > 0:
                                t_student = student_list[row]

                                # If swapping results in yet another unsatisfied student, skip it
                                if t_student.project_preferences[assigned_proj] == 0:
                                    continue

                                if t_student.selected_partner:
                                    t_add = 2
                                else:
                                    t_add = 1

                                if OptimizationFunctions.check_viable_swap(ind, tentative_proj, assigned_proj, add, t_add, max_per_project):
                                    ind.chrom[j] = tentative_proj
                                    ind.chrom[row] = assigned_proj

                                    ind.num_student_per_project[assigned_proj] -= add
                                    ind.num_student_per_project[assigned_proj] += t_add

                                    ind.num_student_per_project[tentative_proj] -= t_add
                                    ind.num_student_per_project[tentative_proj] += add

                                    ind.dv_matrix[row, tentative_proj] = 0
                                    ind.dv_matrix[row, assigned_proj] = 1
                                    ind.dv_matrix[j, assigned_proj] = 0
                                    ind.dv_matrix[j, tentative_proj] = 1
                                    break
        return population


    @staticmethod
    def get_num_satisfied_students(individual, student_list):
        """
        Finds the number of students in projects they picked for a given individual
        :param student_list: list of Student objects for the class
        :return: Number of students placed in projects they picked
        """
        num_students_picked_project = 0
        for stud in range(len(student_list)):
            student = student_list[stud]
            satisfaction = student.project_preferences[individual.chrom[stud]]
            if satisfaction > 0:
                num_students_picked_project += 1
        return num_students_picked_project

    @staticmethod
    def get_avg_gpa_per_group(individual, student_list):
        """
        Gets average gpa per group for an individual. Not needed unless gamma_gpa was 0 all along.
        :param student_list: list of Student objects for the class
        :return: list avg_gpa_per_group
        """
        avg_gpa_per_group = np.zeros(individual.num_projects)
        for stud in range(len(student_list)):
            proj = individual.chrom[stud]
            student = student_list[stud]
            avg_gpa_per_group[proj] += student.gpa
            if student.selected_partner:
                avg_gpa_per_group[proj] += student.partner_gpa

        for proj in range(individual.num_projects):
            avg_gpa_per_group[proj] /= individual.num_student_per_project[proj]
        return avg_gpa_per_group

# Void function to test functionality implemented here
def test_main():
    num_projects = 27
    num_students = 100
    ind = Individual(num_projects, num_students, 2)

    # Get student list and preference matrix
    student_list = read_from_csv("../data/StudentPreferenceSpring2019_PredetTeamRemoved.csv", 27)
    student_pref_matrix = np.zeros((100, 27))
    for i, student in enumerate(student_list):
        student_pref_matrix[i, :] = student.project_preferences

    gpa_list = np.random.normal(2.5, 0.1, num_students)
    # print (gpa_list)
    for (i, stud) in enumerate(student_list):
        stud.gpa = gpa_list[i]
        if stud.selected_partner:
            stud.partner_gpa = gpa_list[i]

    # for i in range(len(student_list)):
    #     print (student_list[i].gpa)


    for j in range(num_students):
        ind.chrom[j] = np.random.randint(0, high=num_projects)
    for j in range(num_projects):
        ind.chrom[num_students + j] = j

    ind = OptimizationFunctions.evaluate_ind_fitness(ind, student_list, 485, 2.5, gamma=2, gamma_gpa=2)
    print (ind.fitness)

    # print (ind.chrom)
    # # ind = get_ind_students_per_project_ind(student_list, ind)
    # # print (ind.num_student_per_project)
    # # ind = fill_ind_dv_matrix(ind)
    # ind = OptimizationFunctions.repair_ind_dv_matrix(ind, 5, student_list)
    # print("After:")
    # print(ind.chrom)
    # print(sum(ind.num_student_per_project))
    #
    # print(len([stud for stud in student_list if stud.selected_partner]))

if __name__ == '__main__':
    test_main()
