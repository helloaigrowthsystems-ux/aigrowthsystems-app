# analytics.py — AI Growth Systems
# Tracking de eventos por módulo. Responde: ¿qué funciones usan más mis clientes?
# ¿Dónde abandonan? ¿Qué valor generan?
# 
# Tabla Supabase necesaria:
#   CREATE TABLE eventos (
#     id         BIGSERIAL PRIMARY KEY,
#     user_id    UUID REFERENCES auth.users(id),
#     modulo     TEXT NOT NULL,
#     accion     TEXT NOT NULL,
#     metadata   JSONB DEFAULT '{}',
#     created_at TIMESTAMPTZ DEFAULT now()
#   );
#   CREATE INDEX ON eventos(user_id);
#   CREATE INDEX ON eventos(modulo);
#   CREATE INDEX ON eventos(created_at);

import streamlit as st
from datetime import datetime, date, timedelta
from auth import get_supabase
import json


# ─── Registro de eventos ─────────────────────────────────────────────────────

def track(modulo: str, accion: str, metadata: dict = None):
    """
    Registra un evento de uso. Silencioso: nunca rompe la app si falla.
    
    Uso:
        track("Crear documento", "generado", {"tipo": "contrato", "palabras": 450})
        track("Análisis financiero", "roi_calculado", {"valor": 34500})
        track("Propuestas comerciales", "generada")
    """
    try:
        uid = st.session_state.get("usuario") and st.session_state["usuario"].id
        if not uid:
            return
        get_supabase().table("eventos").insert({
            "user_id":  uid,
            "modulo":   modulo,
            "accion":   accion,
            "metadata": metadata or {},
        }).execute()
    except Exception:
        pass  # analytics nunca rompe el flujo principal


def track_inicio_modulo(modulo: str):
    """Llamar cuando el usuario entra a un módulo (mide qué módulos abren)."""
    track(modulo, "vista")


def track_resultado(modulo: str, metadata: dict = None):
    """Llamar cuando la IA devuelve un resultado exitoso."""
    track(modulo, "resultado_generado", metadata)


def track_descarga(modulo: str, formato: str):
    """Llamar cuando el usuario descarga un documento."""
    track(modulo, "descarga", {"formato": formato})


def track_upgrade_intent(modulo: str):
    """Llamar cuando el usuario choca con un muro de plan (mide fricción de conversión)."""
    track(modulo, "upgrade_intent")


# ─── Consultas de analytics (solo admin) ────────────────────────────────────

def obtener_eventos_admin(dias: int = 30) -> list:
    """Todos los eventos de los últimos N días (solo llamar desde panel admin)."""
    try:
        desde = (datetime.utcnow() - timedelta(days=dias)).isoformat()
        res = get_supabase().table("eventos").select("*").gte("created_at", desde).execute()
        return res.data or []
    except Exception:
        return []


def obtener_mis_eventos(dias: int = 30) -> list:
    """Eventos del usuario actual."""
    try:
        uid  = st.session_state["usuario"].id
        desde = (datetime.utcnow() - timedelta(days=dias)).isoformat()
        res  = get_supabase().table("eventos").select("*").eq("user_id", uid).gte("created_at", desde).execute()
        return res.data or []
    except Exception:
        return []


def top_modulos(eventos: list, top_n: int = 10) -> list[tuple[str, int]]:
    """Devuelve lista de (módulo, usos) ordenada por frecuencia."""
    conteo: dict[str, int] = {}
    for e in eventos:
        m = e.get("modulo", "desconocido")
        conteo[m] = conteo.get(m, 0) + 1
    return sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top_n]


def usuarios_activos_hoy(eventos: list) -> int:
    hoy = str(date.today())
    uids = {e["user_id"] for e in eventos if e.get("created_at", "")[:10] == hoy}
    return len(uids)


def tasa_conversion_upgrade(eventos: list) -> float:
    """% de veces que un upgrade_intent resultó en uso posterior del módulo bloqueado."""
    intents = sum(1 for e in eventos if e.get("accion") == "upgrade_intent")
    if not intents:
        return 0.0
    # Proxy: usuarios que tuvieron intent y luego generaron resultado
    uids_con_intent = {e["user_id"] for e in eventos if e.get("accion") == "upgrade_intent"}
    uids_con_resultado = {e["user_id"] for e in eventos if e.get("accion") == "resultado_generado"}
    convertidos = len(uids_con_intent & uids_con_resultado)
    return round(convertidos / len(uids_con_intent) * 100, 1) if uids_con_intent else 0.0


# ─── Widget de analytics para panel admin ───────────────────────────────────

def mostrar_analytics_admin():
    """
    Panel de analytics completo para el módulo de administración.
    Solo mostrar si es_admin == True.
    """
    import plotly.express as px
    import pandas as pd

    st.markdown(
        "<div style='font-family:Sora,sans-serif;font-size:1rem;font-weight:700;"
        "color:#EAEAF0;margin-bottom:16px;'>📊 Analytics de plataforma</div>",
        unsafe_allow_html=True,
    )

    periodo = st.selectbox("Período", ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días"],
                           key="analytics_periodo")
    dias = {"Últimos 7 días": 7, "Últimos 30 días": 30, "Últimos 90 días": 90}[periodo]

    eventos = obtener_eventos_admin(dias)

    if not eventos:
        st.info("Sin datos de eventos todavía. Se registrarán automáticamente con el uso.")
        return

    df = pd.DataFrame(eventos)
    df["fecha"] = pd.to_datetime(df["created_at"]).dt.date

    # KPIs
    total_eventos   = len(eventos)
    usuarios_unicos = df["user_id"].nunique()
    ua_hoy          = usuarios_activos_hoy(eventos)
    upgrade_intents = len(df[df["accion"] == "upgrade_intent"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Eventos totales",     total_eventos)
    c2.metric("Usuarios únicos",     usuarios_unicos)
    c3.metric("Activos hoy",         ua_hoy)
    c4.metric("Upgrade intents",     upgrade_intents,
              help="Veces que un usuario chocó con límite de plan")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(
            "<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;"
            "color:#505060;font-weight:600;margin-bottom:8px;'>Módulos más usados</div>",
            unsafe_allow_html=True,
        )
        top = top_modulos(eventos, top_n=8)
        df_top = pd.DataFrame(top, columns=["Módulo", "Usos"])
        fig = px.bar(
            df_top, x="Usos", y="Módulo", orientation="h",
            color_discrete_sequence=["#C9A84C"],
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9090A8", size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#1E1F2E", zeroline=False),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown(
            "<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;"
            "color:#505060;font-weight:600;margin-bottom:8px;'>Actividad diaria</div>",
            unsafe_allow_html=True,
        )
        df_dia = df.groupby("fecha").size().reset_index(name="eventos")
        fig2 = px.area(
            df_dia, x="fecha", y="eventos",
            color_discrete_sequence=["#C9A84C"],
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9090A8", size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#1E1F2E", zeroline=False),
            yaxis=dict(gridcolor="#1E1F2E", zeroline=False),
            height=280,
        )
        fig2.update_traces(fillcolor="rgba(201,168,76,0.12)", line_color="#C9A84C")
        st.plotly_chart(fig2, use_container_width=True)

    # Acciones más frecuentes
    st.markdown(
        "<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;"
        "color:#505060;font-weight:600;margin:16px 0 8px;'>Desglose de acciones</div>",
        unsafe_allow_html=True,
    )
    df_acc = df.groupby(["modulo", "accion"]).size().reset_index(name="n")
    df_acc = df_acc.sort_values("n", ascending=False).head(20)
    st.dataframe(
        df_acc.rename(columns={"modulo": "Módulo", "accion": "Acción", "n": "Veces"}),
        use_container_width=True, hide_index=True,
    )
