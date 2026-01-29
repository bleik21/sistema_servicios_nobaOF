from app.services.database import supabase

class RequestsService:
    @staticmethod
    def get_all_requests():
        """
        Obtiene el listado completo de solicitudes de la base de datos.
        """
        try:
            # Realiza un SELECT * FROM solicitudes
            response = supabase.table("solicitudes").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener las solicitudes: {str(e)}")

    @staticmethod
    def create_request(data):
        """
        Registra una nueva solicitud de servicio.
        'data' debe incluir: usuario_id, subcategoria_id, descripcion y estado.
        """
        try:
            # Inserta los datos y devuelve el registro creado
            response = supabase.table("solicitudes").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear la solicitud: {str(e)}")

    @staticmethod
    def update_status(request_id, nuevo_estado):
        """
        Actualiza únicamente el campo 'estado' de una solicitud específica.
        """
        try:
            response = supabase.table("solicitudes")\
                .update({"estado": nuevo_estado})\
                .eq("id", request_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar el estado: {str(e)}")

    @staticmethod
    def get_requests_by_user(user_id):
        """
        Recupera el historial de solicitudes de un usuario en particular.
        """
        try:
            response = supabase.table("solicitudes")\
                .select("*")\
                .eq("usuario_id", user_id)\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al filtrar por usuario: {str(e)}")