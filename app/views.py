# en trabajadores/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import TrabajadorForm,EmpresaForm,ObreroForm, PedidoForm , MaterialForm,HerramientaForm, PrestamoForm,PrestamoEditForm,RepuestoForm,RetiroRepuestoForm,UtilesaseoForm
from .models import Trabajador,Empresa,Obrero, Pedido, Material, Herramienta, Prestamo,Repuesto,RetiroRepuesto,Utilesaseo
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum, F
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from tabulate import tabulate
import tabula
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models import F, CharField, ExpressionWrapper, fields,Value,Case, When
from django.db.models.functions import Cast,Concat
from django.utils.dateparse import parse_datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from io import BytesIO
from django.conf import settings
import os

@login_required
def home(request):
    
    return render(request, 'app/home.html')

def registrar_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_trabajador')  # Corregir la redirección aquí
    else:
        form = TrabajadorForm()

    return render(request, 'app/registrar_trabajador.html', {'form': form})

@login_required
def lista_trabajador(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'app/lista_trabajador.html', {'trabajadores': trabajadores})

@login_required
def lista_empresa(request):
    empresas_list = Empresa.objects.all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar materiales por nombre si hay un término de búsqueda
    if search_term:
        empresas_list = empresas_list.filter(Q(nombre__icontains=search_term))

    paginator = Paginator(empresas_list, 9)
    page = request.GET.get('page')

    try:
        empresas = paginator.page(page)
    except PageNotAnInteger:
        empresas = paginator.page(1)
    except EmptyPage:
        empresas = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_empresa.html', {'empresas': empresas, 'search_term': search_term})

@login_required
def registro_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            empresa = form.instance
            success_message = 'El trabajador se ha guardado correctamente.'
            empresa.save()
            
            return render(request, 'app/registro_empresa.html', {'form': EmpresaForm(), 'success_message': success_message})
    else:
        form = EmpresaForm()  # Corregir el formulario aquí

    return render(request, 'app/registro_empresa.html', {'form': form})




@login_required
def eliminar(request, id):
    empresa= get_object_or_404(Empresa, id=id)
    empresa.delete()
    messages.success(request,"ELIMINADO CORRECTAMENTE")
    return redirect(to='lista_empresa')

@login_required
def editar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)

    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('lista_empresa')  # Puedes redirigir a la lista o a donde desees después de editar
    else:
        form = EmpresaForm(instance=empresa)

    return render(request, 'editar_empresa.html', {'form': form, 'empresa': empresa})

@login_required
def registro_obrero(request):
    if request.method == 'POST':
        form = ObreroForm(request.POST)
        if form.is_valid():
            form.save()

            obrero = form.instance
            success_message = 'El pedido se ha guardado correctamente.'
            obrero.save()
            return render(request, 'app/registro_obrero.html', {'form': ObreroForm(), 'success_message': success_message})

    else:
        form = ObreroForm()  # Corregir el formulario aquí

    return render(request, 'app/registro_obrero.html', {'form': form})



@login_required
def lista_obrero(request):
    obreros_list = Obrero.objects.all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar materiales por nombre si hay un término de búsqueda
    if search_term:
        obreros_list = obreros_list.filter(Q(nombre__icontains=search_term))

    paginator = Paginator(obreros_list, 9)
    page = request.GET.get('page')

    try:
        obreros = paginator.page(page)
    except PageNotAnInteger:
        obreros = paginator.page(1)
    except EmptyPage:
        obreros = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_obrero.html', {'obreros': obreros, 'search_term': search_term})

@login_required
def eliminar_obrero(request, id):
    obrero= get_object_or_404(Obrero, id=id)
    obrero.delete()
    messages.success(request,"ELIMINADO CORRECTAMENTE")
    return redirect(to='lista_obrero')

@login_required
def editar_obrero(request, obrero_id):
    obrero = get_object_or_404(Obrero, id=obrero_id)
    if request.method == 'POST':
        form = ObreroForm(request.POST, instance=obrero)
        if form.is_valid():
            form.save()
            # Puedes redirigir a la página que desees después de editar
            return redirect('editar_obrero')
    else:
        form = ObreroForm(instance=obrero)
    
    return render(request, 'app/editar_obrero.html', {'form': form, 'obrero': obrero})


@login_required
def registro_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'El pedido se ha guardado correctamente.'
            return redirect('registro_pedido_success')  # Redirigir a una página de éxito o simplemente refrescar esta página

    else:
        form = PedidoForm()

    return render(request, 'app/registro_pedido.html', {'form': form})

@login_required
def registro_pedido_success(request):
    success_message = 'El pedido se ha guardado correctamente.'
    return render(request, 'app/registro_pedido.html', {'form': PedidoForm(), 'success_message': success_message})




@login_required
def lista_pedido_trabajador(request, trabajador_id):
    # Obtén el obrero o muestra una página de error si no existe
    obrero = get_object_or_404(Obrero, id=trabajador_id)

    # Filtra los pedidos por el obrero asociado
    pedidos = Pedido.objects.filter(solicitante=obrero)

    # Formatear la fecha en el lado del servidor
    for pedido in pedidos:
        pedido.fecha_pedido_formatted = pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M")

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar pedidos por cualquier campo si hay un término de búsqueda
    if search_term:
        # Utilizar Q() para construir consultas OR entre campos
        pedidos = pedidos.filter(
            Q(solicitante__nombre__icontains=search_term) |
            Q(compañia__nombre__icontains=search_term) |
            Q(insumo__nombre__icontains=search_term) |
            Q(cantidad__icontains=search_term) |
            Q(area__nombre__icontains=search_term) |
            Q(fecha_pedido__icontains=search_term)
        )

    # Paginación
    paginator = Paginator(pedidos, 9)
    page = request.GET.get('page')

    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_pedido_trabajador.html', {'pedidos': pedidos, 'obrero': obrero, 'search_term': search_term})





@login_required
def lista_pedido(request):
    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Obtener todos los pedidos sin filtrar inicialmente
    pedidos_list = Pedido.objects.all()

    # Filtrar pedidos por cualquier campo si hay un término de búsqueda
    if search_term:
        try:
            # Intentar parsear el término de búsqueda como fecha en formato dd/mm/yyyy
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            # Filtrar por fecha exacta o parcial
            pedidos_list = pedidos_list.filter(fecha_pedido__date=search_date)
        except ValueError:
            # Si el término de búsqueda no es una fecha, buscar en otros campos de texto
            text_search = Q(insumo__nombre__icontains=search_term) | \
                          Q(solicitante__nombre__icontains=search_term) | \
                          Q(compañia__nombre__icontains=search_term) | \
                          Q(area__icontains=search_term)
            pedidos_list = pedidos_list.filter(text_search)

    # Ordenar los resultados por fecha_pedido descendente
    pedidos_list = pedidos_list.order_by('-fecha_pedido')

    # Paginar los resultados
    paginator = Paginator(pedidos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pedidos': page_obj,
        'search_term': search_term,
    }

    # Renderizar la plantilla con los resultados paginados y filtrados
    return render(request, 'app/lista_pedido.html', context)


@login_required
def generar_pdf_pedido(request, obrero_id):
    # Obtener el obrero específico
    obrero = get_object_or_404(Obrero, id=obrero_id)

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar', '')

    # Obtener los préstamos asociados al obrero
    pedidos = Pedido.objects.filter(solicitante=obrero)

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedidos = pedidos.filter(fecha_pedido=search_date)
        except ValueError:
            pass

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prestamos_{obrero.nombre}.pdf"'

    # Crear el objeto PDF con ReportLab, con orientación horizontal
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(letter[1], letter[0]))  # Intercambiar ancho y alto

    # Crear una tabla para los datos
    data = [
        ['FECHA', 'NOMBRE DEL SOLICITANTE', 'INSUMO SOLICITADO', 'CANTIDAD', 'AREA TRABAJO','EMPRESA'],
    ]

    for pedido in pedidos:
        fecha_y_hora = pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M")
        data.append([
            fecha_y_hora,
            pedido.solicitante.nombre,
            pedido.insumo.nombre,
            pedido.cantidad,  # Elimina la llamada a str() aquí
            pedido.area,
            pedido.compañia.nombre,
        ])

    # Configurar el estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter[1], letter[0]  # Intercambiar ancho y alto
    table.wrapOn(p, width, height)
    table.drawOn(p, 100, height - 200)  # Bajar la tabla

    # Agregar título
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "ENTREGA DE INSUMOS DIARIOS | PAÑOL")

    # Agregar el nombre del usuario que está generando el PDF
    usuario = request.user
    p.setFont("Helvetica-Bold", 12)
    text = f"PAÑOLERO: {usuario.username}"
    text_width = p.stringWidth(text, "Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, height - 90, text)
    p.line(100, height - 92, 100 + text_width, height - 92)  # Subrayar el texto

    # Agregar la fecha filtrada debajo del nombre del usuario
    if search_term:
        p.setFont("Helvetica", 12)
        p.setFillColor(colors.black)
        p.drawString(100, height - 110, f"Fecha filtrada: {search_term}")


 

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response

@login_required
def generar_pdf_pedidos(request):
    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Obtener todos los pedidos y aplicar filtro de búsqueda si es necesario
    pedidos = Pedido.objects.all()

    if search_term:
        # Formatear la fecha si se proporciona
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedidos = pedidos.filter(
                Q(solicitante__nombre__icontains=search_term) |
                Q(compañia__nombre__icontains=search_term) |
                Q(insumo__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(area__icontains=search_term) |
                Q(fecha_pedido__date=search_date)
            )
        except ValueError:
            # Manejar el caso en que el término de búsqueda no sea una fecha válida
            pass

    # Después de aplicar el filtro
    print("Pedidos después de aplicar filtro:", pedidos)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PEDIDOS.pdf"'

    # Crear el objeto PDF con ReportLab, con orientación horizontal
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(letter[1], letter[0]))  # Intercambiar ancho y alto

    # Crear una tabla para los datos
    data = [
        ['FECHA', 'NOMBRE DEL SOLICITANTE', 'INSUMO SOLICITADO', 'CANTIDAD', 'AREA TRABAJO','EMPRESA'],
    ]

    for pedido in pedidos:
        fecha_y_hora = pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M")
        data.append([
            fecha_y_hora,
            pedido.solicitante.nombre,
            pedido.insumo.nombre,
            str(pedido.cantidad),
            pedido.area,
            pedido.compañia.nombre,
        ])

    # Configurar el estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter[1], letter[0]  # Intercambiar ancho y alto
    table.wrapOn(p, width, height)
    table.drawOn(p, 55, height - 250)  # Bajar la tabla

    # Agregar título
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "ENTREGA DE INSUMOS DIARIOS | PAÑOL")

    # Agregar el nombre del usuario que está generando el PDF
    usuario = request.user
    p.setFont("Helvetica-Bold", 12)
    text = f"PAÑOLERO: {usuario.username}"
    text_width = p.stringWidth(text, "Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, height - 90, text)
    p.line(100, height - 92, 100 + text_width, height - 92)  # Subrayar el texto

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response



@login_required
def calcular_totales(pedidos):
    """
    Calcula los totales por semana, mes y año para cada insumo en los pedidos.
    """
    insumos_totales = {}

    # Obtener la fecha actual
    fecha_actual = datetime.now().date()

    for pedido in pedidos:
        insumo = pedido.insumo.nombre
        fecha_pedido = pedido.fecha_pedido.date()  # Convertir a datetime.date
        cantidad = pedido.cantidad

        if insumo not in insumos_totales:
            insumos_totales[insumo] = {
                'total': 0,
                'totales_por_periodo': {
                    'semana': 0,
                    'mes': 0,
                    'año': 0,
                }
            }

        # Total general
        insumos_totales[insumo]['total'] += cantidad

        # Totales por semana, mes y año
        semana_inicio = fecha_pedido - timedelta(days=fecha_pedido.weekday())
        if semana_inicio <= fecha_actual <= semana_inicio + timedelta(days=6):
            insumos_totales[insumo]['totales_por_periodo']['semana'] += cantidad

        if fecha_pedido.month == fecha_actual.month and fecha_pedido.year == fecha_actual.year:
            insumos_totales[insumo]['totales_por_periodo']['mes'] += cantidad

        if fecha_pedido.year == fecha_actual.year:
            insumos_totales[insumo]['totales_por_periodo']['año'] += cantidad

    return insumos_totales


MESES_EN_ESPAÑOL = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

@login_required
def pedidos_total(request):
    search_term = request.GET.get('buscar')
    pedidos = Pedido.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedidos = pedidos.filter(
                Q(solicitante__nombre__icontains=search_term) |
                Q(compañia__nombre__icontains=search_term) |
                Q(insumo__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(area__icontains=search_term) |
                Q(fecha_pedido__date=search_date)
            )
        except ValueError:
            pass

    # Calcular totales
    insumos_totales = calcular_totales(pedidos)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PEDIDOS_TOTAL.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar título
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, "INFORME DE INSUMOS")

    # Obtener el mes y el año actual
    fecha_actual = datetime.now()
    mes_actual = fecha_actual.strftime("%B")
    año_actual = fecha_actual.year

    # Traducir el nombre del mes al español
    mes_actual_es = MESES_EN_ESPAÑOL.get(mes_actual, mes_actual).capitalize()

    # Agregar la fecha del mes y año
    p.setFont("Helvetica", 12)
    p.drawString(50, letter[1] - 80, f"Mes: {mes_actual_es} {año_actual}")

    # Configurar la tabla
    data = [['PERÍODO', 'NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        total = totales['total']
        mes_total = totales['totales_por_periodo']['mes']
        año_total = totales['totales_por_periodo']['año']

        # Añadir insumo y totales
        data.append(['INSUMO', insumo, total])
        data.append(['TOTAL POR MES', '', mes_total])
        data.append(['TOTAL POR AÑO', '', año_total])

    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar el estilo de fondo amarillo para las celdas específicas
    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'PERÍODO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (2, 0), (2, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'PERÍODO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (2, 0), (2, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Aplicar el estilo para las celdas con 'INSUMO'
    for row in range(len(data)):
        for col in range(len(data[row])):
            if isinstance(data[row][col], str) and 'INSUMO' in data[row][col]:
                style.add('BACKGROUND', (col, row), (col, row), colors.yellow)

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 120  # Ajustar la posición vertical para incluir el texto de la fecha

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response



@login_required
def calcular_totales_semanales(pedidos, semana_inicio, semana_fin):
    insumos_totales = {}

    for pedido in pedidos:
        insumo = pedido.insumo.nombre
        cantidad = pedido.cantidad
        fecha_pedido = pedido.fecha_pedido.date()

        # Verificar si el pedido está dentro del rango de fechas de la semana
        if semana_inicio <= fecha_pedido <= semana_fin:
            if insumo not in insumos_totales:
                insumos_totales[insumo] = {
                    'total': 0,
                    'totales_por_periodo': {
                        'semana': 0,
                    }
                }

            insumos_totales[insumo]['totales_por_periodo']['semana'] += cantidad
            insumos_totales[insumo]['total'] += cantidad

    return insumos_totales

@login_required
def pedidos_semanales(request):
    search_term = request.GET.get('buscar')
    pedidos = Pedido.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            semana_inicio = search_date - timedelta(days=search_date.weekday())
            semana_fin = semana_inicio + timedelta(days=6)
            
            pedidos = pedidos.filter(
                Q(solicitante__nombre__icontains=search_term) |
                Q(compañia__nombre__icontains=search_term) |
                Q(insumo__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(area__icontains=search_term) |
                Q(fecha_pedido__date__range=[semana_inicio, semana_fin])
            )
        except ValueError:
            pass
    else:
        # Si no hay término de búsqueda, usar la semana actual
        hoy = datetime.now().date()
        semana_inicio = hoy - timedelta(days=hoy.weekday())
        semana_fin = semana_inicio + timedelta(days=6)
        pedidos = pedidos.filter(
            fecha_pedido__date__range=[semana_inicio, semana_fin]
        )

    # Calcular totales semanales
    insumos_totales = calcular_totales_semanales(pedidos, semana_inicio, semana_fin)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_SEMANAL_{semana_inicio.strftime("%d_%m_%Y")}_a_{semana_fin.strftime("%d_%m_%Y")}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar título
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, f"INFORME DE INSUMOS SEMANALES ({semana_inicio.strftime('%d/%m/%Y')} - {semana_fin.strftime('%d/%m/%Y')})")

    # Configurar la tabla
    data = [['PERÍODO', 'NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        semana_total = totales['totales_por_periodo']['semana']

        # Añadir insumo y totales semanales
        data.append(['INSUMO', insumo, totales['total']])
        data.append(['TOTAL POR SEMANA', '', semana_total])

    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar el estilo de fondo amarillo para las celdas específicas
    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'PERÍODO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (2, 0), (2, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'PERÍODO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (2, 0), (2, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Aplicar el estilo para las celdas con 'INSUMO'
    for row in range(len(data)):
        for col in range(len(data[row])):
            if isinstance(data[row][col], str) and 'INSUMO' in data[row][col]:
                style.add('BACKGROUND', (col, row), (col, row), colors.yellow)

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 100  # Ajustar la posición vertical

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response

MESES_EN_ESPAÑOL = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

@login_required
def calcular_totales_mensuales(pedidos, mes_inicio, mes_fin):
    insumos_totales = {}
    semana_inicio = mes_inicio - timedelta(days=mes_inicio.weekday())
    
    while semana_inicio <= mes_fin:
        semana_fin = semana_inicio + timedelta(days=6)
        semana_pedidos = pedidos.filter(fecha_pedido__date__range=[semana_inicio, semana_fin])
        
        for pedido in semana_pedidos:
            insumo = pedido.insumo.nombre
            cantidad = pedido.cantidad

            if insumo not in insumos_totales:
                insumos_totales[insumo] = {
                    'total': 0,
                    'totales_por_periodo': {
                        'semana': 0,
                        'mes': 0,
                    },
                    'totales_por_semana': {}
                }

            # Calcular totales semanales
            semana_key = f'Semana del {semana_inicio.strftime("%d-%m")} al {semana_fin.strftime("%d-%m")}'
            if semana_key not in insumos_totales[insumo]['totales_por_semana']:
                insumos_totales[insumo]['totales_por_semana'][semana_key] = 0

            insumos_totales[insumo]['totales_por_semana'][semana_key] += cantidad
            insumos_totales[insumo]['totales_por_periodo']['mes'] += cantidad
            insumos_totales[insumo]['total'] += cantidad

        semana_inicio += timedelta(days=7)

    return insumos_totales


@login_required
def pedidos_mensuales(request):
    search_term = request.GET.get('buscar')
    pedidos = Pedido.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            mes_inicio = search_date.replace(day=1)
            mes_fin = (mes_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            
            pedidos = pedidos.filter(
                Q(solicitante__nombre__icontains=search_term) |
                Q(compañia__nombre__icontains=search_term) |
                Q(insumo__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(area__icontains=search_term) |
                Q(fecha_pedido__date__range=[mes_inicio, mes_fin])
            )
        except ValueError:
            pass
    else:
        hoy = datetime.now().date()
        mes_inicio = hoy.replace(day=1)
        mes_fin = (mes_inicio + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        pedidos = pedidos.filter(
            fecha_pedido__date__range=[mes_inicio, mes_fin]
        )

    # Calcular totales mensuales
    insumos_totales = calcular_totales_mensuales(pedidos, mes_inicio, mes_fin)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_MENSUAL_{mes_inicio.strftime("%m_%Y")}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Obtener el nombre del mes en español
    mes_nombre = MESES_EN_ESPAÑOL[mes_inicio.month]

    # Agregar título
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, f"INFORME DE INSUMOS MENSUALES ({mes_nombre} {mes_inicio.year})")

    # Configurar la tabla
    data = [['PERÍODO', 'NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        mes_total = totales['totales_por_periodo']['mes']

        # Añadir insumo y totales mensuales
        data.append(['INSUMO', insumo, totales['total']])
        data.append(['TOTAL POR MES', '', mes_total])
        
        # Añadir totales semanales con fechas
        for semana, cantidad in totales['totales_por_semana'].items():
            data.append([semana, '', cantidad])
        
    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar el estilo de fondo amarillo para las celdas específicas
    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'PERÍODO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (2, 0), (2, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'PERÍODO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (2, 0), (2, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Aplicar el estilo para las celdas con 'INSUMO'
    for row in range(len(data)):
        for col in range(len(data[row])):
            if isinstance(data[row][col], str) and 'INSUMO' in data[row][col]:
                style.add('BACKGROUND', (col, row), (col, row), colors.yellow)

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 100  # Ajustar la posición vertical

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response



@login_required
def eliminar_pedido(request, pedido_id):
    # Obtiene el pedido o muestra una página de error si no existe
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Elimina el pedido
    pedido.delete()

    # Redirige a la lista de pedidos después de la eliminación
    return redirect('lista_pedido')

# views.py

import logging

logger = logging.getLogger(__name__)

@login_required
def editar_pedido(request, pedido_id):
    logger.info("Iniciando la edición del pedido con id %s", pedido_id)
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'El pedido se ha modificado correctamente.')
            return redirect('lista_pedido')
        else:
            logger.error("Error al modificar el pedido: %s", form.errors)
            messages.error(request, 'Hubo un error al modificar el pedido. Por favor, verifica los datos.')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'app/editar_pedido.html', {'form': form, 'pedido': pedido})



@login_required
def registro_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            material = form.instance
            success_message = 'El trabajador se ha guardado correctamente.'
            material.save()
            
            return render(request, 'app/registro_material.html', {'form': MaterialForm(), 'success_message': success_message})
    else:
        form = MaterialForm()  # Corregir el formulario aquí

    return render(request, 'app/registro_material.html', {'form': form})




@login_required
def eliminar_material(request, material_id):
    # Obtiene el pedido o muestra una página de error si no existe
    material = get_object_or_404(Material, id=material_id)

    # Elimina el pedido
    material.delete()

    # Redirige a la lista de pedidos después de la eliminación
    return redirect('lista_material')

@login_required
def lista_material(request):
    materiales_list = Material.objects.all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar materiales por nombre si hay un término de búsqueda
    if search_term:
        materiales_list = materiales_list.filter(Q(nombre__icontains=search_term))

    paginator = Paginator(materiales_list, 9)
    page = request.GET.get('page')

    try:
        materiales = paginator.page(page)
    except PageNotAnInteger:
        materiales = paginator.page(1)
    except EmptyPage:
        materiales = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_material.html', {'materiales': materiales, 'search_term': search_term})

@login_required
def editar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('lista_material')  # Puedes redirigir a la lista o a donde desees después de editar
    else:
        form = MaterialForm(instance=material)

    return render(request, 'editar_material.html', {'form': form, 'material': material})

@login_required
def registro_Herramienta(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_Herramienta')
    else:
        form = HerramientaForm()  # Corregir el formulario aquí

    return render(request, 'app/registro_Herramienta.html', {'form': form})

@login_required
def lista_Herramienta(request):
    herramientas_list = Herramienta.objects.order_by('id').all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar herramientas por nombre si hay un término de búsqueda
    if search_term:
        herramientas_list = herramientas_list.filter(Q(nombre__icontains=search_term))

    paginator = Paginator(herramientas_list, 9)
    page = request.GET.get('page')

    try:
        herramientas = paginator.page(page)
    except PageNotAnInteger:
        herramientas = paginator.page(1)
    except EmptyPage:
        herramientas = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_Herramienta.html', {'herramientas': herramientas, 'search_term': search_term})

@login_required
def editar_herramienta(request, id):  # Ajusta el nombre del parámetro aquí
    # Obtén la herramienta correspondiente al ID o devuelve un 404 si no existe
    herramienta = get_object_or_404(Herramienta, id=id)

    if request.method == 'POST':
        # Lógica para procesar el formulario cuando se envía
        form = HerramientaForm(request.POST, instance=herramienta)
        if form.is_valid():
            form.save()
            # Redirige a la página de lista de herramientas después de editar
            return redirect('lista_Herramienta')
    else:
        # Muestra el formulario con los datos actuales de la herramienta
        form = HerramientaForm(instance=herramienta)

    return render(request, 'app/editar_herramienta.html', {'form': form, 'herramienta': herramienta})

@login_required
def eliminar_herramienta(request, id):
    # Lógica para eliminar la herramienta con el ID proporcionado
    herramienta = get_object_or_404(Herramienta, id=id)
    herramienta.delete()
    
    # Redirige a la página de lista de herramientas después de la eliminación
    return redirect('lista_Herramienta')

@login_required
def registrar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            if prestamo.status == 'ENTREGADO':
                prestamo.fecha_recepcion = prestamo.fecha_creacion
            prestamo.save()
            
            messages.success(request, 'El préstamo se ha registrado correctamente.')
            return redirect('registro_prestamo_success')  # Redirigir a una página de éxito

    else:
        form = PrestamoForm()

    return render(request, 'app/registrar_prestamo.html', {'form': form})

@login_required
def registro_prestamo_success(request):
    messages.success(request, 'El préstamo se ha registrado correctamente.')
    return render(request, 'app/registrar_prestamo.html', {'form': PrestamoForm(), 'success_message': messages.get_messages(request)})


@login_required
def lista_prestamo(request):
    # Initialize search_term to an empty string
    search_term = request.GET.get('buscar', '')

    # Obtener todos los préstamos
    prestamos_list = Prestamo.objects.all()

    # Iterar sobre los préstamos para formatear las fechas
    for prestamo in prestamos_list:
        # Check if fecha_recepcion is not None before formatting
        if prestamo.fecha_recepcion:
            prestamo.fecha_recepcion_formatted = prestamo.fecha_recepcion.strftime("%d/%m/%Y %H:%M")
        else:
            prestamo.fecha_recepcion_formatted = None

        # Check if fecha_creacion is not None before formatting
        if prestamo.fecha_creacion:
            prestamo.fecha_creacion_formatted = prestamo.fecha_creacion.strftime("%d/%m/%Y %H:%M")
        else:
            prestamo.fecha_creacion_formatted = None

    # Filtrar préstamos por cualquier campo si hay un término de búsqueda
    if search_term:
        try:
            # Intentar parsear el término de búsqueda como fecha
            search_date = datetime.strptime(search_term, "%d/%m/%Y")
            prestamos_list = prestamos_list.filter(
                Q(nombre_solicitante__nombre__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(herramienta__nombre__icontains=search_term) |
                Q(fecha_creacion__icontains=search_term) |
                Q(status__icontains=search_term) |
                Q(fecha_recepcion=search_date)
            )
        except ValueError:
            # Si no es una fecha válida, buscar en otros campos
            prestamos_list = prestamos_list.filter(
                Q(nombre_solicitante__nombre__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(herramienta__nombre__icontains=search_term) |
                Q(fecha_creacion__icontains=search_term) |
                Q(status__icontains=search_term)
            )

    paginator = Paginator(prestamos_list, 4)  # Número de elementos por página
    page = request.GET.get('page', 1)  # Obtener el número de página desde los parámetros GET

    try:
        prestamos = paginator.page(page)
    except PageNotAnInteger:
        prestamos = paginator.page(1)  # Si el parámetro page no es un entero, mostrar la primera página
    except EmptyPage:
        prestamos = paginator.page(paginator.num_pages)  # Si el parámetro page está fuera de rango, mostrar la última página

    # Renderizar la plantilla normalmente
    return render(request, 'app/lista_Prestamo.html', {'prestamos': prestamos, 'search_term': search_term})


@login_required
def generar_pdf_prestamos(request):
    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Obtener todos los préstamos y aplicar filtro de búsqueda si es necesario
    prestamos_list = Prestamo.objects.all()

    if search_term:
        # Formatear la fecha si se proporciona
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            # Filtrar por nombre, empresa, herramienta, fecha_creacion y estado
            prestamos_list = prestamos_list.filter(
                Q(nombre_solicitante__nombre__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(herramienta__nombre__icontains=search_term) |
                Q(fecha_creacion=search_date) |
                Q(status__icontains=search_term)
            )
        except ValueError:
            # Si no es una fecha válida, buscar en otros campos
            prestamos_list = prestamos_list.filter(
                Q(nombre_solicitante__nombre__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(herramienta__nombre__icontains=search_term) |
                Q(status__icontains=search_term)
            )

    # Verificar si hay resultados para la búsqueda
    if prestamos_list.exists():
        # Crear el objeto PDF con ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="prestamos_{search_term}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=(letter[1], letter[0]))  # Intercambiar ancho y alto

        elements = []

        # Agregar título
        title_style = ParagraphStyle(
            'Title',
            parent=getSampleStyleSheet()['Title'],
            alignment=1,  # 0=Left, 1=Center, 2=Right
            textColor=colors.black,
            fontName='Helvetica-Bold',
            fontSize=14
        )
        elements.append(Paragraph("PRESTAMO DE HERRAMIENTAS | PAÑOL", title_style))
        elements.append(Spacer(1, 12))

        # Crear una tabla para los datos
        data = [
            ['NOMBRE SOLICITANTE', 'EMPRESA', 'HERRAMIENTA', 'FECHA PRESTAMO', 'FECHA RECEPCION', 'ESTADO'],
        ]

        for prestamo in prestamos_list:
            # Determinar el color del texto según el estado
            if prestamo.status == 'NO_ENTREGADO':
                text_color = colors.red
            else:
                text_color = colors.black

            data.append([
                prestamo.nombre_solicitante.nombre,
                prestamo.empresa.nombre,
                prestamo.herramienta.nombre,
                prestamo.fecha_creacion.strftime("%d/%m/%Y %H:%M") if prestamo.fecha_creacion else 'Sin fecha de creación',
                prestamo.fecha_recepcion.strftime("%d/%m/%Y %H:%M") if prestamo.fecha_recepcion else 'Sin fecha de recepción',
                Paragraph(prestamo.status, ParagraphStyle('', textColor=text_color)),  # Aplicar color al estado
            ])

        # Configurar el estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)

        return response
    else:
        return HttpResponse("No se encontraron resultados para la búsqueda.")




@login_required
def generar_pdf_prestamo(request, obrero_id):
    # Obtener el trabajador específico
    trabajador = get_object_or_404(Obrero, id=obrero_id)

    # Obtener los préstamos asociados al trabajador
    prestamos = Prestamo.objects.filter(nombre_solicitante=trabajador)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prestamos_{trabajador.nombre}.pdf"'

    # Crear el objeto PDF con ReportLab, con orientación horizontal
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(letter[1], letter[0]))  # Intercambiar ancho y alto

    # Crear una tabla para los datos
    data = [
        ['NOMBRE SOLICITANTE', 'EMPRESA', 'HERRAMIENTA', 'FECHA PRESTAMO', 'FECHA RECEPCION', 'ESTADO'],
    ]

    for prestamo in prestamos:
        data.append([
            prestamo.nombre_solicitante.nombre,
            prestamo.empresa.nombre,
            prestamo.herramienta.nombre,
            prestamo.fecha_creacion.strftime("%d/%m/%Y"),
            prestamo.fecha_recepcion.strftime("%d/%m/%Y") if prestamo.fecha_recepcion else '-',
            prestamo.status,
        ])

    # Configurar el estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter[1], letter[0]  # Intercambiar ancho y alto
    table.wrapOn(p, width, height)
    table.drawOn(p, 90, height - 170)  # Bajar la tabla

    # Agregar título
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "PRESTAMO DE HERRAMIENTAS | PAÑOL")

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response

@login_required
def editar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == 'POST':
        form = PrestamoEditForm(request.POST, instance=prestamo)
        if form.is_valid():
            # Actualiza el estado y la fecha de recepción si el estado es "ENTREGADO"
            if form.cleaned_data['status'] == 'ENTREGADO':
                prestamo.status = 'ENTREGADO'
                prestamo.fecha_recepcion = timezone.now()
            else:
                prestamo.status = 'NO ENTREGADO'
                prestamo.fecha_recepcion = None

            prestamo.save()
            return redirect('lista_prestamo')  # Puedes redirigir a donde quieras después de editar
    else:
        form = PrestamoEditForm(instance=prestamo)

    return render(request, 'app/editar_prestamo.html', {'form': form, 'prestamo': prestamo})


@login_required
def lista_prestamos_obrero(request, obrero_id):
    # Obtiene el obrero correspondiente al ID o devuelve un 404 si no existe
    obrero = get_object_or_404(Obrero, id=obrero_id)

    # Filtra los préstamos por el obrero asociado
    prestamos_obrero = Prestamo.objects.filter(nombre_solicitante=obrero)

    # Paginación (si es necesario)
    paginator = Paginator(prestamos_obrero,5)
    page = request.GET.get('page')
    prestamos_pagina = paginator.get_page(page)

    # Formatear la fecha y la hora antes de pasarla a la plantilla
    for prestamo in prestamos_pagina:
        prestamo.fecha_creacion_formatted = prestamo.fecha_creacion.strftime("%d/%m/%Y %H:%M")
        prestamo.fecha_recepcion_formatted = prestamo.fecha_recepcion.strftime("%d/%m/%Y %H:%M") if prestamo.fecha_recepcion else None

    return render(request, 'app/lista_prestamos_obrero.html', {'obrero': obrero, 'prestamos_obrero': prestamos_pagina})



@login_required
def registro_Repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_Repuesto')
    else:
        form = RepuestoForm()  # Corregir el formulario aquí

    return render(request, 'app/registro_Repuesto.html', {'form': form})

@login_required
def lista_Repuesto(request):
    repuestos_list = Repuesto.objects.order_by('id').all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar herramientas por nombre si hay un término de búsqueda
    if search_term:
        repuestos_list = repuestos_list.filter(Q(nombre__icontains=search_term))

    paginator = Paginator(repuestos_list, 9)
    page = request.GET.get('page')

    try:
        repuestos = paginator.page(page)
    except PageNotAnInteger:
        repuestos = paginator.page(1)
    except EmptyPage:
        repuestos = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_Repuesto.html', {'repuestos': repuestos, 'search_term': search_term})

@login_required
def eliminar_repuesto(request, id):
    # Lógica para eliminar la herramienta con el ID proporcionado
    repuesto = get_object_or_404(Repuesto, id=id)
    repuesto.delete()
    
    # Redirige a la página de lista de herramientas después de la eliminación
    return redirect('lista_Repuesto')

@login_required
def editar_Repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)

    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            return redirect('lista_Repuesto')  # Puedes redirigir a la lista o a donde desees después de editar
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'app/editar_Repuesto.html', {'form': form, 'repuesto': repuesto})

@login_required
def registro_RetiroRepuesto(request):
    if request.method == 'POST':
        form = RetiroRepuestoForm(request.POST)
        if form.is_valid():
            repuesto = form.cleaned_data['repuesto']
            cantidad_retirada = form.cleaned_data['cantidad']
            
            try:
                repuesto_obj = Repuesto.objects.get(id=repuesto.id)
                
                if repuesto_obj.cantidad < cantidad_retirada:
                    messages.error(request, 'No hay suficiente cantidad disponible para retirar.')
                    return redirect('registro_RetiroRepuesto')

                Repuesto.objects.filter(id=repuesto.id, cantidad__gte=cantidad_retirada).update(cantidad=F('cantidad') - cantidad_retirada)

                form.save()

                # Mensaje de éxito antes de redirigir
                messages.success(request, 'El retiro de repuesto se ha registrado correctamente.')
                return redirect('registro_RetiroRepuesto_success')

            except Repuesto.DoesNotExist:
                messages.error(request, 'El repuesto no se encontró en la base de datos.')
                return redirect('registro_RetiroRepuesto')
        else:
            messages.error(request, f'Error en el formulario: {form.errors}')

    else:
        form = RetiroRepuestoForm()

    return render(request, 'app/registro_RetiroRepuesto.html', {'form': form})

@login_required
def registro_RetiroRepuesto_success(request):
    messages.success(request, 'El retiro de repuesto se ha registrado correctamente.')
    return render(request, 'app/registro_RetiroRepuesto.html', {'form': RetiroRepuestoForm(), 'success_message': messages.get_messages(request)})

@login_required
def lista_RetiroRepuesto(request):
    search_term = request.GET.get('buscar')
    retirorepuestos_list = RetiroRepuesto.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            retirorepuestos_list = retirorepuestos_list.filter(fecha_retiro__date=search_date)
        except ValueError:
            text_search = (
                Q(repuesto__nombre__icontains=search_term) | 
                Q(trabajador__nombre__icontains=search_term) |  # Cambia esto según tu modelo
                Q(empresa__nombre__icontains=search_term) |  # Si existe
                Q(cantidad__icontains=search_term)
            )
            retirorepuestos_list = retirorepuestos_list.filter(text_search)

    retirorepuestos_list = retirorepuestos_list.order_by('-fecha_retiro')
    paginator = Paginator(retirorepuestos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'retirorepuestos': page_obj,
        'search_term': search_term,
    }

    return render(request, 'app/lista_RetiroRepuesto.html', context)




@login_required
def eliminar_RetiroRepuesto(request, id):
    # Lógica para eliminar la herramienta con el ID proporcionado
    retirorepuesto = get_object_or_404(RetiroRepuesto, id=id)
    retirorepuesto.delete()
    
    # Redirige a la página de lista de herramientas después de la eliminación
    return redirect('lista_RetiroRepuesto')

@login_required
def editar_RetiroRepuesto(request, retirorepuesto_id):
    retirorepuesto = get_object_or_404(RetiroRepuesto, id=retirorepuesto_id)

    if request.method == 'POST':
        form = RetiroRepuestoForm(request.POST, instance=retirorepuesto)
        if form.is_valid():
            form.save()
            return redirect('lista_RetiroRepuesto')  # Puedes redirigir a la lista o a donde desees después de editar
    else:
        form = RetiroRepuestoForm(instance=retirorepuesto)

    return render(request, 'app/editar_RetiroRepuesto.html', {'form': form, 'retirorepuesto': retirorepuesto})



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime
from .models import RetiroRepuesto, Obrero

@login_required
def lista_RetiroRepuesto_obrero(request, obrero_id):
    # Obtiene el obrero correspondiente al ID o devuelve un 404 si no existe
    obrero = get_object_or_404(Obrero, id=obrero_id)

    # Filtra los retiros de repuestos por el obrero asociado
    retirorepuesto_obrero = RetiroRepuesto.objects.filter(trabajador=obrero)

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar retiros por cualquier campo si hay un término de búsqueda
    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            retirorepuesto_obrero = retirorepuesto_obrero.filter(fecha_retiro__date=search_date)
        except ValueError:
            text_search = (
                Q(repuesto__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(fecha_retiro__icontains=search_term)
            )
            retirorepuesto_obrero = retirorepuesto_obrero.filter(text_search)
    
    retirorepuesto_obrero = retirorepuesto_obrero.order_by('-fecha_retiro')

    # Paginación
    paginator = Paginator(retirorepuesto_obrero, 10)
    page = request.GET.get('page')

    try:
        retirorepuesto_pagina = paginator.page(page)
    except PageNotAnInteger:
        retirorepuesto_pagina = paginator.page(1)
    except EmptyPage:
        retirorepuesto_pagina = paginator.page(paginator.num_pages)

    # Formatear la fecha antes de pasarla a la plantilla
    for retirorepuesto in retirorepuesto_pagina:
        retirorepuesto.fecha_retiro_formatted = retirorepuesto.fecha_retiro.strftime("%d/%m/%Y %H:%M")

    return render(request, 'app/lista_RetiroRepuesto_obrero.html', {
        'retirorepuesto_obrero': retirorepuesto_pagina,
        'obrero': obrero,
        'search_term': search_term
    })





from django.core.paginator import Paginator





@login_required
def lista_utilesaseo(request):
    search_term = request.GET.get('buscar', '')
    utilesaseos_list = Utilesaseo.objects.all()

    if search_term:
        try:
            # Intentar parsear el término de búsqueda como fecha en formato dd/mm/yyyy
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            # Filtrar por fecha exacta
            date_search = Q(fecha_creacion=search_date)
            utilesaseos_list = utilesaseos_list.filter(date_search)
        except ValueError:
            # Si el término de búsqueda no es una fecha, buscar en otros campos de texto
            text_search = Q(mes__icontains=search_term) | \
                          Q(producto__icontains=search_term) | \
                          Q(cantidad__icontains=search_term) | \
                          Q(nombre_solicitante__nombre__icontains=search_term) | \
                          Q(empresa__nombre__icontains=search_term) | \
                          Q(run__icontains=search_term)
            utilesaseos_list = utilesaseos_list.filter(text_search)

    # Ordenar los resultados por fecha_creacion descendente
    utilesaseos_list = utilesaseos_list.order_by('-fecha_creacion')

    # Paginar los resultados
    paginator = Paginator(utilesaseos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'utilesaseos': page_obj,
        'search_term': search_term,
    }

    return render(request, 'app/lista_utilesaseo.html', context)



@login_required
def registro_utilesaseo(request):
    if request.method == 'POST':
        form = UtilesaseoForm(request.POST)
        if form.is_valid():
            # Guardar el formulario para crear el objeto Utilesaseo
            utilesaseo = form.save(commit=False)
            utilesaseo.save()  # Guardar primero el objeto principal

            # Guardar las relaciones ManyToMany
            form.save_m2m()  # Guardar las relaciones ManyToMany después de guardar el objeto

            # Mensaje de éxito
            success_message = 'El pedido se ha guardado correctamente.'
            return render(request, 'app/registro_utilesaseo.html', {'form': UtilesaseoForm(), 'success_message': success_message})
    else:
        form = UtilesaseoForm()

    return render(request, 'app/registro_utilesaseo.html', {'form': form})



@login_required
def generar_pdf_utiles_aseo(request):
    search_term = request.GET.get('buscar', '')

    if search_term:
        try:
            search_datetime = parse_datetime(search_term)
            search_date = search_datetime.date() if search_datetime else None

            # Construir la consulta de búsqueda
            text_search = Q(mes__icontains=search_term) | \
                           Q(productos__nombre__icontains=search_term) | \
                           Q(cantidad__icontains=search_term) | \
                           Q(nombre_solicitante__nombre__icontains=search_term) | \
                           Q(empresa__nombre__icontains=search_term) | \
                           Q(fecha_creacion__icontains=search_term) | \
                           Q(run__icontains=search_term)

            utilesaseos = Utilesaseo.objects.all()

            # Filtrar por fecha_creacion solo si search_date no es None
            if search_date:
                utilesaseos = utilesaseos.filter(fecha_creacion__date=search_date)

            utilesaseos = utilesaseos.filter(text_search).distinct()

        except ValueError:
            utilesaseos = Utilesaseo.objects.all()
    else:
        utilesaseos = Utilesaseo.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="UTILES_ASEO.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    # Ruta al archivo del logo
    logo_path = os.path.join(settings.STATIC_ROOT, 'app', 'imgenes', 'Logo.png')

    # Verificar si el archivo del logo existe
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f'El archivo {logo_path} no existe.')

    # Agregar el logo al documento con un ancho de 200 unidades y altura de 50 unidades
    logo = Image(logo_path, width=200, height=50)
    elements.append(logo)

    # Agregar el título centrado y en negrita con texto negro
    title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        alignment=1,
        textColor='black',
        fontName='Helvetica-Bold',
        fontSize=18  # Tamaño de fuente ajustado
    )
    elements.append(Paragraph("ENTREGA UTILES DE ASEO", title_style))

    # Obtener los datos del trabajador y la empresa (asumiendo que se relacionan con el primer utilesaseo)
    primer_utilesaseo = utilesaseos.first()
    trabajador_nombre = primer_utilesaseo.nombre_solicitante.nombre if primer_utilesaseo and primer_utilesaseo.nombre_solicitante else ""
    empresa_nombre = primer_utilesaseo.empresa.nombre if primer_utilesaseo and primer_utilesaseo.empresa else ""

    # Agregar nombre del trabajador y empresa debajo del título
    nombre_style = ParagraphStyle(
        'NombreTrabajador',
        parent=getSampleStyleSheet()['Normal'],
        alignment=1,
        textColor='black',
        fontSize=12,
        leading=16  # Ajusta el espacio entre líneas
    )
    elements.append(Paragraph(f"NOMBRE TRABAJADOR: {trabajador_nombre} | EMPRESA: {empresa_nombre}", nombre_style))

    # Agregar espacio en blanco centrado
    elements.append(Spacer(1, 12))

    # Agregar espacio en blanco antes de la tabla
    elements.append(Spacer(1, 12))

    # Agregar la tabla de datos centrada
    data = [
        ['MES', 'PRODUCTO', 'CANTIDAD', 'FECHA DE ENTREGA'],
    ]

    for utilesaseo in utilesaseos:
        productos_nombres = ', '.join([producto.nombre for producto in utilesaseo.productos.all()])
        data.append([
            utilesaseo.mes,
            productos_nombres,
            str(utilesaseo.cantidad),
            utilesaseo.fecha_creacion.strftime("%d/%m/%Y"),
        ])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'yellow'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
    ])

    table = Table(data)
    table.setStyle(style)
    elements.append(table)

    # Agregar espacio en blanco antes del campo de firma
    elements.append(Spacer(1, 24))

    # Agregar el campo de firma más ancho
    signature_style = ParagraphStyle(
        'Signature',
        parent=getSampleStyleSheet()['Normal'],
        alignment=1,
        textColor='black',
        fontSize=12,
        leading=16  # Ajusta el espacio entre líneas
    )
    elements.append(Paragraph("Firma: ____________________________________________", signature_style))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response



@login_required
def generar_pdf_retiro(request, obrero_id):
    # Obtener el obrero específico
    obrero = get_object_or_404(Obrero, id=obrero_id)

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar', '')

    # Obtener los retiros asociados al obrero
    retiros = RetiroRepuesto.objects.filter(trabajador=obrero)

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            retiros = retiros.filter(fecha_retiro__date=search_date)
        except ValueError:
            pass

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="retiros_{obrero.nombre}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    data = [
        ['Fecha', 'Obrero', 'Repuesto', 'Cantidad', 'Empresa'],
    ]

    for retiro in retiros:
        fecha_y_hora = retiro.fecha_retiro.strftime("%d/%m/%Y %H:%M")
        data.append([
            fecha_y_hora,
            retiro.trabajador.nombre,
            retiro.repuesto.nombre,
            retiro.cantidad,
            retiro.empresa.nombre,
        ])

    if len(data) == 1:
        # Si no hay datos, agregar un mensaje a la tabla
        data.append(['No hay registros', '', '', '', ''])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table = Table(data)
    table.setStyle(style)

    width, height = letter
    table.wrapOn(p, width, height)
    table.drawOn(p, 60, height - 200)

    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, f"RETIRO DE REPUESTOS")
    
    
    usuario = request.user
    p.setFont("Helvetica-Bold", 12)
    text = f"PAÑOLERO: {usuario.username}"
    text_width = p.stringWidth(text, "Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, height - 90, text)
    p.line(100, height - 92, 100 + text_width, height - 92)



    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response


@login_required
def generar_pdf_retiros_general(request):
    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar', '')

    # Obtener todos los retiros de repuestos
    retiros = RetiroRepuesto.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            retiros = retiros.filter(fecha_retiro__date=search_date)
        except ValueError:
            pass

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="retiros_general.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    data = [
        ['FECHA', 'TRABAJADOR', 'REPUESTO', 'CANTIDAD', 'EMPRESA'],
    ]

    for retiro in retiros:
        fecha_y_hora = retiro.fecha_retiro.strftime("%d/%m/%Y %H:%M")
        data.append([
            fecha_y_hora,
            retiro.trabajador.nombre,
            retiro.repuesto.nombre,
            retiro.cantidad,
            retiro.empresa.nombre,
        ])

    if len(data) == 1:
        # Si no hay datos, agregar un mensaje a la tabla
        data.append(['No hay registros', '', '', '', ''])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table = Table(data)
    table.setStyle(style)

    width, height = letter
    table.wrapOn(p, width, height)
    table.drawOn(p, 60, height - 250)

    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 40, f"RETIRO DE REPUESTOS")

    usuario = request.user
    p.setFont("Helvetica-Bold", 12)
    text = f"PAÑOLERO: {usuario.username}"
    text_width = p.stringWidth(text, "Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, height - 60, text)
  

 

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response

MESES_EN_ESPAÑOL = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

@login_required
def traducir_mes_en_espanol(fecha):
    """Convierte el nombre del mes en inglés a español."""
    return MESES_EN_ESPAÑOL[fecha.strftime('%B')]

@login_required
def calcular_totales_dia(pedidos, fecha_seleccionada):
    """
    Calcula los totales por día para cada insumo en los pedidos.
    """
    insumos_totales = {}

    for pedido in pedidos:
        insumo = pedido.insumo.nombre
        fecha_pedido = pedido.fecha_pedido.date()  # Convertir a datetime.date
        cantidad = pedido.cantidad

        if fecha_pedido != fecha_seleccionada:
            continue  # Solo procesar pedidos del día seleccionado

        if insumo not in insumos_totales:
            insumos_totales[insumo] = {
                'total': 0,
            }

        # Total general
        insumos_totales[insumo]['total'] += cantidad

    return insumos_totales

@login_required
def pedidos_dia(request):
    fecha_seleccionada_str = request.GET.get('fecha')
    if not fecha_seleccionada_str:
        return HttpResponse("Por favor, seleccione una fecha.")

    try:
        fecha_seleccionada = datetime.strptime(fecha_seleccionada_str, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponse("Fecha inválida. Asegúrese de usar el formato YYYY-MM-DD.")

    # Filtrar pedidos por la fecha seleccionada
    pedidos = Pedido.objects.filter(fecha_pedido__date=fecha_seleccionada)

    # Calcular totales
    insumos_totales = calcular_totales_dia(pedidos, fecha_seleccionada)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{fecha_seleccionada}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar título
    mes_espanol = traducir_mes_en_espanol(fecha_seleccionada)
    fecha_formateada = fecha_seleccionada.strftime(f'%d {mes_espanol} %Y')
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, f"INFORME DE INSUMOS - {fecha_formateada}")

    # Configurar la tabla
    data = [['NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        total = totales['total']
        # Añadir insumo y total
        data.append([insumo, total])

    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar el estilo de fondo amarillo para las celdas específicas
    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 100  # Ajustar la posición vertical

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response

@login_required
def calcular_totales_semana(pedidos, fecha_inicio, fecha_fin):
    """
    Calcula los totales por semana para cada insumo en los pedidos.
    """
    insumos_totales = {}

    for pedido in pedidos:
        insumo = pedido.insumo.nombre
        fecha_pedido = pedido.fecha_pedido.date()  # Convertir a datetime.date
        cantidad = pedido.cantidad

        if not (fecha_inicio <= fecha_pedido <= fecha_fin):
            continue  # Solo procesar pedidos dentro del rango de fechas

        if insumo not in insumos_totales:
            insumos_totales[insumo] = {
                'total': 0,
            }

        # Total general
        insumos_totales[insumo]['total'] += cantidad

    return insumos_totales


@login_required
def pedidos_semana(request):
    fecha_inicio_str = request.GET.get('fecha_inicio')
    if not fecha_inicio_str:
        return HttpResponse("Por favor, seleccione una fecha de inicio.")

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        # Calcula el fin de semana (sábado) de la semana correspondiente
        fecha_fin = fecha_inicio + timedelta(days=6 - fecha_inicio.weekday())
    except ValueError:
        return HttpResponse("Fecha inválida. Asegúrese de usar el formato YYYY-MM-DD.")

    # Filtrar pedidos por la semana seleccionada
    pedidos = Pedido.objects.filter(fecha_pedido__date__range=(fecha_inicio, fecha_fin))

    # Calcular totales
    insumos_totales = calcular_totales_semana(pedidos, fecha_inicio, fecha_fin)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{fecha_inicio}_a_{fecha_fin}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar título
    mes_espanol = traducir_mes_en_espanol(fecha_inicio)
    fecha_formateada_inicio = fecha_inicio.strftime(f'%d {mes_espanol} %Y')
    fecha_formateada_fin = fecha_fin.strftime(f'%d {mes_espanol} %Y')
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, f"INFORME DE INSUMOS - {fecha_formateada_inicio} a {fecha_formateada_fin}")

    # Configurar la tabla
    data = [['NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        total = totales['total']
        # Añadir insumo y total
        data.append([insumo, total])

    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar el estilo de fondo amarillo para las celdas específicas
    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 100  # Ajustar la posición vertical

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response

@login_required
def pedidos_mes(request):
    mes_str = request.GET.get('mes')
    anio_str = request.GET.get('anio')
    
    if not mes_str or not anio_str:
        return HttpResponse("Por favor, seleccione el mes y el año.")

    try:
        mes = int(mes_str)
        anio = int(anio_str)
        fecha_inicio = datetime(anio, mes, 1).date()
        # Determinar el último día del mes
        if mes == 12:
            fecha_fin = datetime(anio + 1, 1, 1).date() - timedelta(days=1)
        else:
            fecha_fin = datetime(anio, mes + 1, 1).date() - timedelta(days=1)
    except ValueError:
        return HttpResponse("Mes o año inválido. Asegúrese de ingresar valores válidos.")

    # Filtrar pedidos por el rango de fechas del mes seleccionado
    pedidos = Pedido.objects.filter(fecha_pedido__date__range=(fecha_inicio, fecha_fin))

    # Calcular totales
    insumos_totales = calcular_totales_mes(pedidos, fecha_inicio, fecha_fin)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{fecha_inicio.strftime("%Y_%m")}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar título
    mes_espanol = traducir_mes_en_espanol(fecha_inicio)
    fecha_formateada_inicio = fecha_inicio.strftime(f'%d {mes_espanol} %Y')
    fecha_formateada_fin = fecha_fin.strftime(f'%d {mes_espanol} %Y')
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, f"INFORME DE INSUMOS MENSUAL - {fecha_formateada_inicio} a {fecha_formateada_fin}")

    # Configurar la tabla
    data = [['NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        total = totales['total']
        # Añadir insumo y total
        data.append([insumo, total])

    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar el estilo de fondo amarillo para las celdas específicas
    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 100  # Ajustar la posición vertical

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response


@login_required
def calcular_totales_mes(pedidos, fecha_inicio, fecha_fin):
    """
    Calcula los totales por mes para cada insumo en los pedidos.
    """
    insumos_totales = {}

    for pedido in pedidos:
        insumo = pedido.insumo.nombre
        cantidad = pedido.cantidad

        if insumo not in insumos_totales:
            insumos_totales[insumo] = {
                'total': 0,
            }

        # Total general
        insumos_totales[insumo]['total'] += cantidad

    return insumos_totales


@login_required
def traducir_mes_en_espanol(fecha):
    """ 
    Traduce el mes al español.
    """
    meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]
    return meses[fecha.month - 1]

@login_required
def pedidos_anio(request):
    anio_str = request.GET.get('anio')
    if not anio_str:
        return HttpResponse("Por favor, seleccione un año.")

    try:
        anio = int(anio_str)
    except ValueError:
        return HttpResponse("Año inválido. Asegúrese de ingresar un número válido.")

    # Filtrar pedidos por el año seleccionado
    pedidos = Pedido.objects.filter(fecha_pedido__year=anio)

    # Calcular totales
    insumos_totales = calcular_totales_anio(pedidos, anio)

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{anio}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar título
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(letter[0] / 2, letter[1] - 40, f"INFORME DE INSUMOS AÑO - {anio}")

    # Configurar la tabla
    data = [['NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    
    for insumo, totales in insumos_totales.items():
        total = totales['total']
        data.append([insumo, total])

    # Estilo para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado de la tabla
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    style.add('BACKGROUND', (0, 0), (0, 0), colors.yellow)  # 'NOMBRE DEL PRODUCTO'
    style.add('BACKGROUND', (1, 0), (1, 0), colors.yellow)  # 'CANTIDAD TOTAL'
    style.add('TEXTCOLOR', (0, 0), (0, 0), colors.black)  # 'NOMBRE DEL PRODUCTO'
    style.add('TEXTCOLOR', (1, 0), (1, 0), colors.black)  # 'CANTIDAD TOTAL'

    # Crear la tabla
    table = Table(data)
    table.setStyle(style)

    # Posicionar la tabla en la página
    width, height = letter
    table_width, table_height = table.wrap(width, height)

    # Calcular la posición para centrar la tabla horizontalmente
    x = (width - table_width) / 2
    y = height - table_height - 100  # Ajustar la posición vertical

    table.drawOn(p, x, y)

    # Guardar el PDF en el buffer
    p.showPage()
    p.save()

    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Establecer el contenido del response con el PDF generado
    response.write(pdf)

    return response

@login_required
def calcular_totales_anio(pedidos, anio):
    """
    Calcula los totales por insumo en los pedidos de un año.
    """
    insumos_totales = {}

    for pedido in pedidos:
        insumo = pedido.insumo.nombre
        cantidad = pedido.cantidad

        if insumo not in insumos_totales:
            insumos_totales[insumo] = {
                'total': 0,
            }

        # Total general
        insumos_totales[insumo]['total'] += cantidad

    return insumos_totales



from django.shortcuts import render
from django.contrib import messages
from tablib import Dataset
from openpyxl import load_workbook
from .models import congelado

@login_required
def upload_csv(request):
    if request.method == 'POST':
        # Obtener el archivo cargado
        new_congelado = request.FILES['file']

        # Verificar que el archivo tenga extensión .xlsx
        if not new_congelado.name.endswith('.xlsx'):
            messages.error(request, 'Por favor sube un archivo en formato Excel (.xlsx).')
            return render(request, 'app/upload_csv.html')

        # Cargar los datos del archivo Excel
        workbook = load_workbook(filename=new_congelado, read_only=True)
        sheet = workbook.active
        data = list(sheet.values)

        # Eliminar la primera fila si contiene encabezados
        headers = data[0]
        rows = data[1:]

        # Iterar sobre las filas e insertar los datos en la base de datos
        for row in rows:
            congelado_obj = congelado(
                orden=row[0],
                caso=row[1] if row[1] is not None else "",  # Asignar vacío si el valor es None
                tag=row[2],
                descripcion_de_equipo=row[3],
                Descripcion_del_fallo=row[4],
                personal=row[5],
                fecha_de_inicio=row[6],
                especialidad=row[7],
                empresa=row[8],
                turno=row[9]
            )
            congelado_obj.save()

        messages.success(request, 'Los datos han sido importados exitosamente.')

    return render(request, 'app/upload_csv.html')


# views.py
from django.core.paginator import Paginator

@login_required
def lista_congelado(request):
    # Obtener todos los objetos Congelado
    queryset = congelado.objects.all()

    # Obtener los valores de los campos de búsqueda
    orden = request.GET.get('orden', '')
    caso = request.GET.get('caso', '')
    tag = request.GET.get('tag', '')
    descripcion_de_equipo = request.GET.get('descripcion_de_equipo', '')
    descripcion_del_fallo = request.GET.get('descripcion_del_fallo', '')
    personal = request.GET.get('personal', '')
    fecha_de_inicio = request.GET.get('fecha_de_inicio', '')
    especialidad = request.GET.get('especialidad', '')
    empresa = request.GET.get('empresa', '')
    turno = request.GET.get('turno', '')

    # Filtrar el queryset en función de los valores de búsqueda
    if orden:
        queryset = queryset.filter(orden__icontains=orden)
    if caso:
        queryset = queryset.filter(caso__icontains=caso)
    if tag:
        queryset = queryset.filter(tag__icontains=tag)
    if descripcion_de_equipo:
        queryset = queryset.filter(descripcion_de_equipo__icontains=descripcion_de_equipo)
    if descripcion_del_fallo:
        queryset = queryset.filter(descripcion_del_fallo__icontains=descripcion_del_fallo)
    if personal:
        queryset = queryset.filter(personal__icontains=personal)
    if fecha_de_inicio:
        queryset = queryset.filter(fecha_de_inicio__icontains=fecha_de_inicio)
    if especialidad:
        queryset = queryset.filter(especialidad__icontains=especialidad)
    if empresa:
        queryset = queryset.filter(empresa__icontains=empresa)
    if turno:
        queryset = queryset.filter(turno__icontains=turno)

    # Paginar los resultados filtrados
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizar la página con los resultados filtrados
    return render(request, 'app/lista_congelado.html', {
        'page_obj': page_obj,
        'orden': orden,
        'caso': caso,
        'tag': tag,
        'descripcion_de_equipo': descripcion_de_equipo,
        'descripcion_del_fallo': descripcion_del_fallo,
        'personal': personal,
        'fecha_de_inicio': fecha_de_inicio,
        'especialidad': especialidad,
        'empresa': empresa,
        'turno': turno,
    })





from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from io import BytesIO
import logging
from xhtml2pdf import pisa
from django.core.paginator import Paginator

@login_required
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")),
        dest=result,
        # Tamaño A4 Landscape
        page_size=(842, 595)
    )
    
    if pisa_status.err:
        logging.error(f"Error en la generación del PDF: {pisa_status.err}")
        return None

    return HttpResponse(result.getvalue(), content_type='application/pdf')

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from PyPDF2 import PdfFileMerger
from django.templatetags.static import static
from django.utils import timezone

from PyPDF2 import PdfMerger
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.templatetags.static import static
from xhtml2pdf import pisa
from django.utils import timezone


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")),
        dest=result,
        # Tamaño A4 Landscape
        page_size=(842, 595)
    )

    if pisa_status.err:
        return None

    return result.getvalue()

@login_required
def generate_pdf(request, personal=None, empresa=None):
    personal = personal or request.GET.get('personal')
    empresa = empresa or request.GET.get('empresa')

    congelados = congelado.objects.all()
    if personal:
        congelados = congelados.filter(personal=personal)
    if empresa:
        congelados = congelados.filter(empresa=empresa)

    # Obtener la URL absoluta de la imagen
    logo_url = request.build_absolute_uri(static('static/app/imgenes/minera.png'))
    logo_url1 = request.build_absolute_uri(static('static/app/imgenes/logo.png'))

    # Obtener la lista de personas dentro de la empresa
    personas = congelados.values_list('personal', flat=True).distinct()

    # Crear un PdfMerger para combinar los PDFs
    merger = PdfMerger()

    # Generar un PDF por cada persona
    for persona in personas:
        # Filtrar los congelados para la persona actual
        congelados_persona = congelados.filter(personal=persona)

        # Calcular filas_vacias para llenar las filas vacías
        max_filas = 16  # O el número de filas que deseas tener en el PDF
        filas_vacias = max_filas - congelados_persona.count()
        
        # Crear una lista de vacías filas
        vacias_filas = [{}] * filas_vacias
        
        context = {
            'congelados': congelados_persona,
            'date': timezone.now().strftime("%d/%m/%Y"),
            'vacias_filas': vacias_filas,
            'logo_url': logo_url,
            'logo_url1': logo_url1,
        }

        # Renderizar el PDF para la persona actual
        pdf = render_to_pdf('app/pdf_template.html', context)
        if pdf:
            # Añadir el PDF generado al merger
            merger.append(BytesIO(pdf))
        else:
            return HttpResponse("Error al generar el PDF para persona: {}".format(persona), status=500)

    # Crear una respuesta HTTP con el PDF combinado
    result = BytesIO()
    merger.write(result)
    merger.close()
    result.seek(0)

    return HttpResponse(result, content_type='application/pdf')


@login_required
def pagina_con_botones(request):
    # Obtener listas únicas de personal y empresas
    lista_personal = congelado.objects.values_list('personal', flat=True).distinct()
    lista_empresas = congelado.objects.values_list('empresa', flat=True).distinct()
    
    # Agregar paginación a la lista de personal
    paginator = Paginator(lista_personal, 10)  # Mostrar 10 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'lista_personal': page_obj,  # Pasa el objeto de paginación a la plantilla
        'lista_empresas': lista_empresas,
    }
    
    return render(request, 'app/pagina_con_botones.html', context)
