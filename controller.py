import sqlite3
import os
from flask import Flask, redirect, url_for
from flask_cors import CORS
from login_page import login_bp
from register_page import register_bp
from dashboard import dashboard_bp

app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"

DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT,
        work_hours TEXT,
        flexible TEXT,
        no_way TEXT,
        breaks TEXT,
        categories TEXT,
        style TEXT,
        goal TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(register_bp, url_prefix="/register")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")


@app.route("/")
def home():
    return redirect(url_for("login.home"))

if __name__ == "__main__":
    app.run(debug=True)
