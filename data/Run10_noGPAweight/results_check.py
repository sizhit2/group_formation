import pandas as pd

def read_from_csv(filename, num_projects):
    student_list = []
    reader = pd.read_csv(filename,delimiter = ',')
    for row in range(reader.shape[0]):
        last_name = reader['Last Name'][row]
        first_name = reader['First Name'][row]
        gpa = reader['GPA'][row]
        selected_partner = reader['Selected Partner?'][row]

        project_preferences = np.zeros(num_projects)
        ind = 0
        for i in range(num_projects):
            # if i == 4:              # Temporary, because Project 5 does not exist
            #     continue
            project_preferences[ind] = reader['Project ' + str(i+1)][row]
            ind += 1
        # project_preferences = project_preferences[:-1] # To fix an off-by-one error

        student = Student(gpa, selected_partner, last_name, first_name)
        student.update_project_preferences(project_preferences)
        if selected_partner:
            partner_last = reader['Partner Last'][row]
            partner_first = reader['Partner First'][row]
            partner_gpa = reader['Partner GPA'][row]
            student.update_partner_info(partner_last, partner_first, partner_gpa)
        student_list.append(student)
    return student_list

def analyze_results(results_file):
    total_satisfaction = 0
    num_satisfied = 0
    reader = pd.read_csv(results_file, delimiter=',')
