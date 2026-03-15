# invoice_generator.py — AImpulsa v2 — Generador de facturas profesionales
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from io import BytesIO
from datetime import date, timedelta
import re

AZUL = colors.HexColor("#1E3A5F")
AZUL_SUAVE = colors.HexColor("#2E6DA4")
AZUL_CLARO = colors.HexColor("#EEF4FB")
GRIS = colors.HexColor("#64748B")
GRIS_CLARO = colors.HexColor("#F8FAFC")
NEGRO = colors.HexColor("#1A1A2E")
VERDE = colors.HexColor("#166534")
BLANCO = colors.white

def generar_factura_pdf(datos):
    """
    Genera una factura profesional en PDF.
    datos: dict con todos los campos de la factura
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    s_normal = ParagraphStyle("n", fontSize=9, fontName="Helvetica", textColor=NEGRO, leading=13)
    s_bold = ParagraphStyle("b", fontSize=9, fontName="Helvetica-Bold", textColor=NEGRO, leading=13)
    s_azul = ParagraphStyle("az", fontSize=9, fontName="Helvetica-Bold", textColor=AZUL, leading=13)
    s_gris = ParagraphStyle("g", fontSize=8, fontName="Helvetica", textColor=GRIS, leading=12)
    s_titulo = ParagraphStyle("t", fontSize=28, fontName="Helvetica-Bold", textColor=AZUL, leading=32)
    s_right = ParagraphStyle("r", fontSize=9, fontName="Helvetica", textColor=NEGRO, alignment=TA_RIGHT, leading=13)
    s_right_bold = ParagraphStyle("rb", fontSize=10, fontName="Helvetica-Bold", textColor=NEGRO, alignment=TA_RIGHT, leading=14)
    s_total = ParagraphStyle("tot", fontSize=12, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_RIGHT, leading=16)

    historia = []
    ancho = doc.width

    # ── Cabecera: empresa + FACTURA ──
    cab = Table([[
        Table([[
            [Paragraph(datos.get("empresa_nombre","Tu Empresa"), ParagraphStyle("en", fontSize=16, fontName="Helvetica-Bold", textColor=AZUL, leading=20))],
            [Paragraph(datos.get("empresa_direccion",""), s_gris)],
            [Paragraph(datos.get("empresa_ciudad",""), s_gris)],
            [Paragraph(f"CIF: {datos.get('empresa_cif','')}", s_gris)],
            [Paragraph(f"Tel: {datos.get('empresa_telefono','')}  ·  {datos.get('empresa_email','')}", s_gris)],
        ]], colWidths=[ancho*0.55]),
        Table([[
            [Paragraph("FACTURA", s_titulo)],
            [Paragraph(f"Nº {datos.get('numero_factura','001')}", ParagraphStyle("nf", fontSize=13, fontName="Helvetica-Bold", textColor=AZUL_SUAVE, alignment=TA_RIGHT, leading=16))],
            [Paragraph(f"Fecha: {datos.get('fecha_emision', str(date.today().strftime('%d/%m/%Y')))}", s_right)],
            [Paragraph(f"Vencimiento: {datos.get('fecha_vencimiento','')}", s_right)],
        ]], colWidths=[ancho*0.45]),
    ]], colWidths=[ancho*0.55, ancho*0.45])
    cab.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (1,0), (1,0), "RIGHT"),
    ]))
    historia.append(cab)
    historia.append(Spacer(1, 0.4*cm))
    historia.append(HRFlowable(width="100%", thickness=2, color=AZUL))
    historia.append(Spacer(1, 0.4*cm))

    # ── Datos cliente ──
    cliente_box = Table([[
        Table([[
            [Paragraph("FACTURAR A:", ParagraphStyle("fa", fontSize=8, fontName="Helvetica-Bold", textColor=AZUL_SUAVE, leading=12))],
            [Paragraph(datos.get("cliente_nombre",""), ParagraphStyle("cn", fontSize=11, fontName="Helvetica-Bold", textColor=NEGRO, leading=15))],
            [Paragraph(datos.get("cliente_direccion",""), s_normal)],
            [Paragraph(datos.get("cliente_ciudad",""), s_normal)],
            [Paragraph(f"CIF/NIF: {datos.get('cliente_cif','')}", s_normal)],
            [Paragraph(datos.get("cliente_email",""), s_gris)],
        ]], colWidths=[ancho*0.55]),
        Table([[
            [Paragraph("MÉTODO DE PAGO:", ParagraphStyle("mp", fontSize=8, fontName="Helvetica-Bold", textColor=AZUL_SUAVE, leading=12))],
            [Paragraph(datos.get("metodo_pago","Transferencia bancaria"), s_normal)],
            [Paragraph(datos.get("iban",""), s_gris)],
            [Spacer(1, 0.2*cm)],
            [Paragraph("REFERENCIA:", ParagraphStyle("ref", fontSize=8, fontName="Helvetica-Bold", textColor=AZUL_SUAVE, leading=12))],
            [Paragraph(datos.get("referencia",""), s_normal)],
        ]], colWidths=[ancho*0.45]),
    ]], colWidths=[ancho*0.55, ancho*0.45])
    cliente_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_CLARO),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [6,6,6,6]),
    ]))
    historia.append(cliente_box)
    historia.append(Spacer(1, 0.5*cm))

    # ── Tabla de líneas ──
    borde = colors.HexColor("#E2E8F0")
    lineas_tabla = [
        [Paragraph("DESCRIPCIÓN", ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold", textColor=BLANCO)),
         Paragraph("CANT.", ParagraphStyle("thc", fontSize=9, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_CENTER)),
         Paragraph("PRECIO UNIT.", ParagraphStyle("thp", fontSize=9, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_RIGHT)),
         Paragraph("DESC. %", ParagraphStyle("thd", fontSize=9, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_CENTER)),
         Paragraph("TOTAL", ParagraphStyle("tht", fontSize=9, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_RIGHT))],
    ]

    subtotal = 0.0
    for linea in datos.get("lineas", []):
        desc = linea.get("descripcion","")
        cant = float(linea.get("cantidad", 1))
        precio = float(linea.get("precio_unitario", 0))
        desc_pct = float(linea.get("descuento", 0))
        total_linea = cant * precio * (1 - desc_pct/100)
        subtotal += total_linea

        lineas_tabla.append([
            Paragraph(desc, s_normal),
            Paragraph(f"{cant:g}", ParagraphStyle("c", fontSize=9, fontName="Helvetica", alignment=TA_CENTER, textColor=NEGRO)),
            Paragraph(f"{precio:,.2f} €", s_right),
            Paragraph(f"{desc_pct:g}%" if desc_pct else "—", ParagraphStyle("d", fontSize=9, fontName="Helvetica", alignment=TA_CENTER, textColor=GRIS)),
            Paragraph(f"{total_linea:,.2f} €", s_right_bold),
        ])

    tabla_lineas = Table(lineas_tabla,
        colWidths=[ancho*0.44, ancho*0.1, ancho*0.16, ancho*0.1, ancho*0.2])
    tabla_lineas.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BLANCO, GRIS_CLARO]),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-1), 0.3, borde),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    historia.append(tabla_lineas)
    historia.append(Spacer(1, 0.3*cm))

    # ── Totales ──
    iva_pct = float(datos.get("iva", 21))
    irpf_pct = float(datos.get("irpf", 0))
    iva_importe = subtotal * iva_pct / 100
    irpf_importe = subtotal * irpf_pct / 100
    total_final = subtotal + iva_importe - irpf_importe

    filas_total = [
        [Paragraph("Subtotal:", s_right), Paragraph(f"{subtotal:,.2f} €", s_right_bold)],
        [Paragraph(f"IVA ({iva_pct:.0f}%):", s_right), Paragraph(f"{iva_importe:,.2f} €", s_right)],
    ]
    if irpf_pct > 0:
        filas_total.append([Paragraph(f"IRPF (-{irpf_pct:.0f}%):", s_right), Paragraph(f"-{irpf_importe:,.2f} €", s_right)])
    filas_total.append([
        Paragraph("TOTAL:", ParagraphStyle("tl", fontSize=12, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_RIGHT)),
        Paragraph(f"{total_final:,.2f} €", ParagraphStyle("tv", fontSize=13, fontName="Helvetica-Bold", textColor=BLANCO, alignment=TA_RIGHT)),
    ])

    tabla_total = Table(filas_total, colWidths=[ancho*0.7, ancho*0.3])
    tabla_total.setStyle(TableStyle([
        ("BACKGROUND", (0, len(filas_total)-1), (-1,-1), AZUL),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("LINEABOVE", (0, len(filas_total)-1), (-1,-1), 1, AZUL),
    ]))

    contenedor_total = Table([[Paragraph(""), tabla_total]], colWidths=[ancho*0.5, ancho*0.5])
    historia.append(contenedor_total)

    # ── Notas y condiciones ──
    if datos.get("notas"):
        historia.append(Spacer(1, 0.5*cm))
        historia.append(HRFlowable(width="100%", thickness=0.5, color=borde))
        historia.append(Spacer(1, 0.2*cm))
        historia.append(Paragraph("Notas:", ParagraphStyle("nota_t", fontSize=8, fontName="Helvetica-Bold", textColor=AZUL_SUAVE)))
        historia.append(Paragraph(datos.get("notas",""), s_gris))

    # Pie
    historia.append(Spacer(1, 0.5*cm))
    historia.append(HRFlowable(width="100%", thickness=0.5, color=borde))
    pie_texto = datos.get("pie", f"Gracias por confiar en {datos.get('empresa_nombre','')} · {datos.get('empresa_web','')} · {datos.get('empresa_email','')}")
    historia.append(Paragraph(pie_texto, ParagraphStyle("pie", fontSize=8, fontName="Helvetica", textColor=GRIS, alignment=TA_CENTER, leading=12)))

    doc.build(historia)
    buffer.seek(0)
    return buffer.read(), total_final