import sqlite3
import time
import os
import re
from tkinter import INSERT
from uuid import UUID, uuid4
from flask import Flask, make_response, redirect, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.wrappers import response
from database import Database

database = Database()

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
@app.before_request
def log_in_debug():
    # Check if Flask is in debug mode, if so, automatically log in with a test user
    if app.debug and not is_logged_in(request.cookies) and not request.path == "/debug-test-session-token":
        return redirect("/debug-test-session-token")

@app.before_request
def check_logged_in():
    if request.path.startswith("/api") and not is_logged_in(request.cookies):
        return "Unauthorized", 503

@app.route("/api/products")
def get_products():
    # Join products with sellers on sellerid to get the seller's name
    return database.query_json("""SELECT p.*, u.username as sellername
                                FROM products AS p
                                LEFT JOIN sellers AS s ON p.sellerid = s.id
                                LEFT JOIN users   AS u ON s.userid   = u.id;""")

@app.route("/api/sellers")
def get_sellers():
    # Join products with sellers on sellerid to get the seller's name
    return database.query_json("""SELECT s.id, u.username
                                     FROM sellers AS s
                                     LEFT JOIN users AS u ON s.userid = u.id
                                  """)

@app.route("/login")
def login():
    return render_template("login.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies),
                           error = None)

@app.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    cursor = database.query(f"SELECT id, username, email FROM users WHERE (username=? OR email=?) AND password=?", (username, username, password))
    user_data = cursor.fetchone()

    if user_data is None:
        return render_template("login.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Invalid username/email or password")

    user = User(user_data[0], user_data[1], user_data[2])
    session = Session(time.time() + 3600.0, user)
    sessions[session.token] = session

    response = redirect("/")
    response.set_cookie("session_token", session.token.hex, max_age=3600)

    return response

@app.route("/signup")
def signup():
    return render_template("signup.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies),
                           error = None)

@app.post("/signup")
def signup_post():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    repeat_password = request.form["password2"]

    # Check email against a RegEx to ensure it's a KU Address
    # Check if email is either in the format of 3 letters followed by 3 numbers and then @alumni.ku.dk, or any email that ends with @di.ku.dk
    regex = r"^(?:[A-Za-z]{3}[0-9]{3}@alumni\.ku\.dk|.+@di\.ku\.dk)$"

    if not re.match(regex, email):
        return render_template("signup.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Please enter a valid KU Student email address.")

    if password != repeat_password:
        return render_template("signup.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Passwords do not match!")

    try:
        cursor = database.query(f"INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        database.commit()

        response = redirect("/")
        return response
    except sqlite3.IntegrityError as e:
        error = e.args[0]
        if "username" in error:
            error = "Username already taken"
        elif "email" in error:
            error = "Email already in use"
        return render_template("signup.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = f"error creating user: {error}")

# TODO: Implement seller registration functionality
@app.route("/seller")
def seller():
    if not is_logged_in(request.cookies):
        return redirect("/login")

    return render_template("seller.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies))

@app.route("/create-listing")
def create_listing():
    if not is_logged_in(request.cookies):
        return redirect("/login")

    # Add Seller Check Here once that functionality is implemented
    if not is_seller(request.cookies):
        return redirect("/seller")

    return render_template("create_listing.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies))

# TODO: Implement create listing functionality, including database insertion and form validation
@app.post("/create-listing")
def create_listing_post():
    if not is_logged_in(request.cookies):
        return redirect("/login")

    if not is_seller(request.cookies):
        return redirect("/seller")

    product_name = request.form["product_name"]
    product_description = request.form["product_description"]
    product_price = float(request.form["product_price"])
    amount_available = int(request.form["amount_available"])

    # Form Validation
    if len(product_name) == 0:
        return render_template("create_listing.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Product name cannot be empty")

    if len(product_description) == 0:
        return render_template("create_listing.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Product description cannot be empty")

    if product_price < 0:
        return render_template("create_listing.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Price cannot be negative")

    if amount_available <= 0:
        return render_template("create_listing.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Amount available cannot be zero or negative")

    # Add logic to create the listing in the database here.
    # INSERT INTO sellers (userid) VALUES (1),(2),(3);
    # INSERT INTO products (sellerid, name, description, price, units)
    try:
        cursor = database.query(f"SELECT id FROM sellers WHERE userid=?", (get_logged_in(request.cookies).id,))
        seller_data = cursor.fetchone()

        # This should never happen but a final safety check to ensure the user is actually a seller before allowing them to create a listing.
        if seller_data is None:
            return render_template("create_listing.html",
                                signed_in = is_logged_in(request.cookies),
                                person = get_logged_in(request.cookies),
                                error = "Seller not found. Please register as a seller before creating a listing.")

        # Add the listing to the database
        cursor = database.query(f"INSERT INTO products (sellerid, name, description, price, units) VALUES (?, ?, ?, ?, ?)",
                                (seller_data[0], product_name, product_description, int(product_price * 100), amount_available))

        database.commit()
        return redirect("/")  # Redirect to the marketplace page. Post should be visible immediately.
    # TODO: Error handling and messages for database insertion failures.
    except sqlite3.IntegrityError as e:
            error = e.args[0]
            if "PLACEHOLDER" in error:
                error = "ERROR"
            elif "PLACEHOLDER2" in error:
                error = "ERROR2"
            return render_template("create-listing.html",
                                signed_in = is_logged_in(request.cookies),
                                person = get_logged_in(request.cookies),
                                error = f"Error3: {error}")

@app.route("/debug-test-session-token")
def test_sesh():
    global sessions
    response = redirect("/")
    test_user = User(0, "[Test Account]", "test@ku.dk")
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