from flask import Flask, render_template, session, redirect, request
from dashlogger import Logger
import config_handler
from flaskext.mysql import MySQL
from db_handler import DB_Handler
from werkzeug.security import generate_password_hash, check_password_hash
from config_handler import *

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
            return redirect("signin")

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


@app.route("/signup")
def signup():
    return "signup"


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/auth/login", methods=["POST"])
def handle_login():
    login_email = request.form["login-email"]
    login_password = request.form["login-password"]

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
    if user_record["role_id"] == check_config_entry("role_id-board-administrator"):
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
