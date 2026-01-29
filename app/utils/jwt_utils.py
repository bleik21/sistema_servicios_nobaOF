import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "tu_clave_secreta_super_segura")

class JWTUtils:
    @staticmethod
    def generate_token(user_data: dict):
        """Genera un token JWT que expira en 24 horas."""
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(user_data.get("id")),
            "user": user_data
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token: str):
        """Valida un token y devuelve su contenido."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"error": "El token ha expirado"}
        except jwt.InvalidTokenError:
            return {"error": "Token inválido"}