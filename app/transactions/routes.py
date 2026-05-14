from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_jwt_extended import get_jwt_identity

from app.exceptions import AppError
from app.transactions.services import CATEGORY_COLORS, TransactionService
from app.users_authentication.decorators import jwt_page_required
from app.users_authentication.services.user_service import UserService


transactions = Blueprint(
    "transactions",
    __name__,
    url_prefix="/transactions",
    static_folder="static",
    template_folder="templates",
)


@transactions.route("/", methods=["GET"])
@jwt_page_required
def transactions_page():
    user_id = get_jwt_identity()
    user = UserService.get_user(user_id)
    filters = TransactionService.build_filters(request.args)
    transactions_list = TransactionService.list_transactions(filters, user_id)

    return render_template(
        "transactions_list_page.html",
        user=user,
        transactions=transactions_list,
        transactions_filters=filters,
        category_colors=CATEGORY_COLORS,
    )


@transactions.route("/create", methods=["GET", "POST"])
@jwt_page_required
def transaction_create_page():
    user_id = get_jwt_identity()

    if request.method == "POST":
        try:
            TransactionService.create_transaction(request.form, user_id)
            flash("Criada com sucesso.", category="success")
            return redirect(url_for("transactions.transactions_page"))
        except AppError as exc:
            flash(exc.message, category="error")

    return render_template("transaction_form_page.html", transaction=None)


@transactions.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
@jwt_page_required
def transaction_edit_page(transaction_id):
    user_id = get_jwt_identity()

    if request.method == "POST":
        try:
            TransactionService.update_transaction(
                transaction_id,
                request.form,
                user_id,
            )
            flash("Editada com sucesso.", category="success")
            return redirect(url_for("transactions.transactions_page"))
        except AppError as exc:
            flash(exc.message, category="error")

    transaction = TransactionService.get_transaction(transaction_id, user_id)
    return render_template(
        "transaction_form_page.html",
        transaction=transaction,
    )


@transactions.route("/delete/<int:transaction_id>", methods=["POST"])
@jwt_page_required
def transaction_delete(transaction_id):
    user_id = get_jwt_identity()
    try:
        TransactionService.delete_transaction(transaction_id, user_id)
        flash("Transacao deletada com sucesso.", category="success")
    except AppError as exc:
        flash(exc.message, category="error")

    return redirect(url_for("transactions.transactions_page"))
