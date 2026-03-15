# ai_processor.py — AImpulsa v2
from groq import Groq
import os, json, re
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def _llamar(prompt, max_tokens=2000, system=None):
    mensajes = []
    if system:
        mensajes.append({"role": "system", "content": system})
    mensajes.append({"role": "user", "content": prompt})
    try:
        res = client.chat.completions.create(model=MODEL, messages=mensajes, max_tokens=max_tokens)
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def procesar_documento(texto, instruccion):
    prompt = f"Instrucción: {instruccion}\n\nDocumento:\n{texto[:6000]}\n\nResponde SOLO en formato JSON limpio y válido, sin markdown, sin explicaciones."
    return _llamar(prompt, max_tokens=2000)

def procesar_pregunta(texto, pregunta):
    prompt = f"Basándote en este documento, responde de forma clara y estructurada:\n\nPregunta: {pregunta}\n\nDocumento:\n{texto[:6000]}"
    return _llamar(prompt, max_tokens=2000)

def analizar_datos_empresa(datos_csv, tipo_analisis):
    prompts = {
        "tendencias": "Analiza estos datos empresariales. Identifica tendencias principales, patrones y qué dicen los números sobre el estado del negocio. Sé muy específico con cifras.",
        "recomendaciones": "Dame 6 recomendaciones concretas y accionables para mejorar el negocio basándote en estos datos. Para cada una indica: qué hacer, por qué, impacto esperado en euros o %.",
        "anomalias": "Detecta anomalías, valores atípicos, problemas e inconsistencias en estos datos. Explica causas probables y acciones correctoras.",
        "ejecutivo": "Genera un resumen ejecutivo para presentar a dirección. Incluye: situación actual, métricas clave, hallazgos críticos, conclusiones y próximos pasos.",
        "previsiones": "Basándote en los datos históricos, genera previsiones para los próximos 3 meses con rangos optimista/realista/pesimista. Justifica cada previsión.",
    }
    prompt = f"{prompts.get(tipo_analisis, prompts['ejecutivo'])}\n\nDATOS:\n{datos_csv}"
    return _llamar(prompt, max_tokens=2500)

def generar_propuesta_comercial(datos):
    prompt = f"""Genera una propuesta comercial persuasiva y profesional en español:

Empresa vendedora: {datos.get('empresa')}
Cliente potencial: {datos.get('cliente')} (sector: {datos.get('sector', 'no indicado')})
Problema que resuelve: {datos.get('problema')}
Solución ofrecida: {datos.get('solucion')}
Precio/inversión: {datos.get('precio')}
Casos de éxito o diferenciadores: {datos.get('diferenciadores', 'ninguno indicado')}

Estructura obligatoria:
1. Resumen ejecutivo (2-3 párrafos impactantes)
2. Análisis del problema específico del cliente
3. Solución propuesta con detalles técnicos/funcionales
4. Beneficios cuantificados (tiempo ahorrado, dinero ahorrado, ingresos generados)
5. Casos de uso concretos para su sector
6. ROI estimado con cálculo detallado
7. Precio e inversión con desglose
8. Garantías y condiciones
9. Próximos pasos y llamada a la acción urgente

Tono: profesional, persuasivo, orientado a resultados. Usa datos y cifras concretas."""
    return _llamar(prompt, max_tokens=3000)

def optimizar_precio(datos_producto):
    prompt = f"""Analiza estos datos y recomienda una estrategia de precios optimizada:

Producto/Servicio: {datos_producto.get('producto')}
Precio actual: {datos_producto.get('precio_actual')}
Coste: {datos_producto.get('coste')}
Competidores y precios: {datos_producto.get('competidores', 'no indicado')}
Segmento cliente: {datos_producto.get('segmento', 'no indicado')}
Volumen ventas mensual: {datos_producto.get('volumen', 'no indicado')}

Proporciona:
1. Análisis del margen actual vs óptimo
2. Precio recomendado con justificación
3. Estrategia de precios diferenciados (básico/pro/enterprise si aplica)
4. Impacto estimado en ingresos mensuales del cambio de precio
5. Riesgos y cómo mitigarlos
6. Táctica de comunicación del precio al cliente"""
    return _llamar(prompt, max_tokens=2000)

def generar_email_cobro(datos):
    niveles = {
        "recordatorio": "amable primer recordatorio, tono cordial, asume que fue un olvido",
        "urgente": "segundo aviso, tono firme pero profesional, indica consecuencias si no se paga",
        "ultimatum": "último aviso antes de acciones legales, tono muy firme, menciona vía judicial y reporte a ficheros de morosos",
    }
    prompt = f"""Escribe un email de cobro de factura impagada. Nivel: {niveles.get(datos.get('nivel','recordatorio'))}.

Remitente: {datos.get('remitente')}
Destinatario: {datos.get('destinatario')}
Importe: {datos.get('importe')}
Factura nº: {datos.get('factura', 'no indicada')}
Vencimiento: {datos.get('vencimiento', 'ya vencida')}
Días de retraso: {datos.get('dias_retraso', 'no indicado')}

Incluye ASUNTO al inicio con formato 'ASUNTO: ...' y luego el cuerpo del email."""
    return _llamar(prompt, max_tokens=800)

def analizar_contrato_riesgos(texto_contrato):
    prompt = f"""Analiza este contrato como un abogado experto y detecta:

1. CLÁUSULAS DE RIESGO ALTO: cláusulas que podrían perjudicar al cliente
2. CLÁUSULAS FAVORABLES: puntos positivos para negociar
3. AUSENCIAS IMPORTANTES: qué falta y debería estar incluido
4. PUNTOS A NEGOCIAR: qué pedir que se modifique antes de firmar
5. RESUMEN EJECUTIVO: decisión recomendada (firmar / negociar / rechazar) con justificación

Contrato:\n{texto_contrato[:8000]}

Sé muy específico, cita las cláusulas por nombre o número cuando sea posible."""
    return _llamar(prompt, max_tokens=3000)

def generar_descripcion_vacante(datos):
    prompt = f"""Genera una descripción de vacante atractiva y profesional:

Puesto: {datos.get('puesto')}
Empresa: {datos.get('empresa')}
Sector: {datos.get('sector', 'no indicado')}
Salario: {datos.get('salario', 'a negociar')}
Modalidad: {datos.get('modalidad', 'presencial')}
Requisitos clave: {datos.get('requisitos')}
Beneficios: {datos.get('beneficios', 'no indicado')}

Incluye: título atractivo, resumen del rol, responsabilidades (bullet points), requisitos imprescindibles vs valorables, qué ofrecemos, y llamada a la acción."""
    return _llamar(prompt, max_tokens=1500)