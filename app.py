from flask import Flask,request,render_template,session
from database import *

app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
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
            return render_template('hrhome.html')
  