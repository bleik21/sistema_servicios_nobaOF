from flask import Blueprint, jsonify, request
from app.services.categories_service import CategoriesService

# Definición del Blueprint
categories_bp = Blueprint('categories_routes', __name__)

@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    """
    Obtener todas las categorías
    ---
    tags:
      - Categorías
    responses:
      200:
        description: Lista de todas las categorías disponibles
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              nombre:
                type: string
                example: "Tecnología"
              icono:
                type: string
                example: "cpu-icon"
              descripcion:
                type: string
                example: "Servicios relacionados con hardware y software"
      500:
        description: Error interno del servidor
    """
    try:
        categories = CategoriesService.get_all_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """
    Obtener una categoría por ID
    ---
    tags:
      - Categorías
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
        description: ID único de la categoría
    responses:
      200:
        description: Datos de la categoría encontrada
      404:
        description: Categoría no encontrada
    """
    try:
        category = CategoriesService.get_category_by_id(category_id)
        if category:
            return jsonify(category), 200
        return jsonify({"message": "Categoría no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@categories_bp.route('/', methods=['POST'])
def create_category():
    """
    Crear una nueva categoría
    ---
    tags:
      - Categorías
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nombre:
              type: string
              example: "Mascotas"
            icono:
              type: string
              example: "dog-icon"
            descripcion:
              type: string
              example: "Servicios de veterinaria y estética"
    responses:
      201:
        description: Categoría creada exitosamente
      400:
        description: Datos inválidos
    """
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "El nombre es obligatorio"}), 400
        
    try:
        new_category = CategoriesService.create_category(data)
        return jsonify(new_category), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500