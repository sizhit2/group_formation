# Team Formation App
This project is an app that assigns students to projects, forming teams based on student preference.

# Usage
Place student csv data in the /data/ directory. Ensure that project numbers are contiguous, as file parsing will be problematic otherwise. Sample data is already in the directory for reference. Update input_data.txt as per instructions below, these are the run-time parameters to the genetic algorithm. To run, edit main.py to make sure the directory is correct. Type in python3 main.py into the terminal, or run main.py from any IDE. Output files from the runs will be written to the data directory, under the output sub-folder.

# Input Data schema
To correctly update the input_data.txt file, the parameters must be passed in the following order:
1. Filename with student roster
2. Number of students (for algorithm, excludes partners)
3. Number of projects
4. Minimum number of projects to be selected by a student
5. Maximum number of students in a given project
6. Population size (for genetic algorithm)
7. Crossover probability
8. Mutation probability
9. Number of chromosomes to keep in the next generation (n_keep)
10. Number of locations where crossover occurs (n_cross)
11. Reassign probability
12. Maximum number of iterations
13. Cost function change tolerance
14. Weight parameter for number of students per group (gamma)
15. Weight parameter for average gpa per group (gamma_gpa)
