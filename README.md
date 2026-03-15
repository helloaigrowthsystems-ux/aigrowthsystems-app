# ⚡ AI Growth Systems — Business AI Platform

> La plataforma de inteligencia artificial para pymes de 1-50 personas que quieren crecer sin contratar más.

---

## Stack

| Capa | Tecnología |
|---|---|
| Frontend / App | Streamlit |
| IA | Groq (Llama 3.3 70B) |
| Base de datos | Supabase (Postgres + Auth) |
| Pagos | Stripe Checkout |
| Emails | Resend |
| Webhook | Flask (Railway/Render) |

---

## Setup local

```bash
# 1. Clonar
git clone https://github.com/tu-usuario/ai-growth-systems.git
cd ai-growth-systems

# 2. Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Variables de entorno
cp .env .env
# Editar .env con tus credenciales

# 5. Ejecutar
streamlit run app.py
```

---

## Variables de entorno

```env
# Requeridas
GROQ_API_KEY=         # groq.com/keys
SUPABASE_URL=         # supabase.com → Settings → API
SUPABASE_ANON_KEY=    # supabase.com → Settings → API
ADMIN_EMAIL=          # tu email de admin

# Para cobrar (Stripe)
STRIPE_SECRET_KEY=    # stripe.com → Developers → API keys
STRIPE_PRICE_PRO=     # ID del precio Pro (price_xxx)
STRIPE_PRICE_BUSINESS=# ID del precio Business
STRIPE_WEBHOOK_SECRET=# stripe.com → Developers → Webhooks

# Para emails automáticos (Resend)
RESEND_API_KEY=       # resend.com
```

---

## Arquitectura de archivos

```
ai-growth-systems/
├── app.py              # App principal (Streamlit) — 3500 líneas
├── auth.py             # Autenticación y gestión de usuarios
├── styles.py           # ✨ CSS centralizado (no duplicar)
├── onboarding.py       # ✨ Wizard de activación (3 pasos)
├── payments.py         # ✨ Stripe Checkout + pricing UI
├── analytics.py        # ✨ Tracking de eventos por módulo
├── emails_auto.py      # ✨ Secuencia de emails automáticos
├── webhook_stripe.py   # ✨ Servidor Flask para webhooks de Stripe
├── MEJORAS_APP.py      # ✨ Guía de integración de mejoras
│
├── ai_processor.py     # Funciones de IA (Groq)
├── batch_processor.py  # Procesar múltiples documentos
├── chatbot.py          # Chatbot de empresa
├── crm.py              # CRM y pipeline
├── customer_service.py # Soporte al cliente
├── exportador.py       # PDF y Word
├── file_handler.py     # Procesado de archivos
├── finance_tools.py    # Análisis financiero
├── generador.py        # Generador de documentos
├── invoice_generator.py# Facturas PDF
├── legal_tools.py      # Herramientas legales
├── meeting_tools.py    # Reuniones
├── seo_content.py      # Marketing y contenido
├── strategy_tools.py   # Estrategia empresarial
├── translator.py       # Traducción
│
├── .env.example        # Template de variables (no incluye secretos)
├── .gitignore          # NUNCA commitear .env
├── requirements.txt    # Dependencias
└── README.md
```

---

## Planes

| Plan | Precio | Límite | Módulos |
|---|---|---|---|
| Demo | Gratis | 3 acciones totales | Asistente IA, Guía |
| Gratuito | Gratis | 5 acciones/día | Básicos |
| Pro | 29€/mes | Ilimitado | Todos |
| Business | 99€/mes | Ilimitado | Todos + CRM, Lote, Facturación |

---

## Tablas Supabase necesarias

Ver `MEJORAS_APP.py` → sección `SUPABASE_SQL` para el SQL completo.

Tablas principales:
- `usuarios` — perfil, plan, métricas básicas
- `metricas` — contadores de uso por usuario
- `eventos` — tracking detallado por módulo
- `emails_enviados` — control de secuencia de emails

---

## Roadmap

- [x] Plataforma base con 25+ módulos
- [x] Autenticación y planes (Supabase)
- [x] Design system dark/gold (Sora + DM Sans)
- [x] CSS centralizado (`styles.py`)
- [x] Onboarding de 3 pasos (`onboarding.py`)
- [x] Stripe Checkout (`payments.py`)
- [x] Analytics por módulo (`analytics.py`)
- [x] Emails automáticos (`emails_auto.py`)
- [x] Webhook Stripe (`webhook_stripe.py`)
- [ ] Integrar pagos en app.py (ver MEJORAS_APP.py)
- [ ] RAG real para Chatbot de empresa
- [ ] Integraciones: WhatsApp, Gmail, Zapier
- [ ] White-label para agencias revendedoras
- [ ] App móvil (Streamlit mobile / React Native)

---

## Contacto

📩 hello.aigrowthsystems@gmail.com  
🌐 [aigrowthsystems.com](https://aigrowthsystems.com)

---

*Construido con ❤️ para que las pymes compitan con recursos de gran empresa.*
