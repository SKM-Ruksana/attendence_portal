import mysql
def get_connection():
    print("🔌 Attempting DB connection...")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="attendance_system",
    )
    print("✅ DB connection successful")
    return conn
def authenticate(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT email FROM employee WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    conn.close()
    return user is not None

