from flask import jsonify, request

from app.exceptions import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        if request.accept_mimetypes.accept_json:
            return jsonify({"error": "Recurso nao encontrado."}), 404
        return "Pagina nao encontrada.", 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        app.logger.exception("Unhandled server error")
        if request.accept_mimetypes.accept_json:
            return jsonify({"error": "Erro interno do servidor."}), 500
        return "Erro interno do servidor.", 500
