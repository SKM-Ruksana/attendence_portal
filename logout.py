from db import get_connection
from db import authenticate
from datetime import datetime, timedelta, time

def logout():
    email = input("Enter email: ")
    password = input("Enter password: ")

    if not authenticate(email, password):
        print("❌ Invalid credentials")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT login_time FROM attendance
        WHERE email=%s AND attendance_date=CURDATE()
    """, (email,))

    row = cursor.fetchone()
    if not row:
        print("❌ No login found today")
        conn.close()
        return

    login_time = row[0]

    # Convert timedelta to time (PyMySQL fix)
    if isinstance(login_time, timedelta):
        total_seconds = int(login_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        login_time = time(hours, minutes, seconds)

    logout_time = datetime.now().time()

    login_dt = datetime.combine(datetime.today(), login_time)
    logout_dt = datetime.combine(datetime.today(), logout_time)

    work_hours = round((logout_dt - login_dt).seconds / 3600, 2)
    status = "Present" if work_hours >= 8 else "Underworked"

    cursor.execute("""
        UPDATE attendance
        SET logout_time=%s, work_hours=%s, status=%s
        WHERE email=%s AND attendance_date=CURDATE()
    """, (logout_time, work_hours, status, email))

    conn.commit()
    conn.close()

    print("✅ Logout successful. Hours:", work_hours)
