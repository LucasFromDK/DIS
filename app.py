import sqlite3
import time
import os
import re
from uuid import UUID, uuid4
from flask import Flask,  redirect, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
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


def is_seller(cookies: ImmutableMultiDict[str,str]) -> bool:
    user = get_logged_in(cookies)
    if user is None: return False
    cursor = database.query(f"SELECT 1 FROM sellers WHERE userid = ?", (user.id,))
    found = cursor.fetchone()
    if found is None: return False
    return True

@app.route("/")
def index():
    return render_template("index.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies),
                           is_seller = is_seller(request.cookies))
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


@app.route("/api/product(<int:id>)")
def get_product_by_id(id):
    # Join products with sellers on sellerid to get the seller's name
    rows = database.query_json("""SELECT p.*, u.username as sellername
                                FROM products AS p
                                LEFT JOIN sellers AS s ON p.sellerid = s.id
                                LEFT JOIN users   AS u ON s.userid   = u.id
                                WHERE p.id = ?;""", (id,))
    print(rows)

    if len(rows) == 0:
        return f"Product with id {id} not found", 404

    return rows[0]


@app.route("/api/products/delete(<int:id>)")
def delete_product(id: int):
    user = get_logged_in(request.cookies)

    if user is None:
        raise Exception("Unreachable")

    user_id, = database.query("""SELECT s.userid
                                FROM products AS p
                                INNER JOIN sellers AS s ON p.sellerid = s.id
                                AND p.id = ?;""", (id,)).fetchone()

    if user_id == user.id:
        database.query("DELETE FROM products WHERE id = ?", (id,))
        database.commit()
        return f"Deleted product with id {id}", 200

    return "Not the seller of this product", 503


@app.route("/api/sellers")
def get_sellers():
    # Join products with sellers on sellerid to get the seller's name
    return database.query_json("""SELECT s.id, u.username, s.escrow
                                 FROM sellers AS s
                                 LEFT JOIN users AS u ON s.userid = u.id
                                  """)

@app.route("/api/logged_in_user")
def get_logged_in_user():
    user = get_logged_in(request.cookies)
    if user is None:
        return "Unauthorized", 503
    return {"id": user.id, "name": user.name, "email": user.email}

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
    user = cursor.fetchone()

    if user is None:
        return render_template("login.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               error = "Invalid username/email or password")

    id,username,email = user

    user = User(id,username,email)
    session = Session(time.time() + 3600.0, user)
    sessions[session.token] = session

    response = redirect("/")
    response.set_cookie("session_token", session.token.hex, max_age=3600)
    response.set_cookie("my_id", str(user.id), max_age=3600)

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

@app.route("/seller")
def seller():
    if not is_logged_in(request.cookies):
        return redirect("/login")

    if is_seller(request.cookies):
        return redirect("/create-listing")

    return render_template("seller.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies))


@app.route("/seller", methods=["POST"])
def becum_seller():
    user = get_logged_in(request.cookies)
    if user is None:
        return redirect("/login")

    if is_seller(request.cookies):
        return redirect("/create-listing")

    _ = database.query("INSERT INTO sellers (userid) VALUES (?)", (user.id,))
    database.commit()

    return redirect("/seller")

@app.route("/create-listing")
def create_listing():
    product_name = None
    product_description = None
    product_price = None
    amount_available = None
    error = None

    # Should never be reached but just in case, if the user is not logged in, redirect to login page.
    if not is_logged_in(request.cookies):
        return redirect("/login")

    # Should never be reached but just in case, if the user is not a seller, redirect to seller registration page.
    if not is_seller(request.cookies):
        return redirect("/seller")

    # Else render the create listing page.
    return render_template("create-listing.html",
                           signed_in = is_logged_in(request.cookies),
                           person = get_logged_in(request.cookies),
                           product_name = product_name,
                           product_description = product_description,
                           product_price = product_price,
                           amount_available = amount_available,
                           error = error)

# Logic for creating a listing.
@app.post("/create-listing")
def create_listing_post():
    user = get_logged_in(request.cookies)

    # This should never be reached but just in case.
    if user is None:
        return redirect("/login")

    if not is_seller(request.cookies):
        return redirect("/seller")

    product_name = request.form["product_name"]
    product_description = request.form["product_description"]
    product_price = float(request.form["product_price"])
    amount_available = int(request.form["amount_available"])
    error = None

    # Convert e.g. 4,95 to 4.95 if user entered a comma instead of a dot for the price.
    if "," in request.form["product_price"]:
        try:
            product_price = float(request.form["product_price"].replace(",", "."))
        except ValueError:
            error = "Invalid price format. Please enter a valid number for the price."
    else:
        product_price = float(request.form["product_price"])

    # Form Validation
    if len(product_name) == 0:
        error = "Product name can't be empty"
    if len(product_description) == 0:
           error = "Product description can't be empty"
    if product_price < 0 or int(product_price * 100) < 0:
           error = "Price can't be negative"
    if amount_available <= 0:
           error = "Amount available can't be zero or negative"

    if not error == None:
        # If there is an error, re-render the create listing page with the previously entered info and the error message.
        return render_template("create-listing.html",
                               signed_in = is_logged_in(request.cookies),
                               person = get_logged_in(request.cookies),
                               product_name = product_name,
                               product_description = product_description,
                               product_price = product_price,
                               amount_available = amount_available,
                               error = error)
    try:
        cursor = database.query(f"SELECT id FROM sellers WHERE userid = ?", (user.id,))
        seller_id, = cursor.fetchone()

        # This should never happen but a final safety check to ensure the user is actually a seller before allowing them to create a listing.
        if seller_id is None:
            return render_template("create-listing.html",
                                signed_in = is_logged_in(request.cookies),
                                person = get_logged_in(request.cookies),
                                error = "Seller not found. Please register as a seller before creating a listing.")

        # Add the listing to the database
        cursor = database.query(f"INSERT INTO products (sellerid, name, description, price, units, createdOn) VALUES (?, ?, ?, ?, ?, ?)",
                                (seller_id, product_name, product_description, int(product_price * 100), amount_available, int(time.time())))

        database.commit()
        return redirect("/")  # Redirect to the marketplace page. Post should be visible immediately.
    except (sqlite3.IntegrityError, OverflowError) as e:
            if error is OverflowError:
                error = "One of your numbers is too large."
            else:
                error = e.args[0]
            return render_template("create-listing.html",
                                signed_in = is_logged_in(request.cookies),
                                person = get_logged_in(request.cookies),
                                error = f"Error: {error}")

@app.route("/buy-listing")
def buy_listing():
    return render_template("buy-listing.html",
                           signed_in = is_logged_in(request.cookies),
                           card_number = None,
                           card_expiration = None,
                           cvc = None,
                           delivery_address = None)

@app.post("/buy-listing")
def buy_listing_post():
    unit_amount = int(request.form["unit_amount"])
    card_number = request.form["card_number"].replace(" ", "")
    card_expiration = request.form["card_expiration"]
    cvc = request.form["cvc"]
    delivery_address = request.form["delivery_address"]


    render_error = lambda error: render_template("buy-listing.html",
                               signed_in = is_logged_in(request.cookies),
                               unit_amount = unit_amount,
                               card_number = card_number,
                               card_expiration = card_expiration,
                               cvc = cvc,
                               delivery_address = delivery_address,
                               error = error)

    pid = request.args.get("pid")

    if pid is None:
        return redirect("/")

    cursor = database.query("SELECT p.id,p.price,p.units,p.sellerid,s.escrow FROM products AS p LEFT JOIN sellers AS s ON s.id = p.sellerid WHERE p.id = ?",(pid,)).fetchone()

    if cursor is None:
        # invalid product
        return render_error(f"No product with id {pid} found!")

    id,price,units,sellerid,escrow = cursor

    if unit_amount < 1:
        return render_error("Cannot buy less than 1 unit")

    # Check units available
    if units <= 0:
        return render_error("Sorry, this product is out of stock.")

    # Check units available
    if units - unit_amount < 0:
        return render_error(f"Sorry, but theres not enough stock left for you to buy {unit_amount} units")

    # Returns true if given card
    # number is valid
    def checkLuhn(cardNo):
        nDigits = len(cardNo)
        nSum = 0
        isSecond = False

        for i in range(nDigits - 1, -1, -1):
            d = ord(cardNo[i]) - ord('0')

            if (isSecond == True):
                d = d * 2

            # We add two digits to handle
            # cases that make two digits after
            # doubling
            nSum += d // 10
            nSum += d % 10

            isSecond = not isSecond

        if (nSum % 10 == 0):
            return True
        else:
            return False

    # Check if card number is valid using Luhn's algorithm
    if not checkLuhn(card_number):
        return render_error("Invalid card number. Please enter a valid card number from a supported issuer.")

    # Check if valid expiration date (for simplicity, just check if it's in the format MM/YY and is a valid date in the future)
    if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", card_expiration):
        return render_error("Invalid expiration date. Please enter a valid expiration date in the format MM/YY.")
    else:
        month, year = map(int, card_expiration.split("/"))
        year += 2000  # Convert YY to YYYY
        current_year = time.localtime().tm_year
        current_month = time.localtime().tm_mon
        if year < current_year or (year == current_year and month < current_month):
            return render_error("Card has expired. Please enter a valid expiration date in the future.")

    # Check CVC
    if not re.match(r"^\d{3}$", cvc):
        return render_error("Invalid CVC. Please enter a valid 3-digit CVC.")


    try:
        _ = database.query("UPDATE products SET units = ? WHERE id = ?",(units - unit_amount, pid,))
        if not sellerid is None:
            _ = database.query("UPDATE sellers SET escrow = ? WHERE id = ?",((escrow or 0) + price, sellerid,))
        database.commit()
    except Exception as e:
        database.rollback()
        return render_error(f"An error occured when finalizing the purchase. Please try again: {e}")

    return redirect(f"/success?pid={pid}&amount={unit_amount}")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/debug-test-session-token")
def test_sesh():
    global sessions
    response = redirect("/")
    id,name,email = database.query("SELECT id,username,email FROM users WHERE id = 1").fetchone()
    test_user = User(id,name,email)
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