from flask import Blueprint, jsonify, request
from app.services.users_service import UsersService

# Definición del Blueprint para usuarios
users_bp = Blueprint('users_routes', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    """
    Obtener lista completa de usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios registrados
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              nombre:
                type: string
              email:
                type: string
              usuario:
                type: string
              rol:
                type: integer
              estado:
                type: string
    """
    try:
        users = UsersService.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Obtener un usuario específico por ID
    ---
    tags:
      - Usuarios
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Datos del usuario
      404:
        description: Usuario no encontrado
    """
    try:
        user = UsersService.get_user_by_id(user_id)
        if user:
            return jsonify(user), 200
        return jsonify({"message": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
              example: "Juan Perez"
            email:
              type: string
              example: "juan@example.com"
            usuario:
              type: string
              example: "jperez"
            password:
              type: string
              example: "secret123"
            rol:
              type: integer
              example: 3
            estado:
              type: string
              example: "activo"
    responses:
      201:
        description: Usuario creado exitosamente
      400:
        description: Datos incompletos o erróneos
    """
    data = request.get_json()
    
    # Validación simple de campos según tu SQL
    required_fields = ['nombre', 'email', 'usuario', 'password', 'rol']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
        
    try:
        new_user = UsersService.create_user(data)
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Actualizar datos de un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
            estado:
              type: string
    responses:
      200:
        description: Usuario actualizado
    """
    data = request.get_json()
    try:
        updated_user = UsersService.update_user(user_id, data)
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500