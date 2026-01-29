from flask import Blueprint, jsonify, request
from app.services.roles_service import RolesService

# Definición del Blueprint para roles
roles_bp = Blueprint('roles_routes', __name__)

@roles_bp.route('/', methods=['GET'])
def get_all_roles():
    """
    Listar todos los roles definidos
    ---
    tags:
      - Roles
    responses:
      200:
        description: Lista de roles (sistemas, admin, usuario, staff)
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              nombre:
                type: string
                example: "admin"
    """
    try:
        roles = RolesService.get_all_roles()
        return jsonify(roles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@roles_bp.route('/<int:role_id>', methods=['GET'])
def get_role_by_id(role_id):
    """
    Obtener un rol específico por su ID
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalle del rol
      404:
        description: Rol no encontrado
    """
    try:
        role = RolesService.get_role_by_id(role_id)
        if role:
            return jsonify(role), 200
        return jsonify({"message": "Rol no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@roles_bp.route('/', methods=['POST'])
def create_role():
    """
    Crear un nuevo tipo de rol
    ---
    tags:
      - Roles
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
              example: "auditor"
    responses:
      201:
        description: Rol creado exitosamente
      400:
        description: El nombre del rol es requerido
    """
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "El nombre del rol es obligatorio"}), 400
        
    try:
        new_role = RolesService.create_role(data)
        return jsonify(new_role), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500