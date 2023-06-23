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
@app.route('/FillForm/<int:ID>',methods=['GET','POST'])
def FillForm(ID):

    if (request.method=='GET'):
        return render_template('FillForm.html')
    else:   
        userName = request.form['Name']
        userEmail = request.form['Email']
        userEducation = request.form['Education']
        userSkills=request.form['Skills']
        userAddress = request.form['Address']
        userPhoneNumber = request.form['phoneNumber']
        userProjects=request.form['Projects']
        userExperience = request.form['Experience']
        
        userObjective = request.form['Objective']

        if(userName!="" and userEmail!="" and userEducation!="" and userName!="" and userSkills!="" and userAddress!="" and userPhoneNumber!="" and userProjects!="" and userExperience!="" and userObjective!=""):
            fillForm(userName,userEmail,userEducation,userSkills,userAddress,userPhoneNumber,userProjects,userExperience,ID,userObjective)
            return redirect(url_for('home'))




    
@app.route('/AddJobForm')
def AddJobForm():
    return render_template('AddJobForm.html')
@app.route('/BrowseJob')
def BrowseJob():
    return render_template('BrowseJob.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')
@app.route('/Getstarted')
def Getstarted():
    return render_template('Getstarted.html')
@app.route('/Uploadtype/<int:ID>')
def Uploadtype(ID):
    return render_template('Uploadtype.html',id = ID)




@app.route('/NotFound')
def NotFound():
    return render_template('Notfound.html')
@app.route('/UploadCv')
def Uploadcv():
    return render_template('UploadCv.html')
@app.route('/addOpportunity',methods=['GET','POST'])
def addJob():
    if (request.method=='GET'):
       return render_template('AddJobForm.html')
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
    