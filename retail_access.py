from functools import wraps
from flask import session, redirect, url_for, abort

def retail_role_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not session.get("userid"):
                return redirect(url_for("login"))

            if session.get("userrole") not in allowed_roles:
                abort(403)

            return func(*args, **kwargs)

        return wrapper
    return decorator