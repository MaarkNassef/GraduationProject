import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'hrassistant'
)

def signUpRegistration(name,email,password,companyName):
    cursor = conn.cursor()
    cursor.execute('insert into users(name,email,password,companyname) values(%s, %s, %s, %s)',(name,email,password,companyName))

    conn.commit()
    
   