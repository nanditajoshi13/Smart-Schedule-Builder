import os
DB_FILE = "users.db"
def save_user(name, username, password, setup_data):
    with open(DB_FILE, "a") as f:
        line = f"{name}|{username}|{password}"
        for key, value in setup_data.items():
            line += f"|{key}={value}"
        f.write(line + "\n")
def username_exists(uname):
    if not os.path.exists(DB_FILE):
        if not os.path.exists(DB_FILE):
            return False
        with open(DB_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if parts[1] == uname:
                    return True
        return False
def register_user():
    print("\n----USER REGISTRATION---")
    name = input("Enter Full Name: ")
    username = input("Enter Username: ")
    if username_exists(username):
        print("Username already exists!")
        return
    password = input("Enter Password: ")
    print("\n---SETUP---")
    role = input("Role (Student/business/word-from-from/housewife/other): ")
    work_hours = input("Main work/study hours (e.g. 09:00-18:00): ")
    flexible = input("Flexible hours for urgent tasks (e.g. 18:00-20:00): ")
    no_way = input("No-way hours (e.g. 22:00-07:00): ")
    breaks = input("Break preference (e.g. 2h/15m): ")
    categories = input("Main categories (comma separated, e.g. study,work,personal): ")
    style = input("Scheduling style (fixed/flexible): ")
    goal = input("Primary goal (exam prep, project planning, balanced routine, etc.): ")
    setup_data = {
        "role": role,
        "work_hours": work_hours,
        "flexible":  flexible,
        "no_way": no_way,
        "breaks": breaks,
        "categories": categories,
        "style": style,
        "goal": goal
    }
    save_user(name, username, password, setup_data)
    print("Registration & Setup Successful!")
def login_user():
    print("\n---USER LOGIN---")
    uname = input("Enter Username: ")
    passw = input("Enter Password: ")
    if not os.path.exists(DB_FILE):
        print("No users registered yet!")
        return
    with open(DB_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            name, username, password = parts[0], parts[1], parts[2]
            if username == uname and password == passw:
                print(f"\nLogin Succesful! Welcome, {name}")
                setup_info = parts[3:]
                print("Your setup preferences:")
                for item in setup_info:
                    print(" -", item)
                return
    print("Invalid Username or Password!")
def main():
    while True:
        print("\n==============================")
        print(" SMART SCHEDULE BUILDER APP ")
        print("==============================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid choice!")
            continue
        if choice == 1:
            register_user()
        elif choice == 2:
            login_user()
        elif choice == 3:
            print("exiting application...")
            break
        else:
            print("Invalid choice!")
if __name__ == "__main__":
    main()
