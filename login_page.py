import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

login_bp = Blueprint("login", __name__)

DB_FILE = "users.db"


@login_bp.route("/", methods=["GET"])
def home():
    return render_template("login_page.html")


@login_bp.route("/login", methods=["POST"])
def login_user():
    uname = request.form.get("username")
    passw = request.form.get("password")

    if not os.path.exists(DB_FILE):
        flash("No users registered yet!")
        return redirect(url_for("login.home"))

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (uname,))
    row = cur.fetchone()
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

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
            (name, username, password),
        )
        conn.commit()
        user_id = cur.lastrowid

    except sqlite3.IntegrityError:
        flash("Username already exists.")
        conn.close()
        return redirect(url_for("login.home"))

    conn.close()

    session["user_id"] = user_id
    session["name"] = name
    session["username"] = username

    return redirect(url_for("register.register_page"))
