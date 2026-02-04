from db import get_connection
from db import authenticate
from datetime import date, datetime

def login():
    email = input("Enter email: ")
    password = input("Enter password: ")
    print("log_in successful")

    if not authenticate(email, password):
        print(" Invalid email or password")
        return

    conn = get_connection()
    cursor = conn.cursor()

    today = date.today()
    login_time = datetime.now().time()

    # prevent duplicate login
    check = """
    SELECT * FROM attendance
    WHERE email=%s AND attendance_date=%s
    """
    cursor.execute(check, (email, today))

    if cursor.fetchone():
        print(" Already logged in today")
    else:
        insert = """
        INSERT INTO attendance (email, attendance_date, login_time)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert, (email, today, login_time))
        conn.commit()
        print("✅ Login successful")

    conn.close()

