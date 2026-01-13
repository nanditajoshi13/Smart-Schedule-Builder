import os
from flask import Flask, redirect, url_for
from flask_cors import CORS

from login_page import login_bp
from register_page import register_bp

app = Flask(__name__, template_folder=os.path.dirname(os.path.abspath(__file__)))
CORS(app)
app.secret_key = "supersecretkey"

# Register blueprints
app.register_blueprint(login_bp, url_prefix="/login")
app.register_blueprint(register_bp, url_prefix="/register")

@app.route("/")
def home():
    return redirect(url_for("login.home"))

if __name__ == "__main__":
    app.run(debug=True)
