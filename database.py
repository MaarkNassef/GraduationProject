import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'hrassistant'
)

def authenticate(email: str, password: str) -> int:
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = %s AND password = %s', (email, password))
    try:
        id = cursor.fetchone()[0]
        return id
    except:
        return -1
        
def signUpRegistration(name,email,password,companyName):
    cursor = conn.cursor()
    cursor.execute('insert into users(name,email,password,companyname) values(%s, %s, %s, %s)',(name,email,password,companyName))

    conn.commit()

def getHrJobDescription(id):
    cursor = conn.cursor()
    cursor.execute('SELECT jobName,jobDescription,jobId FROM hrJobDescription WHERE userId = %s' , (id,))

    result = cursor.fetchall()
    return result

