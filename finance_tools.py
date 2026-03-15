# finance_tools.py — AImpulsa v2
from groq import Groq
import os
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def _llamar(prompt, max_tokens=2500):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def generar_plan_financiero(datos):
    return _llamar(f"""Crea un plan financiero detallado para:

Empresa/Proyecto: {datos.get('empresa')}
Sector: {datos.get('sector')}
Fase: {datos.get('fase', 'startup / empresa establecida')}
Ingresos actuales o estimados: {datos.get('ingresos')}
Costes fijos mensuales: {datos.get('costes_fijos')}
Costes variables: {datos.get('costes_variables', 'no indicados')}
Inversión inicial disponible: {datos.get('inversion', 'no indicada')}
Objetivo a 12 meses: {datos.get('objetivo')}

Genera:
1. Cuenta de resultados proyectada (12 meses, formato tabla)
2. Punto de equilibrio (break-even) con cálculo detallado
3. Flujo de caja mensual estimado (cash flow)
4. KPIs financieros clave a monitorizar
5. Escenario optimista, realista y pesimista
6. Alertas y riesgos financieros a vigilar
7. Recomendaciones para mejorar rentabilidad""", max_tokens=3500)

def calcular_roi_proyecto(datos):
    return _llamar(f"""Calcula y analiza el ROI de esta inversión/proyecto:

Inversión total: {datos.get('inversion')}
Ingresos esperados: {datos.get('ingresos_esperados')}
Costes operativos: {datos.get('costes_op', '0')}
Período de análisis: {datos.get('periodo', '12 meses')}
Tipo de proyecto: {datos.get('tipo', 'no indicado')}

Calcula y muestra:
1. ROI (%) con fórmula y resultado
2. Período de recuperación de la inversión (payback)
3. VAN (Valor Actual Neto) si se proporcionan datos suficientes
4. TIR estimada
5. Comparativa: ¿es buena esta inversión vs alternativas?
6. Recomendación: ¿proceder, negociar o rechazar?""")

def analizar_rentabilidad_clientes(datos_csv):
    return _llamar(f"""Analiza la rentabilidad de esta cartera de clientes:

{datos_csv}

Identifica:
1. Clientes más rentables (top 20% que generan el 80% del valor)
2. Clientes en riesgo de abandono (señales de alerta)
3. Clientes con potencial de crecimiento
4. Clientes no rentables a considerar desvincular
5. Estrategia de precios diferenciada por segmento
6. Acciones concretas para aumentar el LTV (valor de vida del cliente)
7. Recomendación de segmentación para próximas campañas""")

def generar_presupuesto_departamento(datos):
    return _llamar(f"""Genera un presupuesto anual detallado para el departamento de {datos.get('departamento')}:

Empresa: {datos.get('empresa')}
Sector: {datos.get('sector')}
Nº de empleados en el departamento: {datos.get('empleados')}
Presupuesto total disponible: {datos.get('presupuesto_total')}
Objetivos del departamento: {datos.get('objetivos')}
Partidas especiales: {datos.get('partidas_especiales', 'ninguna')}

Genera una tabla de presupuesto detallada con:
- Personal (salarios, SS, beneficios)
- Tecnología y herramientas
- Formación y desarrollo
- Marketing o comercial si aplica
- Gastos operativos
- Contingencias (10%)
Total mensual y anual por partida, con % sobre el total.""")

def detectar_fraude_facturas(facturas_texto):
    return _llamar(f"""Analiza estas facturas/documentos financieros y detecta posibles irregularidades:

{facturas_texto[:6000]}

Busca y reporta:
1. Importes inusualmente altos o bajos vs media
2. Patrones repetitivos sospechosos (mismo importe, mismo día, etc.)
3. Proveedores desconocidos o con datos incompletos
4. Duplicados potenciales
5. Redondeos sospechosos
6. Inconsistencias en numeración o fechas
7. Nivel de riesgo global (bajo/medio/alto) con justificación
8. Recomendaciones de auditoría""")