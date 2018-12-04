import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import time

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# database-dependent helper functions
# refers to index.html - display 'like' if user has not liked and 'unlike' if user has liked
def isLiked(pid):
    liked = db.execute("SELECT * FROM likes WHERE usr_id=:id AND post_id=:pid", id=session["user_id"], pid=pid)
    if liked:
        return "Unlike"
    return "Like"

# refers to index.html - display number of likes on a post
def likes(pid):
    return len(db.execute("SELECT * FROM likes WHERE post_id=:pid", pid=pid))

# refers to index.html - display number of comments on a post
def comments(pid):
    return len(db.execute("SELECT * FROM comments WHERE post_id=:pid", pid=pid))



# render the home page
@app.route("/home", methods=["GET","POST"])
def homepage():
    if request.method == "GET":
        return render_template("homepage.html")
    return redirect("/login")

# display all posts
@app.route("/", methods=["GET","POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html", posts=db.execute("SELECT * FROM posts ORDER BY dt DESC"), isLiked=isLiked, likes=likes, comments=comments, me=session["user_id"])
    return redirect("/post")


# display logged-in user's posts
@app.route("/my_posts")
@login_required
def my_posts():
    if request.method == "GET":
        return render_template("usr_posts.html", posts=db.execute("SELECT * FROM posts WHERE usr_id=:id ORDER BY dt DESC", id=session["user_id"]), isLiked=isLiked, likes=likes, comments=comments, me=session["user_id"], user=db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"], level=session["priv"])
    return redirect("/account")


# display any user's posts
@app.route("/usr/<usr_scrnm>")
@login_required
def usr(usr_scrnm):
    return render_template("usr_posts.html", posts=db.execute("SELECT * FROM posts WHERE usr_scrnm=:scrnm ORDER BY dt DESC", scrnm=usr_scrnm), isLiked=isLiked, likes=likes, comments=comments, me=session["user_id"], user=db.execute("SELECT scrnm FROM users WHERE scrnm=:scrnm", scrnm=usr_scrnm)[0]["scrnm"], level=db.execute("SELECT * FROM users WHERE scrnm=:scrnm", scrnm=usr_scrnm)[0]["priv"])


# make a post
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "GET":
        return render_template("newpost.html")

    # validate form
    if not request.form.get("title"):
        return apology("Please include a title.")
    if not request.form.get("post"):
        return apology("Your post cannot be blank.")

    # update databse
    db.execute("INSERT INTO posts (usr_id, text, usr_scrnm, title, dt) VALUES (:usr_id, :msg, :scrnm, :title, :dt)", usr_id=session["user_id"], msg=request.form.get("post"), scrnm=db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"], title=request.form.get("title"), dt=time.strftime('%c'))
    return redirect("/")


# delete one of logged-in user's posts
@app.route("/delete/<pid>")
@login_required
def delete(pid):
    # only authorized users can delete posts
    if session["user_id"] == db.execute("SELECT * FROM posts WHERE id=:pid", pid=pid)[0]["usr_id"] or session["priv"] > 0:
        # update database, and delete all comments and likes associated with the post
        db.execute("DELETE FROM posts WHERE id=:id", id=pid)
        db.execute("DELETE FROM comments WHERE post_id=:id", id=pid)
        db.execute("DELETE FROM likes WHERE post_id=:id", id=pid)
    return redirect("/")


# see any post
@app.route("/see_post/<pid>")
@login_required
def see_post(pid):
    # set comment tracking configuration
    session["post"] = pid
    return render_template("see_post.html", title=db.execute("SELECT title FROM posts WHERE id=:id", id=session["post"])[0]["title"], text=db.execute("SELECT text FROM posts WHERE id=:id", id=pid)[0]["text"], comments=db.execute("SELECT * FROM comments WHERE post_id=:id ORDER BY dt ASC", id=session["post"]))


# leave a comment
@app.route("/comment", methods=["POST"])
@login_required
def comment():
    # update database
    db.execute("INSERT INTO comments (usr_id, text, dt, usr_scrnm, post_id) VALUES (:id, :msg, :dt, :scrnm, :post_id)", id=session["user_id"], msg=request.form.get("comment"), dt=time.strftime('%Y-%m-%d %H:%M:%S'), scrnm=db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"], post_id=session["post"])
    return redirect(url_for("see_post", pid=session["post"]))


# like a post
@app.route("/like/<pid>")
@login_required
def like(pid):
    liked = db.execute("SELECT * FROM likes WHERE usr_id=:id AND post_id=:pid", id=session["user_id"], pid=pid)

    # unlike if already liked
    if liked:
        db.execute("DELETE FROM likes WHERE usr_id=:id AND post_id=:pid", id=session["user_id"], pid=pid)

    # like if not already liked
    else:
        db.execute("INSERT INTO likes (usr_id, post_id, usr_scrnm) VALUES (:id, :pid, :scrnm)", id=session["user_id"], pid=pid, scrnm=db.execute("SELECT * FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"])

    return redirect("/")





# admin privileges
# delete any user's account
@app.route("/admin_del/<usr_scrnm>", methods=["POST"])
@login_required
def admin_delete(usr_scrnm):
    # check that user not admin
    if usr_scrnm == "admin":
        return apology("The administrator cannot delete itself.")

    # let admin delete user account
    elif session["priv"] == 2:
        db.execute("DELETE FROM users WHERE scrnm=:scrnm", scrnm=usr_scrnm)
        db.execute("DELETE FROM comments WHERE usr_scrnm=:scrnm", scrnm=usr_scrnm)
        db.execute("DELETE FROM likes WHERE usr_scrnm=:scrnm", scrnm=usr_scrnm)
        db.execute("DELETE FROM posts WHERE usr_scrnm=:scrnm", scrnm=usr_scrnm)

    return redirect("/")


# change user privileges
@app.route("/admin_make_mod/<usr_scrnm>", methods=["GET", "POST"])
@login_required
def make_mod(usr_scrnm):
    # chek that user not admin
    if usr_scrnm == "admin":
        return apology("The administrator cannot demote itself. This action would demote the administrator.")

    # admin action
    elif session["priv"] == 2:
        if db.execute("SELECT * FROM users WHERE scrnm=:scrnm", scrnm=usr_scrnm)[0]["priv"] == 0:
            db.execute("UPDATE users SET priv=1 WHERE scrnm=:scrnm", scrnm=usr_scrnm)

        else:
            db.execute("UPDATE users SET priv=0 WHERE scrnm=:scrnm", scrnm=usr_scrnm)

    return redirect("/")





# account-related methods
# display account settings page
@app.route("/account")
@login_required
def acct():
    return render_template("account.html", screen_name=db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"], level=session["priv"])


# change logged-in user's password
@app.route("/account/change_pwd", methods=["GET", "POST"])
@login_required
def change_pwd():
    if request.method == "GET":
        return render_template("change_pwd.html", screen_name=db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"])

    # validate form
    if not request.form.get("old_pwd"):
        return apology("You must enter your old password before changing it.")
    if not request.form.get("new_pwd"):
        return apology("You must choose a new password.")
    if not request.form.get("new_pwd_cnfrm"):
        return apology("You must confirm your new password.")
    if request.form.get("new_pwd") != request.form.get("new_pwd_cnfrm"):
        return apology("Your new passwords must match.")

    old_hash = db.execute("SELECT hash FROM users WHERE id=:id", id=session["user_id"])[0]["hash"]

    # verify
    if not check_password_hash(old_hash, request.form.get("old_pwd")):
        return apology("You failed to properly input your old password.")
    db.execute("UPDATE users SET hash=:hash WHERE id=:id", id=session["user_id"], hash=generate_password_hash(request.form.get("new_pwd")))

    return redirect("/logout")


# change logged-in user's screen name
@app.route("/account/change_scrnm", methods=["GET", "POST"])
@login_required
def change_scrnm():
    if request.method == "GET":
        return render_template("change_scrnm.html", screen_name=db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"])

    name = db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"]

    if not request.form.get("new_scrnm"):
        return apology("Please enter a new screen name to change it.")
    if not request.form.get("new_scrnm_cnfrm"):
        return apology("Please confirm your screen name.")
    if request.form.get("new_scrnm") != request.form.get("new_scrnm_cnfrm"):
        return apology("Please ensure that your screen names match.")
    if name == "admin":
        return apology("The administrator cannot rename itself.")

    # check for repeats
    result = db.execute("SELECT * FROM users WHERE scrnm=:scrnm", scrnm=request.form.get("new_scrnm"))
    if result:
        return apology("This screen name is taken. Try a different one.")
    db.execute("UPDATE users SET scrnm=:scrnm WHERE id=:id", scrnm=request.form.get("new_scrnm"), id=session["user_id"])

    return redirect("/logout")


# delete logged-in user's account
@app.route("/account/delete", methods=["POST"])
@login_required
def delete_account():
    name = db.execute("SELECT scrnm FROM users WHERE id=:id", id=session["user_id"])[0]["scrnm"]
    if name == "admin":
        return apology("The administrator cannot delete itself.")

    db.execute("DELETE FROM users WHERE id=:id", id=session["user_id"])
    db.execute("DELETE FROM comments WHERE usr_id=:id", id=session["user_id"])
    db.execute("DELETE FROM likes WHERE usr_id=:id", id=session["user_id"])
    db.execute("DELETE FROM posts WHERE usr_id=:id", id=session["user_id"])
    return redirect("/logout")


# log in
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
        rows = db.execute("SELECT * FROM users WHERE scrnm = :scrnm",
                          scrnm=request.form.get("screen_name"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid screen name and/or password.", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # record privileges
        session["priv"] = rows[0]["priv"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# log out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# register for an account
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
            return apology("Please ensure that your password contains at least one digit.")

    # encrypt password and instantiate variables
    pwd = generate_password_hash(request.form.get("password-cnfrm"))
    usr = request.form.get("screen_name")

    # check for repeats
    result = db.execute("SELECT * FROM users WHERE scrnm=:scrnm", scrnm=usr)
    if result:
        return apology("This screen name is taken. Try a different one.")

    # insert user into database
    db.execute("INSERT INTO users (scrnm, hash) VALUES (:scrnm, :pwd)", scrnm=usr, pwd=pwd)

    # log user in
    session["user_id"] = db.execute("SELECT * FROM users WHERE scrnm = :scrnm", scrnm=request.form.get("screen_name"))[0]["id"]

    # record privileges
    session["priv"] = db.execute("SELECT * FROM users WHERE scrnm = :scrnm", scrnm=request.form.get("screen_name"))[0]["priv"]

    return redirect("/")
