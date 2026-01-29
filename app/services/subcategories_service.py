from app.services.database import supabase

class SubcategoriesService:
    @staticmethod
    def get_all_subcategories():
        """
        Obtiene el listado completo de subcategorías.
        """
        try:
            # SELECT * FROM subcategorias
            response = supabase.table("subcategorias").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener subcategorías: {str(e)}")

    @staticmethod
    def get_by_category(categoria_id):
        """
        Filtra subcategorías que pertenecen a una categoría específica.
        Útil para menús desplegables dinámicos.
        """
        try:
            response = supabase.table("subcategorias")\
                .select("*")\
                .eq("categoria_id", categoria_id)\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al filtrar por categoría: {str(e)}")

    @staticmethod
    def create_subcategory(data):
        """
        Registra una nueva subcategoría vinculada a una categoría existente.
        'data' debe incluir: categoria_id y nombre.
        """
        try:
            response = supabase.table("subcategorias").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear subcategoría: {str(e)}")

    @staticmethod
    def get_subcategory_by_id(sub_id):
        """
        Obtiene los detalles de una subcategoría por su ID.
        """
        try:
            response = supabase.table("subcategorias")\
                .select("*")\
                .eq("id", sub_id)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener la subcategoría: {str(e)}")