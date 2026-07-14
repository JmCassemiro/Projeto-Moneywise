from datetime import datetime, timedelta, timezone

from flask import Blueprint, flash, jsonify, make_response, redirect
from flask import render_template, request, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import NoAuthorizationError

from app.exceptions import AppError
from app.users_authentication.decorators import jwt_page_required
from app.users_authentication.forms import (
    RequestResetForm,
    ResetPasswordForm,
    UserDeleteForm,
    UserSigninForm,
    UserSignupForm,
)
from app.users_authentication.services.password_reset_service import (
    PasswordResetService,
)
from app.users_authentication.services.user_service import UserService


users = Blueprint(
    "users",
    __name__,
    static_folder="static",
    template_folder="templates",
    static_url_path="/users/static",
)


@users.route("/signin", methods=["GET", "POST"])
def signin_page():
    authenticated_redirect = _redirect_if_authenticated()
    if authenticated_redirect:
        return authenticated_redirect

    form = UserSigninForm()
    if form.validate_on_submit():
        user = UserService.authenticate(form.email.data, form.password.data)
        if user:
            response = make_response(
                redirect(url_for("transactions.transactions_page"))
            )
            set_access_cookies(
                response,
                create_access_token(identity=str(user.id)),
            )
            return response
        flash("Email ou senha inválidos", category="danger")
    elif form.is_submitted():
        _flash_form_errors(form)

    return render_template("signin_page.html", form=form)


@users.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = UserSignupForm()
    if form.validate_on_submit():
        try:
            UserService.create_user(
                name=form.username.data,
                email=form.email_address.data,
                password=form.password.data,
                birthday=form.birthday.data,
            )
            flash("Conta criada com sucesso. Faça login.", category="auth")
            return redirect(url_for("users.signin_page"))
        except AppError as exc:
            flash(exc.message, category="danger")
    elif form.is_submitted():
        _flash_form_errors(form)

    return render_template("signup_page.html", form=form)


@users.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for("users.signin_page")))
    unset_jwt_cookies(response)
    flash("Logout realizado com sucesso!", category="auth")
    return response


@users.route("/token/expires", methods=["GET"])
@jwt_page_required
def token_expires():
    jwt_payload = get_jwt()
    exp_timestamp = jwt_payload.get("exp")
    if not exp_timestamp:
        return jsonify({"error": "Token nao contem expiracao."}), 400

    brasilia_tz = timezone(timedelta(hours=-3))
    now = datetime.now(timezone.utc).astimezone(brasilia_tz)
    exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).astimezone(
        brasilia_tz
    )
    remaining = exp - now
    if remaining.total_seconds() < 0:
        return jsonify({"message": "Token ja expirou."}), 401

    total_seconds = int(remaining.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    human_readable = (
        f"{days}d {hours}h {minutes}m {seconds}s"
        if days
        else f"{hours}h {minutes}m {seconds}s"
    )
    if not days and not hours:
        human_readable = f"{minutes}m {seconds}s"

    return jsonify(
        {
            "current_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": exp.strftime("%Y-%m-%d %H:%M:%S"),
            "time_remaining_seconds": total_seconds,
            "time_remaining_human": human_readable,
        }
    )


@users.route("/profile")
@jwt_page_required
def profile_page():
    user = UserService.get_user(get_jwt_identity())
    return render_template("profile.html", user=user, form=UserDeleteForm())


@users.route("/profile/update", methods=["POST"])
@jwt_page_required
def update_profile():
    try:
        user = UserService.update_profile(
            get_jwt_identity(),
            request.get_json(silent=True) or {},
        )
        return jsonify(
            {
                "success": True,
                "message": "Dados atualizados com sucesso.",
                "user": user.to_dict(),
            }
        )
    except AppError as exc:
        return jsonify({"success": False, "message": exc.message}), exc.status_code


@users.route("/delete_account", methods=["POST"])
@jwt_page_required
def delete_account():
    form = UserDeleteForm()
    if form.validate_on_submit():
        try:
            UserService.delete_account(get_jwt_identity(), form.password.data)
            response = make_response(redirect(url_for("users.signin_page")))
            unset_jwt_cookies(response)
            flash("Conta excluída com sucesso.", category="auth")
            return response
        except AppError as exc:
            flash(exc.message, category="danger")
    else:
        _flash_form_errors(form)

    return redirect(url_for("users.profile_page"))


@users.route("/forgot-password", methods=["GET", "POST"])
def forgot_password_page():
    form = RequestResetForm()
    if form.validate_on_submit():
        try:
            PasswordResetService.send_reset_link(form.email.data)
            flash(
                "Um link de recuperação foi enviado para seu e-mail.",
                category="info",
            )
            return redirect(url_for("users.signin_page"))
        except AppError as exc:
            flash(exc.message, category="danger")
    elif form.is_submitted():
        _flash_form_errors(form)

    return render_template("request_password_page.html", form=form)


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            PasswordResetService.reset_password(token, form.password.data)
            flash("Senha redefinida com sucesso!", category="success")
            return redirect(url_for("users.signin_page"))
        except AppError as exc:
            flash(exc.message, category="danger")
            return redirect(url_for("users.forgot_password_page"))
    elif form.is_submitted():
        _flash_form_errors(form)

    return render_template("reset_password_page.html", form=form)


def _redirect_if_authenticated():
    try:
        verify_jwt_in_request(optional=True)
        if get_jwt_identity():
            return redirect(url_for("transactions.transactions_page"))
    except NoAuthorizationError:
        return None
    except Exception:
        response = make_response(redirect(url_for("users.signin_page")))
        unset_jwt_cookies(response)
        flash("Sua sessão expirou. Faça login novamente.", category="auth")
        return response
    return None


def _flash_form_errors(form) -> None:
    for messages in form.errors.values():
        for message in messages:
            flash(message, category="danger")
