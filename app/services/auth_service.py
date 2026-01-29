from app.services.database import supabase

class AuthService:
    @staticmethod
    def login(username, password):
        """
        Verifica las credenciales del usuario.
        """
        try:
            # Buscamos al usuario por su nombre de usuario
            response = supabase.table("usuarios")\
                .select("id, nombre, email, usuario, password, rol, estado")\
                .eq("usuario", username)\
                .maybe_single()\
                .execute()
            
            user = response.data
            
            # 1. Validar si el usuario existe
            if not user:
                return {"success": False, "message": "Usuario no encontrado"}
            
            # 2. Validar si el usuario está activo
            if user.get('estado') != 'activo':
                return {"success": False, "message": "El usuario no tiene permiso de acceso (inactivo)"}

            # 3. Validar contraseña
            # Nota: Aquí comparamos texto plano. Si usas password_utils, 
            # deberías usar: if PasswordUtils.check_password(user['password'], password):
            if user.get('password') == password:
                # Eliminamos el password del diccionario antes de devolverlo por seguridad
                user.pop('password')
                return {"success": True, "user": user}
            else:
                return {"success": False, "message": "Contraseña incorrecta"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def verify_user_exists(user_id):
        """
        Verificación rápida para middlewares o guards de rutas.
        """
        response = supabase.table("usuarios")\
            .select("id")\
            .eq("id", user_id)\
            .maybe_single()\
            .execute()
        return response.data is not None