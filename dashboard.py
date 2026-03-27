from flask import Blueprint, render_template, session, redirect, url_for, request
import mysql.connector
from datetime import datetime
from schedule import build_schedule, create_profile_from_db, Task

dashboard_bp = Blueprint("dashboard", __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password", //enter your mysql command line client password
        database="schedule_db"
    )

@dashboard_bp.route("/", methods=["GET", "POST"])
def dashboard_page():

    if "user_id" not in session:
        return redirect(url_for("login.home"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (session["user_id"],))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return "User not found"

    if request.method == "POST":
        task_name = request.form.get("task_name")
        task_duration = request.form.get("task_duration")
        priority = request.form.get("priority") or 3
        task_type = request.form.get("task_type") or "other"
        deadline = request.form.get("deadline")

        if deadline:
             deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        else:
             deadline = None

        if task_name and task_duration:
            cursor.execute("""
                INSERT INTO tasks (user_id, name, duration, priority, task_type, deadline)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (session["user_id"], task_name, float(task_duration), int(priority), task_type, deadline ))
            conn.commit()

        return redirect(url_for("dashboard.dashboard_page"))

    cursor.execute("""
        SELECT * FROM tasks
        WHERE user_id=%s AND status='pending'
    """, (session["user_id"],))
    pending_tasks = cursor.fetchall()

    cursor.execute("""
                   SELECT * FROM tasks 
                   WHERE user_id=%s AND status='done'
                   """, (session["user_id"],))
    completed_tasks = cursor.fetchall()

    used_hours = sum(float(r["duration"]) for r in completed_tasks)

    tasks = []
    for r in pending_tasks:
        deadline_in = 999

        if r["deadline"]:
                today = datetime.now().date()
                diff_days = (r["deadline"] - today).days
                deadline_in = max(diff_days * 24, 1)
            
        task = Task(
            name=r["name"],
            duration=float(r["duration"]),
            task_type=r["task_type"] or "other",
            priority=int(r["priority"] or 3),
            deadline_in=deadline_in, 
            chunk_size=1.0
        )
        tasks.append(task)

    user_data = {
        "work_hours": user["work_hours"] or "9-17",
        "no_way": user["no_way"] or "",
        "breaks": user["breaks"] or "15min/every 1hr",
        "style": (user["style"] or "flexible").lower()
    }

    profile = create_profile_from_db(user_data)

    profile.work_start += used_hours

    if profile.work_start >= profile.work_end:
        profile.work_start = profile.work_end

    schedule = []
    if tasks:
        result = build_schedule(profile, tasks)
        schedule = result["schedule"]

    cursor.close()
    conn.close()


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
    tasks=pending_tasks,
    completed_tasks=completed_tasks,
    schedule=schedule
)

@dashboard_bp.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks set status='done' WHERE id=%s", (task_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("dashboard.dashboard_page"))

@dashboard_bp.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("dashboard.dashboard_page"))

@dashboard_bp.route("/undo/<int:task_id>", methods=["POST"])
def undo_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status='pending' WHERE id=%s", (task_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("dashboard.dashboard_page"))
