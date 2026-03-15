# batch_processor.py — AImpulsa v2
from groq import Groq
import os, json, re
from dotenv import load_dotenv

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extraer_datos_batch(texto, instruccion, nombre_archivo):
    prompt = f"""Instrucción: {instruccion}

Documento ({nombre_archivo}):
{texto[:4000]}

Responde SOLO en formato JSON limpio y válido, sin explicaciones, sin markdown, sin ```json.
Si no encuentras algún campo, ponlo como null."""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        raw = re.sub(r"```json|```", "", res.choices[0].message.content).strip()
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": res.choices[0].message.content, "_error": "JSON inválido"}
    except Exception as e:
        return {"_error": str(e)}

def procesar_batch_completo(documentos, instruccion):
    resultados = []
    for doc in documentos:
        if doc.get("error"):
            resultados.append({"archivo": doc["nombre"], "_error": doc["error"]})
            continue
        if not doc.get("texto", "").strip():
            resultados.append({"archivo": doc["nombre"], "_error": "Documento vacío"})
            continue
        datos = extraer_datos_batch(doc["texto"], instruccion, doc["nombre"])
        datos["archivo"] = doc["nombre"]
        resultados.append(datos)
    return resultados