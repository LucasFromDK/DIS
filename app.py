import os
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="public", static_url_path="/public")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
