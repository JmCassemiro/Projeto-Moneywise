from flask import Blueprint, current_app, flash, redirect, render_template, request
from flask import url_for

from app.home.services import ContactService


home = Blueprint(
    "home",
    __name__,
    static_url_path="",
    template_folder="templates",
    static_folder="static",
)


@home.route("/")
def home_page():
    return render_template("home.html")


@home.route("/informations")
def informations_page():
    return render_template("informations.html")


@home.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        try:
            ContactService.send_contact_message(
                name=request.form.get("name", ""),
                email=request.form.get("email", ""),
                phone=request.form.get("phone", ""),
                message=request.form.get("message", ""),
            )
            flash("Mensagem enviada com sucesso.", category="success")
            return redirect(url_for("home.home_page"))
        except Exception:
            current_app.logger.exception("Failed to send contact email")
            flash("Erro ao enviar mensagem.", category="danger")
            return redirect(url_for("home.contact_page"))

    return render_template("contact.html")
