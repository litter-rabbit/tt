


from flask_login import current_user
from functools import wraps
from flask import abort

def admin_required(func):
    @wraps(func)
    def decrator(*args,**kwargs):
        if not current_user.is_admin:
            abort(404)
        return func(*args,**kwargs)
    return decrator

