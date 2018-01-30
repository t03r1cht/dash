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

    board_content = []

    db_handler = DB_Handler()
    section_list = db_handler.get_section_list(mysql)

    for section in section_list:
        """
        Multiple temps will be appended to the board_content object. 
        Each temp object is a dict that will consist of the title of 
        the section and contain a list under the "subsection_list" key that will
        contain a list of all the subsections of the current section.
        """
        temp = {}
        temp["title"] = str(section[1])
        temp["section_id"] = section[0]
        all_subsections = db_handler.get_subsections_for_section_id(mysql, int(section[0]))
        subsection_list = []

        for subsection in all_subsections:
            # Dictionary that contains the meta data for a subsection
            ss_dict = {}
            ss_dict["subsection_id"] = subsection[0]
            ss_dict["subsection_name"] = subsection[1]
            ss_dict["subsection_desc"] = subsection[2]

            subsection_list.append(ss_dict)

        temp["subsection_list"] = subsection_list
        print(temp)

        # For each iteration for every section append the section and its subsections to the board content that is displayed on the index page
        board_content.append(temp)

    return render_template("board.html", section_list=board_content)


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

    user_added, e = db_handler.add_new_user(mysql, user_data)

    # Catch internal error
    if user_added is False:
        logger.error("Error at registering new user " + str(reg_email) + " with exception:\n" + str(e))
        return render_template("register_failed.html",
                               message="The new user could not be added due to a internal error. Please try again. If the problem continues to exists, please get in touch with a support member.")

    # If the user is already registered
    if user_added is None:
        return render_template("register_failed.html",
                               message="The user already exists. You can login <a href=\"" + url_for(
                                   "login") + "\">here</a>.")

    logger.success("New registration: " + str(reg_email))
    return render_template("register_success.html",
                           message="Your registration has been successful. You can login <b><a href=\"" + url_for(
                               "login") + "\">here</a></b>.")


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


@app.route("/auth/admin/cp")
def admin_cp():
    try:
        session[SESSIONV_ADMIN]

    except:
        try:
            session[SESSIONV_LOGGED_IN]
            logger.error("User " + str(session[SESSIONV_USER]) + " tried to access the Administrator Control Panel.")
            return render_template("error.html",
                                   message="You need administrator privileges to access the Administrator Control Panel. This incident will be reported.")
        except:
            logger.error("Unauthenticated user tried to access the Administrator Control Panel.")
            return render_template("error.html",
                                   message="You need administrator privileges to access the Administrator Control Panel. This incident will be reported.")

    logger.success("Administrator " + str(session[SESSIONV_USER]) + " accessed the Administrator Control Panel.")

    return render_template("admin_cp.html")


@app.route("/about")
def about():
    return "about"


@app.route("/contact")
def contact():
    return "contact"


@app.route("/section")
def show_section():
    section_id = request.args.get("s")

    return "section=" + str(section_id)


@app.route("/subsection")
def show_subsection():
    subsection_id = request.args.get("s")

    return "subsection=" + str(subsection_id)


"""
#############################
Error Handler
#############################
"""


@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
