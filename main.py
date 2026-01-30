import os
import bcrypt
import math
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import wraps

# ======================
# CARGA VARIABLES ENTORNO
# ======================
load_dotenv()

# ======================
# CONFIGURACIÓN RUTAS
# ======================
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'app', 'templates')
static_dir = os.path.join(base_dir, 'app', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_noba_2026')

# ======================
# SUPABASE
# ======================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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
# UTILIDADES
# ======================
def calcular_distancia_facial(rostro_actual, rostro_db):
    if not rostro_actual or not rostro_db:
        return float('inf')

    total = 0
    count = 0

    for i in range(len(rostro_actual)):
        try:
            p1 = rostro_actual[i]
            p2 = rostro_db[i]
            dist = math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
            total += dist
            count += 1
        except:
            continue

    return total / count if count > 0 else float('inf')


def obtener_icono_categoria(nombre):
    iconos = {
        "derecho": "fa-solid fa-gavel",
        "tecnología": "fa-solid fa-computer",
        "salud": "fa-solid fa-stethoscope",
        "higiene": "fa-solid fa-broom",
        "hogar": "fa-solid fa-house"
    }
    return iconos.get(nombre.lower(), "fa-solid fa-layer-group")

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
# 🔥 RUTA TEST SUPABASE
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
# USUARIO
# ======================
@app.route('/servicios')
@login_required
def servicios():
    res = supabase.table('categorias').select("*").order('nombre').execute()
    return render_template('vista_usuario/servicios.html', categorias=res.data)


@app.route('/subcategoria/<int:id_cat>')
@login_required
def subcategoria(id_cat):
    cat = supabase.table('categorias').select("*").eq('id', id_cat).execute()
    sub = supabase.table('subcategorias').select("*").eq('categoria_id', id_cat).execute()

    if not cat.data:
        return redirect(url_for('servicios'))

    return render_template(
        'vista_usuario/subcategoria.html',
        categoria=cat.data[0],
        subcategorias=sub.data
    )


@app.route('/trabajadores/<int:id_sub>')
@login_required
def trabajadores(id_sub):
    sub = supabase.table('subcategorias').select("*").eq('id', id_sub).execute()
    if not sub.data:
        return redirect(url_for('servicios'))

    categoria = supabase.table('categorias').select("nombre").eq(
        'id', sub.data[0]['categoria_id']
    ).execute()

    trabajadores = supabase.table('trabajadores').select("*").eq(
        'subcategoria_id', id_sub
    ).execute()

    return render_template(
        'vista_usuario/trabajadores.html',
        sub={
            "id": sub.data[0]['id'],
            "nombre": sub.data[0]['nombre'],
            "categoria_nombre": categoria.data[0]['nombre']
        },
        trabajadores=trabajadores.data
    )

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
# LOGIN / LOGOUT
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

    valido = (
        bcrypt.checkpw(password.encode(), user['password'].encode())
        if user['password'].startswith('$2b$')
        else password == user['password']
    )

    if not valido:
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for('login_manual_page'))

    session.update({
        "user_id": user['id'],
        "nombre": user['nombre'],
        "rol": user['rol']
    })

    return redirect(url_for('admin_dashboard' if user['rol'] == 2 else 'servicios'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ======================
# MAIN
# ======================
if __name__ == '__main__':
    port = 5000
    print(f"✅ Servidor corriendo en http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
