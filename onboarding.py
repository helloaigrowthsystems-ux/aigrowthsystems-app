# onboarding.py — AI Growth Systems
# Flujo de bienvenida de 3 pasos para nuevos usuarios.
# Aumenta la activación: el usuario entiende qué hacer y personaliza su experiencia.
# Se muestra una sola vez, justo después del primer login.

import streamlit as st
from auth import get_supabase, obtener_perfil

SECTORES = [
    "Consultoría y servicios profesionales",
    "Agencia de marketing / publicidad",
    "Gestoría / asesoría / contabilidad",
    "Inmobiliaria / construcción",
    "E-commerce / retail",
    "Hostelería / restauración",
    "Salud y bienestar",
    "Tecnología / software",
    "Educación / formación",
    "Legal / despacho de abogados",
    "Manufactura / industria",
    "Otro",
]

TAMANIOS = [
    "Solo yo (freelance / autónomo)",
    "2-5 personas",
    "6-20 personas",
    "21-50 personas",
    "Más de 50 personas",
]

OBJETIVOS = [
    ("📄", "Generar documentos y contratos más rápido",       "documentos"),
    ("💰", "Cerrar más ventas con mejores propuestas",        "ventas"),
    ("📊", "Analizar mis datos y tomar mejores decisiones",   "datos"),
    ("📣", "Crear contenido de marketing sin esfuerzo",       "marketing"),
    ("⚖️", "Protegerme legalmente y revisar contratos",      "legal"),
    ("🚀", "Definir mi estrategia y hacer crecer el negocio", "estrategia"),
]

# Módulos recomendados por objetivo principal
MODULOS_POR_OBJETIVO = {
    "documentos": ["Crear documento", "Analizar documento", "Facturación", "Revisar contratos"],
    "ventas":     ["Propuestas comerciales", "Redactar emails", "Clientes y pipeline", "Análisis de mercado"],
    "datos":      ["Generador Excel IA", "Analítica visual", "Análisis financiero", "Centro de informes"],
    "marketing":  ["Marketing y contenidos", "Generador de marca", "Presentaciones IA", "Crear web con IA"],
    "legal":      ["Revisar contratos", "Documentos legales", "Crear documento", "Asistente IA"],
    "estrategia": ["Estrategia empresarial", "Análisis de mercado", "Análisis financiero", "Propuestas comerciales"],
}


def necesita_onboarding() -> bool:
    """Devuelve True si el usuario no ha completado el onboarding."""
    perfil = obtener_perfil()
    return not perfil.get("onboarding_done", False)


def marcar_onboarding_completo():
    """Persiste onboarding_done=True en Supabase."""
    try:
        uid = st.session_state["usuario"].id
        get_supabase().table("usuarios").update({"onboarding_done": True}).eq("id", uid).execute()
    except Exception:
        pass
    st.session_state["onboarding_done"] = True


def mostrar_onboarding():
    """
    Renderiza el wizard de 3 pasos y devuelve True cuando termina.
    Usar en app.py antes de renderizar el módulo normal:
        if necesita_onboarding():
            if mostrar_onboarding():
                st.rerun()
            st.stop()
    """
    paso = st.session_state.get("onboarding_paso", 1)

    # ── Barra de progreso ──────────────────────────────────────────────────────
    pct = int((paso / 3) * 100)
    st.markdown(
        f"""
<div style='max-width:560px;margin:0 auto 32px;'>
  <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
    <span style='font-size:0.72rem;color:#505060;font-family:DM Sans,sans-serif;'>
      Configuración inicial</span>
    <span style='font-size:0.72rem;color:#C9A84C;font-weight:600;font-family:DM Sans,sans-serif;'>
      Paso {paso} de 3</span>
  </div>
  <div style='background:#1E1F2E;border-radius:4px;height:3px;'>
    <div style='background:linear-gradient(90deg,#C9A84C,#E8C96A);width:{pct}%;height:100%;
    border-radius:4px;transition:width 0.4s ease;'></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── PASO 1: Sector ─────────────────────────────────────────────────────────
    if paso == 1:
        st.markdown(
            """
<div class='onboarding-step'>
  <div class='onboarding-step-number'>1</div>
  <div style='font-family:Sora,sans-serif;font-size:1.3rem;font-weight:700;
  color:#EAEAF0;margin-bottom:6px;letter-spacing:-0.03em;'>
    ¿En qué sector trabajas?</div>
  <div style='font-size:0.84rem;color:#505060;margin-bottom:24px;line-height:1.6;'>
    Personalizamos las sugerencias y el tono del asistente según tu industria.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        col_wrap, _ = st.columns([1, 0.001])
        with col_wrap:
            sector = st.selectbox(
                "Sector",
                SECTORES,
                key="ob_sector",
                label_visibility="collapsed",
            )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("Continuar →", type="primary", key="ob_btn1", use_container_width=False):
            st.session_state["ob_sector_val"] = sector
            st.session_state["onboarding_paso"] = 2
            st.rerun()

    # ── PASO 2: Tamaño y objetivo ──────────────────────────────────────────────
    elif paso == 2:
        st.markdown(
            """
<div class='onboarding-step'>
  <div class='onboarding-step-number'>2</div>
  <div style='font-family:Sora,sans-serif;font-size:1.3rem;font-weight:700;
  color:#EAEAF0;margin-bottom:6px;letter-spacing:-0.03em;'>
    ¿Cuál es tu objetivo principal?</div>
  <div style='font-size:0.84rem;color:#505060;margin-bottom:24px;line-height:1.6;'>
    Te mostramos primero las herramientas más útiles para ti.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        tamanio = st.selectbox(
            "Tamaño del equipo",
            TAMANIOS,
            key="ob_tamanio",
            label_visibility="collapsed",
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size:0.75rem;color:#505060;margin-bottom:10px;text-transform:uppercase;"
            "letter-spacing:0.1em;font-weight:600;'>Objetivo principal</div>",
            unsafe_allow_html=True,
        )
        objetivo_sel = st.session_state.get("ob_objetivo_val", None)
        cols = st.columns(2)
        for i, (ico, label, key) in enumerate(OBJETIVOS):
            col = cols[i % 2]
            with col:
                selected = objetivo_sel == key
                border = "rgba(201,168,76,0.5)" if selected else "#1E1F2E"
                bg     = "rgba(201,168,76,0.07)" if selected else "#0F1117"
                if st.button(
                    f"{ico}  {label}",
                    key=f"ob_obj_{key}",
                    use_container_width=True,
                    type="secondary",
                ):
                    st.session_state["ob_objetivo_val"] = key
                    st.rerun()
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Atrás", key="ob_back2"):
                st.session_state["onboarding_paso"] = 1
                st.rerun()
        with c2:
            if st.button("Continuar →", type="primary", key="ob_btn2", use_container_width=True):
                if not st.session_state.get("ob_objetivo_val"):
                    st.warning("Elige un objetivo para continuar.")
                else:
                    st.session_state["ob_tamanio_val"] = tamanio
                    st.session_state["onboarding_paso"] = 3
                    st.rerun()

    # ── PASO 3: Confirmación + módulos recomendados ────────────────────────────
    elif paso == 3:
        sector  = st.session_state.get("ob_sector_val",   "tu sector")
        tamanio = st.session_state.get("ob_tamanio_val",  "tu equipo")
        obj_key = st.session_state.get("ob_objetivo_val", "documentos")
        obj_lbl = next((l for _, l, k in OBJETIVOS if k == obj_key), "")
        modulos = MODULOS_POR_OBJETIVO.get(obj_key, [])

        st.markdown(
            f"""
<div class='onboarding-step'>
  <div style='font-family:Sora,sans-serif;font-size:1.3rem;font-weight:700;
  color:#EAEAF0;margin-bottom:6px;letter-spacing:-0.03em;'>
    ¡Todo listo! 🎉</div>
  <div style='font-size:0.84rem;color:#505060;margin-bottom:20px;line-height:1.6;'>
    Hemos configurado AI Growth Systems para <b style='color:#9090A8;'>{sector}</b>,
    equipo de <b style='color:#9090A8;'>{tamanio}</b>.<br>
    Tu objetivo: <b style='color:#C9A84C;'>{obj_lbl}</b>
  </div>
  <div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;
  color:#505060;font-weight:600;margin-bottom:12px;'>Te recomendamos empezar por</div>
</div>
""",
            unsafe_allow_html=True,
        )

        for m in modulos:
            st.markdown(
                f"<div style='background:#0F1117;border:1px solid #1E1F2E;border-radius:9px;"
                f"padding:11px 16px;margin-bottom:6px;font-size:0.84rem;color:#EAEAF0;"
                f"font-family:DM Sans,sans-serif;'>→ {m}</div>",
                unsafe_allow_html=True,
            )

        # Guardar contexto en session_state para que el Asistente IA lo use
        contexto_generado = (
            f"Empresa en el sector: {sector}. "
            f"Tamaño del equipo: {tamanio}. "
            f"Objetivo principal: {obj_lbl}."
        )
        st.session_state["contexto_asistente"] = contexto_generado

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("Entrar a la plataforma →", type="primary", key="ob_fin", use_container_width=True):
            # Persistir datos en Supabase
            try:
                uid = st.session_state["usuario"].id
                get_supabase().table("usuarios").update({
                    "onboarding_done": True,
                    "sector": sector,
                    "tamanio": tamanio,
                    "objetivo": obj_key,
                }).eq("id", uid).execute()
            except Exception:
                pass
            st.session_state["onboarding_done"] = True
            # Limpiar estado del wizard
            for k in ["onboarding_paso", "ob_sector_val", "ob_tamanio_val", "ob_objetivo_val"]:
                st.session_state.pop(k, None)
            return True  # señal: onboarding completado, hacer st.rerun()

    return False  # todavía en proceso
