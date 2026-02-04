from log_in import login
from logout import logout
from autologout import auto_logout
from report import daily_report

while True:
    print("\n--- Employee Attendance System ---")
    print("1. Login")
    print("2. Logout")
    print("3. Auto Logout (7 PM)")
    print("4. Daily Report")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        login()
    elif choice == "2":
        logout()
    elif choice == "3":
        auto_logout()
    elif choice == "4":
        daily_report()
    elif choice == "5":
        break
    else:
        print("Invalid choice")
