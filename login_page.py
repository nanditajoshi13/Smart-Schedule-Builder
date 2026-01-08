import os
from flask import Flask, request, send_file
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)   

DB_FILE = "users.db"

def save_user(name, username, password):
    with open(DB_FILE, "a") as f:
        f.write(f"{name}|{username}|{password}\n")

def username_exists(uname):
    if not os.path.exists(DB_FILE):
        return False
    with open(DB_FILE, "r") as f:
        for line in f:
            name, username, password = line.strip().split("|")
            if username == uname:
                return True
    return False

@app.route("/")
def home():
    return send_file("login_page.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")

    if username_exists(username):
        return "Username already exists!", 400

    save_user(name, username, password)
    return "Registration Successful!"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    uname = data.get("username")
    passw = data.get("password")

    if not os.path.exists(DB_FILE):
        return "No users registered yet!", 400

    with open(DB_FILE, "r") as f:
        for line in f:
            name, username, password = line.strip().split("|")
            if username == uname and password == passw:
                return f"Login Successful! Welcome, {name}"

    return "Invalid Username or Password!", 401

if __name__ == "__main__":
    app.run(debug=True) 
