from flask import Flask,request,render_template

app = Flask(__name__)
@app.route('/',methods = ["GET","POST"])
def home():
    #NumberOfStudents = 'none'
    '''
    if (request.method == 'POST'):
        NumberOfStudents = request.form['NumberOfStudents']
        NumberOfProjects = request.form['NumberOfProjects']
        
        #return render_template('index.html',var = NumberOfStudents)
        return render_template('index.html',var = NumberOfStudents)

        #print(NumberOfStudents)
    #return render_template('index.html',var = NumberOfStudents)
    '''
    return render_template('index.html')

@app.route('/student',methods=['POST','GET'])
def student():
    return render_template('student.html')

@app.route('/professor',methods=['POST','GET'])
def professor():
    return render_template('professor.html')
if __name__ == "__main__":
    app.run(debug=True)
