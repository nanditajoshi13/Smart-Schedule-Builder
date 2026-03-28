import mysql.connector
from flask import Blueprint, render_template, request, session, redirect, url_for

register_bp = Blueprint("register", __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password", //enter your mysql password here
        database="schedule_db"
    )

@register_bp.route("/", methods=["GET", "POST"])
def register_page():

    if "user_id" not in session:
        return redirect(url_for("login.home"))

    if request.method == "POST":

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

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE users
            SET role=%s, work_hours=%s, flexible=%s, no_way=%s, breaks=%s, 
                categories=%s, style=%s, goal=%s
            WHERE id=%s
        """, (role, work_hours, flexible, no_way, breaks,
              category, style, goal, session["user_id"]))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard.dashboard_page"))

    return render_template(
        "register_page.html",
        name=session.get("name", ""),
        username=session.get("username", "")
    )
