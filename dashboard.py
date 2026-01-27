import os
import datetime
from flask import Blueprint, Flask, render_template, session
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dashboard_bp = Blueprint("dashboard", __name__, template_folder=BASE_DIR)
DB_FILE = "users.db"

@dashboard_bp.route("/", methods=["GET"])
def dashboard_page():

    username = session.get("username")
    if not username:
        return "Please log in first."
    
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT name, username, role, work_hours, flexible,no_way, breaks, categories, style, goal
        FROM users WHERE username=?
        """, (username,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return "No data found for this user."
    
    return render_template(
        "dashboard.html",
        name=row[0],
        username=row[1],
        role=row[2],
        work_hours=row[3],
        flexible=row[4],
        no_way=row[5],
        breaks=row[6],
        categories=row[7],
        style=row[8],
        goal=row[9]
    )
