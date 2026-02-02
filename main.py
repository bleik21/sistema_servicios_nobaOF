import os
import uuid
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

# ======================
# CONFIGURACIÓN
# ======================
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'app', 'templates')
static_dir = os.path.join(base_dir, 'app', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# ======================
# SUPABASE
# ======================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ SUPABASE_URL o SUPABASE_KEY no definidas")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================
# DECORADORES
# ======================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_manual_page'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('rol') != 2:
            return redirect(url_for('login_manual_page'))
        return f(*args, **kwargs)
    return decorated

# ======================
# RUTAS PÚBLICAS
# ======================
@app.route('/')
def home():
    return render_template('login/index.html')


@app.route('/login_manual')
def login_manual_page():
    return render_template('login/login.html')


@app.route('/registro')
def registro_page():
    return render_template('login/registro.html')

# ======================
# PANEL USUARIO
# ======================
@app.route('/servicios')
@login_required
def panel_usuario():
    return render_template('vista_usuario/servicios.html')

# ======================
# REGISTRO
# ======================
@app.route('/ejecutar_registro', methods=['POST'])
def ejecutar_registro():
    nombre = request.form.get('nombre')
    usuario = request.form.get('usuario')
    email = request.form.get('email')
    password = request.form.get('password')

    if not all([nombre, usuario, email, password]):
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('registro_page'))

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    supabase.table('usuarios').insert({
        "id": str(uuid.uuid4()),
        "nombre": nombre,
        "usuario": usuario,
        "email": email,
        "password": password_hash,
        "rol": 3,
        "estado": "activo"
    }).execute()

    flash("Registro exitoso", "success")
    return redirect(url_for('login_manual_page'))

# ======================
# LOGIN
# ======================
@app.route('/ejecutar_login', methods=['POST'])
def ejecutar_login():
    email = request.form.get('email')
    password = request.form.get('password')

    res = supabase.table('usuarios').select("*").or_(
        f"email.eq.{email},usuario.eq.{email}"
    ).execute()

    if not res.data:
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for('login_manual_page'))

    user = res.data[0]

    if not bcrypt.checkpw(password.encode(), user['password'].encode()):
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for('login_manual_page'))

    session['user_id'] = user['id']
    session['rol'] = user['rol']

    return redirect(url_for('admin_dashboard' if user['rol'] == 2 else 'panel_usuario'))

# ======================
# ADMIN
# ======================
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

# ======================
# LOGOUT
# ======================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
