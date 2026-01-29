from app.services.database import supabase

class WorkersService:
    @staticmethod
    def get_all_workers():
        """
        Obtiene la lista de todos los trabajadores registrados.
        """
        try:
            # SELECT * FROM trabajadores
            response = supabase.table("trabajadores").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener trabajadores: {str(e)}")

    @staticmethod
    def get_by_subcategory(sub_id):
        """
        Filtra trabajadores por una subcategoría específica (especialidad).
        """
        try:
            response = supabase.table("trabajadores")\
                .select("*")\
                .eq("subcategoria_id", sub_id)\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al filtrar trabajadores por especialidad: {str(e)}")

    @staticmethod
    def get_worker_by_id(worker_id):
        """
        Obtiene el perfil de un trabajador por su ID único.
        """
        try:
            response = supabase.table("trabajadores")\
                .select("*")\
                .eq("id", worker_id)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener el perfil del trabajador: {str(e)}")

    @staticmethod
    def create_worker(data):
        """
        Registra un nuevo perfil de trabajador.
        'data' debe incluir: usuario_id, subcategoria_id, nombre_completo, ci, descripcion, ubicacion y estado.
        """
        try:
            response = supabase.table("trabajadores").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al registrar el trabajador: {str(e)}")

    @staticmethod
    def update_worker_profile(worker_id, data):
        """
        Actualiza la información profesional o de contacto de un trabajador.
        """
        try:
            response = supabase.table("trabajadores")\
                .update(data)\
                .eq("id", worker_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar el perfil: {str(e)}")

    @staticmethod
    def delete_worker(worker_id):
        """
        Elimina el registro de un trabajador.
        """
        try:
            supabase.table("trabajadores").delete().eq("id", worker_id).execute()
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar el registro del trabajador: {str(e)}")