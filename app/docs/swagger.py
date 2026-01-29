from flask import Blueprint

swagger_bp = Blueprint("swagger", __name__)

@swagger_bp.route("/docs")
def docs():
    return {
        "info": {
            "title": "sistema de servicios NOVA",
            "version": "1.0"
        }
    }
