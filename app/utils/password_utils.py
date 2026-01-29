import bcrypt

class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Convierte una contraseña plana en un hash seguro."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """Compara una contraseña plana con el hash guardado en la DB."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))