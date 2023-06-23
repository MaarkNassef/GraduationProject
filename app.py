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
    if 'ID' in session:
        result = getHrJobOpportunity(session['ID'])
        return render_template('hrHomee.html',Data = result)
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
            return redirect(url_for('home'))
  
@app.route('/aboutus')
def aboutus():
    return render_template('Aboutus.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/addOpportunity',methods=['GET','POST'])
def addJob():
    if (request.method=='GET'):
       return render_template('addOpportunities.html')
    else:   
        jobName = request.form['jobName']
        jobDescription = request.form['jobDescription']
        imageSource=request.form['imageSource']
        if(jobName!="" and jobDescription!="" and imageSource!=""):
            addJobOpportunity(session['ID'],jobName,jobDescription,imageSource)
            return redirect(url_for('home'))

@app.route('/jobDetails/<int:ID>')
def showJobDetails(ID):
    Details=getJobDetails(ID)
    Applicants=getApplicants(ID)
    return render_template('jobDetails.html',details = Details,applicants=Applicants)

@app.route('/deleteOppurtunity/<int:ID>')
def removeOppurtunity(ID):
    deleteJobOpportunity(ID)
    return redirect(url_for('home'))
    