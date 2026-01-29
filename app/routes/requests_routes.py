from flask import Blueprint, jsonify, request
from app.services.requests_service import RequestsService

# Definición del Blueprint para solicitudes
requests_bp = Blueprint('requests_routes', __name__)

@requests_bp.route('/', methods=['GET'])
def get_all_requests():
    """
    Listar todas las solicitudes de servicio
    ---
    tags:
      - Solicitudes
    responses:
      200:
        description: Lista de solicitudes encontradas
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              usuario_id:
                type: integer
              subcategoria_id:
                type: integer
              descripcion:
                type: string
              estado:
                type: string
              fecha:
                type: string
                format: date-time
    """
    try:
        solicitudes = RequestsService.get_all_requests()
        return jsonify(solicitudes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@requests_bp.route('/', methods=['POST'])
def create_request():
    """
    Crear una nueva solicitud de servicio
    ---
    tags:
      - Solicitudes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            usuario_id:
              type: integer
              example: 3
            subcategoria_id:
              type: integer
              example: 10
            descripcion:
              type: string
              example: "Necesito lavado de alfombras urgente"
            estado:
              type: string
              example: "pendiente"
    responses:
      201:
        description: Solicitud creada exitosamente
      400:
        description: Datos incompletos
    """
    data = request.get_json()
    
    # Validación básica según las columnas de tu DB
    required_fields = ['usuario_id', 'subcategoria_id', 'descripcion']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
        
    try:
        new_request = RequestsService.create_request(data)
        return jsonify(new_request), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@requests_bp.route('/<int:request_id>', methods=['PATCH'])
def update_request_status(request_id):
    """
    Actualizar el estado de una solicitud
    ---
    tags:
      - Solicitudes
    parameters:
      - name: request_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            estado:
              type: string
              example: "completado"
    responses:
      200:
        description: Estado actualizado
      404:
        description: Solicitud no encontrada
    """
    data = request.get_json()
    estado = data.get('estado')
    
    try:
        updated = RequestsService.update_status(request_id, estado)
        if updated:
            return jsonify(updated), 200
        return jsonify({"message": "Solicitud no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500