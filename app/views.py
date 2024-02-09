# en trabajadores/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import TrabajadorForm,EmpresaForm,ObreroForm, PedidoForm , MaterialForm,HerramientaForm, PrestamoForm,PrestamoEditForm,RepuestoForm,RetiroRepuestoForm
from .models import Trabajador,Empresa,Obrero, Pedido, Material, Herramienta, Prestamo,Repuesto,RetiroRepuesto
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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


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

            # El pedido
            pedido = form.instance

            # El mensaje de éxito
            success_message = 'El pedido se ha guardado correctamente.'

            # Guardar el pedido
            pedido.save()

            return render(request, 'app/registro_pedido.html', {'form': PedidoForm(), 'success_message': success_message})
    else:
        form = PedidoForm()

    return render(request, 'app/registro_pedido.html', {'form': form})




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
    pedidos_list = Pedido.objects.all()

    # Iterar sobre los pedidos para formatear las fechas
    for pedido in pedidos_list:
        pedido.fecha_pedido_formatted = pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M")

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar pedidos por cualquier campo si hay un término de búsqueda
    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y")
            # Utilizar Q() para construir consultas OR entre campos
            pedidos_list = pedidos_list.filter(
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

    paginator = Paginator(pedidos_list, 4)
    page = request.GET.get('page')

    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)

 

    # Si no se está exportando a PDF, renderizar la plantilla normalmente
    return render(request, 'app/lista_pedido.html', {'pedidos': pedidos, 'search_term': search_term})




from django.http import HttpResponse
from django.shortcuts import get_object_or_404



def generar_pdf_pedido(request, obrero_id):
    # Obtener el obrero específico
    obrero = get_object_or_404(Obrero, id=obrero_id)

    # Obtener los préstamos asociados al obrero
    pedidos = Pedido.objects.filter(solicitante=obrero)



    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prestamos_{obrero.nombre}.pdf"'

    # Crear el objeto PDF con ReportLab, con orientación horizontal
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(letter[1], letter[0]))  # Intercambiar ancho y alto

    # Crear una tabla para los datos
    data = [
        ['FECHA', 'NOMBRE', 'EMPRESA', 'INSUMO', 'CANTIDAD', 'AREA'],
    ]

    for pedido in pedidos:
        data.append([
            pedido.fecha_pedido_formatted(),
            pedido.solicitante.nombre,
            pedido.compañia.nombre,
            pedido.insumo.nombre,
            pedido.cantidad,  # Elimina la llamada a str() aquí
            pedido.area,
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
    table.drawOn(p, 100, height - 150)  # Bajar la tabla

    # Agregar título
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "ENTREGA DE INSUMOS | PAÑOL")

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
        ['FECHA', 'NOMBRE', 'EMPRESA', 'INSUMO', 'CANTIDAD', 'AREA'],
    ]

    for pedido in pedidos:
        data.append([
            pedido.fecha_pedido.strftime("%d/%m/%Y"),
            pedido.solicitante.nombre,
            pedido.compañia.nombre,
            pedido.insumo.nombre,
            str(pedido.cantidad),
            pedido.area,
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
    table.drawOn(p, 100, height - 160)  # Bajar la tabla

    # Agregar título
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "ENTREGA DE INSUMOS | PAÑOL")

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
            return redirect('lista_prestamo')


    else:
        form = PrestamoForm()

    return render(request, 'app/registrar_prestamo.html', {'form': form})




@login_required
def lista_prestamo(request):
    prestamos_list = Prestamo.objects.order_by('id').all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar prestamos por nombre si hay un término de búsqueda
    if search_term:
        prestamos_list = prestamos_list.filter(Q(nombre_solicitante__nombre__icontains=search_term))

    paginator = Paginator(prestamos_list, 5)
    page = request.GET.get('page')

    try:
        prestamos = paginator.page(page)
    except PageNotAnInteger:
        prestamos = paginator.page(1)
    except EmptyPage:
        prestamos = paginator.page(paginator.num_pages)

    # Formatear la fecha y la hora antes de pasarla a la plantilla
    for prestamo in prestamos:
        prestamo.fecha_creacion_formatted = prestamo.fecha_creacion.strftime("%d/%m/%Y %H:%M")
        prestamo.fecha_recepcion_formatted = prestamo.fecha_recepcion.strftime("%d/%m/%Y %H:%M") if prestamo.fecha_recepcion else None

    # Obtener el mensaje de éxito de la URL
    success_message = request.GET.get('success_message', None)

    return render(request, 'app/lista_prestamo.html', {
        'prestamos': prestamos,
        'search_term': search_term,
        'success_message': success_message,
        'form': PrestamoEditForm(),  # Agrega el formulario al contexto
    })


def generar_pdf_prestamos(request):
    # Obtener todos los préstamos
    prestamos = Prestamo.objects.all()

    # Crear el objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="todos_los_prestamos.pdf"'

    # Crear el objeto PDF con ReportLab, con orientación horizontal
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(letter[1], letter[0]))  # Intercambiar ancho y alto

    # Crear una tabla para los datos
    data = [
        ['NOMBRE SOLICITANTE', 'EMPRESA', 'HERRAMIENTA', 'FECHA CREACION', 'FECHA RECEPCION', 'ESTADO'],
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
    table.drawOn(p, 100, height - 160)  # Bajar la tabla

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
        ['NOMBRE SOLICITANTE', 'EMPRESA', 'HERRAMIENTA', 'FECHA CREACION', 'FECHA RECEPCION', 'ESTADO'],
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
    table.drawOn(p, 100, height - 150)  # Bajar la tabla

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

    return render(request, 'app/lista_prestamo.html', {'prestamo': zip(prestamo, prestamo_forms)})

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
            form.save()
            return redirect('lista_RetiroRepuesto')
    else:
        form = RetiroRepuestoForm()  # Corregir el formulario aquí

    return render(request, 'app/registro_RetiroRepuesto.html', {'form': form})

@login_required
def lista_RetiroRepuesto(request):
    retirorepuestos_list = RetiroRepuesto.objects.order_by('id').all()

    # Obtener el término de búsqueda de la URL
    search_term = request.GET.get('buscar')

    # Filtrar retiros de repuestos por nombre si hay un término de búsqueda
    if search_term:
        retirorepuestos_list = retirorepuestos_list.filter(Q(nombre__icontains=search_term))

    paginator = Paginator(retirorepuestos_list, 5)

    # Obtener el número de página, estableciendo 1 como valor predeterminado
    page = request.GET.get('page', 1)

    try:
        retirorepuestos = paginator.page(page)
    except PageNotAnInteger:
        retirorepuestos = paginator.page(1)
    except EmptyPage:
        retirorepuestos = paginator.page(paginator.num_pages)

    return render(request, 'app/lista_RetiroRepuesto.html', {'retirorepuestos': retirorepuestos, 'search_term': search_term})


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