from flask import Blueprint
# Importamos los archivos de rutas según tu estructura de carpetas
from .auth_routes import auth_bp
from .categories_routes import categories_bp
from .requests_routes import requests_bp
from .roles_routes import roles_bp
from .services_routes import services_bp
from .subcategories_routes import subcategories_bp
from .users_routes import users_bp
from .worker_requests_routes import worker_requests_bp
from .workers_routes import workers_bp

def register_routes(app):
    """
    Función para registrar todos los Blueprints en la aplicación principal
    """
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(requests_bp, url_prefix='/api/requests')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(subcategories_bp, url_prefix='/api/subcategories')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(worker_requests_bp, url_prefix='/api/worker-requests')
    app.register_blueprint(workers_bp, url_prefix='/api/workers')