from app.services.database import supabase

class UsersService:
    @staticmethod
    def get_all_users():
        """
        Obtiene la lista de todos los usuarios.
        Excluye la contraseña por razones de seguridad.
        """
        try:
            # Seleccionamos campos específicos para proteger datos sensibles
            response = supabase.table("usuarios")\
                .select("id, nombre, email, usuario, rol, estado")\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")

    @staticmethod
    def get_user_by_id(user_id):
        """
        Obtiene un usuario por su ID único.
        """
        try:
            response = supabase.table("usuarios")\
                .select("id, nombre, email, usuario, rol, estado")\
                .eq("id", user_id)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener el usuario {user_id}: {str(e)}")

    @staticmethod
    def create_user(data):
        """
        Registra un nuevo usuario en la base de datos.
        'data' debe contener: nombre, email, usuario, password, rol y estado.
        """
        try:
            # Insertamos el nuevo usuario
            response = supabase.table("usuarios").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear el usuario: {str(e)}")

    @staticmethod
    def update_user(user_id, data):
        """
        Actualiza los datos de un usuario existente (ej: cambiar nombre o estado).
        """
        try:
            response = supabase.table("usuarios")\
                .update(data)\
                .eq("id", user_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al actualizar el usuario: {str(e)}")

    @staticmethod
    def get_user_by_username(username):
        """
        Busca un usuario por su nombre de usuario. Útil para validaciones.
        """
        try:
            response = supabase.table("usuarios")\
                .select("*")\
                .eq("usuario", username)\
                .maybe_single()\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al buscar usuario por nombre: {str(e)}")