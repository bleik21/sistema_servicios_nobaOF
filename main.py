import os
import bcrypt
import math
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

# --- CONFIGURACIÓN DE RUTAS ---
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'app', 'templates')
static_dir = os.path.join(base_dir, 'app', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_noba_2026')

# --- CONFIGURACIÓN CLIENTE SUPABASE ---
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- DECORADORES DE SEGURIDAD ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_manual_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Cambiado a 2 para que coincida con tu nuevo INSERT
        if 'user_id' not in session or session.get('rol') != 2:
            flash("Acceso denegado", "danger")
            return redirect(url_for('login_manual_page'))
        return f(*args, **kwargs)
    return decorated_function# --- UTILIDADES BIOMÉTRICAS ---
def calcular_distancia_facial(rostro_actual, rostro_db):
    if not rostro_actual or not rostro_db:
        return float('inf')
    total_distancia = 0
    puntos_comparados = 0
    for i in range(len(rostro_actual)):
        try:
            p1 = rostro_actual[i]
            p2 = rostro_db[i]
            dist = math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
            total_distancia += dist
            puntos_comparados += 1
        except (KeyError, IndexError):
            continue
    return total_distancia / puntos_comparados if puntos_comparados > 0 else float('inf')

def obtener_icono_categoria(nombre_cat):
    iconos = {
        "derecho": "fa-solid fa-gavel",
        "tecnología": "fa-solid fa-computer",
        "salud": "fa-solid fa-stethoscope",
        "higiene": "fa-solid fa-broom",
        "hogar": "fa-solid fa-house"
    }
    return iconos.get(nombre_cat.lower(), "fa-solid fa-layer-group")


# --- RUTAS DE NAVEGACIÓN PÚBLICA ---

@app.route('/')
def home():
    return render_template('login/index.html')

@app.route('/login_manual')
def login_manual_page():
    return render_template('login/login.html')

@app.route('/registro')
def registro_page():
    return render_template('login/registro.html')

    
@app.route('/servicios')
@login_required
def servicios():
    try:
        response = supabase.table('categorias').select("*").order('nombre').execute()
        return render_template('vista_usuario/servicios.html', 
                               categorias=response.data)
    except Exception as e:
        print(f"Error: {e}")
        return "Error al cargar servicios", 500
        
@app.route('/asociarse')
@login_required
def asociarse():
    # Opción A: Si tienes un HTML listo, usa: return render_template('vista_usuario/asociarse.html')
    # Opción B: Texto simple para probar que el enlace funciona y quitar el error:
    return """
    <div style="text-align:center; padding:50px;">
        <h1>🚀 ¡Próximamente!</h1>
        <p>Aquí irá el formulario para que te registres como trabajador en NOBA.</p>
        <a href="/servicios">Volver a Servicios</a>
    </div>
    """

# En app.py
@app.route('/subcategoria/<int:id_cat>')
@login_required
def subcategoria(id_cat):
    try:
        # Obtenemos datos de la categoría
        cat_res = supabase.table('categorias').select("*").eq('id', id_cat).execute()
        if not cat_res.data:
            return redirect(url_for('servicios'))
        
        # Obtenemos subcategorías
        sub_res = supabase.table('subcategorias').select("*").eq('categoria_id', id_cat).execute()
        
        return render_template('vista_usuario/subcategoria.html', 
                               categoria=cat_res.data[0], 
                               subcategorias=sub_res.data)
    except Exception as e:
        print(f"Error en sub: {e}")
        return redirect(url_for('servicios'))    
@app.route('/trabajadores/<int:id_sub>')
@login_required
def trabajadores(id_sub):
    try:
        # 1. Obtenemos la subcategoría
        res_sub = supabase.table('subcategorias').select("*").eq('id', id_sub).execute()
        if not res_sub.data:
            return redirect(url_for('servicios'))
        
        datos_sub = res_sub.data[0]

        # 2. Obtenemos el nombre de la categoría padre (para el título)
        res_cat = supabase.table('categorias').select("nombre").eq('id', datos_sub['categoria_id']).execute()
        nombre_cat = res_cat.data[0]['nombre'] if res_cat.data else "General"

        # 3. Preparamos el objeto 'sub' que pide tu HTML
        sub_info = {
            "id": datos_sub['id'],
            "nombre": datos_sub['nombre'],
            "categoria_id": datos_sub['categoria_id'],
            "categoria_nombre": nombre_cat
        }

        # 4. Traemos a los trabajadores (los 2 por subcategoría que insertaste)
        res_trab = supabase.table('trabajadores').select("*").eq('subcategoria_id', id_sub).execute()
        
        # DEBUG: Mira tu terminal de VS Code, debe imprimir un número mayor a 0
        print(f"✅ Trabajadores encontrados para ID {id_sub}: {len(res_trab.data)}")

        return render_template('vista_usuario/trabajadores.html', 
                               sub=sub_info, 
                               trabajadores=res_trab.data)

    except Exception as e:
        print(f"❌ ERROR EN RUTA TRABAJADORES: {e}")
        return redirect(url_for('servicios'))
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    try:
        u_res = supabase.table('usuarios').select('id', count='exact').execute()
        t_res = supabase.table('trabajadores').select('id', count='exact').execute()
        ultimos = supabase.table('trabajadores').select('*').order('id', desc=True).limit(5).execute()

        return render_template('admin/dashboard.html', 
                               usuarios_count=u_res.count or 0,
                               trabajadores_count=t_res.count or 0,
                               ultimos_trabajadores=ultimos.data)
    except Exception as e:
        print(f"Error en dashboard: {e}")
        return render_template('admin/dashboard.html', usuarios_count=0, trabajadores_count=0, )

@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    try:
        res = supabase.table('usuarios').select("*").order('nombre').execute()
        notif_res = supabase.table('solicitudes').select('*').eq('estado', 'pendiente').execute()
        
        return render_template('admin/usuarios.html', 
                               usuarios=res.data,
                               notificaciones=notif_res.data,
                               total_notificaciones=len(notif_res.data))
    except Exception as e:
        print(f"Error en admin_usuarios: {e}")
        flash("No se pudo cargar la lista de usuarios", "danger")
        return redirect(url_for('admin_dashboard'))    
    
@app.route('/admin/trabajadores_admin')
@admin_required
def admin_trabajadores():
    res = supabase.table('trabajadores').select("*").execute()
    return render_template('admin/trabajadores.html', trabajadores=res.data)

@app.route('/admin/categorias')
@admin_required
def admin_categorias():
    res = supabase.table('categorias').select("*").execute()
    return render_template('admin/categorias.html', categorias=res.data)

@app.route('/admin/gestionar_solicitud', methods=['POST'])
@admin_required
def api_gestionar_solicitud():
    try:
        data = request.get_json()
        sol_id = data.get('solicitud_id')
        nuevo_estado = data.get('estado') 
        
        sol_res = supabase.table('solicitudes').select("*").eq('id', sol_id).single().execute()
        if not sol_res.data:
            return jsonify({"success": False, "error": "No existe"})

        user_id = sol_res.data['usuario_id']
        tipo_solicitud = sol_res.data.get('tipo', 'SERVICIO') 

        supabase.table('solicitudes').update({"estado": nuevo_estado}).eq('id', sol_id).execute()

        # Registrar historial
        tipo_log = "ADMIN_APROBAR" if nuevo_estado == 'aprobado' else "ADMIN_RECHAZAR"
        
        # Opcional: Insertar en historial si la tabla existe
        try:
            supabase.table('historial_acciones').insert({
                "usuario_id": session.get('user_id'),
                "tipo_accion": tipo_log,
                "detalle": f"{nuevo_estado.capitalize()} solicitud de {tipo_solicitud} para usuario {user_id}",
                "dispositivo": "Panel Admin"
            }).execute()
        except:
            pass # Si falla el historial no detenemos el proceso

        return jsonify({"success": True})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)})
        
    
# --- LÓGICA DE REGISTRO Y LOGIN ---

@app.route('/ejecutar_registro', methods=['POST'])
def ejecutar_registro():
    nombre = request.form.get('nombre')
    usuario = request.form.get('usuario')
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # 1. Registro Auth en Supabase
        # Esto crea el usuario en la tabla interna auth.users y envía el correo
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "email_redirect_to": "http://localhost:5000/login_manual" 
            }
        })

        # IMPORTANTE: res.user contiene el UUID que necesitamos
        if res.user:
            # 2. Inserción en tu tabla pública 'usuarios'
            nuevo_usuario = {
                "id": res.user.id,  # <--- ESTO ES VITAL: Vincula auth.users con tu tabla
                "nombre": nombre,
                "email": email,
                "usuario": usuario,
                "password": password, 
                "rol": 1,
                "estado": "pendiente"  # Cambiado a pendiente hasta que confirme correo
            }
            
            # Ahora el insert funcionará porque lleva el UUID obligatorio
            supabase.table('usuarios').insert(nuevo_usuario).execute()

            flash("¡Registro exitoso! Por favor, verifica tu correo para activar tu cuenta.", "info")
            return redirect(url_for('login_manual_page'))

    except Exception as e:
        print(f"Error en registro: {e}")
        flash("Hubo un error al procesar el registro. El usuario o email podrían ya existir.", "danger")
        return redirect(url_for('registro_page'))    
            
@app.route('/login_facial', methods=['POST'])
@app.route('/login_biometrico', methods=['POST'])
def login_facial():
    datos = request.get_json()
    face_actual = datos.get('face_data')
    try:
        # 1. Buscamos solo usuarios que tengan face_data registrado
        res = supabase.table('usuarios').select("*").not_.is_('face_data', 'null').execute()
        usuarios = res.data
        
        mejor_usuario = None
        umbral = 0.08
        menor_dist = float('inf')

        for user in usuarios:
            dist = calcular_distancia_facial(face_actual, user['face_data'])
            if dist < umbral and dist < menor_dist:
                menor_dist = dist
                mejor_usuario = user

        if mejor_usuario:
            # Sincronizamos la sesión con los datos de tu nueva tabla
            session.update({
                'user_id': mejor_usuario['id'], 
                'nombre': mejor_usuario['nombre'], 
                'rol': mejor_usuario['rol']
            })
            
            # --- MODIFICACIÓN DE LOGICA DE ROLES ---
            # Si el rol es 2 va al panel de administración
            if mejor_usuario['rol'] == 2:
                target = url_for('admin_dashboard')
            # Si el rol es 3 (o cualquier otro) va a la vista de servicios
            else:
                target = url_for('servicios')
                
            return jsonify({"status": "success", "redirect": target})
        
        return jsonify({"status": "error", "message": "Rostro no reconocido o no vinculado"}), 401

    except Exception as e:
        print(f"Error en login biométrico: {e}")
        # Retornamos el error para debuguear si falta la columna face_data
        return jsonify({"status": "error", "message": str(e)}), 500    
    
@app.route('/ejecutar_login', methods=['POST'])
def ejecutar_login():
    email_user = request.form.get('email')
    password_candidate = request.form.get('password')
    try:
        res = supabase.table('usuarios').select("*").or_(f"email.eq.{email_user},usuario.eq.{email_user}").execute()
        if res.data:
            user = res.data[0]
            stored_password = user['password']
            
            is_valid = False
            if stored_password.startswith('$2b$'):
                is_valid = bcrypt.checkpw(password_candidate.encode('utf-8'), stored_password.encode('utf-8'))
            else:
                is_valid = (password_candidate == stored_password)
            
            if is_valid:
                session.update({'user_id': user['id'], 'nombre': user['nombre'], 'rol': user['rol']})
                
                # CAMBIO: Verificación de rol numérico (2 = Admin)
                if user['rol'] == 2: 
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('servicios'))
               
        flash("Credenciales incorrectas", "danger")
        return redirect(url_for('login_manual_page'))
    except Exception as e:
        return f"Error: {str(e)}", 500

# --- RUTAS EXTRA ---

@app.route('/admin/trabajadores/crear')
@admin_required
def crear_trabajador():
    return render_template('admin/crear_trabajador.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- INICIO DEL SERVIDOR ---

if __name__ == '__main__':
    port = 5000
    print(f"\n✅ Servidor configurado para buscar en: {template_dir}")
    print(f"🏠 URL Local: http://localhost:{port}/") 
    app.run(host='0.0.0.0', port=port, debug=True)