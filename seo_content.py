# seo_content.py — AImpulsa v2
from groq import Groq
import os
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

def generar_articulo_blog(datos):
    return _llamar(f"""Escribe un artículo de blog profesional y optimizado para SEO.

Tema: {datos.get('tema')}
Empresa/marca: {datos.get('empresa')}
Sector: {datos.get('sector')}
Palabra clave principal: {datos.get('keyword')}
Keywords secundarias: {datos.get('keywords_sec', 'ninguna')}
Público objetivo: {datos.get('publico')}
Tono: {datos.get('tono', 'profesional')}
Extensión: {datos.get('extension', '800-1000 palabras')}

Estructura obligatoria:
- Título H1 atractivo con la keyword principal
- Meta descripción (155 caracteres máx)
- Introducción con gancho (problema que resuelve)
- 3-5 secciones H2 con subtítulos descriptivos
- Listas y datos concretos donde sean relevantes
- Conclusión con CTA claro
- Sugerencia de 5 tags/etiquetas

Escribe el artículo completo, listo para publicar.""", max_tokens=3000)

def generar_posts_rrss(datos):
    return _llamar(f"""Genera posts para redes sociales sobre:

Tema/producto: {datos.get('tema')}
Empresa: {datos.get('empresa')}
Objetivo: {datos.get('objetivo', 'aumentar engagement')}
Tono: {datos.get('tono', 'profesional pero cercano')}

Crea posts para:
1. LinkedIn (200-300 palabras, profesional, con hashtags)
2. Instagram (caption 150 palabras + 10 hashtags relevantes)
3. Twitter/X (280 caracteres máx, impactante)
4. Facebook (informal, 150 palabras, pregunta al final)

Para cada red social indica también: mejor hora de publicación y tipo de imagen recomendada.""")

def generar_newsletter(datos):
    return _llamar(f"""Crea una newsletter profesional completa:

Empresa: {datos.get('empresa')}
Tema principal: {datos.get('tema')}
Novedades: {datos.get('novedades', 'ninguna especificada')}
Oferta especial: {datos.get('oferta', 'ninguna')}
Segmento: {datos.get('segmento', 'clientes y suscriptores')}

Incluye:
- Asunto del email (máx 50 caracteres, tasa apertura optimizada)
- Preheader (90 caracteres)
- Saludo personalizable
- Editorial breve (intro 2 párrafos)
- Sección de novedades/contenido principal
- Bloque de oferta o CTA si aplica
- Sección de consejos o valor añadido
- Cierre y firma
- PS con urgencia o dato curioso""", max_tokens=2000)

def generar_descripcion_producto(datos):
    return _llamar(f"""Escribe una descripción de producto/servicio altamente persuasiva y optimizada para conversión:

Producto/Servicio: {datos.get('producto')}
Empresa: {datos.get('empresa')}
Precio: {datos.get('precio', 'no indicado')}
Público objetivo: {datos.get('publico')}
Beneficios principales: {datos.get('beneficios')}
Diferenciadores vs competencia: {datos.get('diferenciadores', 'no indicado')}
Objeciones comunes: {datos.get('objeciones', 'no indicadas')}

Genera:
1. Título principal (headline) — impactante, orientado a beneficio
2. Subtítulo (subheadline) — clarifica la propuesta
3. Descripción corta (50 palabras) — para tarjetas y resúmenes
4. Descripción larga (200 palabras) — para página de producto
5. 5 bullets de beneficios (no características, beneficios)
6. Gestión de 3 objeciones principales
7. Llamada a la acción (CTA) x3 variantes""")

def analizar_competencia(datos):
    return _llamar(f"""Realiza un análisis de competencia detallado:

Mi empresa: {datos.get('mi_empresa')}
Mi producto/servicio: {datos.get('mi_producto')}
Competidores: {datos.get('competidores')}
Mercado/sector: {datos.get('sector')}

Analiza:
1. Posicionamiento de cada competidor (fortalezas y debilidades)
2. Brechas del mercado que no están cubriendo
3. Oportunidades de diferenciación para mi empresa
4. Amenazas a vigilar
5. Estrategia recomendada para destacar
6. Propuesta de valor única sugerida (UVP)
7. Quick wins: 3 acciones concretas para ganar terreno en 30 días""")