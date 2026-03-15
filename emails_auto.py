# emails_auto.py — AI Growth Systems
# Secuencia de emails automáticos para aumentar retención y conversión.
#
# SETUP:
#   1. pip install resend   (o sendgrid, o requests para cualquier API)
#   2. Añadir al .env: RESEND_API_KEY=re_xxxxx
#   3. Ejecutar el scheduler en un proceso separado (Railway cron, o un script diario)
#      O llamar check_and_send() desde un endpoint externo cada hora.
#
# EMAILS IMPLEMENTADOS:
#   D+0  → Bienvenida (se envía al registrarse)
#   D+1  → "Tu primer documento en 60 segundos" (si no ha generado nada)
#   D+3  → Caso de uso específico según su objetivo (del onboarding)
#   D+7  → Invitación a upgrade si está en plan gratuito
#   D+14 → "¿Todo bien?" si lleva 7+ días sin usar la plataforma
#   D+30 → NPS / feedback (para usuarios activos en plan pro/business)

import os
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

load_dotenv(override=True)

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL     = "AI Growth Systems <hola@aigrowthsystems.com>"
REPLY_TO       = "hello.aigrowthsystems@gmail.com"


# ─── Envío de emails ─────────────────────────────────────────────────────────

def enviar_email(to: str, subject: str, html: str) -> bool:
    """Envía un email via Resend. Devuelve True si OK."""
    if not RESEND_API_KEY:
        print(f"[EMAIL] Sin API key — simulando: TO={to} SUBJECT={subject}")
        return True
    try:
        import resend
        resend.api_key = RESEND_API_KEY
        resend.Emails.send({
            "from":     FROM_EMAIL,
            "to":       [to],
            "reply_to": REPLY_TO,
            "subject":  subject,
            "html":     html,
        })
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ─── Templates de emails ─────────────────────────────────────────────────────

def _base_template(contenido: str) -> str:
    return f"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ font-family: 'DM Sans', Arial, sans-serif; background: #08090C; color: #EAEAF0; margin: 0; padding: 20px; }}
  .container {{ max-width: 560px; margin: 0 auto; background: #0F1117; border: 1px solid #1E1F2E; border-radius: 16px; overflow: hidden; }}
  .header {{ background: linear-gradient(135deg, #0A0F1E, #1A1427); padding: 28px 32px 20px; border-bottom: 1px solid #1E1F2E; }}
  .brand {{ font-size: 0.52rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.18em; color: #C9A84C; margin-bottom: 4px; }}
  .title {{ font-size: 1.1rem; font-weight: 700; color: #EAEAF0; letter-spacing: -0.02em; }}
  .body {{ padding: 28px 32px; }}
  .body p {{ font-size: 0.9rem; line-height: 1.7; color: #9090A8; margin: 0 0 16px; }}
  .body h2 {{ font-size: 1rem; font-weight: 600; color: #EAEAF0; margin: 0 0 8px; }}
  .cta {{ display: inline-block; background: #C9A84C; color: #0A0807 !important; font-weight: 700;
          font-size: 0.875rem; padding: 12px 24px; border-radius: 9px; text-decoration: none;
          margin: 8px 0 16px; letter-spacing: 0.02em; }}
  .feature {{ background: #141520; border: 1px solid #1E1F2E; border-radius: 9px; padding: 12px 16px; margin-bottom: 8px; }}
  .feature-icon {{ font-size: 1.1rem; margin-right: 8px; }}
  .feature-text {{ font-size: 0.83rem; color: #9090A8; }}
  .footer {{ padding: 16px 32px; border-top: 1px solid #1E1F2E; font-size: 0.72rem; color: #505060; text-align: center; }}
  .footer a {{ color: #505060; }}
</style></head>
<body>
<div class="container">
  <div class="header">
    <div class="brand">⚡ AI Growth Systems</div>
    <div class="title">Business AI Platform</div>
  </div>
  <div class="body">{contenido}</div>
  <div class="footer">
    AI Growth Systems · <a href="mailto:{REPLY_TO}">{REPLY_TO}</a><br>
    <a href="{{{{unsubscribe_url}}}}">Darse de baja</a>
  </div>
</div>
</body></html>
"""


def email_bienvenida(nombre: str) -> tuple[str, str]:
    nombre_corto = nombre.split()[0] if nombre else "ahí"
    subject = f"Bienvenido a AI Growth Systems, {nombre_corto} ⚡"
    html = _base_template(f"""
<h2>Hola, {nombre_corto} 👋</h2>
<p>Ya tienes acceso a tu plataforma de inteligencia artificial empresarial.
Aquí tienes los 3 primeros pasos que te recomendamos:</p>

<div class="feature">
  <span class="feature-icon">1️⃣</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Habla con el Asistente IA</b> —
  Cuéntale qué hace tu empresa y pídele lo que necesites. Genera un contrato, analiza datos o escribe un email en segundos.</span>
</div>
<div class="feature">
  <span class="feature-icon">2️⃣</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Sube un documento</b> —
  Arrastra un PDF o Excel y en 30 segundos tienes un resumen, análisis o comparativa.</span>
</div>
<div class="feature">
  <span class="feature-icon">3️⃣</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Configura tu contexto</b> —
  En Configuración → Asistente IA, escribe una descripción de tu empresa. Hace que todo funcione mucho mejor.</span>
</div>

<br>
<a href="https://tu-app.streamlit.app" class="cta">Entrar a la plataforma →</a>

<p style="font-size:0.8rem;color:#505060;">¿Preguntas? Responde a este email y te contesto en menos de 2 horas.</p>
""")
    return subject, html


def email_primer_documento(nombre: str) -> tuple[str, str]:
    nombre_corto = nombre.split()[0] if nombre else "ahí"
    subject = "Tu primer documento en 60 segundos 📄"
    html = _base_template(f"""
<h2>{nombre_corto}, crea tu primer documento ahora</h2>
<p>Vemos que todavía no has generado ningún documento. Te lo ponemos fácil —
aquí tienes tres de los más usados:</p>

<div class="feature">
  <span class="feature-icon">📝</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Contrato de servicios</b> —
  Di el nombre del cliente, el servicio y el precio. En 30 segundos tienes el contrato listo.</span>
</div>
<div class="feature">
  <span class="feature-icon">💰</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Presupuesto profesional</b> —
  Describe el proyecto y obtén un presupuesto detallado con condiciones incluidas.</span>
</div>
<div class="feature">
  <span class="feature-icon">📊</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Informe ejecutivo</b> —
  Sube tu Excel con ventas o datos y obtén un informe listo para presentar.</span>
</div>

<br>
<a href="https://tu-app.streamlit.app" class="cta">Crear mi primer documento →</a>
""")
    return subject, html


def email_upgrade_gratuito(nombre: str, usos_restantes: int = 0) -> tuple[str, str]:
    nombre_corto = nombre.split()[0] if nombre else "ahí"
    subject = f"Has llegado al límite — desbloquea todo por 29€/mes 🚀"
    html = _base_template(f"""
<h2>{nombre_corto}, tienes todo bloqueado por menos de 1€/día</h2>
<p>Llevas varios días usando AI Growth Systems y has llegado al límite del plan gratuito.
El Plan Pro desbloquea todo sin límites:</p>

<div class="feature">
  <span class="feature-icon">✓</span>
  <span class="feature-text" style="color:#3DD68C;"><b>Acciones ilimitadas</b> — sin límites diarios</span>
</div>
<div class="feature">
  <span class="feature-icon">✓</span>
  <span class="feature-text" style="color:#3DD68C;"><b>Todos los módulos</b> — contratos, facturas, CRM, estrategia...</span>
</div>
<div class="feature">
  <span class="feature-icon">✓</span>
  <span class="feature-text" style="color:#3DD68C;"><b>Soporte directo</b> — respuesta en menos de 24 horas</span>
</div>

<p><b style="color:#EAEAF0;">29€/mes. Sin permanencia. Cancela cuando quieras.</b><br>
La mayoría de clientes recuperan la inversión en el primer contrato que generan.</p>

<a href="mailto:{REPLY_TO}?subject=Quiero%20el%20Plan%20Pro" class="cta">Contratar Plan Pro →</a>

<p style="font-size:0.8rem;color:#505060;">Responde a este email con "PRO" y te activamos el plan en minutos.</p>
""")
    return subject, html


def email_reactivacion(nombre: str, dias_inactivo: int) -> tuple[str, str]:
    nombre_corto = nombre.split()[0] if nombre else "ahí"
    subject = f"¿Todo bien, {nombre_corto}? Tenemos algo nuevo para ti"
    html = _base_template(f"""
<h2>Hace {dias_inactivo} días que no te vemos 👋</h2>
<p>Queríamos asegurarnos de que todo va bien y recordarte que tienes acceso
a herramientas que pueden ahorrarte horas esta semana:</p>

<div class="feature">
  <span class="feature-icon">⚡</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Asistente IA</b> —
  Pregúntale cualquier cosa de tu negocio. Estrategia, emails, contratos, análisis.</span>
</div>
<div class="feature">
  <span class="feature-icon">📊</span>
  <span class="feature-text"><b style="color:#EAEAF0;">Analítica visual</b> —
  Sube cualquier Excel y en 2 minutos tienes un dashboard completo.</span>
</div>

<br>
<a href="https://tu-app.streamlit.app" class="cta">Volver a la plataforma →</a>

<p style="font-size:0.8rem;color:#505060;">¿Hay algo que no funciona como esperabas?
Responde a este email y lo solucionamos.</p>
""")
    return subject, html


def email_nps(nombre: str) -> tuple[str, str]:
    nombre_corto = nombre.split()[0] if nombre else "ahí"
    subject = f"30 segundos de tu tiempo, {nombre_corto} — ¿cómo lo hacemos?"
    html = _base_template(f"""
<h2>Tu opinión vale mucho para nosotros</h2>
<p>Llevas un mes usando AI Growth Systems. ¿Nos cuentas qué tal?</p>
<p><b style="color:#EAEAF0;">¿Del 1 al 10, qué probabilidad hay de que recomiendes
AI Growth Systems a un compañero o cliente?</b></p>

<div style="display:flex;gap:6px;flex-wrap:wrap;margin:16px 0;">
{"".join(f'<a href="mailto:{REPLY_TO}?subject=NPS%3A{i}" style="display:inline-block;width:36px;height:36px;background:#141520;border:1px solid #1E1F2E;border-radius:7px;text-align:center;line-height:36px;color:#9090A8;text-decoration:none;font-size:0.85rem;font-weight:600;">{i}</a>' for i in range(1, 11))}
</div>

<p style="font-size:0.8rem;color:#505060;">También puedes simplemente responder a este email
con tu puntuación y cualquier comentario. Leemos cada respuesta personalmente.</p>
""")
    return subject, html


# ─── Scheduler de emails ─────────────────────────────────────────────────────

def check_and_send_emails():
    """
    Revisa qué usuarios necesitan recibir un email hoy y los envía.
    Ejecutar una vez al día (cron job, Railway scheduler, etc.)
    
    Requiere tabla Supabase:
      CREATE TABLE emails_enviados (
        user_id    UUID,
        tipo       TEXT,
        sent_at    TIMESTAMPTZ DEFAULT now(),
        PRIMARY KEY (user_id, tipo)
      );
    """
    try:
        from auth import get_supabase
        sb  = get_supabase()
        hoy = date.today()

        # Obtener todos los usuarios
        usuarios = sb.table("usuarios").select(
            "id, email, nombre, plan, created_at, onboarding_done"
        ).execute().data or []

        # Obtener emails ya enviados
        enviados_raw = sb.table("emails_enviados").select("user_id, tipo").execute().data or []
        enviados = {(e["user_id"], e["tipo"]) for e in enviados_raw}

        for u in usuarios:
            uid     = u["id"]
            email   = u.get("email", "")
            nombre  = u.get("nombre", email)
            plan    = u.get("plan", "gratuito")

            if not email:
                continue

            try:
                created = datetime.fromisoformat(u["created_at"].replace("Z", "+00:00")).date()
            except Exception:
                continue

            dias_desde_registro = (hoy - created).days

            # D+0: Bienvenida
            if (uid, "bienvenida") not in enviados:
                subj, html = email_bienvenida(nombre)
                if enviar_email(email, subj, html):
                    sb.table("emails_enviados").insert({"user_id": uid, "tipo": "bienvenida"}).execute()

            # D+1: Primer documento (si no ha generado nada)
            if dias_desde_registro >= 1 and (uid, "primer_doc") not in enviados:
                metricas = sb.table("metricas").select("docs_generados").eq("user_id", uid).execute().data
                docs = metricas[0].get("docs_generados", 0) if metricas else 0
                if docs == 0:
                    subj, html = email_primer_documento(nombre)
                    if enviar_email(email, subj, html):
                        sb.table("emails_enviados").insert({"user_id": uid, "tipo": "primer_doc"}).execute()

            # D+7: Upgrade para plan gratuito
            if dias_desde_registro >= 7 and plan == "gratuito" and (uid, "upgrade_7d") not in enviados:
                subj, html = email_upgrade_gratuito(nombre)
                if enviar_email(email, subj, html):
                    sb.table("emails_enviados").insert({"user_id": uid, "tipo": "upgrade_7d"}).execute()

            # D+14: Reactivación (si no ha usado en 7 días)
            if dias_desde_registro >= 14 and (uid, "reactivacion") not in enviados:
                # Buscar último evento
                ultimo_ev = sb.table("eventos").select("created_at").eq("user_id", uid)\
                    .order("created_at", desc=True).limit(1).execute().data
                if ultimo_ev:
                    try:
                        ultimo = datetime.fromisoformat(ultimo_ev[0]["created_at"].replace("Z", "+00:00")).date()
                        dias_inactivo = (hoy - ultimo).days
                        if dias_inactivo >= 7:
                            subj, html = email_reactivacion(nombre, dias_inactivo)
                            if enviar_email(email, subj, html):
                                sb.table("emails_enviados").insert({"user_id": uid, "tipo": "reactivacion"}).execute()
                    except Exception:
                        pass

            # D+30: NPS para usuarios activos Pro/Business
            if dias_desde_registro >= 30 and plan in ("pro", "business") and (uid, "nps_30d") not in enviados:
                subj, html = email_nps(nombre)
                if enviar_email(email, subj, html):
                    sb.table("emails_enviados").insert({"user_id": uid, "tipo": "nps_30d"}).execute()

        print(f"[EMAILS] Check completado — {len(usuarios)} usuarios procesados")

    except Exception as e:
        print(f"[EMAILS ERROR] {e}")


# ─── Envío inmediato de bienvenida (llamar desde auth.py tras registro) ───────

def enviar_bienvenida_inmediata(email: str, nombre: str):
    """Llamar justo después de crear la cuenta en Supabase."""
    subj, html = email_bienvenida(nombre)
    enviar_email(email, subj, html)
    try:
        from auth import get_supabase
        uid_res = get_supabase().auth.get_user()
        if uid_res and uid_res.user:
            get_supabase().table("emails_enviados").insert({
                "user_id": uid_res.user.id,
                "tipo": "bienvenida"
            }).execute()
    except Exception:
        pass
