# webhook_stripe.py — AI Growth Systems
# Servidor Flask mínimo para recibir eventos de Stripe y actualizar planes.
#
# DEPLOY: Railway, Render, o Fly.io (plan gratuito).
# Este proceso es INDEPENDIENTE de Streamlit. Son ~100 líneas y 15 min de setup.
#
# Variables de entorno necesarias (las mismas del .env):
#   STRIPE_WEBHOOK_SECRET
#   SUPABASE_URL
#   SUPABASE_ANON_KEY
#
# EVENTOS MANEJADOS:
#   checkout.session.completed       → Activa el plan tras pago
#   customer.subscription.deleted   → Baja al plan gratuito al cancelar
#   invoice.payment_failed           → Notifica fallo de pago

import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
SUPABASE_URL          = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY          = os.getenv("SUPABASE_ANON_KEY", "")


def get_supabase_client():
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def actualizar_plan(uid: str, plan: str):
    try:
        sb = get_supabase_client()
        sb.table("usuarios").update({"plan": plan}).eq("id", uid).execute()
        print(f"[WEBHOOK] Plan actualizado: uid={uid} → {plan}")
        return True
    except Exception as e:
        print(f"[WEBHOOK ERROR] No se pudo actualizar el plan: {e}")
        return False


def notificar_fallo_pago(email: str, nombre: str):
    """Envía email de aviso de fallo de pago."""
    try:
        from emails_auto import enviar_email, _base_template
        subj = "Problema con tu pago — AI Growth Systems"
        html = _base_template(f"""
<h2>Tuvimos un problema procesando tu pago</h2>
<p>Hola {nombre.split()[0] if nombre else 'ahí'},</p>
<p>No pudimos procesar el último pago de tu suscripción. Tu cuenta seguirá activa
durante 3 días, pero debes actualizar tu método de pago para evitar interrupciones.</p>
<a href="mailto:{os.getenv('REPLY_TO','hello.aigrowthsystems@gmail.com')}?subject=Problema%20con%20pago"
   style="display:inline-block;background:#C9A84C;color:#0A0807;font-weight:700;font-size:0.875rem;
   padding:12px 24px;border-radius:9px;text-decoration:none;margin:8px 0 16px;">
Contactar soporte →</a>
<p style="font-size:0.8rem;color:#505060;">También puedes responder directamente a este email.</p>
""")
        enviar_email(email, subj, html)
    except Exception as e:
        print(f"[WEBHOOK] No se pudo enviar email de fallo: {e}")


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

    payload   = request.data
    sig_header = request.headers.get("Stripe-Signature", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    event_type = event["type"]
    data       = event["data"]["object"]

    print(f"[WEBHOOK] Evento recibido: {event_type}")

    # ── Pago completado → activar plan ────────────────────────────────────────
    if event_type == "checkout.session.completed":
        uid  = data.get("metadata", {}).get("uid")
        plan = data.get("metadata", {}).get("plan", "pro")
        if uid:
            actualizar_plan(uid, plan)
            # También guardar subscription_id para poder cancelar
            sub_id = data.get("subscription")
            if sub_id:
                try:
                    get_supabase_client().table("usuarios").update({
                        "stripe_subscription_id": sub_id,
                        "stripe_customer_id": data.get("customer"),
                    }).eq("id", uid).execute()
                except Exception:
                    pass

    # ── Suscripción cancelada → bajar a gratuito ──────────────────────────────
    elif event_type == "customer.subscription.deleted":
        customer_id = data.get("customer")
        if customer_id:
            try:
                sb = get_supabase_client()
                res = sb.table("usuarios").select("id, email, nombre").eq(
                    "stripe_customer_id", customer_id
                ).single().execute()
                if res.data:
                    actualizar_plan(res.data["id"], "gratuito")
                    # Email de confirmación de baja
                    from emails_auto import enviar_email, _base_template
                    html = _base_template("""
<h2>Tu suscripción ha sido cancelada</h2>
<p>Tu plan ha vuelto al nivel gratuito (5 acciones/día).
Tus datos están seguros y puedes volver a Pro cuando quieras.</p>
<p style="font-size:0.8rem;color:#505060;">¿Nos cuentas por qué cancelaste?
Responde a este email — nos ayuda a mejorar.</p>
""")
                    enviar_email(
                        res.data["email"],
                        "Tu suscripción ha sido cancelada",
                        html
                    )
            except Exception as e:
                print(f"[WEBHOOK] Error en cancelación: {e}")

    # ── Fallo de pago ─────────────────────────────────────────────────────────
    elif event_type == "invoice.payment_failed":
        customer_id = data.get("customer")
        if customer_id:
            try:
                sb  = get_supabase_client()
                res = sb.table("usuarios").select("email, nombre").eq(
                    "stripe_customer_id", customer_id
                ).single().execute()
                if res.data:
                    notificar_fallo_pago(res.data["email"], res.data.get("nombre", ""))
            except Exception as e:
                print(f"[WEBHOOK] Error en fallo de pago: {e}")

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Growth Systems Webhook"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"[WEBHOOK] Servidor iniciado en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
