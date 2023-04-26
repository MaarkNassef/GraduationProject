from flask import Flask,render_template,redirect,url_for,request,flash,session
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Amir Secret key'
@app.route('/signup',methods=['GET','POST'])
def signUp():
    if request.method=='GET':
        return render_template('signUp.html')
    else:
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirmationPassword=request.form['confirmPassword']
        company_name=request.form['companyName']
        if(password!=confirmationPassword):
             flash("Password doesn't match!!! ")
        else:
            
            signUpRegistration(name,email,password,company_name)
       
        return redirect(url_for('signin'))
       
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/signIn',methods=['GET','POST'])
def signin():
    if (request.method=='GET'):
       return render_template('signin.html')
    else:   
        email = request.form['email']
        password = request.form['password']
        id=authenticate(email=email,password=password)
        if id ==-1 :
            pass
        else:  
            session['Email']=email
            session['ID'] =id
            return redirect(url_for('hrHome'))
  


@app.route('/hrHomePage')
def hrHome():
    result = getHrJobDescription(session['ID'])
    return render_template('hrHomee.html',Data = result)

@app.route('/aboutus')
def aboutus():
    return render_template('Aboutus.html')

