# legal_tools.py — AImpulsa v2
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _llamar(prompt, max_tokens=3000):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def generar_politica_privacidad(datos):
    return _llamar(f"""Genera una Política de Privacidad completa y conforme al RGPD (Reglamento General de Protección de Datos) para:

Empresa: {datos.get('empresa')}
CIF/NIF: {datos.get('cif', '[A RELLENAR]')}
Domicilio: {datos.get('domicilio', '[A RELLENAR]')}
Email DPO/contacto: {datos.get('email', '[A RELLENAR]')}
Tipo de negocio: {datos.get('tipo_negocio')}
Datos que recoge: {datos.get('datos_recoge')}
Finalidad: {datos.get('finalidad')}
Cookies: {datos.get('cookies', 'sí, analíticas y de sesión')}

Incluye todas las secciones obligatorias del RGPD:
responsable del tratamiento, datos recogidos, finalidad y base legal,
derechos del usuario (acceso, rectificación, supresión, portabilidad, oposición),
conservación de datos, transferencias internacionales si aplica, y cookies.""", max_tokens=3500)

def generar_aviso_legal(datos):
    return _llamar(f"""Genera un Aviso Legal completo para web española, conforme a la LSSI-CE:

Empresa: {datos.get('empresa')}
CIF/NIF: {datos.get('cif', '[A RELLENAR]')}
Domicilio: {datos.get('domicilio', '[A RELLENAR]')}
Registro Mercantil: {datos.get('registro', '[A RELLENAR]')}
Email: {datos.get('email', '[A RELLENAR]')}
Web: {datos.get('web', '[A RELLENAR]')}
Actividad: {datos.get('actividad')}

Incluye: identificación del titular, condiciones de uso, propiedad intelectual,
limitación de responsabilidad, ley aplicable y jurisdicción.""", max_tokens=2500)

def generar_terminos_condiciones(datos):
    return _llamar(f"""Genera unos Términos y Condiciones completos para:

Empresa/Servicio: {datos.get('empresa')}
Tipo de servicio: {datos.get('tipo_servicio')}
Precio: {datos.get('precio', 'variable')}
Forma de pago: {datos.get('pago', 'tarjeta y transferencia')}
Política de devoluciones: {datos.get('devoluciones', '14 días para consumidores')}
Jurisdicción: {datos.get('jurisdiccion', 'España, Juzgados de Madrid')}

Incluye: objeto, registro y cuenta, precios y pagos, cancelaciones y devoluciones,
propiedad intelectual, responsabilidad del usuario, suspensión del servicio,
ley aplicable y resolución de disputas.""", max_tokens=3000)

def generar_politica_cookies(datos):
    return _llamar(f"""Genera una Política de Cookies completa y conforme a normativa europea para:

Empresa: {datos.get('empresa')}
Web: {datos.get('web', '[A RELLENAR]')}
Cookies propias: {datos.get('cookies_propias', 'sesión, preferencias')}
Cookies terceros: {datos.get('cookies_terceros', 'Google Analytics, Google Ads')}
¿Tiene banner de cookies? {datos.get('tiene_banner', 'sí')}

Incluye: qué son las cookies, tipos utilizados (tabla), finalidad de cada una,
cómo desactivarlas en cada navegador, y actualización de la política.""", max_tokens=2500)

def simplificar_contrato(texto_contrato):
    return _llamar(f"""Simplifica este contrato legal a lenguaje claro y comprensible para alguien sin formación jurídica.

Para cada cláusula importante:
1. Explica qué significa en lenguaje sencillo
2. Indica si es favorable, desfavorable o neutra para el firmante
3. Señala si hay algo que deba negociarse o aclararse

Contrato:
{texto_contrato[:8000]}

Mantén la estructura del contrato pero en lenguaje accesible.""", max_tokens=3000)