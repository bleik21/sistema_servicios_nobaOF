from flask import Blueprint, jsonify, request
from app.services.subcategories_service import SubcategoriesService

# Definición del Blueprint
subcategories_bp = Blueprint('subcategories_routes', __name__)

@subcategories_bp.route('/', methods=['GET'])
def get_all_subcategories():
    """
    Obtener todas las subcategorías
    ---
    tags:
      - Subcategorías
    responses:
      200:
        description: Lista de todas las subcategorías
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              categoria_id:
                type: integer
              nombre:
                type: string
    """
    try:
        subcategories = SubcategoriesService.get_all_subcategories()
        return jsonify(subcategories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@subcategories_bp.route('/categoria/<int:categoria_id>', methods=['GET'])
def get_subcategories_by_category(categoria_id):
    """
    Obtener subcategorías de una categoría específica
    ---
    tags:
      - Subcategorías
    parameters:
      - name: categoria_id
        in: path
        type: integer
        required: true
        description: ID de la categoría padre
    responses:
      200:
        description: Lista de subcategorías filtradas
    """
    try:
        subcategories = SubcategoriesService.get_by_category(categoria_id)
        return jsonify(subcategories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@subcategories_bp.route('/', methods=['POST'])
def create_subcategory():
    """
    Crear una nueva subcategoría
    ---
    tags:
      - Subcategorías
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            categoria_id:
              type: integer
              example: 2
            nombre:
              type: string
              example: "Inteligencia Artificial"
    responses:
      201:
        description: Subcategoría creada con éxito
      400:
        description: Datos inválidos
    """
    data = request.get_json()
    if not data or 'categoria_id' not in data or 'nombre' not in data:
        return jsonify({"error": "categoria_id y nombre son requeridos"}), 400
        
    try:
        new_sub = SubcategoriesService.create_subcategory(data)
        return jsonify(new_sub), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500