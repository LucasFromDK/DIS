import os
from flask import Flask, render_template, request

# Get public directory path
public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# Create Flask app with static folder configuration
app = Flask(__name__, static_folder=public_dir, static_url_path="/public")

# Variables
person = None
signed_in = False

@app.route("/")
def index():
    return render_template("index.html", signed_in = signed_in, person = person)

@app.route("/login")
def login():
    return render_template("login.html", signed_in = signed_in, person = person)

@app.route("/signup")
def signup():
    return render_template("signup.html", signed_in = signed_in, person = person)