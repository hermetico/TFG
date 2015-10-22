from functools import wraps
from flask import g, request, redirect, url_for
from flask.ext.login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for('main.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function