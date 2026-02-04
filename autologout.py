from db import get_connection
from datetime import datetime, time, timedelta

def auto_logout():
    conn = get_connection()
    cursor = conn.cursor()

    auto_time = time(19, 0, 0)  # 7:00 PM

    cursor.execute("""
        SELECT email, login_time
        FROM attendance
        WHERE attendance_date = CURDATE()
        AND logout_time IS NULL
    """)

    rows = cursor.fetchall()

    for email, login_time in rows:
        # convert timedelta to time if needed
        if isinstance(login_time, timedelta):
            total_seconds = int(login_time.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            login_time = time(hours, minutes, seconds)

        login_dt = datetime.combine(datetime.today(), login_time)
        logout_dt = datetime.combine(datetime.today(), auto_time)

        work_hours = round((logout_dt - login_dt).seconds / 3600, 2)
        status = "Present" if work_hours >= 8 else "Underworked"

        cursor.execute("""
            UPDATE attendance
            SET logout_time=%s, work_hours=%s, status=%s
            WHERE email=%s AND attendance_date=CURDATE()
        """, (auto_time, work_hours, status, email))

    conn.commit()
    conn.close()
    print("✅ Auto logout completed for missing users")
