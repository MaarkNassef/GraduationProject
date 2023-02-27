from flask import Flask,render_template,redirect,url_for,request,flash,session
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Amir Secret key'
@app.route('/signup',methods=['GET','POST'])
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
       
        return redirect(url_for('signin'))
       

@app.route('/signIn',methods=['GET','POST'])
def signin():
    if (request.method=='GET'):
       return render_template('signin.html')
    else:   
        email = request.form['email']
        password = request.form['password']
        id = authenticate(email=email,password=password)
        if id ==-1 :
            pass
        else:  
            session['Email']=email
            session['ID'] =id
            return render_template('hrhome.html')
