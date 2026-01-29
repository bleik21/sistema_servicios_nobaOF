from app.services.database import supabase

class ServicesService:
    @staticmethod
    def get_all_services():
        """
        Recupera todos los servicios definidos en el catálogo maestro.
        """
        try:
            # SELECT * FROM servicios
            response = supabase.table("servicios").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener servicios: {str(e)}")

    @staticmethod
    def get_service_by_id(service_id):
        """
        Busca un servicio específico por su ID único.
        """
        try:
            response = supabase.table("servicios")\
                .select("*")\
                .eq("id", service_id)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener el servicio {service_id}: {str(e)}")

    @staticmethod
    def create_service(data):
        """
        Registra un nuevo servicio en el catálogo.
        'data' debe incluir: nombre, descripcion, categoria_id, estado.
        """
        try:
            # Insertamos y retornamos el objeto creado
            response = supabase.table("servicios").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear el servicio: {str(e)}")

    @staticmethod
    def update_service(service_id, data):
        """
        Actualiza la información de un servicio existente.
        """
        try:
            response = supabase.table("servicios")\
                .update(data)\
                .eq("id", service_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar el servicio: {str(e)}")