import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'hrassistant'
)

def authenticate(email: str, password: str) -> int:
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = %s AND hashed_password = %s', (email, password))
    try:
        id = cursor.fetchone()[0]
        return id
    except:
        return -1
        
def signUpRegistration(name,email,password,companyName):
    cursor = conn.cursor()
    cursor.execute('insert into users(username,email,hashed_password,company_name, role) values(%s, %s, %s, %s, %s)',(name,email,password,companyName, 'normal'))

    conn.commit()

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
    cursor.execute('SELECT application.filename,application.similarity,application.experience, application.skills, application.id FROM job,application WHERE application.jobid= %s ORDER BY similarity DESC'  , (id,))

    result = cursor.fetchall()
    return result

def deleteJobOpportunity(ID):
    cursor = conn.cursor()
    cursor.execute('delete from job where id=%s',(ID,))

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
        print((float(similarities[i]), applicants_id[i]))