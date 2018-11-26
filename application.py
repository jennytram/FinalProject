import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def render():
    # NOTE TO JENNY: create "index.html"
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("screen_name"):
            return apology("Please provide your screen name.", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide your password.", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid screen name and/or password.", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # check form
    if not request.form.get("screen_name"):
        return apology("Please provide a screen name.")
    if not request.form.get("password"):
        return apology("Please provide a password.")
    if not request.form.get("password-cnfrm"):
        return apology("Please confirm your password.")
    if request.form.get("password-cnfrm") != request.form.get("password"):
        return apology("Please ensure that your passwords match.")

    # check that password contains a digit
    digits = "1234567890"

    for i in range(len(digits)):
        if digits[i] in request.form.get("password-cnfrm"):
            break
        if digits[i] == "0":
            return apology("Please ensure that password contains at least one digit.")

    # encrypt password and instantiate variables
    pwd = generate_password_hash(request.form.get("password-cnfrm"))
    usr = request.form.get("screen_name")

    # check for repeats
    result = db.execute("SELECT * FROM users WHERE username=:usr", usr=usr)
    if result:
        return apology("username is taken")

    # insert user into database
    db.execute("INSERT INTO users (username, hash) VALUES (:usr, :pwd)", usr=usr, pwd=pwd)

    # log user in
    session["user_id"] = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))[0]["id"]

    #return redirect(somewhere)
