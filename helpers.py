from functools import wraps
from flask import g, request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_manager") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_admin") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function