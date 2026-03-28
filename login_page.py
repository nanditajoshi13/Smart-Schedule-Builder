import os
import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

login_bp = Blueprint("login", __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password", //write your mysql command line client password here
        database="schedule_db"
    )

@login_bp.route("/", methods=["GET"])
def home():
    return render_template("login_page.html")

@login_bp.route("/login", methods=["POST"])
def login_user():
    uname = request.form.get("username")
    passw = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (uname,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    
    if row and row["password"] == passw:
        session["user_id"] = row["id"]
        session["name"] = row["name"]
        session["username"] = row["username"]
        return redirect(url_for("dashboard.dashboard_page"))
    else:
        flash("Invalid Username or Password!")
        return redirect(url_for("login.home"))


@login_bp.route("/register", methods=["POST"])
def register_user():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    conn =get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
            (name, username, password),
        )
        conn.commit()
        user_id = cursor.lastrowid

    except mysql.connector.IntegrityError:
        flash("Username already exists.")
        cursor.close()
        conn.close()
        return redirect(url_for("login.home"))

    cursor.close()
    conn.close()

    session["user_id"] = user_id
    session["name"] = name
    session["username"] = username

    return redirect(url_for("register.register_page"))
