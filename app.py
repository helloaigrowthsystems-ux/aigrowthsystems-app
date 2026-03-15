# app.py — AI Growth Systems
import streamlit as st
import os, json, re
import pandas as pd
from io import BytesIO
from datetime import date

from file_handler import procesar_archivo_subido, procesar_multiples_archivos, texto_es_valido
from ai_processor import (procesar_documento, procesar_pregunta, analizar_datos_empresa,
    generar_propuesta_comercial, optimizar_precio, generar_email_cobro,
    analizar_contrato_riesgos, generar_descripcion_vacante)
from batch_processor import procesar_batch_completo
from generador import (generar_contrato, generar_presupuesto, generar_informe,
    generar_carta_reclamacion, generar_acuerdo_colaboracion)
from chatbot import chatbot_responder
from exportador import exportar_pdf, exportar_docx
from auth import (mostrar_login, mostrar_uso_sidebar, puede_usar, registrar_uso,
    obtener_metricas_usuario, registrar_accion, obtener_perfil, get_supabase)
from crm import mostrar_crm
from admin_panel import mostrar_admin_panel
from translator import traducir_texto, adaptar_contenido_mercado, IDIOMAS
from seo_content import (generar_articulo_blog, generar_posts_rrss, generar_newsletter,
    generar_descripcion_producto, analizar_competencia)
from legal_tools import (generar_politica_privacidad, generar_aviso_legal,
    generar_terminos_condiciones, generar_politica_cookies, simplificar_contrato)
from finance_tools import (generar_plan_financiero, calcular_roi_proyecto,
    analizar_rentabilidad_clientes, generar_presupuesto_departamento, detectar_fraude_facturas)
from meeting_tools import (resumir_reunion, generar_agenda_reunion,
    generar_presentacion_outline, redactar_acta_reunion, generar_email_seguimiento_reunion)
from customer_service import (responder_queja_cliente, generar_faq_empresa,
    analizar_satisfaccion_clientes, generar_guion_llamada_ventas, crear_programa_fidelizacion)
from strategy_tools import (generar_plan_negocio, analizar_dafo, generar_okrs,
    generar_plan_marketing, generar_pitch_inversores)
from invoice_generator import generar_factura_pdf
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@aimpulsa.com")
MODEL = "llama-3.3-70b-versatile"

st.set_page_config(
    page_title="AI Growth Systems",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM — Luxury Minimal / Editorial Dark
# Palette: #08090C base · #0F1117 surface · #1A1B26 border
# Accent: #C9A84C (gold) · Text: #EAEAF0 · Muted: #606070
# Font: Sora (display) + DM Sans (body)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

:root {
  --base:    #08090C;
  --surface: #0F1117;
  --surface2:#141520;
  --border:  #1E1F2E;
  --border2: #282938;
  --gold:    #C9A84C;
  --gold2:   #E8C96A;
  --text:    #EAEAF0;
  --text2:   #9090A8;
  --text3:   #505060;
  --green:   #3DD68C;
  --red:     #F87171;
  --amber:   #FBBF24;
  --radius:  12px;
  --radius2: 8px;
}

/* ── Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', system-ui, sans-serif !important;
    background: var(--base) !important;
    color: var(--text) !important;
    -webkit-font-smoothing: antialiased;
}
.main .block-container {
    padding-top: 2rem !important;
    max-width: 1060px !important;
    background: transparent !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
}
section[data-testid="stSidebar"] * { color: var(--text2) !important; }

section[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius2) !important;
    padding: 7px 14px !important;
    margin-bottom: 1px !important;
    font-size: 0.83rem !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text3) !important;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
    font-weight: 400 !important;
    letter-spacing: 0.01em !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(201,168,76,0.07) !important;
    color: var(--gold2) !important;
    padding-left: 18px !important;
    border-left: 2px solid var(--gold) !important;
}
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    display: none !important;
}
/* Category separators */
section[data-testid="stSidebar"] .stRadio > div > label[aria-label^="—"] {
    font-size: 0.56rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.14em !important;
    color: var(--border2) !important;
    padding: 20px 14px 4px !important;
    pointer-events: none !important;
    cursor: default !important;
    font-family: 'DM Sans', sans-serif !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[aria-label^="—"]:hover {
    background: transparent !important;
    color: var(--border2) !important;
    padding-left: 14px !important;
    border-left: none !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    border-radius: var(--radius2) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button[kind="primary"] {
    background: var(--gold) !important;
    border: none !important;
    color: #0A0807 !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 12px rgba(201,168,76,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--gold2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.4) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}
.stButton > button:not([kind="primary"]) {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text2) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: var(--surface) !important;
    border-color: var(--gold) !important;
    color: var(--gold2) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius2) !important;
    font-size: 0.875rem !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.18s !important;
    caret-color: var(--gold);
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: var(--text3) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12) !important;
    background: var(--surface) !important;
}
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius2) !important;
    color: var(--text) !important;
}
.stSelectbox [data-baseweb="select"] * { color: var(--text) !important; }
.stNumberInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius2) !important;
    color: var(--text) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 22px 24px !important;
    transition: all 0.22s ease !important;
    position: relative; overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: "";
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--gold), transparent);
    opacity: 0; transition: opacity 0.22s;
}
[data-testid="metric-container"]:hover {
    border-color: var(--border2) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35) !important;
}
[data-testid="metric-container"]:hover::before { opacity: 1; }
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.68rem !important;
    color: var(--text3) !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    font-family: 'Sora', sans-serif !important;
    letter-spacing: -0.03em !important;
}

/* ── Chat ── */
div[data-testid="stChatMessage"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 8px !important;
    background: var(--surface) !important;
}

/* ── Expanders ── */
div[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    color: var(--text2) !important;
    background: var(--surface) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius2) !important;
    padding: 8px 20px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: var(--text3) !important;
    transition: all 0.15s !important;
    background: transparent !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--gold2) !important;
    box-shadow: none !important;
}

/* ── In-page Radio ── */
.main .stRadio > div { gap: 6px !important; flex-wrap: wrap !important; }
.main .stRadio > div > label {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius2) !important;
    padding: 7px 16px !important;
    font-size: 0.83rem !important;
    font-weight: 400 !important;
    color: var(--text2) !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
    font-family: 'DM Sans', sans-serif !important;
}
.main .stRadio > div > label > div:first-child { display: none !important; }
.main .stRadio > div > label:hover {
    border-color: var(--gold) !important;
    color: var(--gold2) !important;
    background: rgba(201,168,76,0.06) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed var(--border2) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--gold) !important;
    background: rgba(201,168,76,0.03) !important;
}
[data-testid="stFileUploader"] * { color: var(--text2) !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden !important; }
[data-testid="stDataFrame"] * { background: var(--surface) !important; color: var(--text2) !important; }

/* ── Code ── */
.stCode { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: var(--radius2) !important; }

/* ── Alerts ── */
.stAlert { border-radius: var(--radius2) !important; border: none !important; font-family: 'DM Sans', sans-serif !important; }
[data-testid="stInfo"]    { background: rgba(201,168,76,0.07) !important; color: var(--gold2) !important; border-left: 2px solid var(--gold) !important; }
[data-testid="stSuccess"] { background: rgba(61,214,140,0.07) !important; color: var(--green) !important; border-left: 2px solid var(--green) !important; }
[data-testid="stWarning"] { background: rgba(251,191,36,0.07) !important; color: var(--amber) !important; border-left: 2px solid var(--amber) !important; }
[data-testid="stError"]   { background: rgba(248,113,113,0.07) !important; color: var(--red) !important; border-left: 2px solid var(--red) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--base); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* ── Progress ── */
.stProgress > div > div { background: var(--gold) !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ══════════════════════════════════════════
   UTILITY CLASSES
   ══════════════════════════════════════════ */
.tip-box {
    background: rgba(61,214,140,0.06);
    border: 1px solid rgba(61,214,140,0.2);
    border-radius: var(--radius2);
    padding: 11px 16px;
    font-size: 0.84rem;
    color: var(--green);
    margin-bottom: 16px;
    display: flex; align-items: flex-start; gap: 9px;
    font-family: 'DM Sans', sans-serif;
}

/* Page header */
.ph { margin-bottom: 0; }
.ph-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--text) !important;
    margin: 0 0 5px;
    letter-spacing: -0.03em;
}
.ph-desc { color: var(--text3); font-size: 0.875rem; margin: 0; font-family: 'DM Sans', sans-serif; }
.ph-line { height: 1px; background: var(--border); margin: 12px 0 22px; }

/* Card */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
}
.card:hover {
    border-color: var(--border2);
    box-shadow: 0 6px 32px rgba(0,0,0,0.25);
    transform: translateY(-1px);
}

/* Gold label */
.gold-label {
    display: inline-block;
    font-size: 0.65rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--gold);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 4px; padding: 2px 8px;
    font-family: 'DM Sans', sans-serif;
}

/* ── Keyframes ── */
@keyframes glow {
    0%,100% { filter: drop-shadow(0 0 6px rgba(201,168,76,0.5)); }
    50%      { filter: drop-shadow(0 0 16px rgba(201,168,76,0.9)); }
}
@keyframes floatUp {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
@keyframes fadeUp  { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
@keyframes slideIn { from { opacity:0; transform:translateX(-12px); } to { opacity:1; transform:translateX(0); } }
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes borderPulse {
    0%,100% { border-color: var(--border); }
    50%      { border-color: rgba(201,168,76,0.4); }
}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    mostrar_login()
    st.stop()

# ─── NAVEGACIÓN OVERRIDE ──────────────────────────────────────────────────────
_override = st.session_state.pop("_modulo_override", None)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<style>
.sb-wrap { padding:22px 16px 18px; border-bottom:1px solid var(--border); margin-bottom:8px; animation:slideIn 0.3s ease; }
.sb-mark { display:inline-block; font-size:1.1rem; animation:glow 3s ease-in-out infinite; vertical-align:middle; cursor:default; }
.sb-name {
    font-family:'Sora',sans-serif; font-size:0.86rem; font-weight:700;
    color:#EAEAF0 !important; vertical-align:middle; margin-left:9px; letter-spacing:-0.01em;
}
.sb-sub { font-size:0.57rem; color:#282938 !important; margin-top:5px; letter-spacing:0.13em; font-weight:600; text-transform:uppercase; font-family:'DM Sans',sans-serif; }
</style>
<div class="sb-wrap">
    <div><span class="sb-mark">⚡</span><span class="sb-name">AI Growth Systems</span></div>
    <div class="sb-sub">Business AI Platform</div>
</div>
""", unsafe_allow_html=True)

    perfil = obtener_perfil()
    es_admin = perfil.get("email", "") == ADMIN_EMAIL
    plan_actual = perfil.get("plan", "gratuito")

    # ── Module access by plan ──
    MODULOS_DEMO     = {"Dashboard", "Asistente IA", "Guía de uso", "Mi cuenta"}
    MODULOS_GRATUITO = {"Dashboard", "Asistente IA", "Analizar documentos", "Guía de uso", "Mi cuenta", "Configuración"}
    MODULOS_PRO = MODULOS_GRATUITO | {
        "Crear documentos", "Facturación", "Revisar contratos", "Documentos legales",
        "Propuestas y ventas", "Clientes y CRM", "Finanzas y datos", "Estrategia",
        "Emails y comunicación", "Marketing y contenidos", "Traducción",
        "Recursos humanos", "Reuniones",
        "Presentaciones", "Análisis de mercado", "Identidad de marca",
        "Atención al cliente", "Chatbot de empresa", "Crear web con IA",
        "Generador Excel IA",
    }
    MODULOS_BUSINESS = MODULOS_PRO | {
        "Procesar en lote", "Informes ejecutivos", "Analítica avanzada",
    }

    def tiene_acceso(nombre):
        if es_admin: return True
        if plan_actual in ("admin","business"): return nombre in MODULOS_BUSINESS
        if plan_actual == "pro":               return nombre in MODULOS_PRO
        if plan_actual == "demo":              return nombre in MODULOS_DEMO
        return nombre in MODULOS_GRATUITO

    PLAN_REQUERIDO = {
        # Business only
        "Procesar en lote": "Business", "Informes ejecutivos": "Business", "Analítica avanzada": "Business",
        # Pro
        "Crear documentos": "Pro", "Facturación": "Pro", "Revisar contratos": "Pro", "Documentos legales": "Pro",
        "Propuestas y ventas": "Pro", "Clientes y CRM": "Pro", "Finanzas y datos": "Pro", "Estrategia": "Pro",
        "Emails y comunicación": "Pro", "Marketing y contenidos": "Pro", "Traducción": "Pro",
        "Recursos humanos": "Pro", "Reuniones": "Pro",
        "Presentaciones": "Pro", "Análisis de mercado": "Pro", "Identidad de marca": "Pro",
        "Atención al cliente": "Pro", "Chatbot de empresa": "Pro", "Crear web con IA": "Pro",
        "Generador Excel IA": "Pro",
    }
    ICONOS_PLAN = {"Pro": "⭐", "Business": "🚀"}

    def label_menu(nombre):
        if nombre.startswith("—") or tiene_acceso(nombre): return nombre
        return f"{nombre}  {ICONOS_PLAN.get(PLAN_REQUERIDO.get(nombre,''),'')}"

    # ── Clean 6-section menu ──
    todos_raw = [
        "Dashboard", "Asistente IA", "Guía de uso",
        "— Documentos",
            "Analizar documentos", "Crear documentos", "Facturación",
            "Revisar contratos", "Documentos legales", "Procesar en lote",
        "— Negocio",
            "Propuestas y ventas", "Clientes y CRM", "Finanzas y datos",
            "Estrategia", "Análisis de mercado",
        "— Marketing",
            "Emails y comunicación", "Marketing y contenidos",
            "Identidad de marca", "Presentaciones", "Traducción",
            "Crear web con IA",
        "— Equipo",
            "Recursos humanos", "Reuniones", "Atención al cliente",
            "Chatbot de empresa",
        "— IA Avanzada",
            "Generador Excel IA", "Informes ejecutivos", "Analítica avanzada",
        "— Mi cuenta",
            "Mi cuenta", "Configuración",
    ]
    if es_admin:
        todos_raw += ["— Administración", "Gestión de empresas", "Cambiar plan a usuario"]

    opciones_menu = [label_menu(m) for m in todos_raw]
    label_a_modulo = {label_menu(m): m for m in todos_raw if not m.startswith("—")}

    _default_idx = 0
    if _override:
        for _i, _lbl in enumerate(opciones_menu):
            if label_a_modulo.get(_lbl) == _override:
                _default_idx = _i
                break

    modulo_label = st.radio("Nav", opciones_menu, index=_default_idx, label_visibility="collapsed")
    modulo_raw = label_a_modulo.get(modulo_label, modulo_label)
    modulo = modulo_raw if not modulo_raw.startswith("—") else "Dashboard"

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    mostrar_uso_sidebar()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def es_separador(m):
    return m is None or m.startswith("—")

# ── Module name aliases (old names → new clean names) ──
_ALIAS = {
    "Analizar documentos":   "Analizar documento",
    "Crear documentos":      "Crear documento",
    "Propuestas y ventas":   "Propuestas comerciales",
    "Clientes y CRM":        "Clientes y pipeline",
    "Finanzas y datos":      "Análisis financiero",
    "Estrategia":            "Estrategia empresarial",
    "Emails y comunicación": "Redactar emails",
    "Identidad de marca":    "Generador de marca",
    "Presentaciones":        "Presentaciones IA",
    "Atención al cliente":   "Soporte al cliente",
    "Informes ejecutivos":   "Centro de informes",
    "Analítica avanzada":    "Analítica visual",
}
modulo = _ALIAS.get(modulo, modulo)

if es_separador(modulo):
    st.stop()

def _bloquear_si_sin_acceso(nombre):
    req = PLAN_REQUERIDO.get(nombre)
    if not req or tiene_acceso(nombre): return False
    ico = ICONOS_PLAN.get(req, "")
    brd = "#C9A84C" if req == "Pro" else "#E8C96A"
    txt = "#E8C96A" if req == "Pro" else "#FCD34D"
    st.markdown(
        f"<div style='max-width:440px;margin:80px auto;background:#0F1117;"
        f"border:1px solid rgba(201,168,76,0.2);border-radius:16px;padding:48px 40px;"
        "text-align:center;box-shadow:0 40px 80px rgba(0,0,0,0.6);animation:fadeUp 0.4s ease;'>"
        f"<div style='width:52px;height:52px;margin:0 auto 20px;background:rgba(201,168,76,0.08);"
        "border:1px solid rgba(201,168,76,0.2);border-radius:12px;"
        f"display:flex;align-items:center;justify-content:center;font-size:1.6rem;'>{ico}</div>"
        f"<div style='font-family:Sora,sans-serif;font-size:1.3rem;font-weight:700;"
        f"color:#EAEAF0;margin-bottom:10px;letter-spacing:-0.02em;'>Plan {req} requerido</div>"
        f"<div style='color:#606070;font-size:0.875rem;line-height:1.75;margin-bottom:28px;'>"
        f"<span style='color:{txt};font-weight:500;'>{nombre}</span> está disponible "
        f"desde el plan <span style='color:{txt};font-weight:500;'>{req}</span>.<br>"
        "Actualiza tu cuenta para acceder ahora.</div>"
        "<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.15);"
        "border-radius:10px;padding:14px 18px;font-size:0.84rem;'>"
        "<span style='color:#C9A84C;font-weight:600;'>hello.aigrowthsystems@gmail.com</span><br>"
        "<span style='font-size:0.75rem;color:#404050;margin-top:3px;display:block;'>"
        "Respuesta en menos de 1 hora · Sin permanencia</span>"
        "</div></div>",
        unsafe_allow_html=True
    )
    return True

def header(titulo, descripcion="", badge=""):
    dh  = f"<p class='ph-desc'>{descripcion}</p>" if descripcion else ""
    bdg = f"<span style='display:inline-block;font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:var(--gold);background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.2);border-radius:4px;padding:2px 8px;margin-bottom:6px;'>{badge}</span><br>" if badge else ""
    st.markdown(
        f"<div class='ph'>{bdg}<p class='ph-title'>{titulo}</p>{dh}</div>"
        "<div class='ph-line'></div>",
        unsafe_allow_html=True
    )

def tip(texto):
    st.markdown(f"<div class='tip-box'><span>💡</span><span>{texto}</span></div>", unsafe_allow_html=True)

def check_y_usar():
    ok, msg = puede_usar()
    if not ok:
        st.warning(f"Límite diario alcanzado. {msg}  →  hello.aigrowthsystems@gmail.com")
        return False
    registrar_uso()
    return True

def groq_call(prompt, max_tokens=2500):
    res = groq_client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}], max_tokens=max_tokens)
    return res.choices[0].message.content

def botones_descarga(contenido, tipo_doc, metadata=None, nombre_base="documento"):
    c1, c2, c3 = st.columns(3)
    with c1:
        try:
            pdf = exportar_pdf(contenido, tipo_doc=tipo_doc, metadata=metadata)
            st.download_button("⬇ PDF", data=pdf, file_name=f"{nombre_base}.pdf",
                mime="application/pdf", use_container_width=True, type="primary")
        except Exception as e:
            st.error(f"PDF: {e}")
    with c2:
        try:
            docx = exportar_docx(contenido, tipo_doc=tipo_doc, metadata=metadata)
            st.download_button("⬇ Word", data=docx, file_name=f"{nombre_base}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True)
        except Exception as e:
            st.error(f"Word: {e}")
    with c3:
        st.download_button("⬇ Texto", data=contenido, file_name=f"{nombre_base}.txt",
            mime="text/plain", use_container_width=True)

def resultado_con_descarga(resultado, tipo, nombre):
    st.text_area("Resultado:", resultado, height=380)
    botones_descarga(resultado, tipo, nombre_base=nombre)


if modulo == "Dashboard":
    metricas       = obtener_metricas_usuario()
    nombre_usuario = perfil.get("nombre") or perfil.get("email", "Usuario")
    nombre_corto   = nombre_usuario.split()[0] if nombre_usuario else ""

    # Plan badge para el hero
    PLAN_HERO = {
        "demo":     ("Demo",     "#606070"),
        "gratuito": ("Gratuito", "#8B8B9E"),
        "pro":      ("Pro ⭐",   "#C9A84C"),
        "business": ("Business 🚀", "#E8C96A"),
        "admin":    ("Admin 🔑", "#3DD68C"),
    }
    plan_lbl_h, plan_col_h = PLAN_HERO.get(plan_actual, PLAN_HERO["gratuito"])

    # Hero mejorado
    hora = __import__("datetime").datetime.now().hour
    saludo = "Buenos días" if hora < 13 else "Buenas tardes" if hora < 20 else "Buenas noches"

    st.markdown(
        f"<div style='background:linear-gradient(135deg,#0A0F1E 0%,#131627 50%,#0D1117 100%);"
        "border-radius:20px;padding:30px 36px 26px;margin-bottom:20px;"
        "border:1px solid rgba(201,168,76,0.15);position:relative;overflow:hidden;"
        "animation:fadeUp 0.45s ease;box-shadow:0 8px 48px rgba(0,0,0,0.5);'>"
        # Top shimmer line
        "<div style='position:absolute;top:0;left:0;right:0;height:1px;"
        "background:linear-gradient(90deg,transparent,rgba(201,168,76,0.5),transparent);'></div>"
        # Decorative circle
        "<div style='position:absolute;right:-40px;top:-40px;width:200px;height:200px;"
        "border-radius:50%;background:radial-gradient(circle,rgba(201,168,76,0.08),transparent 70%);'></div>"
        "<div style='display:flex;align-items:flex-start;justify-content:space-between;'>"
        "<div style='flex:1;'>"
        f"<div style='font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:0.16em;"
        f"color:rgba(201,168,76,0.6);margin-bottom:12px;font-family:DM Sans,sans-serif;'>AI Growth Systems · Business Platform</div>"
        f"<div style='font-family:Sora,sans-serif;font-size:0.9rem;color:#606070;margin-bottom:4px;'>{saludo}</div>"
        f"<div style='font-family:Sora,sans-serif;font-size:2rem;font-weight:800;"
        f"color:#EAEAF0;letter-spacing:-0.04em;line-height:1.1;margin-bottom:10px;'>{nombre_corto}</div>"
        f"<div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap;'>"
        f"<span style='background:rgba({','.join(str(int(plan_col_h.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.12);"
        f"color:{plan_col_h};border:1px solid rgba({','.join(str(int(plan_col_h.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.3);"
        f"border-radius:6px;padding:3px 12px;font-size:0.72rem;font-weight:700;"
        f"font-family:DM Sans,sans-serif;'>{plan_lbl_h}</span>"
        f"<span style='color:#404050;font-size:0.8rem;font-family:DM Sans,sans-serif;'>Tu plataforma de inteligencia artificial empresarial</span>"
        f"</div></div>"
        # Animated bolt
        "<div style='font-size:3rem;cursor:default;flex-shrink:0;"
        "animation:floatUp 4s ease-in-out infinite;"
        "filter:drop-shadow(0 0 24px rgba(201,168,76,0.6));'>⚡</div>"
        "</div>"
        # Pills row
        "<div style='margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.04);"
        "display:flex;flex-wrap:wrap;gap:6px;'>" +
        "".join(
            f"<span style='background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.2);"
            f"border-radius:6px;padding:3px 12px;font-size:0.7rem;color:#C9A84C;font-weight:500;'>{t}</span>"
            for t in ["🧠 Estrategia IA", "📄 Documentos", "📊 Analítica", "🌐 Webs", "⚖️ Legal", "👥 Equipo", "🚀 Resultados"]
        ) +
        "</div></div>",
        unsafe_allow_html=True
    )
    # Stats mejoradas con plan actual
    docs_p = metricas.get("docs_procesados", 0)
    docs_g = metricas.get("docs_generados", 0)
    chats  = metricas.get("chat_consultas", 0)
    props  = metricas.get("propuestas_generadas", 0)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl, delta_label in [
        (c1, docs_p, "Docs analizados",  None),
        (c2, docs_g, "Docs generados",   None),
        (c3, chats,  "Consultas IA",     None),
        (c4, props,  "Propuestas",       None),
    ]:
        col.metric(lbl, val)

    # Banner de plan con upgrade CTA si es gratuito/demo
    hoy_d  = str(__import__("datetime").date.today())
    usos_h = perfil.get("usos_hoy", 0) if perfil.get("fecha_usos") == hoy_d else 0

    if plan_actual == "gratuito":
        restantes = max(0, 5 - usos_h)
        bar_pct   = min(100, int(usos_h / 5 * 100))
        bar_color = "#3DD68C" if restantes > 2 else "#FBBF24" if restantes > 0 else "#F87171"
        st.markdown(
            f"<div style='background:rgba(201,168,76,0.05);border:1px solid rgba(201,168,76,0.18);"
            "border-radius:14px;padding:16px 22px;margin-top:16px;margin-bottom:4px;"
            "display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;'>"
            "<div style='flex:1;min-width:200px;'>"
            "<div style='font-family:Sora,sans-serif;font-size:0.72rem;font-weight:700;"
            "color:var(--gold);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;'>Plan Gratuito</div>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:6px;'>"
            f"<span style='font-size:0.8rem;color:var(--text2);'>Acciones hoy</span>"
            f"<span style='font-size:0.8rem;font-weight:700;color:{bar_color};'>{usos_h}/5 · {restantes} restantes</span></div>"
            f"<div style='background:var(--border);border-radius:4px;height:5px;overflow:hidden;'>"
            f"<div style='background:{bar_color};width:{bar_pct}%;height:100%;border-radius:4px;transition:width 0.4s;'></div></div>"
            "</div>"
            "<div style='text-align:right;'>"
            "<div style='font-size:0.78rem;color:var(--text3);margin-bottom:4px;'>Desbloquea todo con</div>"
            "<div style='font-family:Sora,sans-serif;font-size:1rem;font-weight:700;color:var(--gold2);'>Plan Pro — 29€/mes</div>"
            "<div style='font-size:0.72rem;color:var(--text3);margin-top:2px;'>hello.aigrowthsystems@gmail.com</div>"
            "</div></div>",
            unsafe_allow_html=True
        )
    elif plan_actual == "demo":
        total_demo = perfil.get("usos_total", 0)
        restantes_demo = max(0, 3 - total_demo)
        st.markdown(
            f"<div style='background:rgba(248,113,113,0.05);border:1px solid rgba(248,113,113,0.18);"
            "border-radius:14px;padding:14px 22px;margin-top:16px;margin-bottom:4px;'>"
            f"<span style='color:#F87171;font-weight:600;font-size:0.85rem;'>Demo — {restantes_demo} acciones restantes</span>"
            f"<span style='color:var(--text3);font-size:0.8rem;'> · Crea una cuenta gratuita para continuar</span>"
            "</div>",
            unsafe_allow_html=True
        )
    elif plan_actual in ("pro", "business", "admin"):
        st.markdown(
            "<div style='background:rgba(61,214,140,0.05);border:1px solid rgba(61,214,140,0.15);"
            "border-radius:12px;padding:12px 20px;margin-top:16px;margin-bottom:4px;"
            "display:flex;align-items:center;gap:12px;'>"
            f"<span style='color:#3DD68C;font-size:0.9rem;font-weight:700;'>✓ Plan {plan_actual.capitalize()} activo</span>"
            "<span style='color:var(--text3);font-size:0.8rem;'>· Acciones ilimitadas · Todos los módulos</span>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='display:flex;align-items:center;gap:12px;margin-bottom:18px;'>"
        "<div style='height:1px;flex:1;background:var(--border);'></div>"
        "<span style='font-family:DM Sans,sans-serif;font-size:0.62rem;font-weight:600;"
        "text-transform:uppercase;letter-spacing:0.12em;color:var(--text3);'>Acceso directo a todas las funciones</span>"
        "<div style='height:1px;flex:1;background:var(--border);'></div>"
        "</div>",
        unsafe_allow_html=True
    )

    # Tools organized by the PROBLEM they solve
    accesos = [
        # ── Ahorra tiempo ──
        ("⚡", "Asistente IA",          "En 1 min: respuestas, estrategia y análisis de negocio"),
        ("📄", "Analizar documento",     "En 30 seg: extrae todos los datos de cualquier PDF o Excel"),
        ("✍️", "Crear documento",        "En 2 min: contratos, presupuestos e informes listos"),
        ("🧾", "Facturación",            "En 1 min: factura profesional en PDF con tu marca"),
        # ── Vende más ──
        ("🤝", "Propuestas comerciales", "Propuestas con ROI calculado que aceleran el cierre"),
        ("📧", "Redactar emails",        "Emails de ventas que consiguen respuesta"),
        ("👥", "Clientes y pipeline",    "CRM para no perder ningún cliente ni oportunidad"),
        ("💬", "Chatbot de empresa",     "Atiende clientes automáticamente 24/7"),
        # ── Decide mejor ──
        ("📊", "Generador Excel IA",     "Crea y analiza cualquier Excel en segundos con IA"),
        ("📈", "Analítica visual",       "Dashboards automáticos y gráficos desde tus datos"),
        ("💰", "Análisis financiero",    "KPIs, ROI, previsiones y detección de anomalías"),
        ("📋", "Centro de informes",     "Informes ejecutivos listos en 3 minutos"),
        # ── Crece y comunica ──
        ("🌐", "Crear web con IA",       "Landing pages y webs corporativas listas para publicar"),
        ("🎨", "Generador de marca",     "Naming, identidad, mensajes y guía de estilo"),
        ("📣", "Marketing y contenidos", "Blog, redes sociales, newsletter y fichas de producto"),
        ("🎯", "Presentaciones IA",      "Slides profesionales con notas del presentador"),
        # ── Protege tu negocio ──
        ("⚖️", "Revisar contratos",      "Detecta riesgos antes de firmar — en 2 minutos"),
        ("🛡️", "Documentos legales",     "Política de privacidad, aviso legal y cookies RGPD"),
        # ── Gestiona tu equipo ──
        ("🏭", "Recursos humanos",       "Ofertas de trabajo, onboarding y evaluaciones"),
        ("📅", "Reuniones",              "Agendas, actas y resúmenes automáticos"),
        # ── Escala ──
        ("🔍", "Análisis de mercado",    "Estudia competidores, tendencias y precios de mercado"),
        ("🚀", "Estrategia empresarial", "Plan de negocio, DAFO, OKRs y pitch para inversores"),
        ("🌍", "Traducción",             "Traduce documentos y emails a 10 idiomas"),
        ("📦", "Procesar en lote",       "Extrae datos de 50+ documentos en una sola acción"),
        ("🎧", "Soporte al cliente",     "Gestiona quejas, mide satisfacción y fideliza clientes"),
    ]

    rows = [accesos[i:i+3] for i in range(0, len(accesos), 3)]
    for row in rows:
        cols = st.columns(3)
        for col, (ico, nm, desc) in zip(cols, row):
            with col:
                bloqueado = not tiene_acceso(nm)
                req       = PLAN_REQUERIDO.get(nm, "")
                op        = "0.4" if bloqueado else "1"
                badge_html = (
                    f"<span style='position:absolute;top:10px;right:10px;font-size:0.58rem;"
                    "font-weight:700;text-transform:uppercase;letter-spacing:0.06em;"
                    f"color:rgba(201,168,76,0.8);background:rgba(201,168,76,0.08);"
                    f"border:1px solid rgba(201,168,76,0.2);border-radius:4px;padding:1px 6px;'>"
                    f"{ICONOS_PLAN.get(req,'')}</span>"
                ) if bloqueado else ""
                st.markdown(
                    f"<div style='background:var(--surface);border:1px solid var(--border);"
                    f"border-radius:13px;padding:18px 18px 13px;margin-bottom:4px;opacity:{op};"
                    "position:relative;min-height:96px;"
                    "transition:border-color 0.2s,box-shadow 0.2s;'>"
                    f"{badge_html}"
                    f"<div style='font-size:1.5rem;margin-bottom:9px;'>{ico}</div>"
                    f"<div style='font-family:Sora,sans-serif;font-weight:600;font-size:0.83rem;"
                    f"color:var(--text);line-height:1.2;margin-bottom:5px;'>{nm}</div>"
                    f"<div style='color:var(--text3);font-size:0.72rem;line-height:1.45;"
                    f"font-family:DM Sans,sans-serif;'>{desc}</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
                lbl = f"{'🔒 ' if bloqueado else '→ '}{nm}"
                if st.button(lbl, key=f"da_{nm}", use_container_width=True,
                             type="primary" if not bloqueado else "secondary"):
                    st.session_state["_modulo_override"] = nm
                    st.rerun()
        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

elif modulo == "Asistente IA":
    ctx_guardado = st.session_state.get("contexto_asistente","")
    tono_ai = st.session_state.get("tono_asistente","Profesional y directo")
    idioma_ai = st.session_state.get("idioma_preferido","Español")

    st.markdown("""
<div style='background:linear-gradient(135deg,#0D0F1C,#141829);border:1px solid rgba(201,168,76,0.15);
border-radius:16px;padding:22px 28px 18px;margin-bottom:20px;position:relative;overflow:hidden;'>
<div style='position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,rgba(201,168,76,0.4),transparent);'></div>
<div style='display:flex;align-items:center;gap:14px;'>
  <div style='width:44px;height:44px;background:linear-gradient(135deg,rgba(201,168,76,0.2),rgba(201,168,76,0.05));
  border:1px solid rgba(201,168,76,0.3);border-radius:12px;display:flex;align-items:center;
  justify-content:center;font-size:1.4rem;flex-shrink:0;'>🤖</div>
  <div>
    <div style='font-family:Sora,sans-serif;font-weight:700;font-size:1.05rem;color:#EAEAF0;margin-bottom:3px;'>
      Asistente IA · AI Growth Systems</div>
    <div style='font-size:0.78rem;color:#606070;font-family:DM Sans,sans-serif;'>
      Puedo generar documentos, analizar datos, crear emails, hacer estrategia y mucho más —
      dímelo en lenguaje natural</div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

    # Context + file sidebar
    col_chat, col_tools = st.columns([3,1])

    with col_tools:
        # Capabilities showcase
        st.markdown(
            "<div style='background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin-bottom:10px;'>"
            "<div style='font-family:Sora,sans-serif;font-size:0.62rem;font-weight:700;text-transform:uppercase;"
            "letter-spacing:0.1em;color:var(--text3);margin-bottom:10px;'>Puedo hacer</div>",
            unsafe_allow_html=True
        )
        capacidades = [
            ("📄","Crear un contrato","Crea un contrato de servicios para [cliente]"),
            ("📊","Analizar mis datos","Aquí están mis ventas del Q3, analízalas"),
            ("📧","Escribir un email","Email de seguimiento para un cliente que no responde"),
            ("🚀","Plan de negocio","Plan de negocio para una app de delivery en Madrid"),
            ("💰","Calcular ROI","Tengo un proyecto de 50k€, ¿cuánto tardará en recuperarse?"),
            ("🔍","Estudiar competencia","Analiza los competidores de mi empresa de consultoría"),
            ("📣","Post para LinkedIn","Post sobre los beneficios de la IA para pymes"),
            ("⚖️","Revisar contrato","Aquí está el contrato, dime si hay riesgos"),
        ]
        for ico, label, ejemplo in capacidades:
            if st.button(f"{ico} {label}", key=f"cap_{label[:15]}", use_container_width=True):
                st.session_state["_ai_preset"] = ejemplo
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # File attachment
        archivo_ai = st.file_uploader("📎 Adjuntar archivo",
            type=["pdf","xlsx","xls","csv","txt"], key="ai_file_up",
            help="PDF, Excel, CSV o texto — la IA lo leerá y podrá responder sobre él")
        if archivo_ai:
            try:
                archivo_ai.seek(0)
                texto_f, _ = procesar_archivo_subido(archivo_ai)
                st.session_state["ai_file_ctx"] = texto_f[:5000]
                st.success(f"✅ {archivo_ai.name}")
            except Exception as e:
                st.error(f"Error: {e}")

        # Context
        with st.expander("⚙️ Contexto empresa", expanded=False):
            ctx_new = st.text_area("Contexto", value=ctx_guardado, height=110, key="ctx_ai_box",
                label_visibility="collapsed",
                placeholder="Sector, tamaño, clientes, facturación, objetivos...")
            if st.button("Guardar", type="primary", key="btn_ctx_ai_save", use_container_width=True):
                st.session_state["contexto_asistente"] = ctx_new
                st.success("✅")

    with col_chat:
        if ctx_guardado:
            st.markdown(
                f"<div style='font-size:0.75rem;color:var(--gold);padding:6px 12px;background:rgba(201,168,76,0.06);"
                "border-radius:6px;border-left:2px solid var(--gold);margin-bottom:10px;'>"
                f"📌 Contexto: {ctx_guardado[:100]}{'...' if len(ctx_guardado)>100 else ''}</div>",
                unsafe_allow_html=True
            )

        if "asistente_historial" not in st.session_state:
            st.session_state.asistente_historial = []

        # Show chat history
        for msg in st.session_state.asistente_historial:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Handle preset from capability buttons
        preset = st.session_state.pop("_ai_preset", None)
        pregunta = st.chat_input("Pregunta o pide cualquier cosa — documento, análisis, estrategia, email...")
        if preset and not pregunta:
            pregunta = preset

        if pregunta:
            with st.chat_message("user"):
                st.markdown(pregunta)

            if check_y_usar():
                file_ctx = st.session_state.pop("ai_file_ctx", "")
                tono_inst = {
                    "Profesional y directo": "Sé directo y conciso.",
                    "Detallado y explicativo": "Sé detallado, explica el razonamiento paso a paso.",
                    "Conciso y breve": "Responde en máximo 3-4 frases. Solo lo esencial."
                }.get(tono_ai, "")

                system = f"""Eres el asistente de negocio de AI Growth Systems. Eres un experto senior en:
- Estrategia empresarial, finanzas, marketing, ventas y operaciones
- Redacción de documentos profesionales (contratos, propuestas, informes, emails)
- Análisis de datos y métricas de negocio
- Recursos humanos, legal y comunicación corporativa

Reglas:
- Responde en {idioma_ai}. {tono_inst}
- Usa markdown: tablas, listas, negrita cuando ayude a la claridad
- Cuando el usuario pida un documento (contrato, propuesta, etc.), GENÉRALO COMPLETO, no solo el esquema
- Cuando pida análisis, sé específico con números y recomendaciones accionables
- Si no tienes suficiente info, haz las preguntas más importantes (máx 2-3)
- NUNCA digas "no puedo" si la tarea es empresarial — siempre encuentra la forma de ayudar
{f"CONTEXTO DE LA EMPRESA: {ctx_guardado}" if ctx_guardado else ""}
{f"ARCHIVO ADJUNTO DEL USUARIO: {file_ctx}" if file_ctx else ""}"""

                msgs = [{"role":"system","content":system}]
                for m in st.session_state.asistente_historial[-14:]:
                    msgs.append(m)
                msgs.append({"role":"user","content":pregunta})

                with st.spinner("Analizando..."):
                    try:
                        res = groq_client.chat.completions.create(
                            model=MODEL, messages=msgs, max_tokens=3000)
                        respuesta = res.choices[0].message.content
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.stop()

                with st.chat_message("assistant"):
                    st.markdown(respuesta)

                st.session_state.asistente_historial += [
                    {"role":"user","content":pregunta},
                    {"role":"assistant","content":respuesta}
                ]
                registrar_accion("chat_consulta")
                st.rerun()

        # Actions
        if st.session_state.asistente_historial:
            ca, cb, cc = st.columns([1,1,3])
            with ca:
                if st.button("🗑 Limpiar", key="ai_clr"):
                    st.session_state.asistente_historial = []
                    st.rerun()
            with cb:
                transcript = "\n\n".join([
                    f"{'Tú' if m['role']=='user' else 'IA'}: {m['content']}"
                    for m in st.session_state.asistente_historial
                ])
                st.download_button("⬇ Exportar", data=transcript,
                    file_name="conversacion_ia.txt", mime="text/plain", key="ai_exp")


elif modulo == "Analizar documento":
    header("Analizar documento", "Extrae datos, haz preguntas, resume o compara documentos PDF y Excel")

    modo = st.radio("¿Qué quieres hacer?", [
        "Extraer datos estructurados",
        "Hacer preguntas al documento",
        "Generar resumen",
        "Comparar dos documentos",
    ], horizontal=True)

    if modo == "Comparar dos documentos":
        c1, c2 = st.columns(2)
        with c1: a1 = st.file_uploader("Documento A", type=["pdf","xlsx","xls"], key="da")
        with c2: a2 = st.file_uploader("Documento B", type=["pdf","xlsx","xls"], key="db")
        if a1 and a2 and st.button("Comparar documentos", type="primary"):
            if check_y_usar():
                a1.seek(0); a2.seek(0)
                t1,_ = procesar_archivo_subido(a1); t2,_ = procesar_archivo_subido(a2)
                with st.spinner("Comparando..."):
                    r = procesar_pregunta(f"DOCUMENTO A:\n{t1}\n\nDOCUMENTO B:\n{t2}",
                        "Compara ambos documentos en detalle: diferencias clave, similitudes y qué es más favorable o completo.")
                st.write(r); registrar_accion("doc_procesado")
                botones_descarga(r, "informe", nombre_base="comparacion_documentos")
    else:
        archivo = st.file_uploader("Sube tu documento (PDF o Excel)", type=["pdf","xlsx","xls"])
        if archivo:
            texto, nombre = procesar_archivo_subido(archivo)
            if not texto_es_valido(texto):
                st.warning("El documento parece estar vacío o es un PDF escaneado. Asegúrate de que sea un PDF con texto digital.")
            else:
                st.success(f"✅ Documento cargado: **{nombre}**")

            if modo == "Extraer datos estructurados":
                plantillas = st.selectbox("Plantilla de extracción:", [
                    "Personalizado...",
                    "Factura — proveedor, fecha, número, base imponible, IVA, total",
                    "Cliente — nombre, NIF/CIF, dirección, email, teléfono",
                    "Contrato — partes, fecha de firma, duración, importe, penalizaciones",
                    "Albarán — producto, cantidad, precio unitario, descuento, total",
                    "Nómina — empleado, puesto, salario bruto, IRPF, neto",
                ])
                instruccion = st.text_input("Describe qué extraer:") if plantillas == "Personalizado..." else plantillas
                if st.button("Extraer datos", type="primary") and instruccion:
                    if check_y_usar():
                        with st.spinner("Extrayendo datos..."):
                            r = procesar_documento(texto, instruccion)
                        st.code(r, language="json")
                        try:
                            datos = json.loads(re.sub(r"```json|```", "", r).strip())
                            if isinstance(datos, dict): datos = [datos]
                            df = pd.DataFrame(datos)
                            st.dataframe(df, use_container_width=True)
                            buf = BytesIO(); df.to_excel(buf, index=False); buf.seek(0)
                            st.download_button("⬇ Descargar Excel", data=buf,
                                file_name="datos_extraidos.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                type="primary")
                        except: pass
                        registrar_accion("doc_procesado")

            elif modo == "Hacer preguntas al documento":
                pregunta = st.text_input("¿Qué quieres saber sobre este documento?",
                    placeholder="Ej: ¿Cuál es el importe total con IVA?  /  ¿Cuáles son las condiciones de rescisión?")
                if st.button("Obtener respuesta", type="primary") and pregunta:
                    if check_y_usar():
                        with st.spinner("Analizando..."): r = procesar_pregunta(texto, pregunta)
                        st.markdown(f"""
                        <div style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:16px 20px;margin-top:8px;'>
                            <div style='font-size:0.75rem;color:#64748B;margin-bottom:8px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;'>Respuesta</div>
                            <div style='color:#0F172A;line-height:1.7;'>{r}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        registrar_accion("doc_procesado")

            elif modo == "Generar resumen":
                nivel = st.select_slider("Nivel de detalle:", ["Muy breve", "Ejecutivo", "Detallado"])
                if st.button("Generar resumen", type="primary"):
                    if check_y_usar():
                        inst = {
                            "Muy breve": "Resume en máximo 5 líneas los puntos más importantes.",
                            "Ejecutivo": "Genera un resumen ejecutivo estructurado con: contexto, puntos clave, cifras y conclusión.",
                            "Detallado": "Genera un análisis completo con todas las secciones importantes, cifras y conclusiones.",
                        }
                        with st.spinner("Generando resumen..."): r = procesar_pregunta(texto, inst[nivel])
                        st.write(r); registrar_accion("doc_procesado")
                        botones_descarga(r, "informe", nombre_base="resumen_documento")
        else:
            st.markdown("""
            <div style='text-align:center;padding:60px 20px;border:1.5px dashed #E2E8F0;border-radius:12px;background:#FAFAFA;'>
                <div style='font-size:2.5rem;margin-bottom:12px;'>📄</div>
                <div style='font-weight:500;color:#0F172A;margin-bottom:6px;'>Sube un documento para empezar</div>
                <div style='font-size:0.85rem;color:#94A3B8;'>Admite PDF, Excel (.xlsx, .xls)</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROCESAR EN LOTE
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Procesar en lote":
    if _bloquear_si_sin_acceso("Procesar en lote"): st.stop()
    header("Procesar en lote", "Sube múltiples documentos a la vez y extrae todos los datos en un Excel")

    archivos = st.file_uploader("Sube los documentos", type=["pdf","xlsx","xls"], accept_multiple_files=True)
    plantillas = st.selectbox("¿Qué datos extraer?", [
        "Factura — proveedor, fecha, número de factura, base imponible, IVA, total",
        "Cliente — nombre, NIF/CIF, dirección, email, teléfono",
        "Contrato — partes, fecha de firma, duración, importe total",
        "Nómina — empleado, puesto, salario bruto, fecha de incorporación",
        "Personalizado...",
    ])
    instruccion = st.text_input("Instrucción personalizada:") if plantillas == "Personalizado..." else plantillas

    if archivos:
        st.info(f"📁 {len(archivos)} archivo(s) listos para procesar")
        if st.button(f"Procesar {len(archivos)} documentos", type="primary", use_container_width=True):
            if check_y_usar():
                with st.spinner(f"Procesando {len(archivos)} documentos..."):
                    prog = st.progress(0, "Leyendo documentos...")
                    docs = procesar_multiples_archivos(archivos)
                    prog.progress(40, "Extrayendo datos con IA...")
                    resultados = procesar_batch_completo(docs, instruccion)
                    prog.progress(100, "Completado")

                ok = [r for r in resultados if "_error" not in r]
                err = [r for r in resultados if "_error" in r]
                c1, c2 = st.columns(2)
                c1.metric("Procesados correctamente", len(ok))
                c2.metric("Con errores", len(err))

                if ok:
                    df = pd.DataFrame(ok)
                    cols = ["archivo"] + [c for c in df.columns if c != "archivo"]
                    df = df[[c for c in cols if c in df.columns]]
                    st.dataframe(df, use_container_width=True)
                    buf = BytesIO(); df.to_excel(buf, index=False); buf.seek(0)
                    st.download_button(f"⬇ Descargar Excel ({len(ok)} registros)", data=buf,
                        file_name="datos_extraidos.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary", use_container_width=True)
                    registrar_accion("batch_procesado")
                if err:
                    with st.expander(f"{len(err)} documento(s) con error"):
                        for e in err: st.error(f"{e.get('archivo','?')}: {e.get('_error','Error')}")

# ══════════════════════════════════════════════════════════════════════════════
# CREAR DOCUMENTO
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Crear documento":
    if _bloquear_si_sin_acceso("Crear documento"): st.stop()
    header("Crear documento", "Genera contratos, presupuestos, informes y más en segundos")

    tipo = st.radio("Tipo de documento:", [
        "Contrato", "Presupuesto", "Informe ejecutivo",
        "Acuerdo de colaboración", "Carta de reclamación",
        "Propuesta comercial",
    ], horizontal=True)

    if tipo == "Contrato":
        c1, c2 = st.columns(2)
        with c1:
            t = st.selectbox("Tipo de contrato:", ["Servicios", "Trabajo", "Alquiler", "Compraventa", "Confidencialidad (NDA)", "Colaboración", "Agencia"])
            proveedor = st.text_input("Tu empresa:")
            cliente = st.text_input("Cliente:")
        with c2:
            servicio = st.text_input("Servicio o descripción:")
            importe = st.text_input("Importe:")
            duracion = st.text_input("Duración:", placeholder="6 meses")
            fecha = st.text_input("Fecha de inicio:")
        if st.button("Generar contrato", type="primary"):
            if proveedor and cliente and servicio:
                if check_y_usar():
                    with st.spinner("Redactando contrato..."):
                        r = generar_contrato({"tipo":t,"proveedor":proveedor,"cliente":cliente,"servicio":servicio,"importe":importe,"duracion":duracion,"fecha_inicio":fecha})
                    registrar_accion("doc_generado")
                    resultado_con_descarga(r, "contrato", f"contrato_{cliente.replace(' ','_')}")
            else: st.warning("Completa los campos: empresa, cliente y servicio.")

    elif tipo == "Presupuesto":
        c1, c2 = st.columns(2)
        with c1: empresa = st.text_input("Tu empresa:"); cliente = st.text_input("Cliente:")
        with c2: validez = st.text_input("Validez:", placeholder="30 días"); fecha = st.text_input("Fecha:")
        servicios = st.text_area("Servicios y precios:", placeholder="Desarrollo web: 3.500€\nMantenimiento mensual: 250€")
        if st.button("Generar presupuesto", type="primary"):
            if empresa and cliente and servicios:
                if check_y_usar():
                    with st.spinner("Creando presupuesto..."):
                        r = generar_presupuesto({"empresa":empresa,"cliente":cliente,"servicios":servicios,"validez":validez,"fecha":fecha})
                    registrar_accion("doc_generado")
                    resultado_con_descarga(r, "presupuesto", f"presupuesto_{cliente.replace(' ','_')}")

    elif tipo == "Informe ejecutivo":
        c1, c2 = st.columns(2)
        with c1: empresa = st.text_input("Empresa:"); tema = st.text_input("Tema del informe:")
        with c2: periodo = st.text_input("Período:", placeholder="Q1 2026")
        datos = st.text_area("Datos clave:", placeholder="Ventas: 180.000€\nClientes nuevos: 31\nTicket medio: 5.800€")
        if st.button("Generar informe", type="primary"):
            if empresa and tema and datos:
                if check_y_usar():
                    with st.spinner("Redactando informe..."):
                        r = generar_informe({"empresa":empresa,"tema":tema,"periodo":periodo,"datos":datos})
                    registrar_accion("doc_generado")
                    resultado_con_descarga(r, "informe", f"informe_{tema.replace(' ','_')}")

    elif tipo == "Acuerdo de colaboración":
        c1, c2 = st.columns(2)
        with c1: pa = st.text_input("Parte A:"); pb = st.text_input("Parte B:"); obj = st.text_input("Objetivo:")
        with c2: dur = st.text_input("Duración:"); comp = st.text_input("Compensación:"); resp = st.text_area("Responsabilidades:", height=80)
        if st.button("Generar acuerdo", type="primary"):
            if pa and pb and obj:
                if check_y_usar():
                    with st.spinner("Redactando acuerdo..."):
                        r = generar_acuerdo_colaboracion({"parte_a":pa,"parte_b":pb,"objetivo":obj,"duracion":dur,"compensacion":comp,"responsabilidades":resp})
                    registrar_accion("doc_generado")
                    resultado_con_descarga(r, "contrato", f"acuerdo_{pb.replace(' ','_')}")

    elif tipo == "Carta de reclamación":
        c1, c2 = st.columns(2)
        with c1: remitente = st.text_input("Tu empresa:"); destinatario = st.text_input("Destinatario:")
        with c2: asunto = st.text_input("Asunto:"); importe = st.text_input("Importe reclamado:")
        descripcion = st.text_area("Descripción del problema:", height=120)
        if st.button("Generar carta", type="primary"):
            if remitente and destinatario and descripcion:
                if check_y_usar():
                    with st.spinner("Redactando carta..."):
                        r = generar_carta_reclamacion({"remitente":remitente,"destinatario":destinatario,"asunto":asunto,"importe":importe,"descripcion":descripcion})
                    registrar_accion("doc_generado")
                    resultado_con_descarga(r, "contrato", f"carta_{destinatario.replace(' ','_')}")

    elif tipo == "Propuesta comercial":
        c1, c2 = st.columns(2)
        with c1:
            empresa = st.text_input("Tu empresa:"); cliente = st.text_input("Empresa cliente:")
            sector = st.text_input("Sector del cliente:"); problema = st.text_input("Problema que resuelves:")
        with c2:
            solucion = st.text_input("Tu solución:"); precio = st.text_input("Precio:")
            diferenciadores = st.text_area("Casos de éxito o ventajas:", height=100)
        if st.button("Generar propuesta", type="primary"):
            if empresa and cliente and problema:
                if check_y_usar():
                    with st.spinner("Generando propuesta..."):
                        r = generar_propuesta_comercial({"empresa":empresa,"cliente":cliente,"sector":sector,"problema":problema,"solucion":solucion,"precio":precio,"diferenciadores":diferenciadores})
                    registrar_accion("propuesta_generada")
                    resultado_con_descarga(r, "propuesta", f"propuesta_{cliente.replace(' ','_')}")

# ══════════════════════════════════════════════════════════════════════════════
# FACTURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Facturación":
    if _bloquear_si_sin_acceso("Facturación"): st.stop()
    header("Facturación", "Genera facturas profesionales en PDF con tu imagen corporativa")

    tip("Rellena solo los campos que apliquen — todos son opcionales excepto nombre de empresa, cliente y al menos una línea.")

    st.markdown("##### Datos de tu empresa")
    c1, c2, c3 = st.columns(3)
    with c1: en=st.text_input("Nombre empresa:"); ecif=st.text_input("CIF/NIF:"); edir=st.text_input("Dirección:")
    with c2: eciu=st.text_input("Ciudad y CP:"); etel=st.text_input("Teléfono:"); eemail=st.text_input("Email:")
    with c3: eweb=st.text_input("Web:"); eiban=st.text_input("IBAN:"); epie=st.text_input("Texto pie de factura:")

    st.markdown("##### Datos del cliente")
    c1, c2 = st.columns(2)
    with c1: cn=st.text_input("Nombre cliente:"); ccif=st.text_input("CIF/NIF cliente:"); cdir=st.text_input("Dirección cliente:")
    with c2: cciu=st.text_input("Ciudad cliente:"); cemail=st.text_input("Email cliente:"); metodo=st.selectbox("Método de pago:",["Transferencia bancaria","Tarjeta","PayPal","Efectivo"])

    st.markdown("##### Datos de la factura")
    c1,c2,c3,c4 = st.columns(4)
    nf=c1.text_input("Nº Factura:", value=f"FAC-{date.today().year}-001")
    fe=c2.text_input("Fecha emisión:", value=date.today().strftime("%d/%m/%Y"))
    fv=c3.text_input("Fecha vencimiento:")
    ref=c4.text_input("Referencia:")

    st.markdown("##### Líneas de factura")
    n_lineas = st.number_input("Número de líneas:", min_value=1, max_value=20, value=3)
    lineas = []
    for i in range(int(n_lineas)):
        ci1,ci2,ci3,ci4 = st.columns([4,1,1.5,1])
        desc = ci1.text_input(f"Descripción {i+1}:", key=f"d{i}", placeholder="Descripción del servicio")
        cant = ci2.number_input("Cant.", key=f"c{i}", min_value=0.0, value=1.0, step=0.5)
        precio = ci3.number_input("Precio €", key=f"p{i}", min_value=0.0, value=0.0, step=10.0)
        dto = ci4.number_input("Dto %", key=f"dt{i}", min_value=0.0, max_value=100.0, value=0.0)
        if desc: lineas.append({"descripcion":desc,"cantidad":cant,"precio_unitario":precio,"descuento":dto})

    c1,c2,c3 = st.columns(3)
    iva = c1.number_input("IVA %:", value=21.0, min_value=0.0, max_value=21.0)
    irpf = c2.number_input("IRPF % (retención):", value=0.0, min_value=0.0, max_value=21.0)
    notas = c3.text_input("Notas adicionales:")

    if st.button("Generar factura PDF", type="primary", use_container_width=True):
        if en and cn and lineas:
            datos_f = {"empresa_nombre":en,"empresa_cif":ecif,"empresa_direccion":edir,"empresa_ciudad":eciu,"empresa_telefono":etel,"empresa_email":eemail,"empresa_web":eweb,"cliente_nombre":cn,"cliente_cif":ccif,"cliente_direccion":cdir,"cliente_ciudad":cciu,"cliente_email":cemail,"numero_factura":nf,"fecha_emision":fe,"fecha_vencimiento":fv,"referencia":ref,"metodo_pago":metodo,"iban":eiban,"lineas":lineas,"iva":iva,"irpf":irpf,"notas":notas,"pie":epie}
            try:
                pdf_bytes, total = generar_factura_pdf(datos_f)
                st.success(f"✅ Factura generada — Total: **{total:,.2f} €**")
                st.download_button("⬇ Descargar factura PDF", data=pdf_bytes, file_name=f"{nf}.pdf",
                    mime="application/pdf", type="primary", use_container_width=True)
                registrar_accion("doc_generado")
            except Exception as e:
                st.error(f"Error: {e}")
        else: st.warning("Completa el nombre de tu empresa, el cliente y al menos una línea.")

# ══════════════════════════════════════════════════════════════════════════════
# PROPUESTAS COMERCIALES
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Propuestas comerciales":
    if _bloquear_si_sin_acceso("Propuestas comerciales"): st.stop()
    header("Propuestas comerciales", "Genera propuestas personalizadas con cálculo de ROI para cada cliente")
    tip("Cuanto más detallado seas, más persuasiva y específica será la propuesta generada.")
    c1, c2 = st.columns(2)
    with c1:
        empresa=st.text_input("Tu empresa:"); cliente=st.text_input("Empresa cliente:")
        sector=st.text_input("Sector del cliente:"); problema=st.text_input("Problema que resuelves:")
    with c2:
        solucion=st.text_input("Tu solución:"); precio=st.text_input("Precio:")
        diferenciadores=st.text_area("Casos de éxito o diferenciadores:", height=120)
    if st.button("Generar propuesta comercial", type="primary", use_container_width=True):
        if empresa and cliente and problema:
            if check_y_usar():
                with st.spinner("Generando propuesta..."):
                    r = generar_propuesta_comercial({"empresa":empresa,"cliente":cliente,"sector":sector,"problema":problema,"solucion":solucion,"precio":precio,"diferenciadores":diferenciadores})
                registrar_accion("propuesta_generada")
                resultado_con_descarga(r, "propuesta", f"propuesta_{cliente.replace(' ','_')}")
        else: st.warning("Completa empresa, cliente y problema.")

# ══════════════════════════════════════════════════════════════════════════════
# CLIENTES Y PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Clientes y pipeline":
    if _bloquear_si_sin_acceso("Clientes y pipeline"): st.stop()
    header("Clientes y pipeline", "Gestiona contactos, oportunidades y el seguimiento comercial")
    mostrar_crm()

# ══════════════════════════════════════════════════════════════════════════════
# ANÁLISIS FINANCIERO
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Análisis financiero":
    if _bloquear_si_sin_acceso("Análisis financiero"): st.stop()
    header("Análisis financiero", "Analiza datos, obtén KPIs, detecta tendencias y genera informes ejecutivos")

    tipo = st.radio("Herramienta:", ["Analizar datos Excel/CSV", "Plan financiero", "Calcular ROI", "Detectar irregularidades en facturas"], horizontal=True)

    if tipo == "Analizar datos Excel/CSV":
        archivo = st.file_uploader("Sube tu archivo de datos", type=["xlsx","xls","csv"])
        if archivo:
            ext = archivo.name.split(".")[-1]
            try:
                df = pd.read_csv(archivo) if ext=="csv" else pd.read_excel(archivo)
                st.success(f"✅ {len(df)} filas × {len(df.columns)} columnas")
                st.dataframe(df.head(10), use_container_width=True)
                numericas = df.select_dtypes(include="number").columns.tolist()
                if numericas:
                    import plotly.express as px
                    col_sel = st.selectbox("Visualizar columna:", numericas)
                    fig = px.histogram(df, x=col_sel, template="simple_white", color_discrete_sequence=["#6366F1"])
                    st.plotly_chart(fig, use_container_width=True)
                tipo_a = st.radio("Tipo de análisis:", ["tendencias","recomendaciones","anomalias","ejecutivo","previsiones"],
                    format_func=lambda x:{"tendencias":"Tendencias","recomendaciones":"Recomendaciones","anomalias":"Anomalías","ejecutivo":"Resumen ejecutivo","previsiones":"Previsiones 3 meses"}[x], horizontal=True)
                if st.button("Analizar con IA", type="primary"):
                    if check_y_usar():
                        rd = f"Columnas:{list(df.columns)}\nFilas:{len(df)}\nPrimeras:\n{df.head(8).to_string()}\nEstadísticas:\n{df.describe().to_string() if numericas else 'Sin numéricas'}"
                        with st.spinner("Analizando..."): r = analizar_datos_empresa(rd, tipo_a)
                        st.write(r); botones_descarga(r, "informe", nombre_base=f"analisis_{tipo_a}")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    elif tipo == "Plan financiero":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); sector=st.text_input("Sector:"); fase=st.selectbox("Fase:",["Startup","Crecimiento","Empresa establecida"])
        with c2: ing=st.text_input("Ingresos actuales:"); cf=st.text_input("Costes fijos mensuales:"); obj=st.text_input("Objetivo a 12 meses:")
        if st.button("Generar plan financiero", type="primary", use_container_width=True):
            if emp and ing:
                if check_y_usar():
                    with st.spinner("Generando..."):
                        r = generar_plan_financiero({"empresa":emp,"sector":sector,"fase":fase,"ingresos":ing,"costes_fijos":cf,"objetivo":obj})
                    st.write(r); botones_descarga(r, "informe", nombre_base="plan_financiero")

    elif tipo == "Calcular ROI":
        c1,c2=st.columns(2)
        with c1: inv=st.text_input("Inversión total:"); ing=st.text_input("Ingresos esperados:")
        with c2: per=st.text_input("Período:",value="12 meses"); tipo_p=st.text_input("Tipo de inversión:")
        if st.button("Calcular ROI", type="primary", use_container_width=True):
            if inv and ing:
                if check_y_usar():
                    with st.spinner("Calculando..."):
                        r = calcular_roi_proyecto({"inversion":inv,"ingresos_esperados":ing,"periodo":per,"tipo":tipo_p})
                    st.write(r); botones_descarga(r, "informe", nombre_base="analisis_roi")

    elif tipo == "Detectar irregularidades en facturas":
        archivo = st.file_uploader("Sube las facturas", type=["pdf","xlsx","xls","csv"])
        texto_m = st.text_area("O pega los datos aquí:", height=150)
        if st.button("Detectar irregularidades", type="primary", use_container_width=True):
            texto = ""
            if archivo: texto,_ = procesar_archivo_subido(archivo)
            elif texto_m: texto = texto_m
            if texto:
                if check_y_usar():
                    with st.spinner("Analizando..."):
                        r = detectar_fraude_facturas(texto)
                    st.write(r); botones_descarga(r, "informe", nombre_base="auditoria_facturas")

# ══════════════════════════════════════════════════════════════════════════════
# ESTRATEGIA EMPRESARIAL
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Estrategia empresarial":
    if _bloquear_si_sin_acceso("Estrategia empresarial"): st.stop()
    header("Estrategia empresarial", "Plan de negocio, análisis DAFO, OKRs, plan de marketing y pitch para inversores")
    tipo = st.radio("Herramienta:", ["Plan de negocio","Análisis DAFO","OKRs","Plan de marketing","Pitch para inversores"], horizontal=True)

    if tipo == "Plan de negocio":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); sector=st.text_input("Sector:"); prod=st.text_input("Producto/Servicio:"); merc=st.text_input("Mercado objetivo:")
        with c2: uvp=st.text_input("Propuesta de valor:"); comp=st.text_input("Competidores:"); inv=st.text_input("Inversión disponible:"); obj=st.text_input("Objetivo a 3 años:")
        if st.button("Generar plan de negocio", type="primary", use_container_width=True):
            if emp and prod:
                if check_y_usar():
                    with st.spinner("Generando..."):
                        r = generar_plan_negocio({"empresa":emp,"sector":sector,"producto":prod,"mercado":merc,"uvp":uvp,"competidores":comp,"inversion":inv,"objetivo":obj})
                    st.write(r); botones_descarga(r, "informe", nombre_base="plan_negocio")

    elif tipo == "Análisis DAFO":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); sector=st.text_input("Sector:")
        with c2: ctx=st.text_area("Situación actual:", height=120)
        if st.button("Generar análisis DAFO", type="primary", use_container_width=True):
            if emp:
                if check_y_usar():
                    with st.spinner("Analizando..."):
                        r = analizar_dafo({"empresa":emp,"sector":sector,"contexto":ctx})
                    st.write(r); botones_descarga(r, "informe", nombre_base="dafo")

    elif tipo == "OKRs":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); dept=st.text_input("Departamento:",value="Toda la empresa"); per=st.text_input("Período:",value="Q3 2026")
        with c2: est=st.text_area("Estrategia general:", height=80); ret=st.text_area("Retos principales:", height=80)
        if st.button("Generar OKRs", type="primary", use_container_width=True):
            if emp and est:
                if check_y_usar():
                    with st.spinner("Definiendo OKRs..."):
                        r = generar_okrs({"empresa":emp,"departamento":dept,"periodo":per,"estrategia":est,"retos":ret})
                    st.write(r); botones_descarga(r, "informe", nombre_base="okrs")

    elif tipo == "Plan de marketing":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); prod=st.text_input("Producto/Servicio:"); pub=st.text_input("Público objetivo:")
        with c2: pres=st.text_input("Presupuesto mensual:"); obj=st.text_input("Objetivo principal:")
        if st.button("Generar plan de marketing", type="primary", use_container_width=True):
            if emp and prod:
                if check_y_usar():
                    with st.spinner("Creando plan..."):
                        r = generar_plan_marketing({"empresa":emp,"producto":prod,"publico":pub,"presupuesto":pres,"objetivo":obj})
                    st.write(r); botones_descarga(r, "informe", nombre_base="plan_marketing")

    elif tipo == "Pitch para inversores":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); sector=st.text_input("Sector:"); prob=st.text_input("Problema que resuelve:"); sol=st.text_input("Solución:")
        with c2: modelo=st.text_input("Modelo de negocio:"); trac=st.text_input("Tracción actual:"); inv=st.text_input("Inversión buscada:"); uso=st.text_input("Uso de los fondos:")
        if st.button("Generar pitch", type="primary", use_container_width=True):
            if emp and prob:
                if check_y_usar():
                    with st.spinner("Preparando pitch..."):
                        r = generar_pitch_inversores({"empresa":emp,"sector":sector,"problema":prob,"solucion":sol,"modelo":modelo,"traccion":trac,"inversion_buscada":inv,"uso_fondos":uso})
                    st.write(r); botones_descarga(r, "informe", nombre_base="pitch_inversores")

# ══════════════════════════════════════════════════════════════════════════════
# REDACTAR EMAILS
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Redactar emails":
    if _bloquear_si_sin_acceso("Redactar emails"): st.stop()
    header("Redactar emails", "Emails profesionales para cualquier situación — en segundos")

    tipo = st.radio("Tipo de email:", [
        "Presentación y ventas", "Seguimiento", "Cobro de factura",
        "Respuesta a queja", "Anuncio o novedad", "Colaboración",
    ], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        remitente = st.text_input("Tu nombre y empresa:")
        destinatario = st.text_input("Destinatario:")
        empresa_dest = st.text_input("Empresa del destinatario:")
    with c2:
        tono = st.select_slider("Tono:", ["Muy formal", "Formal", "Profesional", "Cercano", "Directo"])
        contexto = st.text_area("Contexto adicional:", height=100,
            placeholder="Nos conocimos en el evento X / Es un cliente frío / Ya hemos hablado antes...")

    if tipo == "Cobro de factura":
        st.markdown("##### Datos de la factura impagada")
        c1, c2 = st.columns(2)
        with c1: importe=st.text_input("Importe:"); factura=st.text_input("Nº Factura:")
        with c2: vencimiento=st.text_input("Fecha vencimiento:"); dias=st.text_input("Días de retraso:")
        nivel = st.radio("Nivel de urgencia:", ["recordatorio", "urgente", "ultimatum"], horizontal=True,
            format_func=lambda x: {"recordatorio":"Primer aviso","urgente":"Segundo aviso","ultimatum":"Último aviso"}[x])

    if st.button("Redactar email", type="primary"):
        if remitente and destinatario:
            if check_y_usar():
                if tipo == "Cobro de factura":
                    with st.spinner("Redactando..."):
                        eg = generar_email_cobro({"remitente":remitente,"destinatario":destinatario,"importe":importe,"factura":factura,"vencimiento":vencimiento,"dias_retraso":dias,"nivel":nivel})
                else:
                    prompts = {
                        "Presentación y ventas": f"Email de ventas de {remitente} para {destinatario} de {empresa_dest}. Tono:{tono}. Contexto:{contexto}. Identifica un dolor, presenta solución brevemente, CTA (reunión 20 min). Máx 200 palabras.",
                        "Seguimiento": f"Email de seguimiento de {remitente} para {destinatario} de {empresa_dest}. Tono:{tono}. Contexto:{contexto}. Recuerda conversación anterior, nuevo valor, pide respuesta. Máx 150 palabras.",
                        "Respuesta a queja": f"Email de disculpa y resolución de {remitente} para {destinatario} de {empresa_dest}. Tono:{tono}. Contexto:{contexto}. Reconoce problema, solución concreta. Máx 180 palabras.",
                        "Anuncio o novedad": f"Email anunciando novedad de {remitente} para {destinatario} de {empresa_dest}. Tono:{tono}. Contexto:{contexto}. Destaca valor, anticipa objeciones. Máx 200 palabras.",
                        "Colaboración": f"Email de propuesta de colaboración de {remitente} para {destinatario} de {empresa_dest}. Tono:{tono}. Contexto:{contexto}. Sinergia clara, beneficio mutuo, CTA. Máx 200 palabras.",
                    }
                    with st.spinner("Redactando..."):
                        eg = groq_call(prompts[tipo] + "\n\nIncluye ASUNTO: al inicio y el cuerpo en español.", 800)

                lineas = eg.strip().split("\n")
                asunto = next((l.replace("ASUNTO:","").strip() for l in lineas if l.startswith("ASUNTO:")), "")
                cuerpo = "\n".join(l for l in lineas if not l.startswith("ASUNTO:")).strip()
                if asunto:
                    st.markdown(f"""
                    <div style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-bottom:12px;'>
                        <div style='font-size:0.72rem;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px;'>Asunto</div>
                        <div style='font-weight:500;color:#0F172A;'>{asunto}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.text_area("Cuerpo del email:", cuerpo, height=280)
                botones_descarga(eg, "informe", nombre_base="email")
        else: st.warning("Completa tu nombre y el destinatario.")

# ══════════════════════════════════════════════════════════════════════════════
# MARKETING Y CONTENIDOS
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Marketing y contenidos":
    if _bloquear_si_sin_acceso("Marketing y contenidos"): st.stop()
    header("Marketing y contenidos", "Artículos de blog, posts para redes sociales, newsletters y descripciones de producto")
    tipo = st.radio("Herramienta:", ["Artículo de blog", "Posts para redes sociales", "Newsletter", "Descripción de producto"], horizontal=True)

    if tipo == "Artículo de blog":
        c1,c2=st.columns(2)
        with c1: tema=st.text_input("Tema:"); emp=st.text_input("Empresa:"); kw=st.text_input("Palabra clave principal:")
        with c2: pub=st.text_input("Público objetivo:"); ext=st.selectbox("Extensión:",["600-800 palabras","800-1000 palabras","1000-1500 palabras"]); tono=st.selectbox("Tono:",["profesional","educativo","cercano","técnico"])
        if st.button("Generar artículo", type="primary", use_container_width=True):
            if tema and kw:
                if check_y_usar():
                    with st.spinner("Escribiendo artículo..."):
                        r = generar_articulo_blog({"tema":tema,"empresa":emp,"keyword":kw,"publico":pub,"tono":tono,"extension":ext})
                    st.write(r); botones_descarga(r, "informe", nombre_base=f"blog_{tema[:30].replace(' ','_')}")

    elif tipo == "Posts para redes sociales":
        c1,c2=st.columns(2)
        with c1: tema=st.text_input("Tema:"); emp=st.text_input("Empresa:")
        with c2: obj=st.text_input("Objetivo:"); tono=st.selectbox("Tono:",["profesional","inspiracional","educativo","promocional"])
        if st.button("Generar posts", type="primary", use_container_width=True):
            if tema:
                if check_y_usar():
                    with st.spinner("Creando posts para LinkedIn, Instagram, Twitter y Facebook..."):
                        r = generar_posts_rrss({"tema":tema,"empresa":emp,"objetivo":obj,"tono":tono})
                    st.write(r); botones_descarga(r, "informe", nombre_base=f"posts_{tema[:20].replace(' ','_')}")

    elif tipo == "Newsletter":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); tema=st.text_input("Tema principal:"); novedades=st.text_area("Novedades:", height=80)
        with c2: oferta=st.text_input("Oferta especial (opcional):"); seg=st.text_input("Segmento:",value="clientes y suscriptores")
        if st.button("Generar newsletter", type="primary", use_container_width=True):
            if emp and tema:
                if check_y_usar():
                    with st.spinner("Creando newsletter..."):
                        r = generar_newsletter({"empresa":emp,"tema":tema,"novedades":novedades,"oferta":oferta,"segmento":seg})
                    st.write(r); botones_descarga(r, "informe", nombre_base="newsletter")

    elif tipo == "Descripción de producto":
        c1,c2=st.columns(2)
        with c1: prod=st.text_input("Producto/Servicio:"); emp=st.text_input("Empresa:"); precio=st.text_input("Precio:")
        with c2: bens=st.text_area("Beneficios principales:", height=80); difs=st.text_area("Diferenciadores:", height=80)
        if st.button("Generar descripción", type="primary", use_container_width=True):
            if prod:
                if check_y_usar():
                    with st.spinner("Creando descripciones..."):
                        r = generar_descripcion_producto({"producto":prod,"empresa":emp,"precio":precio,"beneficios":bens,"diferenciadores":difs})
                    st.write(r); botones_descarga(r, "informe", nombre_base=f"descripcion_{prod[:20].replace(' ','_')}")

# ══════════════════════════════════════════════════════════════════════════════
# TRADUCCIÓN
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Traducción":
    if _bloquear_si_sin_acceso("Traducción"): st.stop()
    header("Traducción profesional", "Traduce documentos, contratos y emails a 10 idiomas con tono empresarial")
    tipo = st.radio("Herramienta:", ["Traducir texto", "Adaptar para otro mercado"], horizontal=True)

    if tipo == "Traducir texto":
        c1, c2 = st.columns([1, 2])
        with c1:
            idioma = st.selectbox("Idioma destino:", IDIOMAS, key="trad_idioma")
            tono = st.selectbox("Tono:", ["profesional","formal","técnico","legal","comercial"], key="trad_tono")
            contexto_t = st.selectbox("Tipo de contenido:", ["documento empresarial","contrato","email","web o marketing","presentación","informe"], key="trad_ctx")
            traducir_btn = st.button(f"🌍 Traducir al {idioma}", type="primary", use_container_width=True, key="trad_btn")
        with c2:
            texto = st.text_area("Texto a traducir:", height=320, key="trad_texto",
                placeholder="Pega aquí el texto que quieres traducir...")
        if traducir_btn:
            if not texto:
                st.warning("Escribe o pega el texto que quieres traducir.")
            elif check_y_usar():
                with st.spinner(f"Traduciendo al {idioma}..."):
                    r = traducir_texto(texto, idioma, tono, contexto_t)
                st.success(f"✅ Traducción al {idioma} completada")
                st.text_area(f"Resultado:", r, height=300, key="trad_result")
                st.download_button("⬇ Descargar traducción", data=r,
                    file_name=f"traduccion_{idioma.lower()}.txt", mime="text/plain", type="primary")

    elif tipo == "Adaptar para otro mercado":
        tip("La adaptación va más allá de traducir — ajusta el tono, referencias culturales y formato al mercado destino.")
        c1, c2 = st.columns([1, 2])
        with c1:
            pais = st.text_input("País o mercado destino:", placeholder="Alemania, México, Francia...", key="adapt_pais")
            adaptar_btn = st.button("🌐 Adaptar contenido", type="primary", use_container_width=True, key="adapt_btn")
        with c2:
            texto = st.text_area("Texto a adaptar:", height=280, key="adapt_texto")
        if adaptar_btn:
            if not texto or not pais:
                st.warning("Rellena el país y el texto a adaptar.")
            elif check_y_usar():
                with st.spinner(f"Adaptando para {pais}..."):
                    r = adaptar_contenido_mercado(texto, pais)
                st.write(r)
                botones_descarga(r, "informe", nombre_base=f"adaptacion_{pais.replace(' ','_')}")

# ══════════════════════════════════════════════════════════════════════════════
# RECURSOS HUMANOS
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Recursos humanos":
    if _bloquear_si_sin_acceso("Recursos humanos"): st.stop()
    header("Recursos humanos", "Ofertas de trabajo, onboarding, evaluaciones y planes de formación")
    tipo = st.radio("Herramienta:", ["Oferta de trabajo", "Plan de onboarding", "Evaluación de desempeño", "Plan de formación"], horizontal=True)

    if tipo == "Oferta de trabajo":
        c1,c2=st.columns(2)
        with c1: puesto=st.text_input("Puesto:"); emp=st.text_input("Empresa:"); sector=st.text_input("Sector:"); sal=st.text_input("Salario:")
        with c2: mod=st.selectbox("Modalidad:",["Presencial","Híbrido","100% remoto"]); bens=st.text_area("Beneficios:",height=80); reqs=st.text_area("Requisitos clave:",height=80)
        if st.button("Generar oferta de trabajo", type="primary", use_container_width=True):
            if puesto and emp:
                if check_y_usar():
                    with st.spinner("Generando oferta..."):
                        r = generar_descripcion_vacante({"puesto":puesto,"empresa":emp,"sector":sector,"salario":sal,"modalidad":mod,"beneficios":bens,"requisitos":reqs})
                    resultado_con_descarga(r, "informe", f"oferta_{puesto.replace(' ','_')}")

    elif tipo == "Plan de onboarding":
        c1,c2=st.columns(2)
        with c1: puesto=st.text_input("Puesto:"); emp=st.text_input("Empresa:"); dur=st.selectbox("Duración:",["1 semana","2 semanas","1 mes","3 meses"])
        with c2: herr=st.text_input("Herramientas a aprender:"); obj=st.text_area("Objetivos del puesto:",height=80)
        if st.button("Generar plan de onboarding", type="primary", use_container_width=True):
            if puesto and emp:
                if check_y_usar():
                    pr = f"Plan de onboarding para {puesto} en {emp}. Duración:{dur}. Herramientas:{herr}. Objetivos:{obj}. Incluye: objetivos por semana, actividades, KPIs, personas clave y checklist."
                    with st.spinner("Generando plan..."): r = groq_call(pr, 2000)
                    st.write(r); botones_descarga(r, "informe", nombre_base=f"onboarding_{puesto.replace(' ','_')}")

    elif tipo == "Evaluación de desempeño":
        c1,c2=st.columns(2)
        with c1: emp_n=st.text_input("Nombre empleado:"); puesto=st.text_input("Puesto:"); per=st.text_input("Período evaluado:")
        with c2: logros=st.text_area("Logros destacados:",height=100); areas=st.text_area("Áreas de mejora:",height=100)
        if st.button("Generar evaluación", type="primary", use_container_width=True):
            if emp_n and puesto:
                if check_y_usar():
                    pr = f"Evaluación de desempeño para {emp_n}, {puesto}. Período:{per}. Logros:{logros}. Mejoras:{areas}. Incluye: resumen ejecutivo, competencias (1-5), logros, áreas de desarrollo, objetivos y recomendación."
                    with st.spinner("Generando..."): r = groq_call(pr, 2000)
                    st.write(r); botones_descarga(r, "informe", nombre_base=f"evaluacion_{emp_n.replace(' ','_')}")

    elif tipo == "Plan de formación":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); dept=st.text_input("Departamento:"); presup=st.text_input("Presupuesto anual:")
        with c2: gaps=st.text_area("Necesidades de formación detectadas:",height=100); obj=st.text_input("Objetivo del equipo:")
        if st.button("Generar plan de formación", type="primary", use_container_width=True):
            if emp and gaps:
                if check_y_usar():
                    pr = f"Plan de formación para {dept} en {emp}. Presupuesto:{presup}. Necesidades:{gaps}. Objetivo:{obj}. Incluye: formaciones recomendadas, proveedores, costes, calendario y KPIs."
                    with st.spinner("Diseñando plan..."): r = groq_call(pr, 2000)
                    st.write(r); botones_descarga(r, "informe", nombre_base=f"formacion_{dept.replace(' ','_')}")

# ══════════════════════════════════════════════════════════════════════════════
# REUNIONES
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Reuniones":
    if _bloquear_si_sin_acceso("Reuniones"): st.stop()
    header("Reuniones", "Agendas, resúmenes, actas y emails de seguimiento")
    tipo = st.radio("Herramienta:", ["Resumir reunión", "Crear agenda", "Redactar acta", "Email de seguimiento"], horizontal=True)

    if tipo == "Resumir reunión":
        tipo_r = st.selectbox("Tipo de reunión:", ["General","Ventas","Dirección","Técnica","Retrospectiva"])
        trans = st.text_area("Transcripción o notas:", height=250)
        if st.button("Generar resumen", type="primary", use_container_width=True):
            if trans:
                if check_y_usar():
                    with st.spinner("Resumiendo..."): r = resumir_reunion(trans, tipo_r)
                    st.write(r); botones_descarga(r, "informe", nombre_base="resumen_reunion")

    elif tipo == "Crear agenda":
        c1,c2=st.columns(2)
        with c1: tipo_r=st.text_input("Tipo de reunión:"); dur=st.text_input("Duración:",value="60 minutos"); partic=st.text_input("Participantes:")
        with c2: obj=st.text_input("Objetivo:"); temas=st.text_area("Temas a tratar:",height=100)
        if st.button("Crear agenda", type="primary", use_container_width=True):
            if tipo_r and obj:
                if check_y_usar():
                    with st.spinner("Creando agenda..."): r = generar_agenda_reunion({"tipo":tipo_r,"duracion":dur,"participantes":partic,"objetivo":obj,"temas":temas})
                    st.write(r); botones_descarga(r, "informe", nombre_base="agenda_reunion")

    elif tipo == "Redactar acta":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); tipo_r=st.text_input("Tipo:"); fec=st.text_input("Fecha:"); asist=st.text_area("Asistentes:",height=80)
        with c2: puntos=st.text_area("Puntos tratados:",height=100); acuerdos=st.text_area("Acuerdos:",height=100)
        if st.button("Redactar acta", type="primary", use_container_width=True):
            if emp and puntos:
                if check_y_usar():
                    with st.spinner("Redactando..."): r = redactar_acta_reunion({"empresa":emp,"tipo":tipo_r,"fecha":fec,"asistentes":asist,"puntos":puntos,"acuerdos":acuerdos})
                    registrar_accion("doc_generado"); resultado_con_descarga(r, "contrato", f"acta_{fec.replace('/','_')}")

    elif tipo == "Email de seguimiento":
        c1,c2=st.columns(2)
        with c1: rem=st.text_input("Remitente:"); dest=st.text_input("Destinatarios:"); tema=st.text_input("Tema:")
        with c2: acuerdos=st.text_area("Acuerdos:",height=80); pasos=st.text_area("Próximos pasos:",height=80)
        if st.button("Redactar email post-reunión", type="primary", use_container_width=True):
            if rem and tema:
                if check_y_usar():
                    with st.spinner("Redactando..."): r = generar_email_seguimiento_reunion({"remitente":rem,"destinatarios":dest,"tema":tema,"acuerdos":acuerdos,"proximos_pasos":pasos})
                    lineas = r.strip().split("\n"); asunto = next((l.replace("ASUNTO:","").strip() for l in lineas if l.startswith("ASUNTO:")),"")
                    cuerpo = "\n".join(l for l in lineas if not l.startswith("ASUNTO:")).strip()
                    if asunto: st.markdown(f"<div style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-bottom:12px;'><div style='font-size:0.72rem;color:#64748B;font-weight:600;text-transform:uppercase;margin-bottom:4px;'>Asunto</div><div style='font-weight:500;'>{asunto}</div></div>",unsafe_allow_html=True)
                    st.text_area("Email:", cuerpo, height=250); botones_descarga(r, "informe", nombre_base="email_reunion")

# ══════════════════════════════════════════════════════════════════════════════
# REVISAR CONTRATOS
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Revisar contratos":
    if _bloquear_si_sin_acceso("Revisar contratos"): st.stop()
    header("Revisar contratos", "Detecta riesgos, cláusulas problemáticas y simplifica el lenguaje legal")
    tipo = st.radio("Herramienta:", ["Análisis de riesgos", "Simplificar a lenguaje claro"], horizontal=True)
    archivo = st.file_uploader("Sube el contrato (PDF)", type=["pdf"])
    texto_m = st.text_area("O pega el texto aquí:", height=180)

    if tipo == "Análisis de riesgos":
        if st.button("Analizar contrato", type="primary", use_container_width=True):
            texto = ""
            if archivo: texto,_ = procesar_archivo_subido(archivo)
            elif texto_m: texto = texto_m
            if texto:
                if check_y_usar():
                    with st.spinner("Analizando contrato..."):
                        r = analizar_contrato_riesgos(texto)
                    st.write(r); registrar_accion("doc_procesado"); botones_descarga(r, "informe", nombre_base="analisis_contrato")
            else: st.warning("Sube un PDF o pega el texto del contrato.")

    elif tipo == "Simplificar a lenguaje claro":
        if st.button("Simplificar contrato", type="primary", use_container_width=True):
            texto = ""
            if archivo: texto,_ = procesar_archivo_subido(archivo)
            elif texto_m: texto = texto_m
            if texto:
                if check_y_usar():
                    with st.spinner("Simplificando..."):
                        r = simplificar_contrato(texto)
                    st.write(r); botones_descarga(r, "informe", nombre_base="contrato_simplificado")
            else: st.warning("Sube un PDF o pega el texto del contrato.")

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTOS LEGALES
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Documentos legales":
    if _bloquear_si_sin_acceso("Documentos legales"): st.stop()
    header("Documentos legales", "Política de privacidad, aviso legal, términos y condiciones y política de cookies")
    tipo = st.radio("Documento:", ["Política de privacidad", "Aviso legal", "Términos y condiciones", "Política de cookies"], horizontal=True)

    if tipo == "Política de privacidad":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); cif=st.text_input("CIF/NIF:"); dom=st.text_input("Domicilio:"); email=st.text_input("Email de contacto:")
        with c2: tipo_neg=st.text_input("Tipo de negocio:"); datos=st.text_area("Datos que recoge:",height=80); final=st.text_area("Finalidad del tratamiento:",height=80)
        if st.button("Generar política de privacidad", type="primary", use_container_width=True):
            if emp:
                if check_y_usar():
                    with st.spinner("Generando..."):
                        r = generar_politica_privacidad({"empresa":emp,"cif":cif,"domicilio":dom,"email":email,"tipo_negocio":tipo_neg,"datos_recoge":datos,"finalidad":final})
                    registrar_accion("doc_generado"); resultado_con_descarga(r, "informe", "politica_privacidad")

    elif tipo == "Aviso legal":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); cif=st.text_input("CIF/NIF:"); dom=st.text_input("Domicilio:"); reg=st.text_input("Registro mercantil:")
        with c2: email=st.text_input("Email:"); web=st.text_input("Web:"); act=st.text_input("Actividad:")
        if st.button("Generar aviso legal", type="primary", use_container_width=True):
            if emp:
                if check_y_usar():
                    with st.spinner("Generando..."):
                        r = generar_aviso_legal({"empresa":emp,"cif":cif,"domicilio":dom,"registro":reg,"email":email,"web":web,"actividad":act})
                    registrar_accion("doc_generado"); resultado_con_descarga(r, "informe", "aviso_legal")

    elif tipo == "Términos y condiciones":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); serv=st.text_input("Tipo de servicio:"); pago=st.text_input("Forma de pago:")
        with c2: dev=st.text_input("Política de devoluciones:",value="14 días"); jur=st.text_input("Jurisdicción:",value="España")
        if st.button("Generar términos y condiciones", type="primary", use_container_width=True):
            if emp and serv:
                if check_y_usar():
                    with st.spinner("Generando..."):
                        r = generar_terminos_condiciones({"empresa":emp,"tipo_servicio":serv,"pago":pago,"devoluciones":dev,"jurisdiccion":jur})
                    registrar_accion("doc_generado"); resultado_con_descarga(r, "informe", "terminos_condiciones")

    elif tipo == "Política de cookies":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); web=st.text_input("Web:"); banner=st.selectbox("¿Tiene banner de cookies?",["Sí","No"])
        with c2: propias=st.text_input("Cookies propias:",value="sesión, preferencias"); terceros=st.text_input("Cookies de terceros:",value="Google Analytics, Google Ads")
        if st.button("Generar política de cookies", type="primary", use_container_width=True):
            if emp:
                if check_y_usar():
                    with st.spinner("Generando..."):
                        r = generar_politica_cookies({"empresa":emp,"web":web,"cookies_propias":propias,"cookies_terceros":terceros,"tiene_banner":banner})
                    registrar_accion("doc_generado"); resultado_con_descarga(r, "informe", "politica_cookies")

# ══════════════════════════════════════════════════════════════════════════════
# CHATBOT DE EMPRESA
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Chatbot de empresa":
    if _bloquear_si_sin_acceso("Chatbot de empresa"): st.stop()
    header("Chatbot de empresa", "Asistente virtual entrenado con la información de tu empresa — responde a clientes automáticamente")

    with st.expander("⚙️ Configurar información de tu empresa", expanded="info_empresa" not in st.session_state):
        info = st.text_area("Información de tu empresa:", height=220, key="conf_emp",
            placeholder="Empresa: Tech Solutions S.L.\nServicios: Desarrollo web, apps móviles, automatización IA\nPrecios: Desde 1.500€ · Mantenimiento desde 200€/mes\nHorario: L-V 9:00-18:00\nContacto: info@empresa.com\nFAQ:\n- ¿Presupuesto gratis? Sí, sin compromiso\n- ¿Trabajáis fuera de España? Sí")
        if st.button("Guardar configuración", type="primary"):
            st.session_state["info_empresa"] = info
            st.success("✅ Configuración guardada. El chatbot ya está listo.")
            st.rerun()

    emp_conf = st.session_state.get("info_empresa","")
    if emp_conf:
        if "historial_chat" not in st.session_state: st.session_state.historial_chat = []
        for m in st.session_state.historial_chat:
            with st.chat_message(m["role"]): st.write(m["content"])
        preg = st.chat_input("Escribe una pregunta como si fueras un cliente...")
        if preg:
            with st.chat_message("user"): st.write(preg)
            if check_y_usar():
                with st.spinner(""): resp = chatbot_responder(st.session_state.historial_chat, emp_conf, preg)
                with st.chat_message("assistant"): st.write(resp)
                st.session_state.historial_chat += [{"role":"user","content":preg},{"role":"assistant","content":resp}]
                registrar_accion("chat_consulta")
        if st.session_state.get("historial_chat"):
            if st.button("🗑 Nueva conversación"): st.session_state.historial_chat = []; st.rerun()
    else:
        st.info("⚙️ Configura la información de tu empresa arriba para activar el chatbot.")

# ══════════════════════════════════════════════════════════════════════════════
# SOPORTE AL CLIENTE
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Soporte al cliente":
    if _bloquear_si_sin_acceso("Soporte al cliente"): st.stop()
    header("Soporte al cliente", "Responde quejas, genera preguntas frecuentes y analiza la satisfacción")
    tipo = st.radio("Herramienta:", ["Responder queja", "Generar preguntas frecuentes", "Analizar reseñas y opiniones", "Programa de fidelización"], horizontal=True)

    if tipo == "Responder queja":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Tu empresa:"); cli=st.text_input("Nombre del cliente:"); queja=st.text_area("Queja recibida:",height=120)
        with c2: causa=st.text_input("Causa del problema:"); sol=st.text_input("Solución que ofrecemos:"); comp=st.text_input("Compensación (si aplica):")
        if st.button("Redactar respuesta profesional", type="primary", use_container_width=True):
            if emp and queja:
                if check_y_usar():
                    with st.spinner("Redactando respuesta..."):
                        r = responder_queja_cliente({"empresa":emp,"cliente":cli,"queja":queja,"causa":causa,"solucion":sol,"compensacion":comp})
                    lineas = r.strip().split("\n"); asunto = next((l.replace("ASUNTO:","").strip() for l in lineas if l.startswith("ASUNTO:")),"")
                    cuerpo = "\n".join(l for l in lineas if not l.startswith("ASUNTO:")).strip()
                    if asunto: st.markdown(f"<div style='background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:12px 16px;margin-bottom:12px;'><div style='font-size:0.72rem;color:#64748B;font-weight:600;text-transform:uppercase;margin-bottom:4px;'>Asunto</div><div style='font-weight:500;'>{asunto}</div></div>",unsafe_allow_html=True)
                    st.text_area("Respuesta:", cuerpo, height=280); botones_descarga(r, "informe", nombre_base="respuesta_queja")

    elif tipo == "Generar preguntas frecuentes":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); sector=st.text_input("Sector:"); prod=st.text_input("Producto/Servicio:")
        with c2: pregs=st.text_area("Preguntas habituales:",height=120,placeholder="¿Cuánto cuesta?\n¿Cuánto tarda?\n¿Tenéis garantía?")
        if st.button("Generar preguntas frecuentes", type="primary", use_container_width=True):
            if emp and prod:
                if check_y_usar():
                    with st.spinner("Generando FAQ..."):
                        r = generar_faq_empresa({"empresa":emp,"sector":sector,"producto":prod,"preguntas_comunes":pregs})
                    st.write(r); botones_descarga(r, "informe", nombre_base="faq_empresa")

    elif tipo == "Analizar reseñas y opiniones":
        comentarios = st.text_area("Pega aquí las reseñas o comentarios de clientes:", height=250)
        if st.button("Analizar opiniones", type="primary", use_container_width=True):
            if comentarios:
                if check_y_usar():
                    with st.spinner("Analizando..."):
                        r = analizar_satisfaccion_clientes(comentarios)
                    st.write(r); botones_descarga(r, "informe", nombre_base="analisis_satisfaccion")

    elif tipo == "Programa de fidelización":
        c1,c2=st.columns(2)
        with c1: emp=st.text_input("Empresa:"); sector=st.text_input("Sector:"); ticket=st.text_input("Compra media:")
        with c2: frec=st.text_input("Frecuencia de compra:"); pres=st.text_input("Presupuesto para el programa:"); obj=st.text_input("Objetivo:",value="Retener clientes y aumentar recompra")
        if st.button("Diseñar programa de fidelización", type="primary", use_container_width=True):
            if emp:
                if check_y_usar():
                    with st.spinner("Diseñando programa..."):
                        r = crear_programa_fidelizacion({"empresa":emp,"sector":sector,"ticket_medio":ticket,"frecuencia":frec,"presupuesto":pres,"objetivo":obj})
                    st.write(r); botones_descarga(r, "informe", nombre_base="programa_fidelizacion")

# ══════════════════════════════════════════════════════════════════════════════
# GESTIÓN DE EMPRESAS (ADMIN)
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Gestión de empresas":
    if not es_admin:
        st.error("No tienes permisos para acceder a esta sección.")
        st.stop()

    mostrar_admin_panel(get_supabase, perfil)

# ══════════════════════════════════════════════════════════════════════════════
# CAMBIAR PLAN A USUARIO (Admin — acceso rápido desde sidebar)
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Cambiar plan a usuario":
    if not es_admin:
        st.error("No tienes permisos para acceder a esta sección.")
        st.stop()

    from admin_panel import _cambiar_plan_usuario, PLANES

    # Header
    st.markdown("""
<div style='background:linear-gradient(135deg,#0A1E14,#0D1117);
border-radius:16px;padding:22px 28px 18px;margin-bottom:22px;
border:1px solid rgba(61,214,140,0.15);position:relative;overflow:hidden;'>
<div style='position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,rgba(61,214,140,0.4),transparent);'></div>
<div style='font-family:Sora,sans-serif;font-size:0.58rem;font-weight:700;text-transform:uppercase;
letter-spacing:0.14em;color:rgba(61,214,140,0.7);margin-bottom:8px;'>Admin · Acceso rápido</div>
<div style='font-family:Sora,sans-serif;font-size:1.3rem;font-weight:700;
color:#EAEAF0;letter-spacing:-0.03em;margin-bottom:5px;'>🎯 Cambiar plan a usuario</div>
<div style='font-size:0.82rem;color:#506060;font-family:DM Sans,sans-serif;'>
Cambia el plan de cualquier cliente al instante — sin que ellos hagan nada</div>
</div>
""", unsafe_allow_html=True)

    tip("Ideal cuando conoces a alguien en una empresa y quieres asignarle un plan distinto al que están pagando — por ejemplo darle Business a alguien que está en Pro.")

    # Formulario central
    st.markdown("""
<div style='background:var(--surface);border:1px solid var(--border);
border-radius:14px;padding:24px 28px;max-width:640px;'>
<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:700;
text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:16px;'>
Datos del cambio</div>
""", unsafe_allow_html=True)

    sb_quick = get_supabase()

    email_q = st.text_input("Email del usuario", placeholder="cliente@empresa.com", key="qp_email")

    # Mostrar plan actual si existe
    if email_q and "@" in email_q:
        try:
            res_check = sb_quick.table("usuarios").select("nombre,plan,email").eq("email", email_q).execute()
            if res_check.data:
                u = res_check.data[0]
                plan_act = u.get("plan", "gratuito")
                meta_act = PLANES.get(plan_act, PLANES["gratuito"])
                _color_act = meta_act["color"]
                _icon_act  = meta_act["icon"]
                _label_act = meta_act["label"]
                _nombre_act = u.get("nombre", "—")
                st.markdown(
                    f"<div style='background:rgba(61,214,140,0.06);border:1px solid rgba(61,214,140,0.15);"
                    f"border-radius:8px;padding:10px 14px;margin-bottom:12px;'>"
                    f"<span style='color:#3DD68C;font-size:0.82rem;'>✓ Usuario encontrado: </span>"
                    f"<span style='color:var(--text2);font-size:0.82rem;font-weight:600;'>{_nombre_act}</span>"
                    f"<span style='color:var(--text3);font-size:0.82rem;'> · Plan actual: </span>"
                    f"<span style='color:{_color_act};font-size:0.82rem;font-weight:700;'>"
                    f"{_icon_act} {_label_act}</span></div>",
                    unsafe_allow_html=True
                )
            elif len(email_q) > 5:
                st.markdown(
                    "<div style='background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.15);"
                    "border-radius:8px;padding:10px 14px;margin-bottom:12px;'>"
                    "<span style='color:#F87171;font-size:0.82rem;'>⚠ No se encontró ningún usuario con ese email</span></div>",
                    unsafe_allow_html=True
                )
        except Exception:
            pass

    plan_opciones = list(PLANES.keys())

    def _fmt_plan(x):
        lim = PLANES[x]["limite"]
        lim_str = "Sin límite" if lim is None else f"{lim} acciones/día"
        return f"{PLANES[x]['icon']} {PLANES[x]['label']} · {lim_str}"

    nuevo_plan_q = st.selectbox(
        "Nuevo plan a asignar",
        options=plan_opciones,
        format_func=lambda x: _fmt_plan(x),
        key="qp_plan"
    )

    motivo_q = st.text_area(
        "Motivo del cambio (solo visible para ti)",
        height=80,
        placeholder="Ej: Amigo en empresa cliente, socio estratégico, beta tester, contacto de networking...",
        key="qp_motivo"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # Plan info cards
    meta_nuevo = PLANES.get(nuevo_plan_q, PLANES["gratuito"])
    plan_features = {
        "demo":     ["3 acciones totales", "Solo Asistente IA", "Solo Analizar docs", "Sin guardar datos"],
        "gratuito": ["5 acciones/día", "Asistente IA", "Analizar documentos", "Guía de uso"],
        "pro":      ["Acciones ilimitadas", "Todos los módulos", "Crear documentos", "CRM · Facturación · Legal"],
        "business": ["Acciones ilimitadas", "Todo el plan Pro", "Procesar en lote", "Analítica avanzada · Informes"],
        "admin":    ["Acceso total", "Panel de administración", "Sin restricciones", "Gestión de todos los usuarios"],
    }
    features = plan_features.get(nuevo_plan_q, [])
    st.markdown(
        f"<div style='background:rgba({','.join(str(int(meta_nuevo['color'].lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.06);"
        f"border:1px solid rgba({','.join(str(int(meta_nuevo['color'].lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.18);"
        "border-radius:12px;padding:16px 20px;margin-bottom:16px;'>"
        f"<div style='font-weight:700;color:{meta_nuevo['color']};font-size:0.9rem;margin-bottom:10px;'>"
        f"{meta_nuevo['icon']} Plan {meta_nuevo['label']}</div>"
        "<div style='display:flex;flex-wrap:wrap;gap:8px;'>" +
        "".join(f"<span style='font-size:0.78rem;color:var(--text2);background:var(--surface);border:1px solid var(--border);border-radius:5px;padding:3px 10px;'>✓ {f}</span>" for f in features) +
        "</div></div>",
        unsafe_allow_html=True
    )

    if st.button("🎯 Aplicar cambio de plan", type="primary", use_container_width=True, key="btn_qp"):
        if not email_q:
            st.warning("Introduce el email del usuario.")
        else:
            _cambiar_plan_usuario(sb_quick, email_q, nuevo_plan_q)


elif modulo == "Mi cuenta":
    header("Mi cuenta", "Tu cuenta, plan activo y estadísticas de uso")
    perfil   = obtener_perfil()
    metricas = obtener_metricas_usuario()
    plan     = perfil.get("plan", "gratuito")
    from datetime import date as _d
    hoy      = str(_d.today())
    usos_hoy = perfil.get("usos_hoy", 0) if perfil.get("fecha_usos") == hoy else 0
    docs_p   = metricas.get("docs_procesados", 0)
    docs_g   = metricas.get("docs_generados", 0)
    chats    = metricas.get("chat_consultas", 0)
    props    = metricas.get("propuestas_generadas", 0)
    total    = docs_p + docs_g + chats + props

    PLAN_COL = {"gratuito":("#606070","#141520","Gratuito"),"pro":("#C9A84C","#1E1A0A","Pro ⭐"),"business":("#E8C96A","#1E1800","Business 🚀"),"admin":("#3DD68C","#0A1E14","Admin 🔑")}
    txt_c, bg_c, plan_lbl = PLAN_COL.get(plan, PLAN_COL["gratuito"])
    usos_txt = (f"{usos_hoy}/5 · renuevan mañana" if plan == "gratuito" else "Ilimitadas ✓")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "<div style='background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px 24px;'>"
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;"
            "letter-spacing:0.1em;color:var(--text3);margin-bottom:14px;'>Cuenta</div>"
            "<table style='width:100%;font-size:0.85rem;border-collapse:collapse;'>"
            f"<tr><td style='color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border);'>Email</td>"
            f"<td style='text-align:right;color:var(--text2);padding:8px 0;border-bottom:1px solid var(--border);'>{perfil.get('email','—')}</td></tr>"
            f"<tr><td style='color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border);'>Empresa</td>"
            f"<td style='text-align:right;color:var(--text);font-weight:500;padding:8px 0;border-bottom:1px solid var(--border);'>{perfil.get('nombre','—')}</td></tr>"
            f"<tr><td style='color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border);'>Plan</td>"
            f"<td style='text-align:right;padding:8px 0;border-bottom:1px solid var(--border);'>"
            f"<span style='background:{bg_c};color:{txt_c};border:1px solid {txt_c}33;border-radius:5px;"
            f"padding:2px 9px;font-size:0.72rem;font-weight:600;'>{plan_lbl}</span></td></tr>"
            f"<tr><td style='color:var(--text3);padding:8px 0;'>Acciones hoy</td>"
            f"<td style='text-align:right;color:{txt_c};font-weight:600;padding:8px 0;'>{usos_txt}</td></tr>"
            "</table></div>",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            "<div style='background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px 24px;'>"
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;"
            "letter-spacing:0.1em;color:var(--text3);margin-bottom:14px;'>Actividad total</div>"
            "<table style='width:100%;font-size:0.85rem;border-collapse:collapse;'>"
            f"<tr><td style='color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border);'>Docs analizados</td>"
            f"<td style='text-align:right;color:var(--text);font-weight:600;padding:8px 0;border-bottom:1px solid var(--border);'>{docs_p}</td></tr>"
            f"<tr><td style='color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border);'>Docs generados</td>"
            f"<td style='text-align:right;color:var(--text);font-weight:600;padding:8px 0;border-bottom:1px solid var(--border);'>{docs_g}</td></tr>"
            f"<tr><td style='color:var(--text3);padding:8px 0;border-bottom:1px solid var(--border);'>Consultas IA</td>"
            f"<td style='text-align:right;color:var(--text);font-weight:600;padding:8px 0;border-bottom:1px solid var(--border);'>{chats}</td></tr>"
            f"<tr><td style='color:var(--text3);padding:8px 0;'>Propuestas</td>"
            f"<td style='text-align:right;color:var(--text);font-weight:600;padding:8px 0;'>{props}</td></tr>"
            "</table></div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    for col, val, lbl, sub, col_rgb in [
        (s1, total,       "Acciones totales",      "Tareas completadas con IA",       "201,168,76"),
        (s2, docs_p+docs_g,"Documentos",            "Analizados y generados",          "61,214,140"),
        (s3, chats,        "Consultas IA",          "Preguntas al asistente",          "110,107,245"),
    ]:
        with col:
            col.markdown(
                f"<div style='background:rgba({col_rgb},0.07);border:1px solid rgba({col_rgb},0.18);"
                "border-radius:14px;padding:20px;text-align:center;'>"
                f"<div style='font-family:Sora,sans-serif;font-size:2rem;font-weight:700;"
                f"color:rgba({col_rgb},1);letter-spacing:-0.03em;'>{val}</div>"
                f"<div style='font-weight:600;font-size:0.82rem;color:rgba({col_rgb},0.85);margin-top:5px;'>{lbl}</div>"
                f"<div style='font-size:0.72rem;color:rgba({col_rgb},0.5);margin-top:4px;'>{sub}</div>"
                "</div>", unsafe_allow_html=True
            )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if plan == "gratuito":
        st.markdown(
            "<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.18);"
            "border-radius:14px;padding:22px 26px;'>"
            "<div style='font-family:Sora,sans-serif;font-size:1rem;font-weight:700;"
            "color:var(--gold2);margin-bottom:8px;'>Desbloquea el plan Pro</div>"
            "<div style='font-size:0.875rem;color:var(--text3);margin-bottom:12px;line-height:1.65;'>"
            "Con el <b style='color:var(--gold);'>Plan Pro (29€/mes)</b> tienes acciones ilimitadas, "
            "todos los módulos y soporte directo.</div>"
            "<div style='font-size:0.85rem;color:var(--gold);'>"
            "hello.aigrowthsystems@gmail.com</div>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='background:rgba(61,214,140,0.06);border:1px solid rgba(61,214,140,0.18);"
            "border-radius:14px;padding:18px 22px;'>"
            "<div style='font-size:0.875rem;color:var(--green);font-weight:600;'>✓ Plan activo — acciones ilimitadas</div>"
            "<div style='font-size:0.82rem;color:var(--text3);margin-top:4px;'>hello.aigrowthsystems@gmail.com</div>"
            "</div>",
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Configuración":
    header("Configuración", "Personaliza tu cuenta y ajusta las preferencias de la plataforma")

    perfil = obtener_perfil()

    tab_perfil, tab_ia, tab_plan = st.tabs(["  Perfil  ", "  Asistente IA  ", "  Plan y facturación  "])

    with tab_perfil:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Los cambios de nombre se guardan en tu perfil y se reflejan en toda la plataforma.")

        nombre_actual = perfil.get("nombre", "")
        nuevo_nombre = st.text_input("Nombre o empresa", value=nombre_actual, key="cfg_nombre",
            placeholder="Tu empresa S.L.")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:var(--surface);border:1px solid var(--border);border-radius:10px;"
            "padding:12px 16px;font-size:0.83rem;color:var(--text3);margin-bottom:12px;'>"
            "📧 <b style='color:var(--text2);'>Email:</b> " + perfil.get("email","—") +
            "<span style='margin-left:12px;font-size:0.75rem;color:var(--text3);'>"
            "(para cambiar el email contacta con soporte)</span></div>",
            unsafe_allow_html=True
        )

        if st.button("Guardar nombre", type="primary", key="btn_save_nombre"):
            if nuevo_nombre.strip():
                try:
                    uid = st.session_state["usuario"].id
                    get_supabase().table("usuarios").update({"nombre": nuevo_nombre.strip()}).eq("id", uid).execute()
                    st.success("✅ Nombre actualizado correctamente.")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.warning("El nombre no puede estar vacío.")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Cambiar contraseña</div>",
            unsafe_allow_html=True
        )
        pwd1 = st.text_input("Nueva contraseña", type="password", key="cfg_pwd1", placeholder="Mín. 6 caracteres")
        pwd2 = st.text_input("Confirmar contraseña", type="password", key="cfg_pwd2", placeholder="Repite la contraseña")
        if st.button("Cambiar contraseña", key="btn_pwd"):
            if not pwd1:
                st.warning("Escribe una nueva contraseña.")
            elif len(pwd1) < 6:
                st.warning("La contraseña debe tener al menos 6 caracteres.")
            elif pwd1 != pwd2:
                st.error("Las contraseñas no coinciden.")
            else:
                try:
                    get_supabase().auth.update_user({"password": pwd1})
                    st.success("✅ Contraseña actualizada.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab_ia:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("El contexto de empresa hace que el Asistente IA responda mucho mejor a tus preguntas. Cuanto más detallado, mejor.")

        ctx_actual = st.session_state.get("contexto_asistente", "")
        ctx_nuevo = st.text_area(
            "Descripción de tu empresa para la IA",
            value=ctx_actual,
            height=180, key="cfg_ctx",
            placeholder="Ej: Somos una agencia de marketing digital con 5 empleados en Madrid. "
                        "Nuestros servicios: SEO, SEM, redes sociales. Clientes principales: pymes de hostelería y retail. "
                        "Facturación anual: ~200.000€. Objetivo: captar 10 clientes nuevos este trimestre."
        )
        if st.button("Guardar contexto IA", type="primary", key="btn_ctx"):
            st.session_state["contexto_asistente"] = ctx_nuevo
            st.success("✅ Contexto guardado. El asistente ya lo usará en todas tus conversaciones.")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Idioma preferido de respuesta</div>",
            unsafe_allow_html=True
        )
        idioma_pref = st.selectbox("Idioma", ["Español", "English", "Français", "Deutsch", "Português"],
            key="cfg_idioma", label_visibility="collapsed")
        if st.button("Guardar idioma", key="btn_idioma"):
            st.session_state["idioma_preferido"] = idioma_pref
            st.success(f"✅ Idioma configurado: {idioma_pref}")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Tono del asistente</div>",
            unsafe_allow_html=True
        )
        tono_pref = st.radio("Tono", ["Profesional y directo", "Detallado y explicativo", "Conciso y breve"],
            key="cfg_tono", label_visibility="collapsed", horizontal=True)
        if st.button("Guardar tono", key="btn_tono"):
            st.session_state["tono_asistente"] = tono_pref
            st.success(f"✅ Tono configurado: {tono_pref}")

    with tab_plan:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        plan_actual_cfg = perfil.get("plan", "gratuito")
        PLAN_DETAILS = {
            "gratuito": {
                "nombre": "Plan Gratuito",
                "precio": "0€/mes",
                "color": "#606070",
                "funciones": ["✓ Asistente IA", "✓ Analizar documentos", "✗ Crear documentos", "✗ Traducción", "✗ Módulos de negocio", "5 acciones/día"],
            },
            "pro": {
                "nombre": "Plan Pro",
                "precio": "29€/mes",
                "color": "#C9A84C",
                "funciones": ["✓ Todo el plan gratuito", "✓ Crear documentos", "✓ Traducción", "✓ Emails, marketing, estrategia", "✓ Legal y RRHH", "✓ Acciones ilimitadas"],
            },
            "business": {
                "nombre": "Plan Business",
                "precio": "Personalizado",
                "color": "#E8C96A",
                "funciones": ["✓ Todo el plan Pro", "✓ CRM y pipeline", "✓ Facturación", "✓ Procesar en lote", "✓ Soporte prioritario", "✓ Onboarding dedicado"],
            },
        }
        det = PLAN_DETAILS.get(plan_actual_cfg, PLAN_DETAILS["gratuito"])
        c_plan = det["color"]

        st.markdown(
            f"<div style='background:var(--surface);border:1px solid {c_plan}33;"
            f"border-radius:14px;padding:22px 26px;margin-bottom:20px;'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;'>"
            f"<div style='font-family:Sora,sans-serif;font-size:1.1rem;font-weight:700;color:{c_plan};'>"
            f"{det['nombre']}</div>"
            f"<div style='font-family:Sora,sans-serif;font-size:1.4rem;font-weight:800;color:var(--text);'>"
            f"{det['precio']}</div></div>"
            "<div style='display:flex;flex-wrap:wrap;gap:8px;'>" +
            "".join(
                f"<span style='font-size:0.8rem;color:{'var(--text2)' if f.startswith('✓') else 'var(--text3)'};'>{f}</span>"
                for f in det["funciones"]
            ) +
            "</div></div>",
            unsafe_allow_html=True
        )

        if plan_actual_cfg == "gratuito":
            st.markdown(
                "<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);"
                "border-radius:14px;padding:22px 26px;'>"
                "<div style='font-family:Sora,sans-serif;font-size:0.95rem;font-weight:700;"
                "color:var(--gold2);margin-bottom:10px;'>Actualizar a Pro — 29€/mes</div>"
                "<div style='font-size:0.85rem;color:var(--text3);line-height:1.65;margin-bottom:14px;'>"
                "Acciones ilimitadas, todos los módulos desbloqueados y soporte directo.<br>"
                "La mayoría recuperan la inversión en el primer documento generado.</div>"
                "<div style='font-size:0.875rem;font-weight:600;color:var(--gold);'>"
                "📩 hello.aigrowthsystems@gmail.com</div>"
                "</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='background:rgba(61,214,140,0.06);border:1px solid rgba(61,214,140,0.15);"
                "border-radius:12px;padding:16px 20px;'>"
                "<div style='font-size:0.875rem;color:var(--green);font-weight:600;'>✓ Plan activo</div>"
                "<div style='font-size:0.82rem;color:var(--text3);margin-top:4px;'>"
                "¿Necesitas cambiar tu plan? Escríbenos a hello.aigrowthsystems@gmail.com</div>"
                "</div>",
                unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════════════════════════
# DATOS EMPRESA
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Datos empresa":
    header("Datos de empresa", "Resumen ejecutivo de tu actividad, clientes, documentos y métricas clave")

    perfil   = obtener_perfil()
    metricas = obtener_metricas_usuario()
    from datetime import date as _d2

    docs_p = metricas.get("docs_procesados", 0)
    docs_g = metricas.get("docs_generados", 0)
    chats  = metricas.get("chat_consultas", 0)
    props  = metricas.get("propuestas_generadas", 0)
    batch  = metricas.get("batch_procesados", 0)
    total  = docs_p + docs_g + chats + props + batch

    # KPI row
    k1, k2, k3, k4, k5 = st.columns(5)
    for col, val, lbl in [
        (k1, docs_p, "Docs analizados"),
        (k2, docs_g, "Docs generados"),
        (k3, chats,  "Consultas IA"),
        (k4, props,  "Propuestas"),
        (k5, batch,  "Lotes procesados"),
    ]:
        col.metric(lbl, val)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    tab_resumen, tab_clientes, tab_docs, tab_actividad = st.tabs([
        "  Resumen  ", "  Clientes CRM  ", "  Documentos  ", "  Actividad  "
    ])

    with tab_resumen:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        ctx = st.session_state.get("contexto_asistente", "")
        if ctx:
            st.markdown(
                "<div style='background:var(--surface);border:1px solid var(--border);"
                "border-radius:12px;padding:18px 22px;margin-bottom:16px;'>"
                "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
                "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:8px;'>"
                "Perfil de empresa configurado</div>"
                f"<div style='font-size:0.875rem;color:var(--text2);line-height:1.65;'>{ctx}</div>"
                "</div>",
                unsafe_allow_html=True
            )
        else:
            tip("Configura el perfil de tu empresa en Configuración → Asistente IA para que aparezca aquí.")

        # Usage breakdown
        st.markdown(
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin:16px 0 10px;'>"
            "Desglose de uso</div>",
            unsafe_allow_html=True
        )
        desglose = [
            ("📄 Documentos analizados", docs_p, total),
            ("✍️ Documentos generados",  docs_g, total),
            ("🤖 Consultas al asistente",chats,  total),
            ("🚀 Propuestas generadas",  props,  total),
            ("📦 Lotes procesados",      batch,  total),
        ]
        for lbl, val, tot in desglose:
            pct = round((val / tot * 100) if tot > 0 else 0)
            st.markdown(
                f"<div style='margin-bottom:10px;'>"
                f"<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>"
                f"<span style='font-size:0.82rem;color:var(--text2);'>{lbl}</span>"
                f"<span style='font-size:0.82rem;color:var(--text3);font-weight:600;'>{val} &nbsp;·&nbsp; {pct}%</span>"
                f"</div>"
                f"<div style='background:var(--border);border-radius:3px;height:4px;overflow:hidden;'>"
                f"<div style='background:rgba(201,168,76,0.7);width:{pct}%;height:100%;border-radius:3px;"
                f"transition:width 0.4s ease;'></div></div></div>",
                unsafe_allow_html=True
            )

    with tab_clientes:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        contactos = st.session_state.get("crm_contactos", [])
        opps      = st.session_state.get("crm_oportunidades", [])

        if contactos:
            st.markdown(f"<div style='font-size:0.82rem;color:var(--text3);margin-bottom:10px;'>{len(contactos)} contactos registrados</div>", unsafe_allow_html=True)
            df_c = pd.DataFrame(contactos)
            cols_show = [col for col in ["nombre","empresa","email","telefono","fecha"] if col in df_c.columns]
            st.dataframe(df_c[cols_show], use_container_width=True, hide_index=True)
            buf = BytesIO(); df_c.to_excel(buf, index=False); buf.seek(0)
            st.download_button("⬇ Exportar contactos Excel", data=buf,
                file_name="contactos.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary")
        else:
            st.markdown(
                "<div style='text-align:center;padding:40px 20px;border:1px dashed var(--border2);"
                "border-radius:12px;color:var(--text3);font-size:0.875rem;'>"
                "No hay contactos en el CRM.<br>"
                "<span style='font-size:0.8rem;color:var(--text3);'>Ve a Clientes y pipeline para añadirlos.</span>"
                "</div>", unsafe_allow_html=True
            )

        if opps:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            df_op = pd.DataFrame(opps)
            total_pipe = df_op["valor"].sum() if "valor" in df_op else 0
            ganadas    = df_op[df_op["estado"]=="Ganado"]["valor"].sum() if "estado" in df_op else 0
            p1, p2, p3 = st.columns(3)
            p1.metric("Pipeline total", f"{total_pipe:,.0f}€")
            p2.metric("Ganadas", f"{ganadas:,.0f}€")
            p3.metric("Oportunidades", len(df_op))
            cols_op = [col for col in ["empresa","valor","estado","fecha_cierre"] if col in df_op.columns]
            st.dataframe(df_op[cols_op], use_container_width=True, hide_index=True)

    with tab_docs:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Aquí se registran automáticamente los documentos que generas o analizas con la plataforma.")

        c1, c2, c3 = st.columns(3)
        c1.metric("Analizados", docs_p)
        c2.metric("Generados", docs_g)
        c3.metric("Total", docs_p + docs_g)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if docs_g > 0 or docs_p > 0:
            import plotly.express as px
            fig = px.bar(
                x=["Analizados", "Generados", "Propuestas", "Lotes"],
                y=[docs_p, docs_g, props, batch],
                color_discrete_sequence=["#C9A84C"],
                labels={"x": "", "y": "Cantidad"},
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_family="DM Sans", font_color="#9090A8",
                margin=dict(l=0,r=0,t=10,b=0), height=220,
                showlegend=False,
            )
            fig.update_traces(marker_line_width=0)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="#1E1F2E", gridwidth=1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                "<div style='text-align:center;padding:32px;border:1px dashed var(--border2);"
                "border-radius:12px;color:var(--text3);font-size:0.875rem;'>"
                "Todavía no hay documentos registrados.<br>"
                "<span style='font-size:0.8rem;'>Empieza a usar los módulos para ver datos aquí.</span>"
                "</div>", unsafe_allow_html=True
            )

    with tab_actividad:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        from datetime import date as _d3

        plan_cfg = perfil.get("plan", "gratuito")
        hoy_str  = str(_d3.today())
        usos_h   = perfil.get("usos_hoy", 0) if perfil.get("fecha_usos") == hoy_str else 0

        PLAN_META2 = {"gratuito":("#606070","Gratuito","5/día"),"pro":("#C9A84C","Pro ⭐","Ilimitadas"),"business":("#E8C96A","Business 🚀","Ilimitadas"),"admin":("#3DD68C","Admin","Ilimitadas")}
        pc, pn, plim = PLAN_META2.get(plan_cfg, PLAN_META2["gratuito"])

        st.markdown(
            "<div style='background:var(--surface);border:1px solid var(--border);"
            "border-radius:14px;padding:20px 24px;margin-bottom:16px;'>"
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:14px;'>Estado de la cuenta</div>"
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:16px;'>"
            f"<div><div style='font-size:0.72rem;color:var(--text3);margin-bottom:3px;'>Plan activo</div>"
            f"<div style='font-weight:600;font-size:0.95rem;color:{pc};'>{pn}</div></div>"
            f"<div><div style='font-size:0.72rem;color:var(--text3);margin-bottom:3px;'>Límite diario</div>"
            f"<div style='font-weight:600;font-size:0.95rem;color:var(--text);'>{plim}</div></div>"
            f"<div><div style='font-size:0.72rem;color:var(--text3);margin-bottom:3px;'>Acciones hoy</div>"
            f"<div style='font-weight:600;font-size:0.95rem;color:var(--text);'>{usos_h}</div></div>"
            f"<div><div style='font-size:0.72rem;color:var(--text3);margin-bottom:3px;'>Total histórico</div>"
            f"<div style='font-weight:600;font-size:0.95rem;color:var(--text);'>{total}</div></div>"
            "</div></div>",
            unsafe_allow_html=True
        )

        # Module usage breakdown
        st.markdown(
            "<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;"
            "text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>"
            "Uso por módulo</div>",
            unsafe_allow_html=True
        )
        modulos_uso = [
            ("Asistente IA / Chat", chats),
            ("Análisis de documentos", docs_p),
            ("Generación de documentos", docs_g),
            ("Propuestas comerciales", props),
            ("Procesamiento en lote", batch),
        ]
        max_val = max((v for _, v in modulos_uso), default=1) or 1
        for nm_uso, val_uso in modulos_uso:
            pct_uso = round(val_uso / max_val * 100)
            st.markdown(
                f"<div style='display:flex;align-items:center;gap:12px;margin-bottom:10px;'>"
                f"<div style='width:160px;font-size:0.8rem;color:var(--text2);flex-shrink:0;'>{nm_uso}</div>"
                f"<div style='flex:1;background:var(--border);border-radius:3px;height:6px;'>"
                f"<div style='background:rgba(201,168,76,0.6);width:{pct_uso}%;height:100%;"
                f"border-radius:3px;'></div></div>"
                f"<div style='width:28px;text-align:right;font-size:0.8rem;color:var(--text3);font-weight:600;'>{val_uso}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════════════════════════
# GENERADOR EXCEL IA
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Generador Excel IA":
    if _bloquear_si_sin_acceso("Generador Excel IA"): st.stop()
    header("Generador Excel IA", "Describe qué tabla o análisis necesitas y la IA lo crea y exporta como Excel")

    tab_gen, tab_analizar, tab_plantillas = st.tabs(["  Crear Excel  ", "  Analizar y enriquecer  ", "  Plantillas  "])

    with tab_gen:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Describe la tabla que necesitas en lenguaje natural. La IA la genera lista para descargar.")

        descripcion_excel = st.text_area(
            "¿Qué Excel necesitas?",
            height=120, key="excel_desc",
            placeholder="Ej: Una tabla de previsión de ventas para 12 meses con columnas: mes, objetivo, real, % desviación, acumulado. Con datos de ejemplo para una empresa de consultoría.\n\nOtro ejemplo: Comparativa de 5 proveedores con columnas precio, calidad (1-10), plazo entrega, valoración total."
        )
        c1, c2 = st.columns(2)
        with c1:
            n_filas = st.number_input("Filas de datos de ejemplo", min_value=3, max_value=50, value=12)
        with c2:
            incluir_formulas = st.checkbox("Incluir fórmulas y totales", value=True)

        if st.button("🤖 Generar Excel con IA", type="primary", use_container_width=True, key="btn_gen_excel"):
            if not descripcion_excel.strip():
                st.warning("Describe qué Excel quieres generar.")
            elif check_y_usar():
                with st.spinner("Generando estructura con IA..."):
                    prompt = f"""Genera datos para un Excel con esta descripción: {descripcion_excel}
Genera exactamente {n_filas} filas de datos realistas y relevantes.
{"Incluye una fila de totales/resumen al final." if incluir_formulas else ""}

Responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
{{
  "titulo": "Nombre del Excel",
  "columnas": ["col1", "col2", ...],
  "datos": [
    {{"col1": valor, "col2": valor, ...}},
    ...
  ],
  "resumen": "Breve descripción de qué contiene"
}}

Sin markdown, sin explicaciones, solo el JSON."""
                    try:
                        raw = groq_call(prompt, max_tokens=3000)
                        raw_clean = re.sub(r"```json|```", "", raw).strip()
                        resultado_json = json.loads(raw_clean)

                        columnas = resultado_json.get("columnas", [])
                        datos    = resultado_json.get("datos", [])
                        titulo   = resultado_json.get("titulo", "datos_ia")
                        resumen  = resultado_json.get("resumen", "")

                        df = pd.DataFrame(datos, columns=columnas)
                        st.success(f"✅ **{titulo}** — {len(df)} filas × {len(df.columns)} columnas")
                        if resumen:
                            st.markdown(f"<div class='tip-box'><span>📊</span><span>{resumen}</span></div>", unsafe_allow_html=True)
                        st.dataframe(df, use_container_width=True, hide_index=True)

                        # Export to Excel with formatting
                        buf = BytesIO()
                        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                            df.to_excel(writer, index=False, sheet_name=titulo[:31])
                        buf.seek(0)
                        st.download_button(
                            f"⬇ Descargar {titulo}.xlsx",
                            data=buf,
                            file_name=f"{titulo.replace(' ','_')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary", use_container_width=True
                        )
                        registrar_accion("doc_generado")

                        # Auto chart if numeric columns exist
                        numericas = df.select_dtypes(include="number").columns.tolist()
                        if numericas and len(df) > 1:
                            import plotly.express as px
                            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                            st.markdown("<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:10px;'>Visualización automática</div>", unsafe_allow_html=True)
                            col_y = st.selectbox("Columna a visualizar:", numericas, key="excel_viz")
                            col_x_opts = [c for c in df.columns if c != col_y]
                            if col_x_opts:
                                col_x = col_x_opts[0]
                                fig = px.bar(df, x=col_x, y=col_y, template="plotly_dark",
                                    color_discrete_sequence=["#C9A84C"])
                                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                    font_family="DM Sans", font_color="#9090A8",
                                    margin=dict(l=0,r=0,t=10,b=0), height=280)
                                fig.update_xaxes(showgrid=False)
                                fig.update_yaxes(gridcolor="#1E1F2E")
                                st.plotly_chart(fig, use_container_width=True)
                    except (json.JSONDecodeError, KeyError) as e:
                        st.error(f"Error al procesar el JSON: {e}")
                        st.text_area("Respuesta raw:", raw, height=200)

    with tab_analizar:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Sube un Excel existente y la IA lo analiza, añade columnas calculadas y genera insights.")

        archivo_xl = st.file_uploader("Sube tu Excel o CSV", type=["xlsx","xls","csv"], key="xl_upload")
        if archivo_xl:
            try:
                ext = archivo_xl.name.split(".")[-1]
                df_up = pd.read_csv(archivo_xl) if ext == "csv" else pd.read_excel(archivo_xl)
                st.success(f"✅ {len(df_up)} filas × {len(df_up.columns)} columnas")
                st.dataframe(df_up.head(8), use_container_width=True, hide_index=True)

                instruccion_xl = st.text_area(
                    "¿Qué quieres hacer con este Excel?",
                    height=100, key="xl_inst",
                    placeholder="Ej: Añade una columna de rentabilidad (%), calcula el total por categoría, detecta los 3 mejores y peores registros, o genera un resumen ejecutivo de los datos."
                )
                if st.button("Analizar y enriquecer con IA", type="primary", use_container_width=True, key="btn_xl_analyze"):
                    if check_y_usar():
                        with st.spinner("Analizando..."):
                            resumen_datos = f"Columnas: {list(df_up.columns)}\nFilas: {len(df_up)}\nPrimeras filas:\n{df_up.head(10).to_string()}\nEstadísticas:\n{df_up.describe().to_string()}"
                            r = analizar_datos_empresa(resumen_datos + f"\n\nInstrucción específica: {instruccion_xl}", "ejecutivo")
                        st.markdown(r)
                        botones_descarga(r, "informe", nombre_base="analisis_excel")
                        registrar_accion("doc_procesado")

                # Auto visualization
                numericas_up = df_up.select_dtypes(include="number").columns.tolist()
                if numericas_up:
                    import plotly.express as px
                    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:10px;'>Visualizar datos</div>", unsafe_allow_html=True)
                    v1, v2, v3 = st.columns(3)
                    tipo_chart = v1.selectbox("Tipo de gráfico:", ["Barras","Línea","Área","Dispersión","Pie"], key="xl_chart_type")
                    eje_y = v2.selectbox("Eje Y (valor):", numericas_up, key="xl_y")
                    otras_cols = [c for c in df_up.columns if c != eje_y]
                    eje_x = v3.selectbox("Eje X (categoría):", otras_cols, key="xl_x") if otras_cols else eje_y

                    chart_map = {
                        "Barras": lambda: px.bar(df_up, x=eje_x, y=eje_y, template="plotly_dark", color_discrete_sequence=["#C9A84C"]),
                        "Línea": lambda: px.line(df_up, x=eje_x, y=eje_y, template="plotly_dark", color_discrete_sequence=["#C9A84C"]),
                        "Área": lambda: px.area(df_up, x=eje_x, y=eje_y, template="plotly_dark", color_discrete_sequence=["#C9A84C"]),
                        "Dispersión": lambda: px.scatter(df_up, x=eje_x, y=eje_y, template="plotly_dark", color_discrete_sequence=["#C9A84C"]),
                        "Pie": lambda: px.pie(df_up, names=eje_x, values=eje_y, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma),
                    }
                    fig = chart_map[tipo_chart]()
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_family="DM Sans", font_color="#9090A8",
                        margin=dict(l=0,r=0,t=20,b=0), height=350)
                    fig.update_xaxes(showgrid=False)
                    fig.update_yaxes(gridcolor="#1E1F2E")
                    st.plotly_chart(fig, use_container_width=True)

                    # Download chart as image hint
                    st.markdown("<div style='font-size:0.75rem;color:var(--text3);'>💡 Haz clic en el gráfico y usa el icono de cámara para descargarlo como imagen PNG.</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    with tab_plantillas:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        plantillas_excel = {
            "Previsión de ventas 12 meses": "Una tabla de previsión de ventas mensual con columnas: Mes, Objetivo ventas (€), Ventas reales (€), % Cumplimiento, Acumulado objetivo, Acumulado real. Incluir datos de ejemplo para empresa de servicios con estacionalidad.",
            "Análisis de rentabilidad por cliente": "Tabla con 15 clientes ficticios: Cliente, Sector, Ingresos anuales (€), Costes servicio (€), Margen bruto (€), % Margen, Horas dedicadas, Rentabilidad/hora (€), Clasificación (A/B/C).",
            "Presupuesto departamental anual": "Presupuesto anual para departamento de marketing con categorías: Personal, Software/Herramientas, Publicidad, Eventos, Formación, Varios. Columnas: Categoría, Q1, Q2, Q3, Q4, Total anual, % sobre total.",
            "Pipeline de ventas CRM": "Pipeline de 20 oportunidades: Empresa, Contacto, Sector, Valor estimado (€), Probabilidad %, Valor ponderado, Etapa (Prospecto/Contactado/Propuesta/Negociación/Cierre), Fecha cierre estimada.",
            "KPIs empresariales mensuales": "Dashboard de KPIs para 12 meses: MRR, Clientes activos, Churn rate %, NPS, Tickets soporte, Tiempo resolución (h), CAC, LTV, Margen operativo %.",
            "Comparativa de proveedores": "Evaluación de 8 proveedores con criterios: Precio unitario, Calidad (1-10), Plazo entrega (días), Fiabilidad (1-10), Condiciones pago, Valoración total ponderada, Recomendación (Sí/No).",
        }
        cols_plant = st.columns(2)
        for i, (nombre_p, desc_p) in enumerate(plantillas_excel.items()):
            with cols_plant[i % 2]:
                st.markdown(
                    f"<div style='background:var(--surface);border:1px solid var(--border);border-radius:12px;"
                    f"padding:16px 18px;margin-bottom:8px;'>"
                    f"<div style='font-family:Sora,sans-serif;font-weight:600;font-size:0.85rem;"
                    f"color:var(--text);margin-bottom:6px;'>{nombre_p}</div>"
                    f"<div style='font-size:0.75rem;color:var(--text3);line-height:1.5;'>{desc_p[:100]}...</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if st.button(f"Generar → {nombre_p}", key=f"plant_{i}", use_container_width=True, type="primary"):
                    st.session_state["excel_desc"] = desc_p
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PRESENTACIONES IA
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Presentaciones IA":
    if _bloquear_si_sin_acceso("Presentaciones IA"): st.stop()
    header("Presentaciones IA", "Genera el contenido completo de una presentación profesional lista para usar")

    tab_nueva, tab_mejorar = st.tabs(["  Nueva presentación  ", "  Mejorar existente  "])

    with tab_nueva:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("La IA genera el guión completo slide a slide. Copia el contenido a PowerPoint, Google Slides o Canva.")

        c1, c2 = st.columns(2)
        with c1:
            tema_pres = st.text_input("Tema de la presentación", key="pres_tema",
                placeholder="Ej: Resultados Q3 2025, Propuesta comercial para cliente X, Plan de negocio...")
            audiencia_pres = st.text_input("Audiencia", key="pres_aud",
                placeholder="Ej: Inversores, Equipo directivo, Clientes potenciales...")
            objetivo_pres = st.text_input("Objetivo principal", key="pres_obj",
                placeholder="Ej: Conseguir financiación, Cerrar venta, Informar resultados...")
        with c2:
            n_slides = st.slider("Número de slides", min_value=5, max_value=20, value=10, key="pres_slides")
            tono_pres = st.selectbox("Tono", ["Ejecutivo y formal", "Dinámico y comercial", "Técnico y detallado", "Inspiracional"], key="pres_tono")
            datos_pres = st.text_area("Datos/información disponible (opcional)", height=100, key="pres_datos",
                placeholder="Ventas Q3: 180k€, +23% vs Q2. Nuevos clientes: 12. NPS: 72...")

        if st.button("🎯 Generar presentación completa", type="primary", use_container_width=True, key="btn_gen_pres"):
            if not tema_pres or not audiencia_pres:
                st.warning("Rellena al menos el tema y la audiencia.")
            elif check_y_usar():
                with st.spinner("Creando presentación..."):
                    prompt_pres = f"""Crea una presentación profesional completa de {n_slides} slides.

Tema: {tema_pres}
Audiencia: {audiencia_pres}
Objetivo: {objetivo_pres}
Tono: {tono_pres}
Datos disponibles: {datos_pres or "usar datos de ejemplo relevantes"}

Para CADA slide escribe:
## SLIDE [N]: [TÍTULO EN MAYÚSCULAS]
**Mensaje clave:** (una frase que resume el slide)
**Contenido principal:**
(bullets, datos, texto — todo lo que iría en el slide)
**Notas del presentador:** (qué decir en voz alta, 2-3 frases)
**Elemento visual sugerido:** (gráfico, imagen, tabla, icono)
---

Crea los {n_slides} slides completos. Sé concreto y persuasivo. Incluye datos reales o ejemplos."""

                    r = groq_call(prompt_pres, max_tokens=4000)

                st.markdown(r)
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

                # Export options
                c1e, c2e, c3e = st.columns(3)
                with c1e:
                    st.download_button("⬇ Descargar guión (.txt)", data=r,
                        file_name=f"presentacion_{tema_pres[:20].replace(' ','_')}.txt",
                        mime="text/plain", type="primary", use_container_width=True)
                with c2e:
                    pdf_pres = exportar_pdf(r, tipo_doc="presentación", metadata={"empresa": tema_pres})
                    st.download_button("⬇ Descargar PDF", data=pdf_pres,
                        file_name=f"presentacion_{tema_pres[:20].replace(' ','_')}.pdf",
                        mime="application/pdf", use_container_width=True)
                with c3e:
                    docx_pres = exportar_docx(r, tipo_doc="presentación", metadata={"empresa": tema_pres})
                    st.download_button("⬇ Descargar Word", data=docx_pres,
                        file_name=f"presentacion_{tema_pres[:20].replace(' ','_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True)
                registrar_accion("doc_generado")

    with tab_mejorar:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Pega el contenido de tu presentación actual y la IA la mejora, refuerza los mensajes y añade datos.")
        contenido_actual = st.text_area("Pega el contenido de tu presentación actual:", height=250, key="pres_actual",
            placeholder="Slide 1: Título...\nSlide 2: Problema...\n...")
        instruccion_mejora = st.text_input("¿Qué mejorar específicamente?", key="pres_mejora_inst",
            placeholder="Hazla más persuasiva, añade datos de mercado, simplifica el mensaje...")
        if st.button("Mejorar presentación", type="primary", use_container_width=True, key="btn_mejorar_pres"):
            if contenido_actual:
                if check_y_usar():
                    with st.spinner("Mejorando..."):
                        r = groq_call(f"Mejora esta presentación: {instruccion_mejora}\n\nCONTENIDO ACTUAL:\n{contenido_actual}", 3000)
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base="presentacion_mejorada")
                    registrar_accion("doc_generado")

# ══════════════════════════════════════════════════════════════════════════════
# ANALÍTICA VISUAL
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Analítica visual":
    if _bloquear_si_sin_acceso("Analítica visual"): st.stop()
    header("Analítica visual", "Sube cualquier dataset y obtén dashboards, gráficos y análisis automáticos con IA")

    archivo_av = st.file_uploader("Sube tu Excel o CSV", type=["xlsx","xls","csv"], key="av_file")

    if not archivo_av:
        st.markdown(
            "<div style='text-align:center;padding:60px 20px;border:1.5px dashed var(--border2);"
            "border-radius:14px;'>"
            "<div style='font-size:2.5rem;margin-bottom:12px;'>📊</div>"
            "<div style='font-family:Sora,sans-serif;font-weight:600;font-size:1rem;color:var(--text);margin-bottom:8px;'>"
            "Sube un Excel o CSV para empezar</div>"
            "<div style='font-size:0.85rem;color:var(--text3);'>"
            "Ventas, clientes, gastos, cualquier dataset — la IA lo analiza automáticamente</div>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        try:
            import plotly.express as px
            import plotly.graph_objects as go

            ext_av = archivo_av.name.split(".")[-1]
            df_av = pd.read_csv(archivo_av) if ext_av == "csv" else pd.read_excel(archivo_av)
            df_av.columns = [str(c).strip() for c in df_av.columns]

            num_cols  = df_av.select_dtypes(include="number").columns.tolist()
            cat_cols  = df_av.select_dtypes(include=["object","category"]).columns.tolist()
            date_cols = [c for c in df_av.columns if any(x in c.lower() for x in ["fecha","date","mes","año","year","month"])]

            # Summary banner
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Filas", len(df_av))
            c2.metric("Columnas", len(df_av.columns))
            c3.metric("Numéricas", len(num_cols))
            c4.metric("Categorías", len(cat_cols))

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            tab_vista, tab_charts, tab_ia, tab_export = st.tabs([
                "  Vista general  ", "  Gráficos  ", "  Análisis IA  ", "  Exportar  "
            ])

            with tab_vista:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.dataframe(df_av, use_container_width=True, hide_index=True)
                if num_cols:
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                    st.markdown("<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:10px;'>Estadísticas descriptivas</div>", unsafe_allow_html=True)
                    st.dataframe(df_av[num_cols].describe().round(2), use_container_width=True)

            with tab_charts:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

                GOLD_PALETTE = ["#C9A84C","#E8C96A","#A67C35","#F5E196","#7A5C1E","#FFD700"]

                # Auto-generate 3 automatic charts
                if num_cols and cat_cols:
                    st.markdown("<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Gráficos automáticos</div>", unsafe_allow_html=True)

                    ca1, ca2 = st.columns(2)
                    with ca1:
                        # Bar chart: top category by first numeric
                        try:
                            df_bar = df_av.groupby(cat_cols[0])[num_cols[0]].sum().reset_index().nlargest(10, num_cols[0])
                            fig_bar = px.bar(df_bar, x=cat_cols[0], y=num_cols[0],
                                title=f"{num_cols[0]} por {cat_cols[0]}",
                                template="plotly_dark", color_discrete_sequence=GOLD_PALETTE)
                            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font_family="DM Sans", font_color="#9090A8",
                                title_font_color="#EAEAF0", margin=dict(l=0,r=0,t=40,b=0), height=300)
                            fig_bar.update_xaxes(showgrid=False)
                            fig_bar.update_yaxes(gridcolor="#1E1F2E")
                            st.plotly_chart(fig_bar, use_container_width=True)
                        except: pass

                    with ca2:
                        # Pie chart
                        try:
                            df_pie = df_av.groupby(cat_cols[0])[num_cols[0]].sum().reset_index().nlargest(8, num_cols[0])
                            fig_pie = px.pie(df_pie, names=cat_cols[0], values=num_cols[0],
                                title=f"Distribución de {num_cols[0]}",
                                template="plotly_dark", color_discrete_sequence=GOLD_PALETTE)
                            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                                font_family="DM Sans", font_color="#9090A8",
                                title_font_color="#EAEAF0", margin=dict(l=0,r=0,t=40,b=0), height=300)
                            st.plotly_chart(fig_pie, use_container_width=True)
                        except: pass

                if len(num_cols) >= 2:
                    try:
                        fig_scatter = px.scatter(df_av, x=num_cols[0], y=num_cols[1],
                            title=f"Correlación: {num_cols[0]} vs {num_cols[1]}",
                            template="plotly_dark", color_discrete_sequence=["#C9A84C"])
                        fig_scatter.update_traces(marker_size=8, marker_opacity=0.8)
                        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font_family="DM Sans", font_color="#9090A8",
                            title_font_color="#EAEAF0", margin=dict(l=0,r=0,t=40,b=0), height=300)
                        fig_scatter.update_xaxes(showgrid=False)
                        fig_scatter.update_yaxes(gridcolor="#1E1F2E")
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    except: pass

                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                st.markdown("<div style='font-family:Sora,sans-serif;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:12px;'>Gráfico personalizado</div>", unsafe_allow_html=True)

                cc1, cc2, cc3, cc4 = st.columns(4)
                tipo_av   = cc1.selectbox("Tipo", ["Barras","Línea","Área","Dispersión","Histograma","Box","Pie"], key="av_tipo")
                eje_x_av  = cc2.selectbox("Eje X", df_av.columns.tolist(), key="av_x")
                eje_y_av  = cc3.selectbox("Eje Y", num_cols if num_cols else df_av.columns.tolist(), key="av_y")
                color_av  = cc4.selectbox("Color por", ["(ninguno)"] + cat_cols, key="av_color")
                color_col = None if color_av == "(ninguno)" else color_av

                chart_fns = {
                    "Barras":     lambda: px.bar(df_av, x=eje_x_av, y=eje_y_av, color=color_col, template="plotly_dark", color_discrete_sequence=GOLD_PALETTE),
                    "Línea":      lambda: px.line(df_av, x=eje_x_av, y=eje_y_av, color=color_col, template="plotly_dark", color_discrete_sequence=GOLD_PALETTE),
                    "Área":       lambda: px.area(df_av, x=eje_x_av, y=eje_y_av, color=color_col, template="plotly_dark", color_discrete_sequence=GOLD_PALETTE),
                    "Dispersión": lambda: px.scatter(df_av, x=eje_x_av, y=eje_y_av, color=color_col, template="plotly_dark", color_discrete_sequence=GOLD_PALETTE),
                    "Histograma": lambda: px.histogram(df_av, x=eje_x_av, template="plotly_dark", color_discrete_sequence=["#C9A84C"]),
                    "Box":        lambda: px.box(df_av, x=color_col, y=eje_y_av, template="plotly_dark", color_discrete_sequence=GOLD_PALETTE),
                    "Pie":        lambda: px.pie(df_av, names=eje_x_av, values=eje_y_av, template="plotly_dark", color_discrete_sequence=GOLD_PALETTE),
                }
                try:
                    fig_custom = chart_fns[tipo_av]()
                    fig_custom.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font_family="DM Sans", font_color="#9090A8",
                        margin=dict(l=0,r=0,t=20,b=0), height=380)
                    if tipo_av not in ("Pie", "Histograma"):
                        fig_custom.update_xaxes(showgrid=False)
                        fig_custom.update_yaxes(gridcolor="#1E1F2E")
                    st.plotly_chart(fig_custom, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al generar gráfico: {e}")

            with tab_ia:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                tipo_analisis_av = st.radio("Tipo de análisis:",
                    ["Resumen ejecutivo", "Tendencias y patrones", "Anomalías y alertas", "Recomendaciones de negocio", "Previsiones 3 meses"],
                    horizontal=True, key="av_tipo_analisis")

                if st.button("🤖 Analizar con IA", type="primary", use_container_width=True, key="btn_av_ia"):
                    if check_y_usar():
                        with st.spinner("Analizando dataset con IA..."):
                            resumen_av = (
                                f"Dataset: {archivo_av.name}\n"
                                f"Filas: {len(df_av)}, Columnas: {list(df_av.columns)}\n"
                                f"Columnas numéricas: {num_cols}\n"
                                f"Columnas categóricas: {cat_cols}\n\n"
                                f"Estadísticas:\n{df_av.describe().to_string()}\n\n"
                                f"Primeras 15 filas:\n{df_av.head(15).to_string()}"
                            )
                            tipo_map = {
                                "Resumen ejecutivo": "ejecutivo",
                                "Tendencias y patrones": "tendencias",
                                "Anomalías y alertas": "anomalias",
                                "Recomendaciones de negocio": "recomendaciones",
                                "Previsiones 3 meses": "previsiones",
                            }
                            r_av = analizar_datos_empresa(resumen_av, tipo_map[tipo_analisis_av])
                        st.markdown(r_av)
                        botones_descarga(r_av, "informe", nombre_base=f"analisis_{tipo_analisis_av.replace(' ','_')}")
                        registrar_accion("doc_procesado")

            with tab_export:
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                tip("Exporta el dataset procesado o las estadísticas en distintos formatos.")
                e1, e2, e3 = st.columns(3)
                with e1:
                    buf_xl = BytesIO(); df_av.to_excel(buf_xl, index=False); buf_xl.seek(0)
                    st.download_button("⬇ Excel original", data=buf_xl,
                        file_name=archivo_av.name.replace(".csv",".xlsx"),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary", use_container_width=True)
                with e2:
                    csv_data = df_av.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇ CSV", data=csv_data,
                        file_name=archivo_av.name.replace(".xlsx",".csv"),
                        mime="text/csv", use_container_width=True)
                with e3:
                    if num_cols:
                        buf_stats = BytesIO()
                        df_av.describe().round(2).to_excel(buf_stats); buf_stats.seek(0)
                        st.download_button("⬇ Estadísticas Excel", data=buf_stats,
                            file_name="estadisticas.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# CREAR WEB CON IA
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Crear web con IA":
    if _bloquear_si_sin_acceso("Crear web con IA"): st.stop()
    header("Crear web con IA", "Genera páginas web completas, landing pages y código HTML listo para publicar")

    tab_landing, tab_corporativa, tab_ecommerce = st.tabs(["  Landing Page  ", "  Web corporativa  ", "  Ficha de producto  "])

    with tab_landing:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("La IA genera una landing page completa con HTML+CSS profesional. Descárgala y publícala directamente.")
        c1, c2 = st.columns(2)
        with c1:
            empresa_web = st.text_input("Nombre de empresa/producto", key="web_emp", placeholder="Ej: Solarify")
            sector_web  = st.text_input("Sector/tipo de negocio", key="web_sec", placeholder="Ej: Software B2B, Clínica dental...")
            propuesta_web = st.text_input("Propuesta de valor principal", key="web_uvp", placeholder="Ej: Gestiona tu equipo en 5 minutos")
        with c2:
            cta_web     = st.text_input("Llamada a la acción (CTA)", key="web_cta", placeholder="Ej: Empieza gratis, Solicita demo...")
            color_web   = st.selectbox("Paleta de colores", ["Oscuro/Premium", "Claro/Profesional", "Azul/Corporativo", "Verde/Confianza", "Rojo/Energía"], key="web_color")
            extras_web  = st.multiselect("Secciones a incluir", ["Características", "Precios", "Testimonios", "FAQ", "Equipo", "Blog preview", "CTA final"], default=["Características","Precios","CTA final"], key="web_extras")

        if st.button("🌐 Generar landing page", type="primary", use_container_width=True, key="btn_web_landing"):
            if empresa_web and propuesta_web:
                if check_y_usar():
                    with st.spinner("Generando página web..."):
                        secciones = ", ".join(extras_web) if extras_web else "Características, Precios, CTA"
                        prompt_web = f"""Crea una landing page completa en HTML con CSS embebido para:
Empresa: {empresa_web} | Sector: {sector_web} | Propuesta de valor: {propuesta_web}
CTA principal: {cta_web or "Empieza ahora"} | Paleta: {color_web}
Secciones: Hero, {secciones}

REQUISITOS:
- HTML5 completo y válido con CSS embebido en <style>
- Diseño moderno, profesional y responsive (mobile-first)
- Tipografía de Google Fonts
- Gradientes y sombras sutiles
- Animaciones CSS suaves en hover
- Paleta {color_web}: usa colores coherentes y profesionales
- Todo el texto en español
- Listo para publicar sin modificaciones
- Incluye meta tags SEO

Devuelve SOLO el código HTML completo, sin explicaciones."""
                        html_generado = groq_call(prompt_web, max_tokens=4000)

                    # Clean and display
                    html_clean = re.sub(r"```html|```", "", html_generado).strip()
                    st.success("✅ Landing page generada")

                    # Preview hint
                    st.markdown(
                        "<div style='background:var(--surface);border:1px solid var(--border);border-radius:10px;"
                        "padding:12px 16px;margin-bottom:12px;font-size:0.82rem;color:var(--text2);'>"
                        "💡 Descarga el archivo HTML y ábrelo en tu navegador para previsualizar. "
                        "Súbelo a cualquier hosting (Netlify, Vercel, etc.) para publicarlo.</div>",
                        unsafe_allow_html=True
                    )

                    # Download
                    st.download_button(
                        "⬇ Descargar landing page (.html)",
                        data=html_clean.encode("utf-8"),
                        file_name=f"{empresa_web.replace(' ','_')}_landing.html",
                        mime="text/html",
                        type="primary", use_container_width=True
                    )
                    with st.expander("Ver código HTML generado"):
                        st.code(html_clean[:3000] + ("..." if len(html_clean)>3000 else ""), language="html")
                    registrar_accion("doc_generado")
            else:
                st.warning("Rellena al menos el nombre de empresa y la propuesta de valor.")

    with tab_corporativa:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Genera el contenido completo de una web corporativa: textos para cada sección, SEO y estructura.")
        c1, c2 = st.columns(2)
        with c1:
            emp_corp = st.text_input("Empresa", key="corp_emp", placeholder="Tu empresa S.L.")
            sector_corp = st.text_input("Sector", key="corp_sec")
            servicios_corp = st.text_area("Servicios/productos principales", height=100, key="corp_srv",
                placeholder="Servicio 1\nServicio 2\nServicio 3")
        with c2:
            clientes_corp = st.text_input("Cliente ideal", key="corp_cli", placeholder="Pymes de 10-50 empleados")
            valores_corp = st.text_input("Valores de marca", key="corp_val", placeholder="Innovación, cercanía, resultados")
            paginas_corp = st.multiselect("Páginas a generar", ["Inicio","Sobre nosotros","Servicios","Por qué elegirnos","Clientes y casos de éxito","Contacto"], default=["Inicio","Sobre nosotros","Servicios","Contacto"], key="corp_pags")

        if st.button("Generar contenido web corporativa", type="primary", use_container_width=True, key="btn_corp"):
            if emp_corp and servicios_corp:
                if check_y_usar():
                    with st.spinner("Generando contenido..."):
                        r = groq_call(
                            f"Genera el contenido completo para la web corporativa de {emp_corp} ({sector_corp}).\n"
                            f"Servicios: {servicios_corp}\nCliente ideal: {clientes_corp}\nValores: {valores_corp}\n"
                            f"Páginas: {', '.join(paginas_corp)}\n\n"
                            "Para cada página escribe:\n"
                            "## [NOMBRE DE PÁGINA]\n"
                            "**Título H1:** ...\n**Meta descripción SEO:** ...\n**Contenido completo:** (párrafos, secciones)\n"
                            "**Llamada a la acción:** ...\n---\n\n"
                            "Tono profesional y persuasivo. Orientado a conversión. Todo en español.", 4000
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base=f"web_{emp_corp.replace(' ','_')}")
                    registrar_accion("doc_generado")

    with tab_ecommerce:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Genera fichas de producto optimizadas para SEO y conversión.")
        c1, c2 = st.columns(2)
        with c1:
            prod_ec = st.text_input("Producto", key="ec_prod", placeholder="Nombre del producto")
            precio_ec = st.text_input("Precio", key="ec_precio")
            categoria_ec = st.text_input("Categoría", key="ec_cat")
        with c2:
            features_ec = st.text_area("Características técnicas", height=100, key="ec_feat",
                placeholder="Material: acero inoxidable\nDimensiones: 30x20x10cm\nPeso: 500g")
            publico_ec = st.text_input("Público objetivo", key="ec_pub")
        n_fichas = st.slider("Número de variantes a generar", 1, 5, 2, key="ec_n")
        if st.button("Generar fichas de producto", type="primary", use_container_width=True, key="btn_ec"):
            if prod_ec:
                if check_y_usar():
                    with st.spinner("Generando fichas..."):
                        r = groq_call(
                            f"Genera {n_fichas} variantes de ficha de producto para e-commerce:\n"
                            f"Producto: {prod_ec} | Precio: {precio_ec} | Categoría: {categoria_ec}\n"
                            f"Características: {features_ec}\nPúblico: {publico_ec}\n\n"
                            "Para cada variante incluye:\n"
                            "- Título optimizado para SEO (max 60 chars)\n"
                            "- Meta descripción (max 155 chars)\n"
                            "- Descripción corta (50 palabras)\n"
                            "- Descripción larga (200 palabras, orientada a beneficios)\n"
                            "- 5 bullets de características/beneficios\n"
                            "- Tags/etiquetas sugeridas\n"
                            "Enfoca en beneficios, no solo características.", 3000
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base=f"ficha_{prod_ec.replace(' ','_')}")
                    registrar_accion("doc_generado")

# ══════════════════════════════════════════════════════════════════════════════
# ANÁLISIS DE MERCADO
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Análisis de mercado":
    if _bloquear_si_sin_acceso("Análisis de mercado"): st.stop()
    header("Análisis de mercado", "Estudia tu mercado, benchmark de competidores, tendencias y oportunidades de negocio")

    tab_comp, tab_tend, tab_cliente, tab_precio = st.tabs([
        "  Competidores  ", "  Tendencias  ", "  Buyer persona  ", "  Estrategia de precios  "
    ])

    with tab_comp:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Describe a tus competidores y la IA genera un benchmark completo con posicionamiento estratégico.")
        c1, c2 = st.columns(2)
        with c1:
            mi_emp = st.text_input("Mi empresa y propuesta de valor", key="comp_mi", placeholder="Ej: SaaS de RRHH para pymes, precio desde 29€/mes")
            sector_comp = st.text_input("Sector", key="comp_sec")
        with c2:
            competidores = st.text_area("Lista de competidores (uno por línea)", height=120, key="comp_list",
                placeholder="Competidor A — precio, propuesta\nCompetidor B — precio, propuesta\nCompetidor C")
        profundidad = st.radio("Profundidad del análisis:", ["Análisis rápido", "Análisis completo", "Análisis estratégico con recomendaciones"], horizontal=True, key="comp_prof")
        if st.button("Analizar competidores", type="primary", use_container_width=True, key="btn_comp"):
            if mi_emp and competidores:
                if check_y_usar():
                    with st.spinner("Analizando mercado..."):
                        r = groq_call(
                            f"Realiza un {profundidad.lower()} de competencia en {sector_comp}.\n"
                            f"MI EMPRESA: {mi_emp}\n"
                            f"COMPETIDORES:\n{competidores}\n\n"
                            "Incluye:\n1. Tabla comparativa (precio, propuesta, fortalezas, debilidades)\n"
                            "2. Mapa de posicionamiento (quién compite en qué)\n"
                            "3. Brechas del mercado sin cubrir\n"
                            "4. Estrategia de diferenciación recomendada\n"
                            "5. Quick wins: 3 acciones concretas para ganar cuota en 30 días\n"
                            "6. Amenazas a vigilar\nUsa tablas markdown cuando sea útil.", 3500
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base="analisis_competencia")
                    registrar_accion("doc_procesado")

    with tab_tend:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Obtén un análisis de tendencias del mercado y cómo tu empresa puede aprovecharlo.")
        c1, c2 = st.columns(2)
        with c1:
            sector_tend = st.text_input("Sector o mercado", key="tend_sec", placeholder="Ej: Fintech, Hostelería, Software B2B")
            horizonte = st.selectbox("Horizonte temporal", ["6 meses", "1 año", "3 años", "5 años"], key="tend_hor")
        with c2:
            pais_tend = st.text_input("País/mercado geográfico", key="tend_pais", value="España", placeholder="España, LATAM, Europa...")
            tipo_tend = st.multiselect("Tipo de tendencias", ["Tecnológicas","De consumo","Regulatorias","Macroeconómicas","Sociales"], default=["Tecnológicas","De consumo"], key="tend_tipo")
        if st.button("Analizar tendencias", type="primary", use_container_width=True, key="btn_tend"):
            if sector_tend:
                if check_y_usar():
                    with st.spinner("Analizando tendencias..."):
                        r = groq_call(
                            f"Analiza las tendencias del mercado de {sector_tend} en {pais_tend} para los próximos {horizonte}.\n"
                            f"Tipos de tendencias: {', '.join(tipo_tend)}\n\n"
                            "Para cada tendencia incluye:\n- Descripción de la tendencia\n- Impacto en el sector (alto/medio/bajo)\n"
                            "- Oportunidades que genera\n- Riesgos si no se adapta\n- Acción recomendada\n\n"
                            "Al final: resumen ejecutivo con las 3 tendencias más críticas y plan de acción.", 3000
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base=f"tendencias_{sector_tend.replace(' ','_')}")
                    registrar_accion("doc_procesado")

    with tab_cliente:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("La IA crea un buyer persona detallado con psicología del cliente y estrategia de captación.")
        c1, c2 = st.columns(2)
        with c1:
            producto_bp = st.text_input("Tu producto/servicio", key="bp_prod")
            sector_bp = st.text_input("Sector", key="bp_sec")
        with c2:
            precio_bp = st.text_input("Precio aproximado", key="bp_precio")
            conoces_bp = st.text_area("¿Qué sabes ya de tu cliente ideal?", height=80, key="bp_conoces",
                placeholder="Empresa de 10-50 empleados, sector servicios, problema con la gestión de equipo...")
        n_personas = st.slider("Número de buyer personas a generar", 1, 3, 2, key="bp_n")
        if st.button("Generar buyer personas", type="primary", use_container_width=True, key="btn_bp"):
            if producto_bp:
                if check_y_usar():
                    with st.spinner("Creando buyer personas..."):
                        r = groq_call(
                            f"Crea {n_personas} buyer personas detallados para: {producto_bp} (sector: {sector_bp}, precio: {precio_bp}).\n"
                            f"Conocimiento previo: {conoces_bp}\n\n"
                            "Para cada persona incluye:\n"
                            "- Nombre ficticio, edad, cargo, empresa tipo\n"
                            "- Día típico y contexto profesional\n"
                            "- Dolores principales (lo que le quita el sueño)\n"
                            "- Objetivos y motivaciones\n"
                            "- Objeciones más comunes ante tu oferta\n"
                            "- Canal preferido para recibir información\n"
                            "- Mensaje clave que le convencería\n"
                            "- Cómo llegar a él/ella y qué decirle", 3000
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base="buyer_personas")
                    registrar_accion("doc_generado")

    with tab_precio:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Optimiza tu estrategia de precios con datos de mercado y psicología del consumidor.")
        c1, c2 = st.columns(2)
        with c1:
            prod_p = st.text_input("Producto/servicio", key="precio_prod")
            precio_actual_p = st.text_input("Precio actual", key="precio_actual")
            coste_p = st.text_input("Coste directo", key="precio_coste")
        with c2:
            comp_precios = st.text_area("Precios de competidores", height=80, key="precio_comp",
                placeholder="Competidor A: 29€/mes\nCompetidor B: 49€/mes")
            segmento_p = st.text_input("Segmento objetivo", key="precio_seg")
        if st.button("Optimizar estrategia de precios", type="primary", use_container_width=True, key="btn_precio"):
            if prod_p and precio_actual_p:
                if check_y_usar():
                    with st.spinner("Analizando precios..."):
                        r = groq_call(
                            f"Analiza y optimiza la estrategia de precios para: {prod_p}\n"
                            f"Precio actual: {precio_actual_p} | Coste: {coste_p} | Segmento: {segmento_p}\n"
                            f"Competencia: {comp_precios}\n\n"
                            "Incluye:\n1. Análisis del margen actual y viabilidad\n"
                            "2. Benchmark de precios en el mercado\n"
                            "3. Elasticidad precio estimada\n"
                            "4. Estrategia de precios recomendada (freemium, escalonada, valor, etc.)\n"
                            "5. Modelo de precios sugerido con 3 niveles (básico/pro/enterprise)\n"
                            "6. Impacto estimado en ingresos de subir/bajar precio un 20%\n"
                            "7. Cómo comunicar el precio para maximizar conversión", 2500
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base="estrategia_precios")

# ══════════════════════════════════════════════════════════════════════════════
# GENERADOR DE MARCA
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Generador de marca":
    if _bloquear_si_sin_acceso("Generador de marca"): st.stop()
    header("Generador de marca", "Naming, identidad de marca, mensajes clave y guía de estilo para tu empresa")

    tab_naming, tab_identidad, tab_copy, tab_guia = st.tabs([
        "  Naming  ", "  Identidad  ", "  Mensajes clave  ", "  Guía de marca  "
    ])

    with tab_naming:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("La IA genera nombres de empresa/producto únicos con análisis de disponibilidad y puntuación.")
        c1, c2 = st.columns(2)
        with c1:
            desc_naming = st.text_area("Describe tu negocio o producto", height=100, key="nm_desc",
                placeholder="Software de gestión para restaurantes que automatiza pedidos y reduce mermas...")
            valores_naming = st.text_input("Valores que debe transmitir", key="nm_val",
                placeholder="Innovación, confianza, simplicidad...")
        with c2:
            estilo_naming = st.multiselect("Estilo del nombre", ["Descriptivo","Abstracto","Acrónimo","Fusión de palabras","Nombre propio","Metáfora"], default=["Abstracto","Fusión de palabras"], key="nm_estilo")
            mercado_naming = st.text_input("Mercado objetivo", key="nm_mkt", placeholder="España, internacional, B2B...")
            n_nombres = st.slider("Nombres a generar", 5, 20, 10, key="nm_n")

        if st.button("Generar nombres de marca", type="primary", use_container_width=True, key="btn_naming"):
            if desc_naming:
                if check_y_usar():
                    with st.spinner("Generando ideas de naming..."):
                        r = groq_call(
                            f"Genera {n_nombres} nombres de marca para: {desc_naming}\n"
                            f"Valores: {valores_naming} | Estilo: {', '.join(estilo_naming)} | Mercado: {mercado_naming}\n\n"
                            "Para cada nombre:\n"
                            "**Nombre:** [nombre]\n"
                            "**Tipo:** [descriptivo/abstracto/etc]\n"
                            "**Significado/origen:** [breve explicación]\n"
                            "**Dominio sugerido:** [nombre.com o alternativas]\n"
                            "**Puntuación:** [1-10 con justificación]\n"
                            "**Por qué funciona:** [1-2 frases]\n---\n"
                            "Al final: TOP 3 recomendados con justificación detallada.", 3500
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base="naming_marca")
                    registrar_accion("doc_generado")

    with tab_identidad:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            nombre_marca = st.text_input("Nombre de la marca", key="id_nombre")
            sector_id = st.text_input("Sector", key="id_sector")
            publico_id = st.text_input("Público objetivo", key="id_pub")
        with c2:
            personalidad_id = st.multiselect("Personalidad de marca", ["Sofisticada","Joven/Dinámica","Confiable/Seria","Innovadora","Cercana/Humana","Atrevida","Sostenible"], default=["Confiable/Seria","Innovadora"], key="id_pers")
            competencia_id = st.text_input("Marcas de referencia (inspírate en)", key="id_ref", placeholder="Apple, Notion, Stripe...")
        if st.button("Definir identidad de marca", type="primary", use_container_width=True, key="btn_id"):
            if nombre_marca:
                if check_y_usar():
                    with st.spinner("Definiendo identidad..."):
                        r = groq_call(
                            f"Define la identidad completa de la marca '{nombre_marca}' (sector: {sector_id}).\n"
                            f"Público: {publico_id} | Personalidad: {', '.join(personalidad_id)} | Referencias: {competencia_id}\n\n"
                            "Desarrolla:\n1. Propuesta de valor única (UVP)\n"
                            "2. Misión y visión\n3. Valores de marca (5, con explicación)\n"
                            "4. Personalidad de marca (arquetipo + descripción)\n"
                            "5. Tono de voz (cómo habla la marca, con ejemplos)\n"
                            "6. Paleta de colores sugerida (con códigos hex y psicología)\n"
                            "7. Tipografías recomendadas (Google Fonts, gratuitas)\n"
                            "8. Palabras que SÍ usa la marca y palabras que NUNCA usa\n"
                            "9. Tagline (3 opciones)", 3000
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base=f"identidad_{nombre_marca.replace(' ','_')}")
                    registrar_accion("doc_generado")

    with tab_copy:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Genera todos los textos de comunicación que necesita tu marca: taglines, bio, pitch, etc.")
        c1, c2 = st.columns(2)
        with c1:
            emp_copy = st.text_input("Empresa", key="cp_emp")
            desc_copy = st.text_area("¿Qué hace tu empresa?", height=80, key="cp_desc")
        with c2:
            pub_copy = st.text_input("Público objetivo", key="cp_pub")
            tono_copy = st.selectbox("Tono", ["Profesional","Cercano","Técnico","Inspiracional","Directo"], key="cp_tono")
        piezas_copy = st.multiselect("Piezas de copy a generar", [
            "Tagline principal (3 opciones)","Bio de empresa (Twitter/LinkedIn)","Descripción larga (web)","Elevator pitch (60 seg)",
            "Intro email de presentación","Bio del fundador","Meta descripción SEO","Headline de hero web",
        ], default=["Tagline principal (3 opciones)","Elevator pitch (60 seg)","Headline de hero web"], key="cp_piezas")
        if st.button("Generar copy de marca", type="primary", use_container_width=True, key="btn_copy"):
            if emp_copy and desc_copy and piezas_copy:
                if check_y_usar():
                    with st.spinner("Escribiendo copy..."):
                        r = groq_call(
                            f"Escribe el siguiente copy de marca para '{emp_copy}':\n"
                            f"Descripción: {desc_copy} | Público: {pub_copy} | Tono: {tono_copy}\n\n"
                            f"Piezas solicitadas:\n" + "\n".join(f"- {p}" for p in piezas_copy) +
                            "\n\nPara cada pieza ofrece al menos 2-3 variantes. Sé creativo y persuasivo.", 2500
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base=f"copy_{emp_copy.replace(' ','_')}")
                    registrar_accion("doc_generado")

    with tab_guia:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        tip("Genera una guía de estilo de marca completa para que tu equipo comunique de forma coherente.")
        emp_guia = st.text_input("Empresa", key="gu_emp")
        contexto_guia = st.text_area("Información de la marca (lo que ya sabes de ella)", height=150, key="gu_ctx",
            placeholder="Nombre: X, sector: Y, valores: Z, colores actuales: #XXX, tipografía actual: Nunito...")
        if st.button("Generar guía de marca", type="primary", use_container_width=True, key="btn_guia"):
            if emp_guia and contexto_guia:
                if check_y_usar():
                    with st.spinner("Redactando guía..."):
                        r = groq_call(
                            f"Crea una guía de estilo de marca completa para '{emp_guia}':\n{contexto_guia}\n\n"
                            "Incluye todas las secciones de una brand guide profesional:\n"
                            "1. Resumen de marca (misión, visión, valores)\n"
                            "2. Logo (uso correcto, variantes, espaciado, usos prohibidos)\n"
                            "3. Paleta de colores (primarios, secundarios, neutros — con hexadecimales)\n"
                            "4. Tipografía (titulares, cuerpo, auxiliar — tamaños y usos)\n"
                            "5. Tono de voz (principios, ejemplos de sí/no)\n"
                            "6. Iconografía y fotografía (estilo visual)\n"
                            "7. Aplicaciones: email, redes sociales, presentaciones\n"
                            "8. Ejemplos de copy correcto e incorrecto", 4000
                        )
                    st.markdown(r)
                    botones_descarga(r, "informe", nombre_base=f"guia_marca_{emp_guia.replace(' ','_')}")
                    registrar_accion("doc_generado")

# ══════════════════════════════════════════════════════════════════════════════
# CENTRO DE INFORMES
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Centro de informes":
    if _bloquear_si_sin_acceso("Centro de informes"): st.stop()
    header("Centro de informes", "Genera informes ejecutivos automáticos, KPIs visuales y reportes listos para presentar")

    tipo_informe = st.radio("Tipo de informe:", [
        "Informe de ventas", "Informe de marketing", "Informe de operaciones",
        "Informe financiero", "Informe de satisfacción", "Informe personalizado"
    ], horizontal=True, key="inf_tipo")

    campos_comunes = {}
    c1, c2 = st.columns(2)
    with c1:
        campos_comunes["empresa"] = st.text_input("Empresa", key="inf_emp")
        campos_comunes["periodo"] = st.text_input("Período", key="inf_per", value="Q3 2025", placeholder="Q1 2025, Octubre 2025...")
    with c2:
        campos_comunes["audiencia"] = st.selectbox("Audiencia", ["CEO/Dirección","Consejo/Inversores","Equipo interno","Cliente"], key="inf_aud")
        campos_comunes["nivel"] = st.select_slider("Nivel de detalle", ["Ejecutivo (1 pág)","Estándar (3-5 págs)","Completo (8-10 págs)"], key="inf_nivel")

    datos_inf = st.text_area("Datos disponibles (pega aquí tus números)", height=150, key="inf_datos",
        placeholder="Ventas: 250.000€ (+15% vs periodo anterior)\nNuevos clientes: 18\nTicket medio: 13.889€\nChurn: 2.3%\nNPS: 68\nCostes: 180.000€")

    if st.button("🎯 Generar informe ejecutivo", type="primary", use_container_width=True, key="btn_informe"):
        if campos_comunes["empresa"] and datos_inf:
            if check_y_usar():
                with st.spinner("Generando informe..."):
                    nivel_inst = {
                        "Ejecutivo (1 pág)": "Resumen ejecutivo de 1 página. Solo lo más crítico.",
                        "Estándar (3-5 págs)": "Informe estándar con análisis moderado y recomendaciones.",
                        "Completo (8-10 págs)": "Informe completo y detallado con análisis profundo, tendencias y plan de acción."
                    }[campos_comunes["nivel"]]

                    r = groq_call(
                        f"Genera un informe ejecutivo de {tipo_informe.lower()} para {campos_comunes['empresa']}.\n"
                        f"Período: {campos_comunes['periodo']} | Audiencia: {campos_comunes['audiencia']}\n"
                        f"Instrucción de longitud: {nivel_inst}\n\n"
                        f"DATOS DISPONIBLES:\n{datos_inf}\n\n"
                        "Estructura del informe:\n"
                        "## RESUMEN EJECUTIVO\n(3-4 frases impactantes con los datos más relevantes)\n\n"
                        "## RESULTADOS DEL PERÍODO\n(análisis de cada métrica clave vs objetivo y período anterior)\n\n"
                        "## ANÁLISIS DE TENDENCIAS\n(qué tendencias muestran los datos)\n\n"
                        "## PUNTOS DE ATENCIÓN\n(qué está bien, qué necesita mejora urgente)\n\n"
                        "## RECOMENDACIONES\n(acciones concretas priorizadas con impacto esperado)\n\n"
                        "## PRÓXIMOS PASOS\n(plan de acción con responsables y fechas)\n\n"
                        "Usa tablas markdown para comparativas. Sé concreto, usa los datos proporcionados.", 4000
                    )
                st.markdown(r)

                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                # Visualization if numeric data detected
                import re as re2
                numeros = re2.findall(r'\b(\d+(?:\.\d+)?)\s*(?:€|%|k€)?', datos_inf)
                if len(numeros) >= 3:
                    import plotly.graph_objects as go
                    try:
                        valores_num = [float(n) for n in numeros[:8]]
                        labels_num  = [f"Métrica {i+1}" for i in range(len(valores_num))]
                        fig_inf = go.Figure(go.Bar(y=valores_num, x=labels_num,
                            marker_color="#C9A84C", marker_line_width=0))
                        fig_inf.update_layout(
                            title="Visualización de métricas",
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font_family="DM Sans", font_color="#9090A8",
                            title_font_color="#EAEAF0",
                            margin=dict(l=0,r=0,t=40,b=0), height=250
                        )
                        fig_inf.update_xaxes(showgrid=False)
                        fig_inf.update_yaxes(gridcolor="#1E1F2E")
                        st.plotly_chart(fig_inf, use_container_width=True)
                    except: pass

                botones_descarga(r, "informe", metadata={"empresa": campos_comunes["empresa"], "fecha": campos_comunes["periodo"]},
                    nombre_base=f"informe_{tipo_informe.replace(' ','_')}_{campos_comunes['periodo'].replace(' ','_')}")
                registrar_accion("doc_generado")
        else:
            st.warning("Rellena empresa y datos para generar el informe.")

# ══════════════════════════════════════════════════════════════════════════════
# GUÍA DE USO
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "Guía de uso":
    st.markdown("""
<div style='background:linear-gradient(135deg,#0D0F1C,#141829);border:1px solid rgba(201,168,76,0.15);
border-radius:16px;padding:24px 30px 20px;margin-bottom:24px;position:relative;overflow:hidden;'>
<div style='position:absolute;top:0;left:0;right:0;height:1px;
background:linear-gradient(90deg,transparent,rgba(201,168,76,0.4),transparent);'></div>
<div style='font-family:Sora,sans-serif;font-size:0.6rem;font-weight:700;text-transform:uppercase;
letter-spacing:0.14em;color:rgba(201,168,76,0.7);margin-bottom:8px;'>Documentación</div>
<div style='font-family:Sora,sans-serif;font-size:1.4rem;font-weight:700;color:#EAEAF0;
letter-spacing:-0.03em;margin-bottom:6px;'>Guía completa de AI Growth Systems</div>
<div style='color:#606070;font-size:0.84rem;font-family:DM Sans,sans-serif;'>
Todo lo que puedes hacer, cómo hacerlo y recomendaciones para obtener los mejores resultados</div>
</div>
""", unsafe_allow_html=True)

    seccion = st.radio("Sección", [
        "🚀 Empezar aquí",
        "🤖 Asistente IA",
        "📄 Documentos",
        "📊 Datos y análisis",
        "📣 Marketing y comunicación",
        "⚖️ Legal y contratos",
        "👥 Equipo y clientes",
        "🔒 Seguridad y privacidad",
        "💡 Consejos avanzados",
    ], horizontal=False, key="guia_sec", label_visibility="collapsed")

    GUIA = {
        "🚀 Empezar aquí": {
            "titulo": "¿Por dónde empezar?",
            "desc": "Si acabas de entrar a la plataforma, esto es lo que necesitas saber.",
            "pasos": [
                ("1. Configura tu empresa", "Ve a **Configuración → Asistente IA** y describe tu empresa: sector, tamaño, clientes ideales y objetivos. Esto hace que el Asistente IA te responda de forma personalizada."),
                ("2. Prueba el Asistente IA", "Es el módulo más potente. Puedes pedirle que genere un contrato, analice un Excel, redacte un email o diseñe una estrategia — todo en lenguaje natural."),
                ("3. Usa los módulos especializados", "Cada sección tiene herramientas específicas con plantillas y opciones predefinidas. Son más rápidas cuando sabes exactamente qué quieres."),
                ("4. Adjunta tus archivos", "En el Asistente IA y en Analizar documentos puedes subir PDFs, Excels y CSVs para que la IA los analice directamente."),
            ],
            "tip": "El 80% de lo que necesitas lo puedes hacer desde el Asistente IA sin salir de ahí. Los módulos especializados son para cuando quieres más control o plantillas concretas.",
        },
        "🤖 Asistente IA": {
            "titulo": "El Asistente IA — tu copiloto empresarial",
            "desc": "El módulo central. Puede hacer prácticamente todo lo que hace la plataforma desde el chat.",
            "pasos": [
                ("Qué puede hacer", "Generar contratos, presupuestos, emails, informes, análisis de datos, estrategias de marketing, planes de negocio, análisis DAFO, FAQs, respuestas a quejas, traducciones, evaluaciones de empleados y mucho más."),
                ("Cómo pedirle las cosas", "Sé específico: en vez de *'escribe un contrato'*, di *'escribe un contrato de servicios de consultoría entre mi empresa Soluciones S.L. y el cliente Empresa X, por 3.000€/mes durante 6 meses'*. Cuanto más detalle, mejor resultado."),
                ("Cómo usar el contexto", "Configura el contexto de tu empresa una vez y el asistente lo usará en todas las conversaciones. Ahorra tiempo porque no tienes que repetir datos."),
                ("Adjuntar archivos", "Sube un PDF o Excel y luego pregunta sobre él: *'¿Cuáles son los 3 principales riesgos de este contrato?'* o *'Analiza estas ventas y dime qué mes fue peor'*."),
                ("Botones de acceso rápido", "Los botones del panel lateral son atajos a tareas frecuentes. Haz clic y la pregunta aparece automáticamente en el chat."),
            ],
            "tip": "Si no sabes cómo pedir algo, empieza con: *'Necesito [resultado concreto] para [contexto]*'. Por ejemplo: *'Necesito un email de cobro firme para un cliente con 45 días de retraso en una factura de 4.000€'*.",
        },
        "📄 Documentos": {
            "titulo": "Documentos — crea, analiza y procesa",
            "desc": "Genera documentos profesionales en segundos y extrae datos de los que ya tienes.",
            "pasos": [
                ("Crear documentos", "Ve a **Crear documentos** y elige el tipo: contrato, presupuesto, informe, carta de reclamación, acuerdo de colaboración o propuesta comercial. Rellena los campos clave y el documento se genera listo para descargar en PDF, Word o texto."),
                ("Analizar documentos", "Sube un PDF o Excel y elige qué hacer: extraer datos estructurados (ideal para facturas, nóminas, contratos), hacer preguntas directas al documento, generar un resumen, o comparar dos documentos."),
                ("Facturación", "Crea facturas profesionales con tu logo e imagen corporativa. Calcula automáticamente IVA, IRPF y totales. Descarga en PDF listo para enviar."),
                ("Procesar en lote", "Sube 5, 10 o 50 documentos del mismo tipo y extrae todos los datos en un solo Excel. Ideal para gestionar muchas facturas o contratos a la vez."),
                ("Revisar contratos", "Sube cualquier contrato y detecta riesgos, cláusulas problemáticas, lo que falta y qué deberías negociar antes de firmar."),
            ],
            "tip": "Para extraer datos de facturas en lote, usa **Procesar en lote** y elige la plantilla 'Factura'. En 2 minutos tienes todos los datos en Excel, sin teclear nada.",
        },
        "📊 Datos y análisis": {
            "titulo": "Datos y análisis — entiende tu negocio",
            "desc": "Convierte cualquier hoja de cálculo en insights accionables y visualizaciones claras.",
            "pasos": [
                ("Generar Excel con IA", "Describe la tabla que necesitas en lenguaje natural: *'Tabla de previsión de ventas mensual para 12 meses con columnas: mes, objetivo, real, % desviación'*. La IA la genera con datos de ejemplo y la exporta."),
                ("Analítica avanzada", "Sube cualquier Excel o CSV y obtén: dashboards automáticos, gráficos interactivos (barras, líneas, dispersión, pie), análisis de tendencias y anomalías con IA."),
                ("Finanzas y datos", "Plan financiero a 12 meses, cálculo de ROI, análisis de rentabilidad por cliente, presupuesto por departamento y detección de irregularidades en facturas."),
                ("Informes ejecutivos", "En 3 minutos: pega tus datos (ventas, KPIs, costes) y obtén un informe ejecutivo completo con análisis, tendencias y recomendaciones listo para presentar a dirección o inversores."),
            ],
            "tip": "Para el análisis financiero, pega directamente en el campo de texto los datos en formato simple: *Ventas Q3: 180k€, Costes: 120k€, Clientes nuevos: 14*. No necesitas Excel — la IA entiende el texto.",
        },
        "📣 Marketing y comunicación": {
            "titulo": "Marketing y comunicación — crece y comunica",
            "desc": "Crea contenido de calidad, gestiona tu marca y comunica de forma profesional.",
            "pasos": [
                ("Emails y comunicación", "7 tipos de email: presentación comercial, seguimiento, cobro de facturas, respuesta a quejas, anuncios, colaboraciones. Elige el tono (formal/cercano/directo) y el contexto."),
                ("Marketing y contenidos", "Artículos de blog optimizados para SEO, posts para LinkedIn/Instagram/Twitter/Facebook, newsletters completas y descripciones de producto persuasivas."),
                ("Identidad de marca", "Naming con puntuación, identidad completa (colores, tipografía, tono de voz), copy de marca (taglines, bio, pitch, headlines) y guía de estilo para que tu equipo comunique de forma coherente."),
                ("Presentaciones", "Genera el guión completo de cualquier presentación slide a slide, con título, mensaje clave, contenido, notas del presentador y sugerencia visual. Exporta a TXT, PDF o Word y llévalo a PowerPoint o Canva."),
                ("Traducción", "Traduce documentos, contratos y emails a 10 idiomas (inglés, francés, alemán, portugués, italiano, chino, árabe, japonés, neerlandés, ruso) con tono empresarial. También adapta contenido culturalmente para diferentes mercados."),
            ],
            "tip": "Para LinkedIn, especifica siempre el objetivo del post: *'Post para conseguir leads'* o *'Post para posicionarme como experto en X'*. El resultado es mucho más efectivo que solo decir el tema.",
        },
        "⚖️ Legal y contratos": {
            "titulo": "Legal — protege tu negocio",
            "desc": "Documentos legales profesionales y análisis de contratos para evitar sorpresas.",
            "pasos": [
                ("Documentos legales", "Genera política de privacidad conforme al RGPD, aviso legal según la LSSI-CE, términos y condiciones, y política de cookies. Rellena los datos de tu empresa y en 2 minutos tienes el documento listo."),
                ("Revisar contratos", "Sube el contrato en PDF o pega el texto. La IA lo analiza como un abogado: detecta cláusulas de riesgo alto, lo que te favorece, lo que falta y qué pedir antes de firmar. También puede simplificar el contrato a lenguaje claro."),
                ("Crear contratos", "Genera contratos de servicios, trabajo, alquiler, compraventa, confidencialidad (NDA), colaboración o agencia. Introduce las partes, el servicio y el importe y obtienes un contrato completo."),
            ],
            "tip": "⚠️ Los documentos generados son una base excelente pero no sustituyen al asesoramiento de un abogado para casos complejos o de alto valor. Úsalos como punto de partida y para situaciones habituales.",
        },
        "👥 Equipo y clientes": {
            "titulo": "Equipo y clientes — gestiona y fideliza",
            "desc": "Herramientas para gestionar tu equipo, tus clientes y la atención que les das.",
            "pasos": [
                ("Recursos humanos", "Genera ofertas de trabajo atractivas, planes de onboarding por semanas, evaluaciones de desempeño estructuradas y planes de formación con presupuesto y calendario."),
                ("Reuniones", "Antes: genera agendas profesionales. Después: pega las notas y obtén resumen ejecutivo, decisiones tomadas, acuerdos y próximos pasos. También redacta el acta formal y el email de seguimiento."),
                ("Atención al cliente", "Responde quejas de forma profesional y empática, genera FAQs completas de tu empresa, analiza reseñas para extraer insights, diseña programas de fidelización y crea guiones de llamada de ventas."),
                ("Clientes y CRM", "Gestiona contactos, añade oportunidades con valor y estado (prospecto/negociación/cerrado), y visualiza tu pipeline con métricas en tiempo real."),
                ("Chatbot de empresa", "Configura la información de tu empresa y activa un asistente virtual entrenado específicamente con tus datos: precios, horarios, FAQs, servicios. Perfectamente para simular cómo respondería a tus clientes."),
            ],
            "tip": "Para la **Atención al cliente**, empieza por generar las FAQs de tu empresa — es lo que más tiempo ahorra al equipo. Luego usa el Chatbot con esa información para ver cómo respondería un asistente automático.",
        },
        "🔒 Seguridad y privacidad": {
            "titulo": "Seguridad y privacidad — tus datos protegidos",
            "desc": "Todo lo que necesitas saber sobre cómo protegemos tu información.",
            "pasos": [
                ("Cifrado de datos", "Toda la comunicación entre tu navegador y nuestros servidores está cifrada con TLS 1.3. Los datos almacenados en nuestra base de datos (Supabase) están cifrados en reposo con AES-256."),
                ("Autenticación segura", "El sistema de autenticación usa Supabase Auth con bcrypt para contraseñas. Las sesiones expiran automáticamente. Nunca almacenamos tu contraseña en texto plano."),
                ("Tus documentos", "Los documentos que generas o analizas NO se almacenan en nuestros servidores. Se procesan en memoria y se descartan inmediatamente. Solo guardamos métricas de uso (cuántas acciones realizaste)."),
                ("Procesamiento de IA", "Las consultas a la IA van a través de Groq (infraestructura en Europa). No usamos tus datos para entrenar modelos. Tu información no se comparte con terceros."),
                ("RGPD", "Cumplimos con el Reglamento General de Protección de Datos (RGPD). Puedes solicitar la eliminación de tu cuenta y todos tus datos en cualquier momento escribiendo a hello.aigrowthsystems@gmail.com."),
                ("Contraseñas", "Usa una contraseña de al menos 12 caracteres. Nunca la compartas. Si sospechas que tu cuenta fue comprometida, cámbiala desde Configuración inmediatamente."),
            ],
            "tip": "Nunca subas información extremadamente sensible (números de cuenta bancaria completos, contraseñas, datos médicos) a ninguna plataforma de IA. Para documentos confidenciales, anonimiza los datos antes de subirlos.",
        },
        "💡 Consejos avanzados": {
            "titulo": "Consejos avanzados para resultados excepcionales",
            "desc": "Técnicas para sacar el máximo partido a la plataforma.",
            "pasos": [
                ("El truco del contexto de empresa", "Cuanto más detallado sea el contexto de tu empresa (en Configuración → Asistente IA), mejores serán todas las respuestas. Incluye: sector exacto, tamaño, clientes ideales, ticket medio, objetivos actuales y retos principales."),
                ("Cadena de prompts", "Para resultados complejos, divide en pasos: primero pide el esquema, luego cada sección. Ejemplo: *'Dame el índice de una propuesta para X'* → *'Ahora desarrolla la sección 2'* → *'Añade datos de ROI'*."),
                ("Revisar y mejorar", "Si el resultado no te gusta, di exactamente qué cambiar: *'Está bien pero hazlo más formal'*, *'Añade un apartado sobre garantías'*, *'El precio está equivocado, son 5.000€ no 3.000€'*."),
                ("Combinar módulos", "El flujo más potente: genera una **propuesta comercial** → pídele al Asistente IA que la convierta en **presentación de slides** → genera el **email de presentación** → si el cliente acepta, crea el **contrato** automáticamente."),
                ("Análisis de datos con contexto", "Al analizar un Excel, añade contexto en el chat: *'Esto es un Excel de ventas de una empresa de software B2B. El objetivo de Q3 era 200k€. Analiza por qué no se llegó al objetivo'*. La IA da recomendaciones mucho más precisas."),
                ("Plantillas de Generador Excel", "Usa las plantillas del Generador Excel como base y luego pídele al Asistente IA que las personalice: *'Tengo esta tabla de pipeline, ahora añade una columna de probabilidad ponderada y un resumen por vendedor'*."),
            ],
            "tip": "La función más infrautilizada es **Procesar en lote**. Si tienes 20 facturas de proveedores en PDF, puedes extraer todos los datos (proveedor, fecha, importe, IVA) en un Excel en menos de 3 minutos.",
        },
    }

    datos_guia = GUIA.get(seccion, {})
    if datos_guia:
        st.markdown(
            f"<div style='margin-bottom:20px;'>"
            f"<div style='font-family:Sora,sans-serif;font-size:1.25rem;font-weight:700;color:var(--text);"
            f"letter-spacing:-0.02em;margin-bottom:6px;'>{datos_guia['titulo']}</div>"
            f"<div style='font-size:0.875rem;color:var(--text3);line-height:1.6;'>{datos_guia['desc']}</div>"
            "</div>",
            unsafe_allow_html=True
        )

        for titulo_paso, contenido_paso in datos_guia["pasos"]:
            st.markdown(
                f"<div style='background:var(--surface);border:1px solid var(--border);border-radius:12px;"
                f"padding:16px 20px;margin-bottom:10px;'>"
                f"<div style='font-family:Sora,sans-serif;font-weight:600;font-size:0.88rem;"
                f"color:var(--gold2);margin-bottom:7px;'>{titulo_paso}</div>"
                f"<div style='font-size:0.84rem;color:var(--text2);line-height:1.7;'>{contenido_paso}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        if "tip" in datos_guia:
            st.markdown(
                f"<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.2);"
                "border-radius:10px;padding:14px 18px;margin-top:6px;'>"
                f"<span style='color:var(--gold);font-weight:600;'>⚡ Pro tip: </span>"
                f"<span style='color:var(--text2);font-size:0.84rem;'>{datos_guia['tip']}</span>"
                "</div>",
                unsafe_allow_html=True
            )