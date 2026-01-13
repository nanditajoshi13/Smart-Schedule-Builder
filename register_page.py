import os
from flask import Blueprint, render_template, request, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
register_bp = Blueprint("register", __name__, template_folder=BASE_DIR)

DB_FILE = "users.db"

def save_user(name, username, password, setup_data):
    with open(DB_FILE, "a") as f:
        line = f"{name}|{username}|{password}"
        for key, value in setup_data.items():
            line += f"|{key}={value}"
        f.write(line + "\n")

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

        setup_data = {
            "role": role,
            "work_hours": f"{work_start}-{work_end}",
            "flexible": f"{flex_start}-{flex_end}",
            "no_way": f"{no_start}-{no_end}",
            "breaks": f"{break_length}{break_length_unit}/every {work_interval}{work_interval_unit}",
            "categories": category,
            "style": style,
            "goal": goal
        }

        save_user(name, username, password, setup_data)
        return f"Registration & Setup Successful! Saved {username} to {DB_FILE}"

    return render_template(
        "register_page.html",
        name=session.get("name", ""),
        username=session.get("username", ""),
        password=session.get("password", "")
    )
