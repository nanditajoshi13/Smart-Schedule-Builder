import mysql.connector
from flask import Flask, redirect, url_for
from flask_cors import CORS

from login_page import login_bp
from register_page import register_bp
from dashboard import dashboard_bp

app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="#N_joshi13",
        database="schedule_db"
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(100),
        work_hours VARCHAR(50),
        flexible VARCHAR(50),
        no_way VARCHAR(50),
        breaks VARCHAR(100),
        categories VARCHAR(100),
        style VARCHAR(50),
        goal VARCHAR(100)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,

        name VARCHAR(255) NOT NULL,
        duration FLOAT NOT NULL,

        priority INT DEFAULT 3,
        task_type VARCHAR(50) DEFAULT 'other',

        deadline DATE,
        status VARCHAR(20) DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_preferences (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,

        date DATE,
        work_hours VARCHAR(50),
        no_way VARCHAR(50),
        breaks VARCHAR(100),

        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cur.close()
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
