from flask import Flask, render_template,request,url_for
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/aboutus.html',methods= ['POST','GET'])
def aboutus():
    message = None
    if request.method  == 'POST':
        dict = request.form
        #if dict is not None:
            #message = "submission succeed"
        print(dict)
        
    
    return render_template("aboutus.html",message = message)

@app.route("/contactus.html",methods= ['POST','GET'])
def contactus():
    #if request.method == 'GET':

    return render_template("contactus.html")

@app.route("/student.html",methods = ['POST','GET'])
def student():

    #if request.method == 'GET':

    return render_template("student.html")


if __name__ == "__main__":
    app.run(debug= True)
