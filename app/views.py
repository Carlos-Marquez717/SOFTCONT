# en trabajadores/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import TrabajadorForm,EmpresaForm,ObreroForm, PedidoForm , MaterialForm,HerramientaForm, PrestamoForm,PrestamoEditForm,RepuestoForm,RetiroRepuestoForm,UtilesaseoForm
from .models import Trabajador,Empresa,Obrero, Pedido, Material, Herramienta, Prestamo,Repuesto,RetiroRepuesto,Utilesaseo
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
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
from datetime import datetime
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
def eliminar_pedido(request, pedido_id):
    # Obtiene el pedido o muestra una página de error si no existe
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Elimina el pedido
    pedido.delete()

    # Redirige a la lista de pedidos después de la eliminación
    return redirect('lista_pedido')

@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'El pedido se ha modificado correctamente.')
            return redirect('lista_pedido')
        else:
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
            # Obtener el objeto de repuesto
            repuesto = form.cleaned_data['repuesto']  # Ajusta según tu formulario

            # Actualizar la cantidad de repuestos
            repuesto.cantidad = F('cantidad') - form.cleaned_data['cantidad']  # Ajusta según tu formulario
            repuesto.save()

            messages.success(request, 'El retiro de repuesto se ha registrado correctamente.')
            return redirect('registro_RetiroRepuesto_success')
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



@login_required
def lista_RetiroRepuesto_obrero(request, obrero_id):
    # Obtiene el obrero correspondiente al ID o devuelve un 404 si no existe
    obrero = get_object_or_404(Obrero, id=obrero_id)

    # Filtra los préstamos por el obrero asociado
    retirorepuesto_obrero = RetiroRepuesto.objects.filter(trabajador=obrero)

    # Paginación (si es necesario)
    paginator = Paginator(retirorepuesto_obrero, 10)
    page = request.GET.get('page')
    retirorepuesto_pagina = paginator.get_page(page)

    # Formatear la fecha y la hora antes de pasarla a la plantilla
    for retirorepuesto in retirorepuesto_pagina:
        
        retirorepuesto.fecha_retiro_formatted = retirorepuesto.fecha_retiro.strftime("%d/%m/%Y %H:%M") 
        
    return render(request, 'app/lista_RetiroRepuesto_obrero.html', {'retirorepuesto_obrero': retirorepuesto_obrero ,'obrero': obrero, })




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
            form.save()

            # El pedido
            utilesaseo = form.instance

            # El mensaje de éxito
            success_message = 'El pedido se ha guardado correctamente.'

            # Guardar el pedido
            utilesaseo.save()

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

            text_search = Q(mes__icontains=search_term) | \
                           Q(producto__icontains=search_term) | \
                           Q(cantidad__icontains=search_term) | \
                           Q(nombre_solicitante__nombre__icontains=search_term) | \
                           Q(empresa__nombre__icontains=search_term) | \
                           Q(fecha_creacion__icontains=search_term) | \
                           Q(run__icontains=search_term)

            utilesaseos = Utilesaseo.objects.all()

            # Filtrar por fecha_creacion solo si search_date no es None
            if search_date:
                utilesaseos = utilesaseos.filter(fecha_creacion__date=search_date)

            utilesaseos = utilesaseos.filter(text_search)

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
        data.append([
            utilesaseo.mes,
            utilesaseo.producto,
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
