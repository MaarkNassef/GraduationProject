from flask import Flask,render_template,redirect,url_for,request,flash,session, send_file
from database import *
from BackendClasses.Similarity import Similarity
from BackendClasses.TextExtraction import *
from BackendClasses.GenerateResume import RESUME_TEXT, GeneratePDF
from io import BytesIO
import hashlib
import pyotp

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
             flash("Password doesn't match.")
             return redirect(url_for('signUp'))
        else:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            r = signUpRegistration(name,email,password,company_name)
            if r == -1:
                flash("Email already exists")
                return redirect("/signup")
       
        return redirect(url_for('signin'))
       
@app.route('/')
def home():
    if 'ID' in session:
        result = getHrJobOpportunity(session['ID'])
        return render_template('hrHomee.html',Data = result)
    return render_template('Getstarted.html')

@app.route('/signIn',methods=['GET','POST'])
def signin():
    if (request.method=='GET'):
       return render_template('signin.html')
    else:   
        email = request.form['email']
        password = request.form['password']
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        id, role=authenticate(email=email,password=password)
        if role == 'admin':
            session['Admin']=1
        if id ==-1 :
            flash("User doesn't exist or wrong password.")
            return redirect('/signIn')
        else:  
            session['Email']=email
            session['tid'] =id
            return redirect(url_for('totp'))
        
@app.route('/signin/2fa', methods = ['GET', 'POST'])
def totp():
    if 'tid' not in session:
        return redirect('/')
    if request.method == 'GET':
        otp = get_otp(session['tid'])
        if otp:
            return render_template('twofa.html', secret=None)
        otp = pyotp.random_base32()
        set_otp(session['tid'], otp)
        return render_template('twofa.html', secret=otp)
    token = get_otp(session['tid'])
    otp = int(request.form.get('otp'))
    if pyotp.TOTP(token).verify(otp):
        session['ID'] = session['tid']
        session.pop('tid')
        return redirect(url_for("home"))
    else:
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("totp"))
  
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

        r_txt = RESUME_TEXT.replace('{{NAME}}', userName)
        r_txt = r_txt.replace('{{EMAIL}}',userEmail)
        r_txt = r_txt.replace('{{EDUCATION}}',userEducation)
        r_txt = r_txt.replace('{{SKILLS}}', userSkills)
        r_txt = r_txt.replace('{{ADDRESS}}', userAddress)
        r_txt = r_txt.replace('{{PHONE}}', userPhoneNumber)
        r_txt = r_txt.replace('{{PROJECTS}}', userProjects)
        r_txt = r_txt.replace('{{EXPERIENCE}}', userExperience)
        r_txt = r_txt.replace('{{OBJECTIVE}}', userObjective)

        pdf_file = GeneratePDF(r_txt)
        filename = f'Generated_{userName}.pdf'
        skills = get_skills(r_txt)
        designation = get_designition(r_txt)
        experience = get_years_of_exp(r_txt)
        add_new_application(filename, pdf_file, ', '.join(skills), ', '.join(designation), experience, ID)
        # fillForm(userName,userEmail,userEducation,userSkills,userAddress,userPhoneNumber,userProjects,userExperience,ID,userObjective)
        flash("Application sent successfully.")
        return redirect(url_for('dispalyAlljobs'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/contactus')
def contactus():
    return render_template('contactus.html', questions=getAllFAQs())
@app.route('/termsAndCondition')
def termsAndCondition():
    return render_template('termsAndCondition.html')


@app.route('/Uploadtype/<int:ID>')
def Uploadtype(ID):
    return render_template('Uploadtype.html',id = ID)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Notfound.html'), 404

@app.route('/addOpportunity',methods=['GET','POST'])
def addJob():
    if 'ID' not in session:
        return redirect('/') # To be changed
    if (request.method=='GET'):
       return render_template('AddJobForm.html')
    else:   
        jobName = request.form['jobName']
        jobDescription = request.form['jobDescription']
        imageSource=request.form['imageSource']
        if(jobName!="" and jobDescription!="" and imageSource!=""):
            addJobOpportunity(session['ID'],jobName,jobDescription,imageSource)
            flash("Job opportunity added successfully.")
            return redirect(url_for('home'))

@app.route('/jobDetails/<int:ID>', methods=['GET', 'POST'])
def showJobDetails(ID):
    if ('ID' not in session) or (ID not in [i[2] for i in getHrJobOpportunity(session['ID'])]):
        return redirect(url_for('applyForJob', job_id=ID))
    if request.method == 'GET':
        Details=getJobDetails(ID)
        Applicants=getApplicants(ID)
        active = get_active(ID)
        return render_template('jobDetails.html',details = Details,applicants=Applicants, active=active)
    Details=getJobDetails(ID)
    Applicants=getApplicantsByExp(ID, int(request.form['experience']))
    apps = []
    valid_designations = get_designition(Details[0]+'\t'+Details[1])
    print(valid_designations)
    def isApplicable(a_designation:list, j_designation:list)->bool:
        for i in a_designation:
            for j in j_designation:
                if i == j:
                    return True
        return False
    for i in Applicants:
        app_designation = i[-1].split(', ')
        if isApplicable(app_designation, valid_designations):
            apps.append(i)
    active = get_active(ID)
    return render_template('jobDetails.html',details = Details,applicants=apps, active=active)

@app.route('/deleteOppurtunity/<int:ID>')
def removeOppurtunity(ID):
    if ('ID' not in session) or (ID not in [i[2] for i in getHrJobOpportunity(session['ID'])]):
        return redirect('/') # To be changed
    deleteJobOpportunity(ID)
    flash("Job opportunity removed successfully.")
    return redirect(url_for('home'))
    
@app.route('/get-best-applicants/<int:jobid>')
def process(jobid):
    if 'ID' in session and jobid in [i[2] for i in getHrJobOpportunity(session['ID'])] and get_active(jobid)==1:
        deactivate_job(jobid)
        data = getApplicants(jobid)
        applicants_id = [i[4] for i in data]
        similarity = Similarity([i[3] for i in data], getJobDetails(jobid)[1])
        save_similarity(applicants_id, similarity)
        return redirect(url_for('showJobDetails',ID=jobid))
    return redirect(url_for('showJobDetails',ID=jobid))

@app.route('/displayAllJobs')
def dispalyAlljobs():
   result=getAllJobs()
   return render_template("allJobs.html", Data=result)

@app.route('/file/<int:file_id>')
def get_file(file_id: int):
    return send_file(
        BytesIO(get_file_by_id(file_id)),
        mimetype='application/pdf'
    )

@app.route('/upload-resume/<int:job_id>', methods=['GET','POST'])
def upload_resume(job_id : int ):
    if request.method == 'GET':
        return render_template('UploadCv.html')
    file = request.files['UploadFile']
    filename = file.filename
    file = file.read()
    resume_txt = extract_text(file)
    skills = get_skills(resume_txt)
    designation = get_designition(resume_txt)
    experience = get_years_of_exp(resume_txt)
    add_new_application(filename, file, ', '.join(skills), ', '.join(designation), experience, job_id)
    flash("Resume uploaded successfully.")
    return redirect(url_for('dispalyAlljobs'))

@app.route('/apply/<int:job_id>')
def applyForJob(job_id: int):
    Details=getJobDetails(job_id)
    return render_template('BrowseJob.html', details=Details)

@app.route('/admin')
def adminPage():
    if 'Admin' not in session:
        return redirect('/')
    return render_template('Admin.html')

@app.route('/admin-users')
def adminUsers():
    if 'Admin' not in session:
        return redirect('/')
    return render_template('adminUsers.html', users=getAllUsers())

@app.route('/admin-promote-users/<int:uid>')

def adminPromoteUsers(uid: int):
    if 'Admin' not in session:
        return redirect('/')
    promoteUser(uid)
    return redirect('/admin-users')

@app.route('/admin-demote-users/<int:uid>')
def adminDemoteUsers(uid: int):
    if 'Admin' not in session:
        return redirect('/')
    demoteUser(uid)
    return redirect('/admin-users')

@app.route('/admin-remove-users/<int:uid>')
def adminRemoveUsers(uid: int):
    if 'Admin' not in session:
        return redirect('/')
    removeUser(uid)
    return redirect('/admin-users')

@app.route('/admin-faqs', methods=['GET', 'POST'])
def adminfaqs():
    if 'Admin' not in session:
        return redirect('/')
    if request.method == 'GET':
        print(getAllFAQs())
        return render_template('adminFAQs.html', questions=getAllFAQs())
    addfaq(request.form['question'], request.form['answer'])
    return redirect('/admin-faqs')

@app.route('/admin-remove-faqs/<int:uid>')
def adminRemovefaqs(uid: int):
    if 'Admin' not in session:
        return redirect('/')
    removefaq(uid)
    return redirect('/admin-faqs')