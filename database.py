import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'hrassistant'
)

def authenticate(email: str, password: str):
    cursor = conn.cursor()
    cursor.execute('SELECT id, role FROM users WHERE email = %s AND hashed_password = %s', (email, password))
    try:
        id, role = cursor.fetchone()
        return id, role
    except:
        return -1, None
        
def signUpRegistration(name,email,password,companyName):
    cursor = conn.cursor()
    try:
        cursor.execute('insert into users(username,email,hashed_password,company_name, role) values(%s, %s, %s, %s, %s)',(name,email,password,companyName, 'normal'))
        conn.commit()
        return 1
    except:
        return -1

def getHrJobOpportunity(id):
    cursor = conn.cursor()
    cursor.execute('SELECT jobname,description,id,img_url FROM job WHERE userid = %s' , (id,))

    result = cursor.fetchall()
    return result


def addJobOpportunity(user_id,job_name,job_description,image):
    cursor = conn.cursor()
    cursor.execute('insert into job(userid,jobname,description,active,img_url) values(%s, %s,%s, %s, %s)',(user_id,job_name,job_description, 1,image))
    conn.commit()

def getJobDetails(id):
    cursor = conn.cursor()
    cursor.execute('SELECT job.jobname,job.description,job.id,users.company_name FROM job,users WHERE users.id = job.userid and job.id= %s ' , (id,))
    result = cursor.fetchone()
    return result

def getApplicants(id):
    cursor = conn.cursor()
    cursor.execute('SELECT application.filename,application.similarity,application.experience, application.skills, application.id FROM application WHERE application.jobid= %s ORDER BY similarity DESC'  , (id,))

    result = cursor.fetchall()
    return result

def deleteJobOpportunity(ID):
    cursor = conn.cursor()
    cursor.execute('delete from job where id=%s',(ID,))

    conn.commit()

def fillForm(userName,userEmail,userEducation,userSkills,userAddress,userPhoneNumber,userProjects,userExperience,jobID,userObjective):
    cursor = conn.cursor()
    cursor.execute('insert into form(name,email,education,skills,address,phone_number,projects,experience,similarity,jobid,Objective) values(%s, %s,%s,%s, %s, %s,%s,%s,%s,%s,%s)',(userName,userEmail,userEducation,userSkills,userAddress,userPhoneNumber,userProjects,userExperience,0,jobID,userObjective))
    conn.commit()

def get_otp(uid):
    cursor = conn.cursor()
    cursor.execute('SELECT otp FROM users WHERE id = %s' , (uid,))
    result = cursor.fetchone()[0]
    return result

def get_active(id):
    cursor = conn.cursor()
    cursor.execute('SELECT active FROM job WHERE id = %s' , (id,))
    result = cursor.fetchone()[0]
    return result

def set_otp(uid, otp):
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET otp=%s WHERE id=%s' , (otp, uid))
    conn.commit()

def deactivate_job(jid):
    cursor = conn.cursor()
    cursor.execute('UPDATE job SET active=%s WHERE id=%s' , (0, jid))
    conn.commit()

def save_similarity(applicants_id: list[int], similarities:list[float]):
    cursor = conn.cursor()
    for i in range(len(applicants_id)):
        cursor.execute('UPDATE application SET similarity=%s WHERE id=%s' , (float(similarities[i]), applicants_id[i]))
        conn.commit()

def getAllJobs():
    cursor = conn.cursor()
    cursor.execute('SELECT jobname,id,img_url FROM job')
    result = cursor.fetchall()
    return result

def get_file_by_id(aid):
    cursor = conn.cursor()
    cursor.execute('SELECT file FROM application WHERE id = %s' , (aid,))
    result = cursor.fetchone()[0]
    return result

def add_new_application(filename: str, file: bytes, skills: str, designation: str, exp: int, jobid: int):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO application (filename, file, skills, designation, experience, jobid) VALUES (%s, %s, %s, %s, %s, %s)"
                   , (filename, file, skills, designation, exp, jobid))
    conn.commit()

def getApplicantsByExp(id, exp):
    cursor = conn.cursor()
    cursor.execute('SELECT application.filename,application.similarity,application.experience, application.skills, application.id, application.designation FROM application WHERE application.jobid= %s AND experience >= %s ORDER BY similarity DESC'  , (id,exp))

    result = cursor.fetchall()
    return result

def getAllUsers():
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role FROM users')
    result = cursor.fetchall()
    return result

def promoteUser(uid):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role='admin' WHERE id = %s", (uid,))
    conn.commit()

def demoteUser(uid):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role='normal' WHERE id = %s", (uid,))
    conn.commit()

def removeUser(uid):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (uid,))
    conn.commit()

def getAllFAQs():
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, answer FROM faqs')
    result = cursor.fetchall()
    return result

def removefaq(fid):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM faqs WHERE id = %s", (fid,))
    conn.commit()

def addfaq(question, answer):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faqs(question, answer) VALUES (%s, %s)", (question, answer))
    conn.commit()
