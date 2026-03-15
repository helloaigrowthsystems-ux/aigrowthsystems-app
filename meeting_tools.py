# meeting_tools.py — AImpulsa v2
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

def resumir_reunion(transcripcion, tipo_reunion="general"):
    return _llamar(f"""Analiza esta transcripción/notas de reunión y genera un resumen ejecutivo profesional:

Tipo de reunión: {tipo_reunion}

Transcripción/Notas:
{transcripcion[:6000]}

Genera:
## RESUMEN EJECUTIVO
(3-4 líneas con lo más importante)

## DECISIONES TOMADAS
(lista numerada de cada decisión)

## ACUERDOS Y COMPROMISOS
(quién hace qué y para cuándo — formato tabla)

## PRÓXIMOS PASOS
(acciones concretas con responsable y fecha)

## PUNTOS PENDIENTES
(temas que quedaron sin resolver)

## FECHA PRÓXIMA REUNIÓN
(si se mencionó)""", max_tokens=2500)

def generar_agenda_reunion(datos):
    return _llamar(f"""Crea una agenda de reunión profesional y eficiente:

Tipo de reunión: {datos.get('tipo')}
Duración: {datos.get('duracion', '60 minutos')}
Participantes: {datos.get('participantes')}
Objetivo principal: {datos.get('objetivo')}
Temas a tratar: {datos.get('temas')}
Decisiones que deben tomarse: {datos.get('decisiones', 'no especificadas')}

Genera agenda con:
- Título y objetivo de la reunión
- Participantes y roles
- Cronograma minuto a minuto (con tiempo para cada punto)
- Documentación a preparar con antelación
- Reglas de la reunión (si aplica)
- Plantilla para acuerdos y próximos pasos""")

def generar_presentacion_outline(datos):
    return _llamar(f"""Crea el guión completo de una presentación de negocios:

Tema: {datos.get('tema')}
Audiencia: {datos.get('audiencia')}
Objetivo: {datos.get('objetivo')}
Duración: {datos.get('duracion', '20 minutos')}
Datos disponibles: {datos.get('datos', 'no especificados')}
Acción deseada del público: {datos.get('accion_deseada')}

Para cada slide proporciona:
- Número y título del slide
- Mensaje clave (1 frase)
- Contenido sugerido (bullets, datos, gráficos)
- Notas del presentador (qué decir)
- Tiempo asignado

Incluye también: gancho de apertura, estructura narrativa y cierre con CTA.""", max_tokens=3000)

def redactar_acta_reunion(datos):
    return _llamar(f"""Redacta un acta formal de reunión:

Empresa: {datos.get('empresa')}
Tipo de reunión: {datos.get('tipo')}
Fecha: {datos.get('fecha')}
Hora: {datos.get('hora', 'no especificada')}
Lugar/Plataforma: {datos.get('lugar', 'no especificado')}
Asistentes: {datos.get('asistentes')}
Convocante: {datos.get('convocante', 'no especificado')}
Puntos tratados: {datos.get('puntos')}
Acuerdos: {datos.get('acuerdos')}
Próxima reunión: {datos.get('proxima', 'por determinar')}

Formato oficial con numeración, firmas y todo lo requerido para validez jurídica.""")

def generar_email_seguimiento_reunion(datos):
    return _llamar(f"""Genera un email de seguimiento post-reunión:

Remitente: {datos.get('remitente')}
Destinatarios: {datos.get('destinatarios')}
Tema de la reunión: {datos.get('tema')}
Fecha de la reunión: {datos.get('fecha')}
Acuerdos principales: {datos.get('acuerdos')}
Próximos pasos: {datos.get('proximos_pasos')}

Email profesional con: asunto claro, resumen de lo acordado, próximos pasos con responsables y fechas,
y CTA para confirmar o corregir si algo no es correcto.
Incluye ASUNTO al inicio con formato 'ASUNTO: ...'""")