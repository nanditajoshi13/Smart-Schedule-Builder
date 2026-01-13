import os
from flask import Blueprint, render_template, request, redirect, url_for, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
login_bp = Blueprint("login", __name__, template_folder=BASE_DIR)

DB_FILE = "users.db"

@login_bp.route("/", methods=["GET"])
def home():
    return render_template("login_page.html")

@login_bp.route("/login", methods=["POST"])
def login():
    uname = request.form.get("username")
    passw = request.form.get("password")

    if not os.path.exists(DB_FILE):
        return "No users registered yet!"

    with open(DB_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 3:
                name, username, password = parts[:3]
                if username == uname and password == passw:
                    session["name"] = name
                    return f"Login Successful! Welcome, {name}"

    return "Invalid Username or Password!"

@login_bp.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    session["name"] = name
    session["username"] = username
    session["password"] = password

    return redirect(url_for("register.register_page")) 
