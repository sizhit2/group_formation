from flask import Flask,request,render_template

app = Flask(__name__)
@app.route('/',methods = ["GET","POST"])
def home():
    NumberOfStudents = 'none'
    if (request.method == 'POST'):
        NumberOfStudents = request.form['NumberOfStudents']
        
        return render_template('index.html',var = NumberOfStudents)

        #print(NumberOfStudents)
    return render_template('index.html',var = NumberOfStudents)
if __name__ == "__main__":
    app.run(debug=True)