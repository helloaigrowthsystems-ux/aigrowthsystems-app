# translator.py — AImpulsa v2
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

IDIOMAS = ["Inglés","Francés","Alemán","Portugués","Italiano","Chino","Árabe","Japonés","Neerlandés","Ruso"]

def traducir_texto(texto, idioma_destino, tono="profesional", contexto="documento empresarial"):
    prompt = f"""Traduce el siguiente texto al {idioma_destino}.
Tono: {tono}. Contexto: {contexto}.
Mantén el formato original (párrafos, listas, puntuación).
Proporciona SOLO la traducción, sin explicaciones ni notas.

Texto a traducir:
{texto}"""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def adaptar_contenido_mercado(texto, pais_destino):
    prompt = f"""Adapta este contenido empresarial para el mercado de {pais_destino}.
Considera: cultura local, expresiones idiomáticas, referencias legales o comerciales relevantes,
moneda y formatos de fecha/número locales, y tono apropiado para ese mercado.

Texto original:
{texto}

Proporciona el texto adaptado y una nota breve explicando los cambios más importantes."""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"