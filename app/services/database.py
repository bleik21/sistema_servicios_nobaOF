import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Es importante usar casting de cadena para que Client no se queje
url: str = str(os.environ.get("SUPABASE_URL", ""))
key: str = str(os.environ.get("SUPABASE_KEY", ""))

if not url or not key:
    raise ValueError("Error: SUPABASE_URL o SUPABASE_KEY no configuradas en el archivo .env")

# El cliente se inicializa así
supabase: Client = create_client(url, key)