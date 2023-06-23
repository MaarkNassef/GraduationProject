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
    cursor.execute('SELECT jobname,description,id FROM job WHERE userid = %s' , (id,))

    result = cursor.fetchall()
    return result

