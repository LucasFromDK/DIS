import time
import os
import re
from uuid import UUID, uuid4
from flask import Flask, make_response, redirect, render_template, request
from werkzeug.datastructures import ImmutableMultiDict

# Get public directory path
public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# Create Flask app with static folder configuration
app = Flask(__name__, static_folder=public_dir, static_url_path="/public")

class User:
    def __init__(self, id:int, name:str, email:str):
        self.id = id
        self.name = name
        self.email = email

class Session:
    def __init__(self,lifetime:float, user:User):
        self.lifetime = lifetime
        self.token = uuid4()
        self.user = user

sessions: dict[UUID,Session] = {}

def get_logged_in(cookies: ImmutableMultiDict[str,str]) -> User | None:
    global sessions
    print("checking if logged in...")
    session_token = cookies.get("session_token")
    print(f"session_token: {session_token}")

    print(f"sessions: {sessions}")

    if session_token is None:
        return None

    try:
        session_token = UUID(session_token)
        if session_token in sessions:
            print(f"session_token is in sessions!")
            session = sessions[session_token]
            if session.lifetime > time.time():
                return session.user
            print(f"session expired")
            _=sessions.pop(session_token)
    except:
        pass

    print(f"invalid session_token...")
    return None

def is_logged_in(cookies: ImmutableMultiDict[str,str]) -> bool:
    return not get_logged_in(cookies) is None

@app.route("/")
def index():
    return render_template("index.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies))

@app.route("/login")
def login():
    return render_template("login.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies))

@app.route("/signup")
def signup():
    return render_template("signup.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies))

@app.route("/debug-test-session-token")
def test_sesh():
    global sessions
    response = redirect("/")
    test_user = User(0, "test_user", "test@ku.dk")
    session = Session(time.time() + 1000.0, test_user)
    sessions[session.token] = session
    response.set_cookie("session_token", session.token.hex, max_age=1000)

    return response

@app.get("/logout")
def logout():
    global sessions
    response = redirect("/")
    response.delete_cookie("session_token")
    session_token = request.cookies.get("session_token")
    if not session_token is None:
        try:
            _=sessions.pop(UUID(session_token))
        except:
            pass
    return response

@app.post("/signup")
def signup_post():
    email = request.form["Email"]
    password = request.form["Password"]
    repeat_password = request.form["Password2"]

    # Check email against a RegEx to ensure it's a KU Address
    # Check if email is either in the format of 3 letters followed by 3 numbers and then @alumni.ku.dk, or any email that ends with @di.ku.dk
    regex = r"^(?:[A-Za-z]{3}[0-9]{3}@alumni\.ku\.dk|.+@di\.ku\.dk)$"

    if not re.match(regex, email):
        return render_template("signup.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               invalid_email = True)

    # If Passwords do not match, set p tag with id "PasswordMismatch" to "Passwords do not match" in DOM
    if password != repeat_password:
        return render_template("signup.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               password_mismatch = True)

    return "TODO"