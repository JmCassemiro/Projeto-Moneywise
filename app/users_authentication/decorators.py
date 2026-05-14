from functools import wraps

from flask import flash, make_response, redirect, url_for
from flask_jwt_extended import unset_jwt_cookies, verify_jwt_in_request


def jwt_page_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            flash("Sua sessão expirou. Faça login novamente.", category="auth")
            response = make_response(redirect(url_for("users.signin_page")))
            unset_jwt_cookies(response)
            return response
        return view(*args, **kwargs)

    return wrapped
