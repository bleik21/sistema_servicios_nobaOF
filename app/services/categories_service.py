from app.services.database import supabase

class CategoriesService:
    @staticmethod
    def get_all_categories():
        """
        Obtiene todos los registros de la tabla categorias.
        """
        try:
            # Realiza un SELECT * FROM categorias
            response = supabase.table("categorias").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener categorías: {str(e)}")

    @staticmethod
    def get_category_by_id(category_id):
        """
        Obtiene una categoría específica por su ID.
        """
        try:
            # .eq() filtra por igualdad y .maybe_single() maneja si no hay resultados
            response = supabase.table("categorias")\
                .select("*")\
                .eq("id", category_id)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener la categoría {category_id}: {str(e)}")

    @staticmethod
    def create_category(data):
        """
        Inserta una nueva categoría. 
        'data' debe ser un diccionario con: nombre, icono, descripcion.
        """
        try:
            # .insert() devuelve una lista con el objeto creado
            response = supabase.table("categorias").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear la categoría: {str(e)}")

    @staticmethod
    def update_category(category_id, data):
        """
        Actualiza los campos de una categoría existente de forma parcial o total.
        """
        try:
            response = supabase.table("categorias")\
                .update(data)\
                .eq("id", category_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar la categoría: {str(e)}")

    @staticmethod
    def delete_category(category_id):
        """
        Elimina físicamente una categoría por su ID.
        """
        try:
            supabase.table("categorias").delete().eq("id", category_id).execute()
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar la categoría: {str(e)}")