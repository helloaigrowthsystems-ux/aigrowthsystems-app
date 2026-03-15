# auth.py — AI Growth Systems v4
import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

LIMITES_PLAN = {
    "demo":     3,
    "gratuito": 5,
    "pro":      99999,
    "business": 99999,
    "admin":    99999,
}

@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def mostrar_login():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
  --base:#08090C; --surface:#0F1117; --surface2:#141520;
  --border:#1E1F2E; --border2:#282938;
  --gold:#C9A84C; --gold2:#E8C96A;
  --text:#EAEAF0; --text2:#9090A8; --text3:#505060;
  --green:#3DD68C; --red:#F87171;
}
html, body, [class*="css"] { font-family:'DM Sans',system-ui,sans-serif !important; background:var(--base) !important; color:var(--text) !important; -webkit-font-smoothing:antialiased; }
.main .block-container { max-width:520px !important; padding-top:2rem !important; background:transparent !important; }
section[data-testid="stSidebar"] { display:none !important; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important; border-radius:10px !important; padding:4px !important; border:1px solid var(--border) !important; gap:2px !important; }
.stTabs [data-baseweb="tab"] { border-radius:7px !important; padding:8px 18px !important; font-size:0.82rem !important; font-weight:500 !important; color:var(--text3) !important; font-family:'DM Sans',sans-serif !important; }
.stTabs [aria-selected="true"] { background:var(--surface2) !important; color:var(--gold2) !important; }
.stTextInput input { background:var(--surface2) !important; border:1px solid var(--border2) !important; border-radius:9px !important; font-size:0.875rem !important; color:var(--text) !important; font-family:'DM Sans',sans-serif !important; caret-color:var(--gold); transition:all 0.18s !important; }
.stTextInput input::placeholder { color:var(--text3) !important; }
.stTextInput input:focus { border-color:var(--gold) !important; box-shadow:0 0 0 3px rgba(201,168,76,0.12) !important; background:var(--surface) !important; }
.stTextInput label { color:var(--text3) !important; font-size:0.78rem !important; font-weight:500 !important; letter-spacing:0.03em !important; }
.stButton > button { font-family:'DM Sans',sans-serif !important; font-weight:600 !important; font-size:0.875rem !important; border-radius:9px !important; transition:all 0.2s !important; letter-spacing:0.02em !important; }
.stButton > button[kind="primary"] { background:var(--gold) !important; border:none !important; color:#0A0807 !important; box-shadow:0 2px 16px rgba(201,168,76,0.3) !important; }
.stButton > button[kind="primary"]:hover { background:var(--gold2) !important; transform:translateY(-1px) !important; box-shadow:0 6px 24px rgba(201,168,76,0.4) !important; }
.stButton > button:not([kind="primary"]) { background:var(--surface2) !important; border:1px solid var(--border2) !important; color:var(--text2) !important; }
.stButton > button:not([kind="primary"]):hover { border-color:var(--gold) !important; color:var(--gold2) !important; }
.stSelectbox > div > div { background:var(--surface2) !important; border:1px solid var(--border2) !important; border-radius:9px !important; color:var(--text) !important; }
.stSelectbox label { color:var(--text3) !important; font-size:0.78rem !important; }
.stAlert { border-radius:9px !important; font-family:'DM Sans',sans-serif !important; }
[data-testid="stSuccess"] { background:rgba(61,214,140,0.07) !important; color:#3DD68C !important; border-left:2px solid #3DD68C !important; }
[data-testid="stWarning"] { background:rgba(251,191,36,0.07) !important; color:#FBBF24 !important; border-left:2px solid #FBBF24 !important; }
[data-testid="stError"]   { background:rgba(248,113,113,0.07) !important; color:#F87171 !important; border-left:2px solid #F87171 !important; }
@keyframes glow   { 0%,100%{filter:drop-shadow(0 0 8px rgba(201,168,76,0.6));} 50%{filter:drop-shadow(0 0 20px rgba(201,168,76,1));} }
@keyframes fadeUp { from{opacity:0;transform:translateY(14px);} to{opacity:1;transform:translateY(0);} }
</style>
""", unsafe_allow_html=True)

    # ── Hero: mensaje central claro ────────────────────────────────────────────
    st.markdown("""
<div style='text-align:center;padding-bottom:20px;animation:fadeUp 0.5s ease;'>
  <div style='display:inline-block;animation:glow 3s ease-in-out infinite;font-size:1.8rem;margin-bottom:10px;cursor:default;'>⚡</div>
  <div style='font-family:Sora,sans-serif;font-size:1.6rem;font-weight:800;color:#EAEAF0;letter-spacing:-0.04em;line-height:1.15;margin-bottom:8px;'>
    AI Growth Systems
  </div>
  <div style='font-size:0.52rem;font-weight:700;text-transform:uppercase;letter-spacing:0.18em;color:#C9A84C;margin-bottom:14px;'>
    Business AI Platform
  </div>
  <!-- Propuesta de valor central -->
  <div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.15);border-radius:12px;padding:14px 18px;margin-bottom:16px;text-align:left;'>
    <div style='font-family:Sora,sans-serif;font-weight:700;font-size:0.92rem;color:#EAEAF0;margin-bottom:6px;'>
      Para pymes de 1-50 personas que quieren crecer sin contratar más
    </div>
    <div style='font-size:0.82rem;color:#9090A8;line-height:1.6;'>
      Genera documentos, analiza datos, crea contenido y toma mejores decisiones —
      todo con IA, todo en español, todo en un solo sitio.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Casos de uso concretos (no funciones técnicas) ─────────────────────────
    casos = [
        ("⏱ 30 seg", "Contrato listo", "Genera un contrato profesional antes de que el cliente cuelgue el teléfono"),
        ("📊 2 min",  "Dashboard de ventas", "Sube tu Excel y obtén gráficos, KPIs y recomendaciones automáticas"),
        ("✉️ 1 min",  "Email que convierte", "Escribe emails de ventas personalizados que consiguen respuesta"),
    ]
    c1, c2, c3 = st.columns(3)
    for col, (t, tt, d) in zip([c1,c2,c3], casos):
        with col:
            st.markdown(
                f"<div style='background:var(--surface);border:1px solid var(--border);border-radius:10px;"
                f"padding:12px 13px;text-align:center;'>"
                f"<div style='font-size:0.68rem;font-weight:700;color:var(--gold);letter-spacing:0.06em;margin-bottom:4px;'>{t}</div>"
                f"<div style='font-size:0.82rem;font-weight:600;color:var(--text);margin-bottom:4px;'>{tt}</div>"
                f"<div style='font-size:0.7rem;color:var(--text3);line-height:1.4;'>{d}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Seguridad (visible, no oculta) ─────────────────────────────────────────
    st.markdown(
        "<div style='display:flex;align-items:center;gap:16px;background:var(--surface);"
        "border:1px solid var(--border);border-radius:8px;padding:10px 14px;margin-bottom:16px;'>"
        "<span style='font-size:0.75rem;color:var(--text3);font-family:DM Sans,sans-serif;'>"
        "🔒 <b style='color:var(--text2);'>Datos cifrados</b> · "
        "🇪🇺 <b style='color:var(--text2);'>Servidores en Europa</b> · "
        "🚫 <b style='color:var(--text2);'>No compartimos tu info</b>"
        "</span></div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────────
    tab_login, tab_reg, tab_demo = st.tabs([" Iniciar sesión ", " Crear cuenta ", " Prueba gratuita "])

    with tab_login:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        email = st.text_input("Email", key="li_email", placeholder="tu@empresa.com")
        pwd   = st.text_input("Contraseña", type="password", key="li_pwd", placeholder="••••••••")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Entrar →", type="primary", use_container_width=True, key="btn_li"):
            _hacer_login(email, pwd)

    with tab_reg:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        email_r  = st.text_input("Email de empresa", key="r_email", placeholder="tu@empresa.com")
        pwd_r    = st.text_input("Contraseña", type="password", key="r_pwd", placeholder="Mínimo 6 caracteres")
        nombre_r = st.text_input("Nombre o empresa", key="r_nombre", placeholder="Tu Empresa S.L.")

        # Plan selector — pricing visible y claro
        st.markdown(
            "<div style='font-size:0.72rem;font-weight:600;color:var(--text3);text-transform:uppercase;"
            "letter-spacing:0.08em;margin:14px 0 8px;'>Elige tu plan</div>",
            unsafe_allow_html=True
        )

        # Plan cards — precios claros
        planes_pub = [
            ("gratuito", "Gratuito", "0€/mes", "5 acciones/día · Funciones básicas · Sin tarjeta", "#8B8B9E"),
            ("pro",      "Pro ⭐",   "29€/mes", "Ilimitado · Todos los módulos · Soporte por email", "#C9A84C"),
            ("business", "Business", "A medida","Volumen alto · API · Soporte prioritario · Onboarding", "#E8C96A"),
        ]
        plan_reg = st.selectbox("Plan", [f"{p[1]} — {p[2]} — {p[3]}" for p in planes_pub],
            key="r_plan", label_visibility="collapsed")
        plan_elegido = {"Gratuito":"gratuito","Pro ⭐":"pro","Business":"business"}.get(plan_reg.split(" — ")[0], "gratuito")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Crear cuenta →", type="primary", use_container_width=True, key="btn_reg"):
            _hacer_registro(email_r, pwd_r, nombre_r, plan_elegido)
        st.markdown(
            "<div style='text-align:center;margin-top:8px;color:var(--text3);font-size:0.72rem;'>"
            "Sin tarjeta de crédito · Cancela cuando quieras · RGPD compliant</div>",
            unsafe_allow_html=True
        )

    with tab_demo:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);"
            "border-radius:12px;padding:16px 18px;margin-bottom:14px;'>"
            "<div style='font-family:Sora,sans-serif;font-weight:700;font-size:0.9rem;"
            "color:var(--gold2);margin-bottom:8px;'>Prueba sin compromiso</div>"
            "<div style='font-size:0.82rem;color:var(--text3);line-height:1.65;'>"
            "✓ 3 acciones para explorar la plataforma<br>"
            "✓ Acceso al Asistente IA y análisis de documentos<br>"
            "✓ Sin tarjeta · Sin permanencia · En 30 segundos"
            "</div></div>",
            unsafe_allow_html=True
        )
        email_d  = st.text_input("Tu email", key="d_email", placeholder="tu@empresa.com")
        nombre_d = st.text_input("Tu nombre o empresa", key="d_nombre", placeholder="Empresa S.L.")
        if st.button("Empezar prueba gratuita →", type="primary", use_container_width=True, key="btn_demo"):
            if not email_d:
                st.warning("Introduce tu email para continuar.")
            else:
                _hacer_registro(email_d, f"demo_{email_d[:8]}_2025", nombre_d or "Demo User", "demo")

    # ── Pricing expandible (no oculta, pero no intrusiva) ─────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with st.expander("💰 Ver todos los planes y precios", expanded=False):
        for _, nombre_p, precio_p, desc_p, color_p in planes_pub:
            st.markdown(
                f"<div style='background:var(--surface);border:1px solid {color_p}22;"
                f"border-radius:10px;padding:12px 16px;margin-bottom:6px;"
                f"display:flex;justify-content:space-between;align-items:center;'>"
                f"<div><span style='font-family:Sora,sans-serif;font-weight:700;font-size:0.85rem;color:{color_p};'>"
                f"{nombre_p}</span>"
                f"<span style='font-size:0.75rem;color:var(--text3);margin-left:10px;'>{desc_p}</span></div>"
                f"<div style='font-weight:700;font-size:0.9rem;color:var(--text);white-space:nowrap;margin-left:12px;'>{precio_p}</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        st.markdown(
            "<div style='text-align:center;font-size:0.75rem;color:var(--text3);margin-top:8px;'>"
            "¿Dudas? hello.aigrowthsystems@gmail.com · Respuesta en menos de 2h</div>",
            unsafe_allow_html=True
        )


def _hacer_login(email, password):
    if not email or not password:
        st.warning("Rellena email y contraseña.")
        return
    try:
        res = get_supabase().auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["usuario"] = res.user
        st.session_state["token"]   = res.session.access_token
        st.rerun()
    except Exception as e:
        msg = str(e)
        if "Email not confirmed" in msg:
            st.error("Confirma tu email antes de entrar (revisa tu bandeja).")
        elif "Invalid login" in msg or "invalid" in msg.lower():
            st.error("Email o contraseña incorrectos.")
        else:
            st.error(f"Error: {e}")

def _hacer_registro(email, password, nombre, plan="gratuito"):
    if not email or not password:
        st.warning("Rellena email y contraseña.")
        return
    if len(password) < 6:
        st.warning("La contraseña debe tener al menos 6 caracteres.")
        return
    try:
        sb  = get_supabase()
        res = sb.auth.sign_up({"email": email, "password": password,
                               "options": {"data": {"nombre": nombre}}})
        try:
            sb.table("usuarios").insert({
                "id": res.user.id, "email": email, "nombre": nombre,
                "plan": plan, "usos_hoy": 0, "fecha_usos": str(date.today()), "usos_total": 0,
            }).execute()
        except Exception:
            pass
        st.success("✅ Cuenta creada. Inicia sesión para empezar.")
    except Exception as e:
        msg = str(e)
        if "already registered" in msg or "already been registered" in msg:
            st.warning("Este email ya está registrado. Inicia sesión.")
        elif "security purposes" in msg:
            st.warning("Espera unos segundos e inténtalo de nuevo.")
        else:
            st.error(f"Error: {e}")

def cerrar_sesion():
    try:
        get_supabase().auth.sign_out()
    except Exception:
        pass
    for k in ["usuario","token","info_empresa","historial_chat","transcript","crm_data",
              "asistente_historial","contexto_asistente","dash_historial"]:
        st.session_state.pop(k, None)
    st.rerun()

def obtener_perfil():
    try:
        uid = st.session_state["usuario"].id
        res = get_supabase().table("usuarios").select("*").eq("id", uid).single().execute()
        return res.data or {}
    except Exception:
        return {}

def puede_usar():
    perfil = obtener_perfil()
    if not perfil: return True, ""
    plan = perfil.get("plan", "gratuito")
    if plan in ("pro","business","admin"): return True, ""
    hoy = str(date.today())
    if plan == "demo":
        total = perfil.get("usos_total") or 0
        if total >= 3:
            return False, "Has agotado las 3 acciones de prueba. Crea una cuenta para continuar."
        return True, ""
    limite = LIMITES_PLAN.get(plan, 5)
    usos = perfil.get("usos_hoy", 0) if perfil.get("fecha_usos") == hoy else 0
    if usos >= limite:
        return False, f"Has alcanzado el límite de {limite} acciones diarias del plan gratuito."
    return True, ""

def registrar_uso():
    try:
        uid    = st.session_state["usuario"].id
        hoy    = str(date.today())
        perfil = obtener_perfil()
        plan   = perfil.get("plan","gratuito")
        total  = (perfil.get("usos_total") or 0) + 1
        if plan == "demo":
            get_supabase().table("usuarios").upsert({"id":uid,"usos_total":total}).execute()
        else:
            usos = perfil.get("usos_hoy",0) if perfil.get("fecha_usos")==hoy else 0
            get_supabase().table("usuarios").upsert({"id":uid,"usos_hoy":usos+1,"fecha_usos":hoy,"usos_total":total}).execute()
    except Exception:
        pass

def obtener_metricas_usuario():
    try:
        uid = st.session_state["usuario"].id
        res = get_supabase().table("metricas").select("*").eq("user_id",uid).single().execute()
        return res.data or {}
    except Exception:
        return {}

def registrar_accion(tipo_accion):
    try:
        uid      = st.session_state["usuario"].id
        metricas = obtener_metricas_usuario()
        campo    = {"doc_procesado":"docs_procesados","doc_generado":"docs_generados",
                    "chat_consulta":"chat_consultas","batch_procesado":"batch_procesados",
                    "propuesta_generada":"propuestas_generadas"}.get(tipo_accion)
        if campo:
            get_supabase().table("metricas").upsert({"user_id":uid,campo:(metricas.get(campo) or 0)+1}).execute()
    except Exception:
        pass

def mostrar_uso_sidebar():
    perfil  = obtener_perfil()
    plan    = perfil.get("plan","gratuito")
    hoy     = str(date.today())
    usos    = perfil.get("usos_hoy",0) if perfil.get("fecha_usos")==hoy else 0
    total   = perfil.get("usos_total") or 0
    nombre  = perfil.get("nombre") or getattr(st.session_state.get("usuario"),"email","Usuario")

    PLAN_META = {
        "demo":     ("#606070","#141520","Demo"),
        "gratuito": ("#8B8B9E","#1A1B26","Gratuito"),
        "pro":      ("#C9A84C","#1E1A0A","Pro ⭐"),
        "business": ("#E8C96A","#1E1800","Business 🚀"),
        "admin":    ("#3DD68C","#0A1E14","Admin"),
    }
    txt_c,bg_c,plan_lbl = PLAN_META.get(plan,PLAN_META["gratuito"])

    st.markdown(
        f"<div style='padding:12px 14px 8px;border-top:1px solid #1E1F2E;margin-top:8px;'>"
        f"<div style='font-size:0.8rem;color:#9090A8;font-weight:500;margin-bottom:6px;"
        f"white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:DM Sans,sans-serif;'>{nombre}</div>"
        f"<span style='background:{bg_c};color:{txt_c};border:1px solid {txt_c}33;"
        f"border-radius:5px;padding:2px 9px;font-size:0.68rem;font-weight:600;letter-spacing:0.04em;"
        f"font-family:DM Sans,sans-serif;'>{plan_lbl}</span></div>",
        unsafe_allow_html=True
    )

    if plan == "demo":
        restantes = max(0,3-total)
        pct = min(100,int((total/3)*100))
        bar_c = "#3DD68C" if restantes>1 else "#FBBF24" if restantes>0 else "#F87171"
        st.markdown(
            f"<div style='padding:6px 14px 10px;'>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:5px;'>"
            f"<div style='font-size:0.7rem;color:#3A3A50;font-family:DM Sans,sans-serif;'>Acciones de prueba</div>"
            f"<div style='font-size:0.7rem;font-weight:600;color:{bar_c};'>{total}/3</div></div>"
            f"<div style='background:#141520;border-radius:3px;height:3px;overflow:hidden;'>"
            f"<div style='background:{bar_c};width:{pct}%;height:100%;border-radius:3px;'></div></div>"
            f"<div style='font-size:0.65rem;color:#2A2A3E;margin-top:4px;font-family:DM Sans,sans-serif;'>"
            f"Quedan {restantes} · Crea una cuenta para continuar</div></div>",
            unsafe_allow_html=True
        )
    elif plan == "gratuito":
        restantes = max(0,5-usos)
        pct = min(100,int((usos/5)*100))
        bar_c = "#3DD68C" if restantes>2 else "#FBBF24" if restantes>0 else "#F87171"
        st.markdown(
            f"<div style='padding:6px 14px 10px;'>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:5px;'>"
            f"<div style='font-size:0.7rem;color:#3A3A50;font-family:DM Sans,sans-serif;'>Acciones hoy</div>"
            f"<div style='font-size:0.7rem;font-weight:600;color:{bar_c};'>{usos}/5</div></div>"
            f"<div style='background:#141520;border-radius:3px;height:3px;overflow:hidden;'>"
            f"<div style='background:{bar_c};width:{pct}%;height:100%;border-radius:3px;'></div></div>"
            f"<div style='font-size:0.65rem;color:#2A2A3E;margin-top:4px;font-family:DM Sans,sans-serif;'>"
            f"Renuevan mañana · Pro desde 29€/mes</div></div>",
            unsafe_allow_html=True
        )
        if restantes == 0:
            st.markdown(
                "<div style='margin:0 14px 8px;background:rgba(201,168,76,0.06);"
                "border:1px solid rgba(201,168,76,0.15);border-radius:8px;padding:9px 12px;"
                "font-size:0.72rem;text-align:center;font-family:DM Sans,sans-serif;'>"
                "<span style='color:#C9A84C;font-weight:600;'>Pro ilimitado — 29€/mes</span><br>"
                "<span style='color:#2A2A3E;font-size:0.65rem;'>hello.aigrowthsystems@gmail.com</span></div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            "<div style='padding:4px 14px 10px;font-size:0.7rem;color:#3DD68C;font-family:DM Sans,sans-serif;'>✓ Acciones ilimitadas</div>",
            unsafe_allow_html=True
        )

    if st.button("Cerrar sesión", use_container_width=True):
        cerrar_sesion()