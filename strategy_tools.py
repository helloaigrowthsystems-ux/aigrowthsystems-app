# strategy_tools.py — AImpulsa v2
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

def generar_plan_negocio(datos):
    return _llamar(f"""Genera un plan de negocio ejecutivo completo:

Empresa/Proyecto: {datos.get('empresa')}
Sector: {datos.get('sector')}
Producto/Servicio: {datos.get('producto')}
Mercado objetivo: {datos.get('mercado')}
Propuesta de valor única: {datos.get('uvp')}
Competidores principales: {datos.get('competidores', 'no indicados')}
Inversión disponible: {datos.get('inversion', 'no indicada')}
Objetivo a 3 años: {datos.get('objetivo')}

Estructura:
1. Resumen Ejecutivo
2. Descripción del negocio y propuesta de valor
3. Análisis de mercado (TAM, SAM, SOM)
4. Análisis DAFO
5. Modelo de negocio y fuentes de ingresos
6. Estrategia de go-to-market
7. Plan de operaciones
8. Equipo y estructura organizativa
9. Proyecciones financieras (3 años)
10. Hitos y roadmap
11. Riesgos y mitigación""", max_tokens=4000)

def analizar_dafo(datos):
    return _llamar(f"""Realiza un análisis DAFO completo y estratégico:

Empresa: {datos.get('empresa')}
Sector: {datos.get('sector')}
Contexto/Situación: {datos.get('contexto')}
Información adicional: {datos.get('info_adicional', 'no proporcionada')}

Genera:
## DEBILIDADES (internas, negativas)
(mínimo 6, priorizadas por impacto)

## AMENAZAS (externas, negativas)
(mínimo 6, con probabilidad e impacto)

## FORTALEZAS (internas, positivas)
(mínimo 6, las que realmente diferencian)

## OPORTUNIDADES (externas, positivas)
(mínimo 6, con potencial cuantificado si es posible)

## ESTRATEGIAS DERIVADAS
- FO (usa fortalezas para aprovechar oportunidades): 3 estrategias
- DO (supera debilidades aprovechando oportunidades): 3 estrategias
- FA (usa fortalezas para contrarrestar amenazas): 3 estrategias
- DA (minimiza debilidades y evita amenazas): 3 estrategias

## TOP 3 ACCIONES PRIORITARIAS con justificación""")

def generar_okrs(datos):
    return _llamar(f"""Genera OKRs (Objectives and Key Results) para:

Empresa: {datos.get('empresa')}
Departamento/Equipo: {datos.get('departamento', 'toda la empresa')}
Período: {datos.get('periodo', 'Q2 2026')}
Estrategia general: {datos.get('estrategia')}
Resultados actuales: {datos.get('resultados_actuales', 'no especificados')}
Retos principales: {datos.get('retos')}

Genera 3-4 Objectives con 3-4 Key Results cada uno.
Para cada KR incluye: métrica base actual, objetivo y cómo medirlo.
Añade también: iniciativas clave sugeridas para alcanzar cada objetivo.""")

def generar_plan_marketing(datos):
    return _llamar(f"""Crea un plan de marketing completo para:

Empresa: {datos.get('empresa')}
Producto/Servicio: {datos.get('producto')}
Público objetivo: {datos.get('publico')}
Presupuesto mensual: {datos.get('presupuesto')}
Objetivo principal: {datos.get('objetivo')}
Canales actuales: {datos.get('canales_actuales', 'ninguno')}
Competidores: {datos.get('competidores', 'no indicados')}

Incluye:
1. Buyer persona detallado
2. Propuesta de valor y mensajes clave
3. Mix de canales recomendado con % de presupuesto
4. Estrategia de contenidos (qué publicar, dónde, cuándo)
5. Plan de paid media (si aplica)
6. Estrategia SEO básica
7. Email marketing y automatizaciones
8. KPIs y métricas a monitorizar
9. Calendario editorial (30 días)
10. Quick wins: 5 acciones para los primeros 15 días""", max_tokens=3500)

def generar_pitch_inversores(datos):
    return _llamar(f"""Crea un pitch deck para inversores:

Startup/Empresa: {datos.get('empresa')}
Sector: {datos.get('sector')}
Problema que resuelve: {datos.get('problema')}
Solución: {datos.get('solucion')}
Mercado total: {datos.get('mercado', 'no cuantificado')}
Modelo de negocio: {datos.get('modelo')}
Tracción actual: {datos.get('traccion', 'en fase early')}
Equipo: {datos.get('equipo', 'no detallado')}
Inversión buscada: {datos.get('inversion_buscada')}
Uso de los fondos: {datos.get('uso_fondos')}

Genera el guión completo de 10 slides:
Para cada slide: título, contenido clave, datos/métricas a incluir y mensaje que debe transmitir.
Añade también el elevator pitch de 60 segundos.""")