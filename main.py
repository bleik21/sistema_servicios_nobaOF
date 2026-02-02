import os
import uuid
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import wraps

# ======================
# CARGAR VARIABLES ENTORNO
# ======================
load_dotenv()

# ======================
# DEBUG VARIABLES (CLAVE PARA RENDER)
# ======================
print("🔎 SUPABASE_URL =", repr(os.getenv("SUPABASE_URL")))
print("🔎 SUPABASE_KEY =", "CARGADA" if os.getenv("SUPABASE_KEY") else "NO CARGADA")
print("🔎 FLASK_SECRET_KEY =", "CARGADA" if os.getenv("FLASK_SECRET_KEY") else "NO CARGADA")

# ======================
# CONFIGURACIÓN RUTAS
# ======================
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'app', 'templates')
static_dir = os.path.join(base_dir, 'app', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_noba_2026')

# ======================
# SUPABASE (VALIDACIÓN DURA)
# ======================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ SUPABASE_URL o SUPABASE_KEY no están definidas")

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
            flash("Acceso denegado", "danger")
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
# TEST SUPABASE
# ======================
@app.route('/test_supabase')
def test_supabase():
    try:
        res = supabase.table('categorias').select('*').execute()
        return jsonify({
            "status": "ok",
            "total": len(res.data),
            "data": res.data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ======================
# REGISTRO DE USUARIO
# ======================
@app.route('/ejecutar_registro', methods=['POST'])
def ejecutar_registro():
    try:
        nombre = request.form.get('nombre')
        usuario = request.form.get('usuario')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([nombre, usuario, email, password]):
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('registro_page'))

        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        nuevo_usuario = {
            "id": str(uuid.uuid4()),   # UUID correcto
            "nombre": nombre,
            "usuario": usuario,
            "email": email,
            "password": password_hash,
            "rol": 3,
            "estado": "activo"
        }

        supabase.table('usuarios').insert(nuevo_usuario).execute()

        flash("Registro exitoso. Ya puedes iniciar sesión.", "success")
        return redirect(url_for('login_manual_page'))

    except Exception as e:
        print("❌ Error registro:", repr(e))
        flash("Error al registrar usuario", "danger")
        return redirect(url_for('registro_page'))

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

    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for('login_manual_page'))

    session.update({
        "user_id": user['id'],
        "nombre": user['nombre'],
        "rol": user['rol']
    })

    return redirect(url_for('admin_dashboard' if user['rol'] == 2 else 'servicios'))

# ======================
# USUARIO
# ======================
@app.route('/servicios')
@login_required
def servicios():
    res = supabase.table('categorias').select("*").order('nombre').execute()
    return render_template('vista_usuario/servicios.html', categorias=res.data)

# ======================
# ADMIN
# ======================
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    usuarios = supabase.table('usuarios').select('id', count='exact').execute()
    trabajadores = supabase.table('trabajadores').select('id', count='exact').execute()

    return render_template(
        'admin/dashboard.html',
        usuarios_count=usuarios.count or 0,
        trabajadores_count=trabajadores.count or 0
    )

# ======================
# LOGOUT
# ======================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ======================
# MAIN
# ======================
if __name__ == '__main__':
    print("✅ Servidor corriendo en http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
