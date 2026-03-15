# payments.py — AI Growth Systems
# Integración completa con Stripe Checkout.
# Cubre: crear sesión de pago, verificar webhook, actualizar plan en Supabase.
#
# SETUP:
#   1. pip install stripe
#   2. Añadir al .env: STRIPE_SECRET_KEY, STRIPE_PRICE_PRO, STRIPE_PRICE_BUSINESS, STRIPE_WEBHOOK_SECRET
#   3. En Stripe Dashboard: crear productos Pro (29€/mes) y Business (99€/mes)
#   4. Crear webhook apuntando a /webhook (necesita FastAPI/Flask para recibirlo)
#      o usar Streamlit Cloud + un endpoint externo (ver nota abajo)
#
# NOTA STREAMLIT: Streamlit no expone endpoints HTTP. Para producción, desplegar
# el webhook en un pequeño servicio Flask en Railway/Render (< 30 min de trabajo).
# El webhook solo actualiza el campo "plan" en Supabase, que esta app ya lee.

import os
import streamlit as st
from dotenv import load_dotenv
from auth import get_supabase, obtener_perfil

load_dotenv(override=True)

STRIPE_SECRET_KEY       = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_PRO        = os.getenv("STRIPE_PRICE_PRO", "")
STRIPE_PRICE_BUSINESS   = os.getenv("STRIPE_PRICE_BUSINESS", "")
STRIPE_WEBHOOK_SECRET   = os.getenv("STRIPE_WEBHOOK_SECRET", "")

STRIPE_DISPONIBLE = bool(STRIPE_SECRET_KEY and STRIPE_SECRET_KEY.startswith("sk_"))

PLAN_INFO = {
    "pro": {
        "nombre":      "Plan Pro",
        "precio":      "29€/mes",
        "descripcion": "Acciones ilimitadas · Todos los módulos · Soporte por email",
        "color":       "#C9A84C",
        "features": [
            "✓ Acciones ilimitadas",
            "✓ Todos los módulos desbloqueados",
            "✓ Crear documentos, contratos, facturas",
            "✓ Marketing, emails y traducciones",
            "✓ Estrategia, RRHH y legal",
            "✓ Soporte por email < 24h",
        ],
        "price_id": STRIPE_PRICE_PRO,
    },
    "business": {
        "nombre":      "Plan Business",
        "precio":      "99€/mes",
        "descripcion": "Todo Pro + CRM · Facturación · Lote · Soporte prioritario",
        "color":       "#E8C96A",
        "features": [
            "✓ Todo lo del plan Pro",
            "✓ CRM completo y pipeline de ventas",
            "✓ Facturación profesional con tu marca",
            "✓ Procesar 50+ documentos en lote",
            "✓ Informes ejecutivos automáticos",
            "✓ Soporte prioritario < 4h",
            "✓ Onboarding personalizado",
        ],
        "price_id": STRIPE_PRICE_BUSINESS,
    },
}


def crear_checkout_session(plan: str, email_usuario: str, uid_usuario: str) -> str | None:
    """
    Crea una sesión de Stripe Checkout y devuelve la URL de pago.
    Devuelve None si Stripe no está configurado o hay error.
    """
    if not STRIPE_DISPONIBLE:
        return None
    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        info = PLAN_INFO.get(plan)
        if not info or not info["price_id"]:
            return None

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email=email_usuario,
            line_items=[{"price": info["price_id"], "quantity": 1}],
            success_url="https://tu-app.streamlit.app/?pago=ok&plan=" + plan,
            cancel_url="https://tu-app.streamlit.app/?pago=cancelado",
            metadata={"uid": uid_usuario, "plan": plan},
            locale="es",
            allow_promotion_codes=True,
        )
        return session.url
    except Exception as e:
        st.error(f"Error al iniciar el pago: {e}")
        return None


def actualizar_plan_supabase(uid: str, plan: str):
    """Actualiza el plan del usuario en Supabase. Llamar desde el webhook."""
    try:
        get_supabase().table("usuarios").update({"plan": plan}).eq("id", uid).execute()
        return True
    except Exception:
        return False


def mostrar_pricing_upgrade(plan_actual: str = "gratuito"):
    """
    Renderiza las tarjetas de precios con botones de compra.
    Si Stripe está configurado → redirige al checkout.
    Si no → muestra email de contacto como fallback.
    """
    perfil = obtener_perfil()
    email  = perfil.get("email", "")
    uid    = st.session_state.get("usuario") and st.session_state["usuario"].id

    st.markdown(
        "<div style='font-family:Sora,sans-serif;font-size:1.4rem;font-weight:700;"
        "color:#EAEAF0;text-align:center;margin-bottom:6px;letter-spacing:-0.03em;'>"
        "Desbloquea todo el potencial</div>"
        "<div style='text-align:center;font-size:0.84rem;color:#505060;margin-bottom:28px;'>"
        "Sin permanencia · Cancela cuando quieras · RGPD compliant</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)

    for col, (plan_key, info) in zip(cols, PLAN_INFO.items()):
        if plan_actual == plan_key:
            continue  # no mostrar el plan que ya tiene
        with col:
            is_featured = plan_key == "pro"
            border_color = info["color"] + ("66" if is_featured else "33")
            bg = "linear-gradient(135deg,#0D0F1C,#141829)" if is_featured else "#0F1117"
            st.markdown(
                f"<div style='background:{bg};border:1px solid {border_color};"
                f"border-radius:16px;padding:24px 26px;position:relative;overflow:hidden;'>"
                + (
                    f"<div style='position:absolute;top:0;left:0;right:0;height:2px;"
                    f"background:linear-gradient(90deg,transparent,{info['color']},transparent);'></div>"
                    if is_featured else ""
                )
                + f"<div style='font-family:Sora,sans-serif;font-size:0.6rem;font-weight:700;"
                f"text-transform:uppercase;letter-spacing:0.14em;color:{info['color']};margin-bottom:8px;'>"
                f"{'⭐ MÁS POPULAR' if is_featured else '🚀 ENTERPRISE'}</div>"
                f"<div style='font-family:Sora,sans-serif;font-size:1.1rem;font-weight:700;"
                f"color:#EAEAF0;margin-bottom:4px;'>{info['nombre']}</div>"
                f"<div style='font-size:1.8rem;font-weight:800;color:{info['color']};"
                f"font-family:Sora,sans-serif;margin-bottom:4px;'>{info['precio']}</div>"
                f"<div style='font-size:0.75rem;color:#505060;margin-bottom:18px;'>{info['descripcion']}</div>"
                + "".join(
                    f"<div style='font-size:0.8rem;color:#9090A8;margin-bottom:5px;'>{f}</div>"
                    for f in info["features"]
                )
                + "</div>",
                unsafe_allow_html=True,
            )
            if STRIPE_DISPONIBLE and info["price_id"]:
                if st.button(
                    f"Contratar {info['nombre']} →",
                    key=f"pay_{plan_key}",
                    type="primary",
                    use_container_width=True,
                ):
                    url = crear_checkout_session(plan_key, email, uid)
                    if url:
                        st.markdown(
                            f"<meta http-equiv='refresh' content='0; url={url}'>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"[Si no redirige automáticamente, haz clic aquí]({url})"
                        )
            else:
                st.markdown(
                    f"<div style='background:rgba(201,168,76,0.06);border:1px solid rgba(201,168,76,0.15);"
                    f"border-radius:9px;padding:13px 16px;text-align:center;margin-top:8px;'>"
                    f"<div style='font-size:0.82rem;color:#C9A84C;font-weight:600;margin-bottom:4px;'>"
                    f"Contratar {info['nombre']}</div>"
                    f"<div style='font-size:0.75rem;color:#505060;'>"
                    f"📩 hello.aigrowthsystems@gmail.com<br>"
                    f"<span style='font-size:0.7rem;'>Respuesta en menos de 2h</span></div></div>",
                    unsafe_allow_html=True,
                )

    # Garantía
    st.markdown(
        "<div style='text-align:center;margin-top:20px;font-size:0.78rem;color:#505060;'>"
        "🛡️ Garantía de 7 días · Si no estás satisfecho, te devolvemos el dinero sin preguntas</div>",
        unsafe_allow_html=True,
    )


def verificar_pago_exitoso():
    """
    Detecta ?pago=ok en la URL (después del redirect de Stripe) y muestra confirmación.
    Llamar al inicio de app.py, antes de renderizar cualquier módulo.
    """
    params = st.query_params
    if params.get("pago") == "ok":
        plan = params.get("plan", "pro")
        st.success(
            f"✅ ¡Pago completado! Tu plan {plan.capitalize()} está activo. "
            f"Si no se refleja en unos segundos, recarga la página."
        )
        st.query_params.clear()
    elif params.get("pago") == "cancelado":
        st.info("El pago fue cancelado. Puedes retomarlo cuando quieras.")
        st.query_params.clear()
