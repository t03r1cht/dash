

def boilerplate_authorization_required(session, redirect):

    # boilerplate::boilerplate_authorization_required
    try:
        session["uid"]
    except KeyError:
        return redirect("login")

    # custom code goes here
