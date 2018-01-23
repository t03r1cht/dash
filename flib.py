import re
from slib import *

"""
Function library.
"""

"""
#######################
Helper
#######################
"""


def check_email(param):
    if not param:
        return False
    if not check_mail(param):
        return False
    return True


def check_id(param):
    if not param:
        return False
    try:
        int_p = int(param)
    except:
        return False
    if int_p < 0:
        return False
    return True


def check_text(param):
    if not param:
        return False
    if param == "":
        return False
    return True


def check_password(param):
    if not param:
        return False
    if param == "":
        return False
    if not check_password_strength(param)[0]:
        return False
    return True


def check_token(param):
    if not param:
        return False
    if param == "":
        return False
    if not param.isalnum():
        return False
    return True



