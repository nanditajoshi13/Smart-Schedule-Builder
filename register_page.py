import os
import sqlite3
from flask import Blueprint, render_template, request, session, redirect, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
register_bp = Blueprint("register", __name__, template_folder=BASE_DIR)

DB_FILE = "users.db"

@register_bp.route("/", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        name = session.get("name")
        username = session.get("username")
        password = session.get("password")

        role = request.form.get("role")
        work_start = request.form.get("work_start")
        work_end = request.form.get("work_end")
        flex_start = request.form.get("flex_start")
        flex_end = request.form.get("flex_end")
        no_start = request.form.get("no_start")
        no_end = request.form.get("no_end")
        break_length = request.form.get("break_length")
        break_length_unit = request.form.get("break_length_unit")
        work_interval = request.form.get("work_interval")
        work_interval_unit = request.form.get("work_interval_unit")
        category = request.form.get("main_category")
        style = request.form.get("scheduling_style")
        goal = request.form.get("primary_goal")

        work_hours = f"{work_start}-{work_end}"
        flexible = f"{flex_start}-{flex_end}"
        no_way = f"{no_start}-{no_end}"
        breaks = f"{break_length}{break_length_unit}/every {work_interval}{work_interval_unit}"

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            UPDATE users
            SET role=?, work_hours=?, flexible=?, no_way=?, breaks=?, categories=?, style=?, goal=?
            WHERE username=?
        """, (role, work_hours, flexible, no_way, breaks, category, style, goal, username))
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard.dashboard_page"))

    return render_template(
        "register_page.html",
        name=session.get("name", ""),
        username=session.get("username", ""),
        password=session.get("password", "")
    )
