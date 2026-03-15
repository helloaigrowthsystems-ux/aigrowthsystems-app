# file_handler.py — AImpulsa v2
import PyPDF2, openpyxl, tempfile, os
from contextlib import contextmanager

@contextmanager
def archivo_temporal(sufijo):
    tmp = tempfile.NamedTemporaryFile(suffix=sufijo, delete=False)
    tmp.close()
    try:
        yield tmp.name
    finally:
        try:
            os.remove(tmp.name)
        except Exception:
            pass

def extraer_texto_pdf(ruta):
    texto = ""
    try:
        with open(ruta, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for pagina in reader.pages:
                texto += pagina.extract_text() or ""
    except Exception as e:
        texto = f"Error al leer PDF: {e}"
    return texto.strip()

def extraer_texto_excel(ruta):
    texto = ""
    try:
        wb = openpyxl.load_workbook(ruta, data_only=True)
        for hoja in wb.sheetnames:
            ws = wb[hoja]
            texto += f"\nHoja: {hoja}\n"
            for fila in ws.iter_rows(values_only=True):
                fila_limpia = [str(c) for c in fila if c is not None]
                if fila_limpia:
                    texto += ", ".join(fila_limpia) + "\n"
    except Exception as e:
        texto = f"Error al leer Excel: {e}"
    return texto.strip()

def procesar_archivo_subido(archivo_subido):
    nombre = archivo_subido.name
    ext = nombre.rsplit(".", 1)[-1].lower()
    with archivo_temporal(f".{ext}") as ruta_tmp:
        with open(ruta_tmp, "wb") as f:
            f.write(archivo_subido.read())
        if ext == "pdf":
            texto = extraer_texto_pdf(ruta_tmp)
        elif ext in ("xlsx", "xls"):
            texto = extraer_texto_excel(ruta_tmp)
        elif ext == "csv":
            with open(ruta_tmp, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
        else:
            texto = f"Formato no soportado: .{ext}"
    return texto, nombre

def procesar_multiples_archivos(archivos_subidos):
    resultados = []
    for archivo in archivos_subidos:
        try:
            archivo.seek(0)
            texto, nombre = procesar_archivo_subido(archivo)
            resultados.append({
                "nombre": nombre,
                "texto": texto,
                "extension": nombre.rsplit(".", 1)[-1].lower(),
                "error": None,
                "caracteres": len(texto),
            })
        except Exception as e:
            resultados.append({
                "nombre": getattr(archivo, "name", "desconocido"),
                "texto": "", "extension": "", "error": str(e), "caracteres": 0,
            })
    return resultados

def texto_es_valido(texto, min_chars=50):
    return len(texto.strip()) >= min_chars