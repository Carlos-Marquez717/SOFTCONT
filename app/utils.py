from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os
from django.conf import settings

from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def generate_pdf(data):
    # Agrupar las órdenes por empresa
    grouped_data = {}
    for row in data:
        if len(row) < 9:  # Asegúrate de que haya al menos 9 columnas
            continue
        
        empresa = row[8]  # Suponiendo que la empresa está en la columna 8
        if empresa not in grouped_data:
            grouped_data[empresa] = []
        grouped_data[empresa].append({
            'orden': row[0],
            'prioridad': row[1],
            'tag': row[2],
            'descripcion_equipo': row[3],
            'descripcion_fallo': row[4],
            'personal': row[5],
            'fecha_inicio': row[6],
            'especialidad': row[7],
            'empresa': row[8]
        })

    pdfs = BytesIO()
    for empresa, rows in grouped_data.items():
        html = render_to_string('pdf_template.html', {'empresa': empresa, 'rows': rows})
        result = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=result)
        if pisa_status.err:
            return None
        pdfs.write(result.getvalue())
    
    pdfs.seek(0)
    return pdfs.getvalue()


from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(grouped_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Establece el punto inicial de Y
    y = 750
    
    for empresa, orders in grouped_data.items():
        p.drawString(100, y, f"Empresa: {empresa}")
        y -= 20
        
        for row in orders:
            if len(row) < 9:
                continue
            p.drawString(100, y, f"Orden: {row[0]}")
            p.drawString(100, y-15, f"Prioridad: {row[1]}")
            p.drawString(100, y-30, f"Tag: {row[2]}")
            p.drawString(100, y-45, f"Descripción del equipo: {row[3]}")
            p.drawString(100, y-60, f"Descripción del fallo: {row[4]}")
            p.drawString(100, y-75, f"Personal: {row[5]}")
            p.drawString(100, y-90, f"Fecha de inicio: {row[6]}")
            p.drawString(100, y-105, f"Especialidad: {row[7]}")
            p.drawString(100, y-120, f"Empresa: {row[8]}")
            
            y -= 135
            
            # Comprueba si hay espacio suficiente en la página
            if y < 100:
                p.showPage()
                p.setPageSize(letter)
                y = 750
        
        # Añadir un espacio adicional entre empresas
        y -= 20
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.getvalue()
