from flask import Blueprint, jsonify, request
from app.services.workers_service import WorkersService

# Definición del Blueprint para trabajadores
workers_bp = Blueprint('workers_routes', __name__)

@workers_bp.route('/', methods=['GET'])
def get_all_workers():
    """
    Listar todos los trabajadores registrados
    ---
    tags:
      - Trabajadores
    responses:
      200:
        description: Lista de trabajadores con sus detalles técnicos
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
              nombre_completo:
                type: string
              ci:
                type: string
              descripcion:
                type: string
              ubicacion:
                type: string
              estado:
                type: string
    """
    try:
        workers = WorkersService.get_all_workers()
        return jsonify(workers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@workers_bp.route('/subcategoria/<int:sub_id>', methods=['GET'])
def get_workers_by_subcategory(sub_id):
    """
    Filtrar trabajadores por subcategoría (especialidad)
    ---
    tags:
      - Trabajadores
    parameters:
      - name: sub_id
        in: path
        type: integer
        required: true
        description: ID de la subcategoría (ej. 10 para Lavandería)
    responses:
      200:
        description: Lista de trabajadores especializados
    """
    try:
        workers = WorkersService.get_by_subcategory(sub_id)
        return jsonify(workers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@workers_bp.route('/', methods=['POST'])
def register_worker():
    """
    Dar de alta a un usuario como trabajador
    ---
    tags:
      - Trabajadores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            usuario_id:
              type: integer
            subcategoria_id:
              type: integer
            nombre_completo:
              type: string
            ci:
              type: string
            descripcion:
              type: string
            ubicacion:
              type: string
            estado:
              type: string
              example: "activo"
    responses:
      201:
        description: Trabajador registrado exitosamente
      400:
        description: Datos incompletos
    """
    data = request.get_json()
    required = ['usuario_id', 'subcategoria_id', 'nombre_completo', 'ci']
    
    if not all(field in data for field in required):
        return jsonify({"error": "Faltan campos críticos para el registro"}), 400
        
    try:
        new_worker = WorkersService.create_worker(data)
        return jsonify(new_worker), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@workers_bp.route('/<int:worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    """
    Eliminar o dar de baja a un trabajador
    ---
    tags:
      - Trabajadores
    parameters:
      - name: worker_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Trabajador eliminado correctamente
    """
    try:
        WorkersService.delete_worker(worker_id)
        return jsonify({"message": "Registro eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500