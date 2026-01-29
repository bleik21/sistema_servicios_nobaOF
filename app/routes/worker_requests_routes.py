from flask import Blueprint, jsonify, request
from app.services.worker_requests_service import WorkerRequestsService

# Definición del Blueprint
worker_requests_bp = Blueprint('worker_requests_routes', __name__)

@worker_requests_bp.route('/', methods=['GET'])
def get_all_worker_requests():
    """
    Obtener todas las solicitudes enviadas a trabajadores
    ---
    tags:
      - Solicitudes a Trabajadores
    responses:
      200:
        description: Lista de solicitudes a trabajadores
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              usuario_id:
                type: integer
              categoria_id:
                type: integer
              subcategoria_id:
                type: integer
              nombre_completo:
                type: string
              estado:
                type: string
              fecha:
                type: string
                format: date-time
    """
    try:
        requests = WorkerRequestsService.get_all_worker_requests()
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@worker_requests_bp.route('/', methods=['POST'])
def create_worker_request():
    """
    Crear una nueva solicitud para un trabajador específico
    ---
    tags:
      - Solicitudes a Trabajadores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            usuario_id:
              type: integer
              example: 4
            categoria_id:
              type: integer
              example: 2
            subcategoria_id:
              type: integer
              example: 5
            nombre_completo:
              type: string
              example: "Manuel Terraza"
            estado:
              type: string
              example: "pendiente"
    responses:
      201:
        description: Registro creado exitosamente
      400:
        description: Datos incompletos
    """
    data = request.get_json()
    
    # Validamos que los campos coincidan con tu tabla solicitudes_trabajador
    required = ['usuario_id', 'categoria_id', 'subcategoria_id', 'nombre_completo']
    if not all(field in data for field in required):
        return jsonify({"error": "Faltan datos obligatorios del trabajador"}), 400
        
    try:
        new_request = WorkerRequestsService.create_worker_request(data)
        return jsonify(new_request), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@worker_requests_bp.route('/usuario/<int:user_id>', methods=['GET'])
def get_requests_by_user(user_id):
    """
    Obtener solicitudes filtradas por usuario_id
    ---
    tags:
      - Solicitudes a Trabajadores
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de solicitudes del usuario
    """
    try:
        user_requests = WorkerRequestsService.get_by_user_id(user_id)
        return jsonify(user_requests), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500