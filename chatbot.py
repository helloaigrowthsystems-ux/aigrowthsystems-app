# chatbot.py — AImpulsa v2
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chatbot_responder(historial, informacion_empresa, pregunta):
    system_prompt = f"""Eres el asistente virtual de una empresa. Responde preguntas de clientes de forma profesional, amable y útil, basándote ÚNICAMENTE en la información proporcionada.

Si te preguntan algo que no está en la información, di amablemente que no tienes esa información y sugiere contactar directamente con la empresa.

INFORMACIÓN DE LA EMPRESA:
{informacion_empresa}

Responde siempre en español. Sé conciso, claro y profesional. Nunca inventes información."""

    mensajes = [{"role": "system", "content": system_prompt}]
    for msg in historial[-10:]:
        mensajes.append(msg)
    mensajes.append({"role": "user", "content": pregunta})

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensajes,
            max_tokens=1000
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error al procesar tu pregunta: {e}"