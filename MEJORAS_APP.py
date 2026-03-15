# MEJORAS_APP.py — AI Growth Systems
# ══════════════════════════════════════════════════════════════════════════════
# PARCHE DE INTEGRACIÓN
# Este archivo documenta exactamente qué cambiar en app.py para activar
# todas las mejoras. Son cambios quirúrgicos — no reescribes nada, solo añades.
# ══════════════════════════════════════════════════════════════════════════════
#
# CAMBIO 1 — Al inicio de app.py, después de los imports existentes:
# ─────────────────────────────────────────────────────────────────────────────

IMPORTS_A_AÑADIR = """
from styles import inject_css               # CSS centralizado
from onboarding import necesita_onboarding, mostrar_onboarding  # Activación
from payments import verificar_pago_exitoso, mostrar_pricing_upgrade  # Stripe
from analytics import track, track_inicio_modulo, track_resultado, track_upgrade_intent  # Métricas
"""

# CAMBIO 2 — Sustituir el bloque st.markdown(CSS...) de app.py por:
# ─────────────────────────────────────────────────────────────────────────────

SUSTITUIR_CSS = """
# ANTES (borrar estas ~200 líneas de CSS inline en app.py):
#   st.markdown(\"\"\"<style>@import url(...)...</style>\"\"\", unsafe_allow_html=True)
#
# DESPUÉS (una sola línea):
inject_css()
"""

# CAMBIO 3 — Después del bloque de autenticación (if "usuario" not in st.session_state):
# ─────────────────────────────────────────────────────────────────────────────

BLOQUE_ONBOARDING = """
# Pegar justo después de validar que el usuario está logueado:

verificar_pago_exitoso()  # detecta ?pago=ok de Stripe redirect

if necesita_onboarding():
    st.markdown("<div style='padding:40px 20px;max-width:600px;margin:0 auto;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Sora,sans-serif;font-size:0.52rem;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.18em;color:#C9A84C;text-align:center;margin-bottom:24px;'>"
        "⚡ AI Growth Systems — Configuración inicial</div>",
        unsafe_allow_html=True
    )
    from onboarding import mostrar_onboarding
    if mostrar_onboarding():
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
"""

# CAMBIO 4 — En la función _bloquear_si_sin_acceso, añadir tracking:
# ─────────────────────────────────────────────────────────────────────────────

BLOQUE_TRACKING_UPGRADE = """
# En _bloquear_si_sin_acceso(nombre), justo antes del return True:
track_upgrade_intent(nombre)
"""

# CAMBIO 5 — En cada módulo, añadir tracking al inicio y al generar resultado:
# ─────────────────────────────────────────────────────────────────────────────

EJEMPLO_TRACKING_MODULO = """
# Al entrar a cada módulo (ej: elif modulo == "Crear documento":)
track_inicio_modulo("Crear documento")

# Al generar resultado exitoso (donde hoy llamas registrar_accion):
track_resultado("Crear documento", {"tipo": tipo_doc_elegido})
# (además de registrar_uso() que ya tienes)
"""

# CAMBIO 6 — Sustituir el bloque de pricing en Configuración → Plan y facturación:
# ─────────────────────────────────────────────────────────────────────────────

BLOQUE_PRICING_NUEVO = """
# En el tab_plan de Configuración, sustituir el bloque de "Actualizar a Pro" por:
from payments import mostrar_pricing_upgrade
mostrar_pricing_upgrade(plan_actual=plan_actual_cfg)
"""

# CAMBIO 7 — En la función _hacer_registro de auth.py, añadir email de bienvenida:
# ─────────────────────────────────────────────────────────────────────────────

BLOQUE_EMAIL_BIENVENIDA = """
# En auth.py, _hacer_registro(), justo después del st.success("✅ Cuenta creada..."):
try:
    from emails_auto import enviar_bienvenida_inmediata
    enviar_bienvenida_inmediata(email, nombre)
except Exception:
    pass  # nunca romper el registro por un email fallido
"""

# CAMBIO 8 — En el módulo "Gestión de empresas" (admin), añadir analytics:
# ─────────────────────────────────────────────────────────────────────────────

BLOQUE_ANALYTICS_ADMIN = """
# En elif modulo == "Gestión de empresas": (o crear un tab nuevo "Analytics")
if es_admin:
    from analytics import mostrar_analytics_admin
    mostrar_analytics_admin()
"""

# ══════════════════════════════════════════════════════════════════════════════
# SUPABASE: TABLAS NUEVAS NECESARIAS
# Ejecutar en Supabase SQL Editor
# ══════════════════════════════════════════════════════════════════════════════

SUPABASE_SQL = """
-- 1. Añadir columnas a la tabla usuarios existente
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS onboarding_done BOOLEAN DEFAULT FALSE;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS sector TEXT;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS tamanio TEXT;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS objetivo TEXT;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS stripe_subscription_id TEXT;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT;

-- 2. Tabla de eventos de analytics
CREATE TABLE IF NOT EXISTS eventos (
    id         BIGSERIAL PRIMARY KEY,
    user_id    UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    modulo     TEXT NOT NULL,
    accion     TEXT NOT NULL,
    metadata   JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_eventos_user_id    ON eventos(user_id);
CREATE INDEX IF NOT EXISTS idx_eventos_modulo     ON eventos(modulo);
CREATE INDEX IF NOT EXISTS idx_eventos_created_at ON eventos(created_at);

-- 3. Tabla de emails enviados (evita duplicados)
CREATE TABLE IF NOT EXISTS emails_enviados (
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    tipo    TEXT NOT NULL,
    sent_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (user_id, tipo)
);

-- 4. RLS (Row Level Security) — cada usuario solo ve sus datos
ALTER TABLE eventos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "usuarios_ven_sus_eventos" ON eventos
    FOR ALL USING (auth.uid() = user_id);

ALTER TABLE emails_enviados ENABLE ROW LEVEL SECURITY;
CREATE POLICY "usuarios_ven_sus_emails" ON emails_enviados
    FOR ALL USING (auth.uid() = user_id);
"""

# ══════════════════════════════════════════════════════════════════════════════
# CHECKLIST DE DEPLOY
# ══════════════════════════════════════════════════════════════════════════════

CHECKLIST = """
□ 1. SEGURIDAD
  □ Rotar GROQ_API_KEY en groq.com/keys (la del .env está comprometida)
  □ Rotar SUPABASE_ANON_KEY en supabase.com (opcional pero recomendado)
  □ Añadir .env al .gitignore (ya hecho)
  □ Nunca subir .env a git

□ 2. SUPABASE
  □ Ejecutar el SQL de arriba en Supabase SQL Editor
  □ Verificar que las tablas se crearon correctamente

□ 3. STRIPE (para cobrar)
  □ Crear cuenta en stripe.com
  □ Crear producto "Plan Pro" (29€/mes, pago recurrente)
  □ Crear producto "Plan Business" (99€/mes)
  □ Copiar Price IDs al .env (STRIPE_PRICE_PRO, STRIPE_PRICE_BUSINESS)
  □ Copiar Secret Key al .env (STRIPE_SECRET_KEY)
  □ Desplegar webhook_stripe.py en Railway o Render
  □ Registrar el endpoint en Stripe Dashboard → Webhooks
  □ Copiar Webhook Secret al .env (STRIPE_WEBHOOK_SECRET)
  □ Actualizar success_url y cancel_url en payments.py con tu URL real

□ 4. EMAILS (para retención)
  □ Crear cuenta en resend.com (gratis hasta 3.000 emails/mes)
  □ Verificar dominio o usar resend's onboarding domain para pruebas
  □ Copiar API Key al .env (RESEND_API_KEY)
  □ Actualizar FROM_EMAIL en emails_auto.py con tu dominio verificado
  □ Configurar cron job para check_and_send_emails() (Railway scheduler)

□ 5. APP.PY
  □ Aplicar los 8 cambios documentados arriba en MEJORAS_APP.py
  □ Eliminar CSS duplicado de auth.py (reemplazar con inject_login_css())
  □ Añadir track() a los módulos más importantes

□ 6. DEPLOY FINAL
  □ Subir a Streamlit Cloud o Railway
  □ Configurar variables de entorno en la plataforma de deploy
  □ Probar flujo completo: registro → onboarding → uso → upgrade → pago
"""

if __name__ == "__main__":
    print("=" * 60)
    print("AI Growth Systems — Guía de integración de mejoras")
    print("=" * 60)
    print(CHECKLIST)
