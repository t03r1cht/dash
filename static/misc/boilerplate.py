

def boilerplate_authorization_required(session, redirect):

    # boilerplate::boilerplate_authorization_required
    try:
        session["uid"]
    except KeyError:
        return redirect("login")

    # custom code goes here

def boilerplate_no_login(session, render_template):

    # boilerplate::boilerplate_no_login
    try:
        if session["logged_in"]:
            return render_template("error.html", message="You are already signed in.")
    except:
        pass
