from flask import Blueprint, jsonify, request
# Aquí importarías tu servicio de Supabase más adelante
# from app.services.auth_service import AuthService 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Inicio de sesión de usuario
    ---
    tags:
      - Autenticación
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Login exitoso
      401:
        description: Credenciales inválidas
    """
    # Lógica de conexión con Supabase a través del servicio
    return jsonify({"message": "Endpoint de login conectado"}), 200