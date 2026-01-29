from flask import Blueprint, jsonify, request
from app.services.services_service import ServicesService

# Definición del Blueprint para la gestión de servicios generales
services_bp = Blueprint('services_routes', __name__)

@services_bp.route('/', methods=['GET'])
def get_all_services():
    """
    Listar todos los servicios generales
    ---
    tags:
      - Servicios
    responses:
      200:
        description: Lista de servicios definidos en el sistema
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              nombre:
                type: string
              descripcion:
                type: string
              categoria_id:
                type: integer
              estado:
                type: string
    """
    try:
        servicios = ServicesService.get_all_services()
        return jsonify(servicios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@services_bp.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    """
    Obtener un servicio por su ID
    ---
    tags:
      - Servicios
    parameters:
      - name: service_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Datos del servicio
      404:
        description: Servicio no encontrado
    """
    try:
        servicio = ServicesService.get_service_by_id(service_id)
        if servicio:
            return jsonify(servicio), 200
        return jsonify({"message": "Servicio no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@services_bp.route('/', methods=['POST'])
def create_service():
    """
    Registrar un nuevo servicio general
    ---
    tags:
      - Servicios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
              example: "Consultoría Legal"
            descripcion:
              type: string
              example: "Servicios de asesoramiento jurídico especializado"
            categoria_id:
              type: integer
              example: 1
            estado:
              type: string
              example: "activo"
    responses:
      201:
        description: Servicio creado con éxito
      400:
        description: Datos incompletos
    """
    data = request.get_json()
    required = ['nombre', 'categoria_id']
    if not all(field in data for field in required):
        return jsonify({"error": "Faltan campos obligatorios (nombre, categoria_id)"}), 400
        
    try:
        new_service = ServicesService.create_service(data)
        return jsonify(new_service), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500