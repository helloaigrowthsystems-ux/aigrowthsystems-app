# customer_service.py — AImpulsa v2
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _llamar(prompt, max_tokens=2000):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def responder_queja_cliente(datos):
    return _llamar(f"""Redacta una respuesta profesional a esta queja/reclamación de cliente:

Empresa: {datos.get('empresa')}
Nombre del cliente: {datos.get('cliente')}
Queja recibida: {datos.get('queja')}
Causa real del problema: {datos.get('causa', 'en investigación')}
Solución que podemos ofrecer: {datos.get('solucion')}
Compensación disponible: {datos.get('compensacion', 'ninguna')}

Genera una respuesta que:
- Reconozca el problema sin excusas
- Se disculpe genuinamente
- Explique qué pasó (sin culpar al cliente)
- Describa la solución concreta
- Ofrezca compensación si aplica
- Retenga al cliente (enfocada en la relación)
- Sea cálida, profesional y empática
Incluye ASUNTO: al inicio.""")

def generar_faq_empresa(datos):
    return _llamar(f"""Genera una sección de Preguntas Frecuentes (FAQ) completa para:

Empresa: {datos.get('empresa')}
Sector: {datos.get('sector')}
Producto/Servicio: {datos.get('producto')}
Preguntas que suelen recibir: {datos.get('preguntas_comunes', 'no especificadas')}

Genera 15-20 preguntas frecuentes con respuestas claras y útiles, organizadas por categorías:
- Sobre el producto/servicio
- Precios y pagos
- Proceso de compra/contratación
- Soporte y garantías
- Devoluciones y cancelaciones
- Aspectos técnicos si aplica

Respuestas concisas, claras y orientadas a generar confianza.""", max_tokens=3000)

def analizar_satisfaccion_clientes(comentarios):
    return _llamar(f"""Analiza estos comentarios/reseñas de clientes y extrae inteligencia de negocio:

{comentarios[:5000]}

Genera:
1. PUNTUACIÓN MEDIA ESTIMADA de satisfacción (1-10)
2. SENTIMIENTO GENERAL (muy positivo/positivo/neutro/negativo/muy negativo)
3. TOP 5 ASPECTOS POSITIVOS más mencionados
4. TOP 5 QUEJAS O PROBLEMAS más frecuentes
5. PALABRAS CLAVE más repetidas (positivas y negativas)
6. OPORTUNIDADES DE MEJORA con prioridad (alta/media/baja)
7. RIESGO DE ABANDONO detectado
8. RECOMENDACIONES CONCRETAS para mejorar NPS
9. EJEMPLOS de respuestas modelo para los 3 tipos de comentario más frecuentes""", max_tokens=2500)

def generar_guion_llamada_ventas(datos):
    return _llamar(f"""Crea un guión completo para llamada de ventas:

Empresa vendedora: {datos.get('empresa')}
Producto/Servicio: {datos.get('producto')}
Precio: {datos.get('precio', 'a negociar')}
Perfil del prospecto: {datos.get('prospecto')}
Sector del prospecto: {datos.get('sector')}
Dolor principal: {datos.get('dolor')}
Objeciones más frecuentes: {datos.get('objeciones', 'precio, tiempo, no es el momento')}

Estructura del guión:
1. APERTURA (primeros 30 segundos — captar atención)
2. RAPPORT (1-2 minutos — conectar)
3. DIAGNÓSTICO (preguntas para descubrir necesidades)
4. PRESENTACIÓN DE SOLUCIÓN (adaptada a sus dolores)
5. MANEJO DE OBJECIONES (respuestas para cada objeción)
6. CIERRE (3 técnicas de cierre diferentes)
7. SEGUIMIENTO (si no cierra en la llamada)

Incluye frases exactas para cada fase.""", max_tokens=3000)

def crear_programa_fidelizacion(datos):
    return _llamar(f"""Diseña un programa de fidelización de clientes para:

Empresa: {datos.get('empresa')}
Sector: {datos.get('sector')}
Ticket medio: {datos.get('ticket_medio')}
Frecuencia de compra típica: {datos.get('frecuencia')}
Presupuesto para el programa: {datos.get('presupuesto', 'no especificado')}
Objetivo: {datos.get('objetivo', 'reducir churn y aumentar LTV')}

Diseña:
1. Nombre y concepto del programa
2. Niveles de membresía (ej: Bronce/Plata/Oro)
3. Sistema de puntos o recompensas
4. Beneficios exclusivos por nivel
5. Mecánica de gamificación
6. Emails de activación del programa
7. KPIs para medir el éxito
8. Herramientas recomendadas para implementarlo
9. Coste estimado vs ROI esperado""")