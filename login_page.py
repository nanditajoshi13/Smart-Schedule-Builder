import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

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
        flash ("No users registered yet!")
        return redirect(url_for("login.home"))

    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT name, password FROM users WHERE username=?", (uname,))
    row = cur.fetchone()
    conn.close()

    if row and row[1] == passw:
        session["name"] = row[0]
        session["username"] = uname
        return redirect(url_for("dashboard.dashboard_page"))
    else:
        flash("Invalid Username or Password!")
        return redirect(url_for("login.home"))


@login_bp.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
                (name, username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        flash("Username already exists. Please choose another one.")
        conn.close()
        return redirect(url_for("login.home"))
    finally: 
        conn.close()

    session["name"] = name
    session["username"] = username
    session["password"] = password

    return redirect(url_for("register.register_page"))
