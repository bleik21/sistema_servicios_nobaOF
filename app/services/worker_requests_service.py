from app.services.database import supabase

class WorkerRequestsService:
    @staticmethod
    def get_all_worker_requests():
        """
        Obtiene el listado de todas las solicitudes vinculadas a trabajadores.
        """
        try:
            # SELECT * FROM solicitudes_trabajador
            response = supabase.table("solicitudes_trabajador").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener solicitudes de trabajadores: {str(e)}")

    @staticmethod
    def create_worker_request(data):
        """
        Registra una nueva solicitud para un trabajador.
        'data' debe contener: usuario_id, categoria_id, subcategoria_id, nombre_completo, estado.
        """
        try:
            # Insertamos los datos del trabajador solicitado
            response = supabase.table("solicitudes_trabajador").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al registrar la solicitud del trabajador: {str(e)}")

    @staticmethod
    def get_by_user_id(user_id):
        """
        Filtra las solicitudes de trabajadores realizadas por un usuario específico.
        """
        try:
            response = supabase.table("solicitudes_trabajador")\
                .select("*")\
                .eq("usuario_id", user_id)\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al filtrar solicitudes por usuario: {str(e)}")

    @staticmethod
    def update_request_status(request_id, nuevo_estado):
        """
        Actualiza el estado de la solicitud del trabajador (ej: 'atendido', 'rechazado').
        """
        try:
            response = supabase.table("solicitudes_trabajador")\
                .update({"estado": nuevo_estado})\
                .eq("id", request_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar estado de la solicitud: {str(e)}")