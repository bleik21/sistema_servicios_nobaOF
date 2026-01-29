from app.services.database import supabase

class RolesService:
    @staticmethod
    def get_all_roles():
        """
        Obtiene la lista de todos los roles disponibles en el sistema.
        """
        try:
            # Consulta SELECT * FROM roles
            response = supabase.table("roles").select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener los roles: {str(e)}")

    @staticmethod
    def get_role_by_id(role_id):
        """
        Obtiene la información de un rol específico por su ID.
        """
        try:
            response = supabase.table("roles")\
                .select("*")\
                .eq("id", role_id)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener el rol {role_id}: {str(e)}")

    @staticmethod
    def create_role(data):
        """
        Permite registrar un nuevo tipo de rol en el sistema.
        'data' debe contener el campo 'nombre'.
        """
        try:
            response = supabase.table("roles").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear el rol: {str(e)}")