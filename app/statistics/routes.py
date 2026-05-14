from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_jwt_extended import get_jwt_identity

from app.statistics.services import StatisticsService
from app.users_authentication.decorators import jwt_page_required


statistics = Blueprint(
    "statistics",
    __name__,
    url_prefix="/statistics",
    static_folder="static",
    template_folder="templates",
)


@statistics.route("/", methods=["GET"])
@jwt_page_required
def statistics_page():
    try:
        dashboard = StatisticsService.dashboard(get_jwt_identity())
        return render_template("statistics.html", **dashboard)
    except Exception:
        current_app.logger.exception("Failed to load statistics")
        flash("Erro ao carregar estatísticas.", category="error")
        return redirect(url_for("transactions.transactions_page"))
