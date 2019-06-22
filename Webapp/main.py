from flask import Flask,request,render_template

app = Flask(__name__)
@app.route('/',methods = ["GET","POST"])
def home():
    NumberOfStudents = 'none'
    if (request.method == 'POST'):
        num_students = request.form['NumberOfStudents']
        num_projects = request.form['NumberOfProjects']
        min_select = request.form['MinimumNumberSelectedProjects']
        max_per_project = request.form['MaximumNumberStudentsPerProject']
        
        pop_size = request.form['PopulationSize']
        crossover_prob = request.form['CrossoverProbability']
        mutation_prob = request.form['MutationProbability']
        n_keep = request.form['N_Keep']
        n_cross = request.form['N_cross']

        reassign = request.form['reassign']
        max_iter = request.form['MaxIteration']
        cost_tol = request.form['costtol']
        gamma = request.form['gamma']
        gamma_gpa = request.form['gamma_gpa']

        input_data = [num_students, num_projects, min_select, max_per_project, pop_size, crossover_prob, mutation_prob,
                        n_keep, n_cross, reassign, max_iter, cost_tol, gamma, gamma_gpa]


        return render_template('index.html',var = NumberOfStudents)

        #print(NumberOfStudents)
    return render_template('index.html',var = NumberOfStudents)

# @app.route('/GA_Params',methods = ["GET","POST"])
# def get_ga_params():
#     input_data = [None for i in range(15)]
#     if request.method == POST:
#         pop_size = request.form['PopulationSize']
#         crossover_prob = request.form['CrossoverProbability']
#         mutation_prob = request.form['MutationProbability']
#         n_keep = request.form['N_Keep']
#         n_cross = request.form['N_cross']
#         input_data = [pop_size, crossover_prob, mutation_prob, n_keep, n_cross]
#
#         return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
