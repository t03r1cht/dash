from flask import Flask, render_template, session, redirect, request, url_for
from dashlogger import Logger
import config_handler
from flaskext.mysql import MySQL
from db_handler import DB_Handler
from werkzeug.security import generate_password_hash, check_password_hash
from config_handler import *
from flib import *
from slib import *

# Flask setup
app = Flask(__name__)
app.secret_key = "e5ac358c-f0bf-11e5-9e39-d3b532c10a28"

app.config["MYSQL_DATABASE_USER"] = "tech_dash_user"
app.config["MYSQL_DATABASE_PASSWORD"] = "dash_mysql_db"
app.config["MYSQL_DATABASE_DB"] = "dash_board_db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"

# MySQL setup
mysql = MySQL()
mysql.init_app(app)

# Logger setup
logger = Logger("log")  # Setup eigener Logger

# Session vars
SESSIONV_LOGGED_IN = "logged_in"
SESSIONV_USER = "user"
SESSIONV_UID = "uid"
SESSIONV_ROLE_ID = "role_id"
SESSIONV_VERIFIED = "verified"
SESSIONV_ADMIN = "is_admin"
SESSIONV_USERNAME = "username"
SESSIONV_ITER = [SESSIONV_LOGGED_IN, SESSIONV_USER, SESSIONV_UID,
                 SESSIONV_VERIFIED, SESSIONV_ADMIN]  # Iterable, für Session Termination


@app.route("/")
@app.route("/index")
def index():
    try:
        session[SESSIONV_LOGGED_IN]
    except:
        # If the user is not logged in and the board is configured to only display the forum to logged in users
        if config_handler.check_config_entry("board-access-mode", "login-required", check_values=True):
            return redirect("login")

    section_list = [
        {
            "title": "General",
            "section_preview": [{
                "name": "Welcome to the Dash Board...",
                "info": "Count: 1"
            },
                {
                    "name": "This is the first thread on the Dash Board...",
                    "info": "Count: 10"
                }]
        },
        {
            "title": "Announcements",
            "section_preview": [{
                "name": "Welcome to the Dash Board...",
                "info": "Count: 1"
            },
                {
                    "name": "his is the first thread on the Dash Board...",
                    "info": "Count: 10"
                }]
        }
    ]

    return render_template("board.html", section_list=section_list)


@app.route("/register")
def register():
    # boilerplate::boilerplate_no_login
    try:
        if session["logged_in"]:
            return render_template("error.html", message="Please log out in order to create a new account.")
    except:
        pass

    return render_template("signup.html")


@app.route("/login")
def login():
    # boilerplate::boilerplate_no_login
    try:
        if session["logged_in"]:
            return render_template("error.html", message="You are already signed in.")
    except:
        pass

    return render_template("signin.html")


@app.route("/auth/register", methods=["POST"])
def handle_register():
    reg_email = clean_text(request.form["reg-email"])
    reg_username = clean_text(request.form["reg-username"])
    reg_password = clean_text(request.form["reg-password"])
    reg_password_confirm = clean_text(request.form["reg-password-confirm"])

    # If the e-mail format was incorrect.
    if not check_email(reg_email):
        return render_template("register_failed.html", message="Please enter a valid E-Mail address.")

    # If the username format was incorrect.
    if not check_text(reg_username):
        return render_template("register_failed.html", message="Please enter a valid username.")

    # If the passwords did not match
    if not reg_password == reg_password_confirm:
        return render_template("register_failed.html", message="The passwords did not match. Please try again.")

    # If the password format (i.e. strength) was incorrect.
    if not check_password(reg_password) or not check_password(reg_password_confirm):
        return render_template("register_failed.html",
                               message="Please enter a valid password. You password must at least contain of 6 characters.")

    db_handler = DB_Handler()

    user_data = {}
    user_data["username"] = reg_username
    user_data["email"] = reg_email
    user_data["password"] = generate_password_hash(reg_password)

    user_added = db_handler.add_new_user(mysql, user_data)

    if not user_added:
        return render_template("register_failed.html",
                               message="The new user could not be added due to a internal error. Please try again. If the problem continues to exists, please get in touch with a support member.")

    if user_added is None:
        return render_template("register_failed.html",
                               message="The user already exists. You can login <a href=\"" + url_for(
                                   "login") + "\">here</a>.")

    return render_template("register_failed.html", message="Register ok. " + str(reg_email))


@app.route("/auth/login", methods=["POST"])
def handle_login():
    login_email = request.form["login-email"]
    login_password = request.form["login-password"]

    # Check for correct parameter format
    if not check_email(login_email) or not check_password(login_password):
        return render_template("error.html", message="Please enter a valid E-mail and password.")

    db_handler = DB_Handler()
    user_record = db_handler.check_for_user_existence(mysql, login_email)

    if user_record == None:
        return render_template("login_failed.html")

    # Check for password equality
    if not check_password_hash(user_record["password"], str(login_password)):
        return render_template("login_failed.html")

    session[SESSIONV_LOGGED_IN] = True
    session[SESSIONV_USER] = login_email
    session[SESSIONV_UID] = user_record["uid"]
    session[SESSIONV_USERNAME] = user_record["username"]

    # Set admin=True if the stored role_id of the user is equal to the configured board admin role_id

    if check_config_entry("role_id-board-administrator", str(user_record["role_id"]), check_values=True):
        session[SESSIONV_ADMIN] = True

    return render_template("login_success.html", user=user_record["username"])


@app.route("/auth/logout")
def logout():
    try:
        session[SESSIONV_LOGGED_IN]
    except:
        return render_template("error.html", message="You have to be signed in to be able to sign out.")

    email = session[SESSIONV_USER]

    for sessionv in SESSIONV_ITER:
        session.pop(sessionv, None)
    logger.success("Benutzer " + str(email) + " wurde erfolgreich ausgeloggt.")
    return render_template("logout_success.html")


@app.route("/about")
def about():
    return "about"


@app.route("/contact")
def contact():
    return "contact"


if __name__ == '__main__':
    app.run(debug=True)
