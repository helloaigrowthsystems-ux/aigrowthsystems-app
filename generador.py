# generador.py — AImpulsa v2
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

def generar_contrato(datos):
    return _llamar(f"""Genera un contrato profesional completo en español:

Tipo: {datos.get('tipo')} | Proveedor: {datos.get('proveedor')} | Cliente: {datos.get('cliente')}
Servicio: {datos.get('servicio')} | Importe: {datos.get('importe')}
Duración: {datos.get('duracion')} | Fecha inicio: {datos.get('fecha_inicio')}

Incluye: encabezado, identificación de partes, objeto, precio y forma de pago, duración y renovación,
obligaciones de cada parte, confidencialidad, rescisión, resolución de conflictos y firmas.
Redacción profesional y legalmente sólida.""")

def generar_presupuesto(datos):
    return _llamar(f"""Genera un presupuesto profesional completo en español:

Empresa: {datos.get('empresa')} | Cliente: {datos.get('cliente')}
Servicios/Productos: {datos.get('servicios')}
Validez: {datos.get('validez')} | Fecha: {datos.get('fecha')}

Incluye: encabezado con datos empresa y cliente, tabla de servicios con precios,
subtotal, IVA (21%), total, condiciones de pago, validez y firma.
Formato claro, profesional y presentable.""", max_tokens=2500)

def generar_informe(datos):
    return _llamar(f"""Genera un informe ejecutivo profesional completo en español:

Empresa: {datos.get('empresa')} | Tema: {datos.get('tema')}
Período: {datos.get('periodo')} | Datos clave: {datos.get('datos')}

Incluye: resumen ejecutivo, contexto y objetivos, análisis de datos,
hallazgos principales, conclusiones y recomendaciones accionables.
Tono ejecutivo, claro y orientado a la toma de decisiones.""", max_tokens=2500)

def generar_carta_reclamacion(datos):
    return _llamar(f"""Genera una carta de reclamación formal y contundente:

De: {datos.get('remitente')} | Para: {datos.get('destinatario')}
Asunto: {datos.get('asunto')} | Importe: {datos.get('importe', 'no aplica')}
Situación: {datos.get('descripcion')}

Incluye: fecha, datos de las partes, exposición de hechos, reclamación concreta,
plazo de 10 días hábiles para responder y advertencia de acciones legales.
Tono firme, profesional y legalmente sólido.""", max_tokens=1500)

def generar_acuerdo_colaboracion(datos):
    return _llamar(f"""Genera un acuerdo de colaboración profesional:

Parte A: {datos.get('parte_a')} | Parte B: {datos.get('parte_b')}
Objetivo de la colaboración: {datos.get('objetivo')}
Duración: {datos.get('duracion')} | Compensación: {datos.get('compensacion', 'no aplica')}
Reparto de responsabilidades: {datos.get('responsabilidades', 'a definir')}

Incluye: partes, objeto, obligaciones de cada parte, reparto de beneficios/costes,
exclusividad, confidencialidad, duración, terminación y ley aplicable.""", max_tokens=2500)