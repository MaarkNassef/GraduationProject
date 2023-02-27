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