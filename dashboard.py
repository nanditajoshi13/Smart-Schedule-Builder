from flask import Blueprint, render_template, session, redirect, url_for, request
import sqlite3
from schedule import build_schedule_round_robin

dashboard_bp = Blueprint("dashboard", __name__)
DATABASE = "users.db"

def calculate_hours(range_str):
    if not range_str or "-" not in range_str:
        return 8
    try:
        start, end = range_str.split("-")
        start_hour = int(start.split(":")[0])
        end_hour = int(end.split(":")[0])
        return max(0, end_hour - start_hour)
    except:
        return 8

@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard_page():

    if "user_id" not in session:
        return redirect(url_for("login.home"))

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (session["user_id"],))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found"

    name = user["name"]
    work_range = user["work_hours"]

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            duration INTEGER
        )
    """)

    if request.method == "POST":
        task_name = request.form.get("task_name")
        task_duration = request.form.get("task_duration")

        if task_name and task_duration:
            cursor.execute("""
                INSERT INTO tasks (user_id, name, duration)
                VALUES (?, ?, ?)
            """, (session["user_id"], task_name, int(task_duration)))
            conn.commit()

        return redirect(url_for("dashboard.dashboard_page"))

    cursor.execute("""
        SELECT name, duration FROM tasks
        WHERE user_id=?
    """, (session["user_id"],))

    rows = cursor.fetchall()
    conn.close()

    tasks = [{"name": r["name"], "duration": r["duration"]} for r in rows]

    user_profile = {
        "work_hours": calculate_hours(work_range)
    }

    schedule = []
    if tasks:
        schedule = build_schedule_round_robin(user_profile, tasks)

    return render_template(
    "dashboard.html",
    name=user["name"],
    username=user["username"],
    categories=user["categories"],
    style=user["style"],
    goal=user["goal"],
    role=user["role"],
    work_hours=user["work_hours"],
    flexible=user["flexible"],
    no_way=user["no_way"],
    breaks=user["breaks"],
    tasks=tasks,
    schedule=schedule
)
