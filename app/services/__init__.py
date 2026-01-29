# app/services/__init__.py

# 1. Importamos la conexión central a Supabase
from .database import supabase

# 2. Importamos todas las clases de servicios
from .auth_service import AuthService
from .categories_service import CategoriesService
from .requests_service import RequestsService
from .roles_service import RolesService
from .services_service import ServicesService
from .subcategories_service import SubcategoriesService
from .users_service import UsersService
from .worker_requests_service import WorkerRequestsService
from .workers_service import WorkersService

# 3. Definimos __all__ para controlar qué se exporta al usar 'from app.services import *'
__all__ = [
    "supabase",
    "AuthService",
    "CategoriesService",
    "RequestsService",
    "RolesService",
    "ServicesService",
    "SubcategoriesService",
    "UsersService",
    "WorkerRequestsService",
    "WorkersService"
]