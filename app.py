from flask import Flask,render_template,redirect,url_for,request,flash,session
from database import signUpRegistration

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Amir Secret key'
@app.route('/',methods=['GET','POST'])
def signUp():
    if request.method=='GET':
        return render_template('signUp.html')
    else:
        name=request.form['Name']
        email=request.form['Email']
        password=request.form['Password']
        confirmationPassword=request.form['comfirmationPassword']
        company_name=request.form['CompanyName']
        if(password!=confirmationPassword):
             flash("Password doesn't match!!! ")
        else:
            
            signUpRegistration(name,email,password,company_name)
       
        return render_template('signUp.html')