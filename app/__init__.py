from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

# Importación de las rutas (Blueprints)
from app.routes.auth_routes import auth_bp
from app.routes.categories_routes import categories_bp
from app.routes.requests_routes import requests_bp
from app.routes.roles_routes import roles_bp
from app.routes.services_routes import services_bp
from app.routes.subcategories_routes import subcategories_bp
from app.routes.users_routes import users_bp
from app.routes.worker_requests_routes import worker_requests_bp
from app.routes.workers_routes import workers_bp

def create_app():
    # Inicialización de la aplicación Flask
    app = Flask(__name__)
    
    # Habilitar CORS para permitir peticiones desde el frontend
    CORS(app)
    
    # Configuración de Swagger para la documentación de la API
    app.config['SWAGGER'] = {
        'title': 'API de Servicios Profesionales',
        'uiversion': 3
    }
    Swagger(app)

    # Registro de los Blueprints (Rutas)
    # Cada uno tendrá su propio prefijo para mantener el orden
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(requests_bp, url_prefix='/requests')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(subcategories_bp, url_prefix='/subcategories')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(worker_requests_bp, url_prefix='/worker-requests')
    app.register_blueprint(workers_bp, url_prefix='/workers')

    return app