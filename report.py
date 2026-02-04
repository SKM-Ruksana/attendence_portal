from db import get_connection

def daily_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email, login_time, logout_time, work_hours, status
        FROM attendance
        WHERE attendance_date = CURDATE()
    """)

    records = cursor.fetchall()

    print("\n--- DAILY ATTENDANCE REPORT ---")
    for row in records:
        print(row)

    conn.close()
