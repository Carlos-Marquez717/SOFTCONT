# en trabajadores/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from httpcore import request
from matplotlib import table
from .forms import TrabajadorForm,EmpresaForm,ObreroForm, PedidoForm , MaterialForm,UtilAseoDetalleFormSet,HerramientaForm,InformeCaso6Form,ImagenInformeFormSet,ImagenSoloImagenFormSet,InformeCaso5Form,InformeCaso2Form,InformeCaso3Form,InformeCaso4Form, PrestamoForm,PrestamoEditForm,RepuestoForm, RetiroRepuestoFormSet, RetiroRepuestoFormSet,UtilesaseoForm, PedidoInsumoForm, PedidoInsumoInlineFormset,InformeForm
from .models import Trabajador,Empresa,Obrero,VerificacionInforme, Pedido, Material, Herramienta,UtilAseoDetalle, Prestamo,Repuesto,RetiroRepuesto,Utilesaseo,PedidoInsumo,Informe,ImagenInforme
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
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .forms import LoginForm
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group, User
from django.conf import settings
import os
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from django.contrib.auth.decorators import login_required


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




def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'Registration/register.html', data)

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



from django.forms import modelformset_factory


@login_required
def registro_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        insumo_formset = PedidoInsumoInlineFormset(request.POST)
        if pedido_form.is_valid() and insumo_formset.is_valid():
            pedido = pedido_form.save()
            insumos = insumo_formset.save(commit=False)
            for insumo in insumos:
                insumo.trabajador = pedido.solicitante  # Asigna el trabajador del pedido
                insumo.area = pedido.area               # Asigna el área del pedido
                insumo.pedido = pedido                  # Asocia el pedido
                insumo.save()
            # Si tienes insumos eliminados, puedes borrarlos así:
            for obj in insumo_formset.deleted_objects:
                obj.delete()
            # Redirige o muestra mensaje de éxito
            return redirect('registro_pedido_success')
    else:
        pedido_form = PedidoForm()
        insumo_formset = PedidoInsumoInlineFormset()
    
    return render(request, 'app/registro_pedido.html', {
        'pedido_form': pedido_form,
        'insumo_formset': insumo_formset
    })


@login_required
def registro_pedido_success(request):
    success_message = 'El pedido se ha guardado correctamente.'
    pedido_form = PedidoForm()
    insumo_formset = PedidoInsumoInlineFormset(queryset=PedidoInsumo.objects.none())
    
    return render(request, 'app/registro_pedido.html', {
        'pedido_form': pedido_form,
        'insumo_formset': insumo_formset,
        'success_message': success_message
    })




from django.db.models import Q

@login_required
def lista_pedido_trabajador(request, trabajador_id):
    obrero = get_object_or_404(Obrero, id=trabajador_id)

    search_term = request.GET.get('buscar', '')
    
    # Base queryset: solo pedidos del trabajador
    pedidos_insumos = PedidoInsumo.objects.filter(trabajador=obrero).select_related(
        'pedido', 'insumos', 'pedido__compañia', 'pedido__solicitante'
    )

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedidos_insumos = pedidos_insumos.filter(pedido__fecha_pedido__date=search_date)
        except ValueError:
            pedidos_insumos = pedidos_insumos.filter(
                Q(insumos__nombre__icontains=search_term) |
                Q(pedido__compañia__nombre__icontains=search_term) |
                Q(pedido__area__icontains=search_term) |
                Q(pedido__solicitante__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term)
            )

    # Ordenar si lo necesitas
    pedidos_insumos = pedidos_insumos.order_by('-pedido__fecha_pedido')

    # Paginación
    paginator = Paginator(pedidos_insumos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'app/lista_pedido_trabajador.html', {
        'obrero': obrero,
        'pedidos': page_obj,
        'search_term': search_term,
    })



@login_required
def lista_pedido(request):
    search_term = request.GET.get('buscar')
    
    pedidos_list = PedidoInsumo.objects.select_related(
        'pedido__solicitante', 'pedido__compañia', 'insumos', 'trabajador'
    ).all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedidos_list = pedidos_list.filter(pedido__fecha_pedido__date=search_date)
        except ValueError:
            text_search = (
                Q(insumos__nombre__icontains=search_term) |
                Q(pedido__solicitante__nombre__icontains=search_term) |
                Q(pedido__compañia__nombre__icontains=search_term) |
                Q(pedido__area__icontains=search_term) |
                Q(cantidad__icontains=search_term)
            )
            pedidos_list = pedidos_list.filter(text_search)

    pedidos_list = pedidos_list.order_by('-pedido__fecha_pedido')

    paginator = Paginator(pedidos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pedidos': page_obj,
        'search_term': search_term,
    }

    return render(request, 'app/lista_pedido.html', context)


  


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import os
from django.conf import settings
from .models import Pedido

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings
from django.db.models import Q
from io import BytesIO
from datetime import datetime
import os
import qrcode

from io import BytesIO
from datetime import datetime
import os
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
import qrcode
from .models import Pedido



from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime
import qrcode
import os

from .models import Pedido, PedidoInsumo  # asegúrate que ambos modelos estén importados


from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os, qrcode
from io import BytesIO
from .models import PedidoInsumo, Pedido, Obrero
from django.conf import settings

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime
import os
import qrcode

from django.urls import reverse
from django.conf import settings
from .models import PedidoInsumo, Pedido, Obrero

@login_required
def generar_pdf_pedido(request, obrero_id):
    search_term = request.GET.get('buscar')
    pedido_insumos = PedidoInsumo.objects.filter(pedido__solicitante_id=obrero_id)

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedido_insumos = pedido_insumos.filter(
                Q(pedido__fecha_pedido__date=search_date) |
                Q(pedido__solicitante__nombre__icontains=search_term) |
                Q(pedido__compañia__nombre__icontains=search_term) |
                Q(insumos__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(pedido__area__icontains=search_term)
            )
        except ValueError:
            pedido_insumos = pedido_insumos.filter(
                Q(pedido__solicitante__nombre__icontains=search_term) |
                Q(pedido__compañia__nombre__icontains=search_term) |
                Q(insumos__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(pedido__area__icontains=search_term)
            )

    ultimo_insumo = pedido_insumos.order_by('-pedido__fecha_pedido').first()
    if ultimo_insumo:
        nombre_trabajador = ultimo_insumo.trabajador.nombre
        nombre_empresa = ultimo_insumo.pedido.compañia.nombre
        codigo_unico = ultimo_insumo.pedido.codigo_unico
    else:
        nombre_trabajador = "N/A"
        nombre_empresa = "N/A"
        codigo_unico = None

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PEDIDOS.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    margin = 50

    logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Logo.png')
    minera_logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Minera.png')

    if codigo_unico:
        url_verificacion = request.build_absolute_uri(
            reverse('verificar_reporte_personal', args=[str(codigo_unico), obrero_id])
        )
    else:
        url_verificacion = "No disponible"

    qr = qrcode.make(url_verificacion)
    qr_io = BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_img = ImageReader(qr_io)

    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(
        'NormalCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=0,
        wordWrap='CJK',
    )
    style_centered = ParagraphStyle(
        name='centered',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=1,  # 1 = CENTER
        wordWrap='CJK',
    )

    minera_width, minera_height = 80, 60
    qr_width, qr_height = 60, 60
    p.drawImage(minera_logo_path, width - margin - minera_width, height - margin - minera_height,
                width=minera_width, height=minera_height, mask='auto')

    qr_x = 150
    qr_y = height - 110
    p.drawImage(qr_img, qr_x, qr_y, width=qr_width, height=qr_height)
    if codigo_unico:
        p.setFont("Helvetica-Bold", 10)
        p.drawCentredString(qr_x + qr_width / 2, qr_y - 20, f"N° REPORTE: {codigo_unico}")

    p.setFont("Helvetica-Bold", 14)
    titulo_y = height - 80
    p.drawCentredString(width / 2, titulo_y, "ENTREGA DE INSUMOS DIARIOS | PAÑOL")

    p.setFont("Helvetica", 10)
    info_y = titulo_y - 15
    p.drawCentredString(width / 2, info_y,
                        f"PAÑOLERO: {request.user.username}    |    FECHA REPORTE: {datetime.now().strftime('%d/%m/%Y')}")
    p.drawCentredString(width / 2, info_y - 15,
                        f"HISTORIAL DE PEDIDOS: {nombre_trabajador} ({nombre_empresa})")

    data = [['FECHA', 'TRABAJADOR', 'EMPRESA', 'INSUMO', 'CANTIDAD', 'AREA']]
    for insumo in pedido_insumos.order_by('-pedido__fecha_pedido'):
        data.append([
            insumo.pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M"),
            Paragraph(str(insumo.trabajador.nombre), style_centered),  # Centrado
            Paragraph(str(insumo.pedido.compañia.nombre), style_centered),  # Centrado
            Paragraph(str(insumo.insumos.nombre), style_centered),  # Centrado
            str(insumo.cantidad),
            Paragraph(str(insumo.pedido.area), style_centered),  # Centrado
        ])

    if len(data) == 1:
        data.append(['No hay registros', '', '', '', '', ''])

    column_widths = [90, 110, 140, 160, 60, 140]
    table = Table(data, colWidths=column_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        # Centrar columnas TRABAJADOR (1), EMPRESA (2), INSUMO (3), AREA (5)
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),
        ('ALIGN', (4, 1), (4, -1), 'CENTER'),  # CANTIDAD
        ('ALIGN', (5, 1), (5, -1), 'CENTER'),

        # Centrar encabezado completo
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
    ]))

    table_width, table_height = table.wrap(0, 0)
    x_centered = (width - table_width) / 2
    y_position = info_y - 40

    table.drawOn(p, x_centered, y_position - table_height)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.utils.timezone import now
from django.urls import reverse
from reportlab.lib.pagesizes import landscape, letter
from uuid import uuid4
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import reverse
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
import qrcode
from .models import Pedido, ReportePedido, ReporteInsumo



@login_required
def generar_pdf_pedidos(request):
    search_term = request.GET.get('buscar', '')
    pedidos = Pedido.objects.all()
    search_date = None
    filtro_insumo_cantidad = False

    if search_term:
        try:
            if "/" in search_term:
                search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            else:
                search_date = datetime.strptime(search_term, "%Y-%m-%d").date()
        except ValueError:
            search_date = None

        if search_date:
            pedidos = pedidos.filter(fecha_pedido__date=search_date)
        else:
            # Detecta si está filtrando por insumo o cantidad
            filtro_insumo_cantidad = Material.objects.filter(nombre__icontains=search_term).exists() or search_term.isdigit()

            pedidos = pedidos.filter(
                Q(solicitante__nombre__icontains=search_term) |
                Q(compañia__nombre__icontains=search_term) |
                Q(pedidoinsumo__insumos__nombre__icontains=search_term) |
                Q(pedidoinsumo__cantidad__icontains=search_term) |
                Q(area__icontains=search_term)
            ).distinct()

    if not pedidos.exists():
        return HttpResponse("No se encontraron pedidos con ese criterio.")

    reporte = ReportePedido.objects.create(generado_por=request.user.username)
    reporte.pedidos.set(pedidos)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{reporte.codigo_reporte}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=80,
        leftMargin=80,
        topMargin=100,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    style_centered = ParagraphStyle(name='centered', alignment=1, fontSize=9)

    url_verificacion = request.build_absolute_uri(
        reverse('verificar_reporte', args=[str(reporte.codigo_reporte)])
    )
    qr = qrcode.make(url_verificacion)
    qr_io = BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_img = ImageReader(qr_io)

    def add_header(canvas, doc):
        width, height = landscape(letter)
        usuario = request.user.username

        logo_izquierdo = os.path.join(settings.BASE_DIR, 'app/static/app/imgenes/Logo.png')
        logo_derecho = os.path.join(settings.BASE_DIR, 'app/static/app/imgenes/minera.png')

        if os.path.exists(logo_izquierdo):
            canvas.drawImage(logo_izquierdo, 40, height - 80, width=100, height=80, preserveAspectRatio=True)
        if os.path.exists(logo_derecho):
            canvas.drawImage(logo_derecho, width - 100, height - 80, width=100, height=60, preserveAspectRatio=True)

        canvas.drawImage(qr_img, 150, height - 100, width=60, height=60)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawCentredString(180, height - 140, f"N° REPORTE: {reporte.codigo_reporte}")
        canvas.setFont("Helvetica-Bold", 13)
        canvas.drawCentredString(width / 2, height - 100, "ENTREGA DE INSUMOS DIARIOS | PAÑOL")
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(40, height - 120, f"PAÑOLERO: {usuario}")
        canvas.drawRightString(width - 40, height - 120, f"FECHA: {now().strftime('%d/%m/%Y')}")

    elements = [Spacer(1, 30)]
    data = [['FECHA', 'TRABAJADOR', 'EMPRESA', 'INSUMO', 'CANT', 'AREA']]

    for pedido in pedidos:
        fecha_y_hora = pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M")
        pedido_insumos = pedido.pedidoinsumo_set.all()

        if filtro_insumo_cantidad:
            pedido_insumos = pedido_insumos.filter(
                Q(insumos__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term)
            )

        for pedido_insumo in pedido_insumos:
            ReporteInsumo.objects.create(
                reporte=reporte,
                pedido=pedido,
                trabajador=pedido.solicitante,
                insumo=pedido_insumo.insumos,
                cantidad=pedido_insumo.cantidad,
                area=pedido.area
            )

            data.append([
                fecha_y_hora,
                Paragraph(str(pedido.solicitante.nombre), style_centered),
                Paragraph(str(pedido.compañia.nombre), style_centered),
                Paragraph(str(pedido_insumo.insumos.nombre), style_centered),
                Paragraph(str(pedido_insumo.cantidad), style_centered),
                Paragraph(str(pedido.area), style_centered),
            ])

    if len(data) == 1:
        data.append(['No hay registros', '', '', '', '', ''])

    table = Table(data, colWidths=[
        1.2 * inch, 1.8 * inch, 2 * inch, 2.5 * inch, 0.8 * inch, 1.7 * inch
    ])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(Spacer(1, 20))
    elements.append(table)

    doc.build(elements, onFirstPage=add_header, onLaterPages=add_header)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response






@login_required
def eliminar_pedido(request, pedido_id):
    pedido_insumo = get_object_or_404(PedidoInsumo, id=pedido_id)
    trabajador_id = request.GET.get('trabajador_id', pedido_insumo.trabajador.id)
    pedido_insumo.delete()
    return redirect(f'/lista_pedido_trabajador/{trabajador_id}/?eliminado=1')


import logging

logger = logging.getLogger(__name__)


@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, instance=pedido)
        insumo_formset = PedidoInsumoInlineFormset(request.POST, instance=pedido)
        if pedido_form.is_valid() and insumo_formset.is_valid():
            pedido = pedido_form.save()
            insumos = insumo_formset.save(commit=False)
            for insumo in insumos:
                insumo.trabajador = pedido.solicitante
                insumo.area = pedido.area
                insumo.pedido = pedido
                insumo.save()
            for obj in insumo_formset.deleted_objects:
                obj.delete()
            return redirect('lista_pedido')
        else:
            # Opcional: mostrar errores en el template
            print(pedido_form.errors, insumo_formset.errors)
    else:
        pedido_form = PedidoForm(instance=pedido)
        insumo_formset = PedidoInsumoInlineFormset(instance=pedido)
    return render(request, 'app/editar_pedido.html', {
        'pedido_form': pedido_form,
        'insumo_formset': insumo_formset,
        'pedido': pedido,
    })

    
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


from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Prestamo  # Asegúrate de importar el modelo correcto

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from .models import Prestamo

from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.conf import settings
from django.urls import reverse
from io import BytesIO
import qrcode
from datetime import datetime

@login_required
def generar_pdf_prestamos(request):
    search_term = request.GET.get('buscar')
    prestamos_list = Prestamo.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            prestamos_list = prestamos_list.filter(
                Q(nombre_solicitante__nombre__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(herramienta__nombre__icontains=search_term) |
                Q(fecha_creacion=search_date) |
                Q(status__icontains=search_term)
            )
        except ValueError:
            prestamos_list = prestamos_list.filter(
                Q(herramienta__nombre__icontains=search_term) |
                Q(status__icontains=search_term)
            )

    if not prestamos_list.exists():
        return HttpResponse("No se encontraron resultados para la búsqueda.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prestamos_{search_term}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    margin = 50

    # Logos
    logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Logo.png')
    minera_logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Minera.png')

    try:
        p.drawImage(minera_logo_path, width - margin - 80, height - margin - 60, width=80, height=60, mask='auto')
    except:
        pass

    # QR Code con URL ficticia (puedes personalizarla)
    url_verificacion = request.build_absolute_uri(reverse('verificar_reporte_prestamos'))

    qr = qrcode.make(url_verificacion)
    qr_io = BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_img = ImageReader(qr_io)
    p.drawImage(qr_img, 150, height - 110, width=60, height=60)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(180, height - 120, "VERIFICACIÓN")

    # Título
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 80, "LISTADO DE PRÉSTAMOS DE HERRAMIENTAS")
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, height - 95,
        f"USUARIO: {request.user.username}  |  FECHA REPORTE: {datetime.now().strftime('%d/%m/%Y')}")

    # Datos
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    styles = getSampleStyleSheet()
    style_center = ParagraphStyle('center', parent=styles['Normal'], alignment=1, fontSize=9)

    data = [[
        'NOMBRE SOLICITANTE', 'EMPRESA', 'HERRAMIENTA',
        'FECHA PRÉSTAMO', 'FECHA RECEPCIÓN', 'ESTADO'
    ]]

    for prestamo in prestamos_list:
        estado_color = colors.red if prestamo.status == 'NO_ENTREGADO' else colors.black
        data.append([
            Paragraph(prestamo.nombre_solicitante.nombre, style_center),
            Paragraph(prestamo.empresa.nombre, style_center),
            Paragraph(prestamo.herramienta.nombre, style_center),
            prestamo.fecha_creacion.strftime("%d/%m/%Y %H:%M") if prestamo.fecha_creacion else 'Sin fecha',
            prestamo.fecha_recepcion.strftime("%d/%m/%Y %H:%M") if prestamo.fecha_recepcion else 'Sin fecha',
            Paragraph(f'<font color="{estado_color}">{prestamo.status}</font>', style_center)
        ])

    col_widths = [120, 100, 120, 100, 110, 100]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
    ]))

    table_width, table_height = table.wrap(0, 0)
    x_centered = (width - table_width) / 2
    y_position = height - 150

    table.drawOn(p, x_centered, y_position - table_height)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


from django.shortcuts import render
from .models import Prestamo

@login_required
def verificar_reporte_prestamos(request):
    prestamos = Prestamo.objects.all().order_by('-fecha_creacion')
    return render(request, 'verificacionqr/verificar_reporte_prestamos.html', {'prestamos': prestamos})




@login_required
def verificar_prestamos(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    return render(request, 'verificacionqr/verificar_prestamoid.html', {'prestamo': prestamo})

from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.contrib.auth.decorators import login_required
import qrcode
from django.templatetags.static import static
from reportlab.lib.utils import ImageReader
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
import qrcode
from .models import Prestamo, DetallePrestamo


from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from PIL import Image
import os
import qrcode
from .models import Prestamo, DetallePrestamo
import qrcode
from reportlab.lib.utils import Image 
from PIL import Image as PILImage  # ✅ Renombramos para evitar conflictos
from io import BytesIO





@login_required
def generar_pdf_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PRESTAMO_{prestamo.id}.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    margin = 50

    # Rutas de imágenes
    logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Logo.png')
    minera_logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Minera.png')

    # Logo Minera
    minera_width, minera_height = 80, 60
    p.drawImage(minera_logo_path, width - margin - minera_width, height - margin - minera_height, width=minera_width, height=minera_height, mask='auto')

    # QR Code
    qr_data = f"http://127.0.0.1:8000/verificar_prestamos/{prestamo.id}/"

    qr_img = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_pil = PILImage.open(qr_buffer)
    p.drawInlineImage(qr_pil, margin, height - margin - 80, width=60, height=60)

    # Título
    p.setFont("Helvetica-Bold", 14)
    titulo_y = height - 80
    p.drawCentredString(width / 2, titulo_y, "REPORTE DE PRÉSTAMO DE HERRAMIENTA")

    # Información del préstamo
    p.setFont("Helvetica", 10)
    info_y = titulo_y - 15
    p.drawCentredString(
        width / 2,
        info_y,
        f"RESPONSABLE: {request.user.username}    |    FECHA PRÉSTAMO: {prestamo.fecha_creacion.strftime('%d/%m/%Y')}"
    )
    p.drawCentredString(
        width / 2,
        info_y - 15,
        f"TRABAJADOR: {prestamo.nombre_solicitante.nombre} ({prestamo.empresa.nombre})"
    )

    # Estilo tabla
    styles = getSampleStyleSheet()
    style_centered = ParagraphStyle(
        name='centered',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        alignment=1,
        wordWrap='CJK',
    )

    # Tabla única (sin DetallePrestamo)
    data = [['FECHA PRÉSTAMO', 'HERRAMIENTA', 'ESTADO', 'FECHA RECEPCIÓN']]
    data.append([
        prestamo.fecha_creacion.strftime("%d/%m/%Y"),
        Paragraph(prestamo.herramienta.nombre, style_centered),
        Paragraph(prestamo.status, style_centered),
        Paragraph(prestamo.fecha_recepcion.strftime("%d/%m/%Y") if prestamo.fecha_recepcion else "Pendiente", style_centered),
    ])

    table = Table(data, colWidths=[120, 250, 120, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
    ]))

    table_width, table_height = table.wrap(0, 0)
    x_centered = (width - table_width) / 2
    y_position = info_y - 60
    table.drawOn(p, x_centered, y_position - table_height)

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
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





from django.forms import modelformset_factory
from .models import RetiroRepuesto
from .forms import RetiroRepuestoForm

RetiroRepuestoFormSet = modelformset_factory(
    RetiroRepuesto,
    form=RetiroRepuestoForm,
    extra=1,
    can_delete=True
)    

from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RetiroRepuesto, Repuesto
from .forms import RetiroRepuestoForm
from django.forms import modelformset_factory
from .models import RetiroRepuesto
from .forms import RetiroRepuestoForm  # adjust the import path as needed
from .forms import InfoGeneralRetiroForm

RetiroRepuestoFormSet = modelformset_factory(
    RetiroRepuesto,
    form=RetiroRepuestoForm,  # custom form if you have one; otherwise omit
    fields=('repuesto', 'cantidad'),  # or use 'form' only if it defines fields
    extra=1,
    can_delete=True  # allows users to delete items in formset
)


@login_required
def registro_RetiroRepuesto(request):
    RetiroFormSet = RetiroRepuestoFormSet
    if request.method == 'POST':
        info_form = InfoGeneralRetiroForm(request.POST)
        formset = RetiroFormSet(request.POST, queryset=RetiroRepuesto.objects.none())

        if info_form.is_valid() and formset.is_valid():
            trabajador = info_form.cleaned_data['trabajador']
            empresa = info_form.cleaned_data['empresa']
            area = info_form.cleaned_data['area']

            valid = True
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    repuesto = form.cleaned_data['repuesto']
                    cantidad = form.cleaned_data['cantidad']
                    if repuesto.cantidad < cantidad:
                        messages.error(request, f"No hay suficiente stock de '{repuesto.nombre}'. Disponible: {repuesto.cantidad}")
                        valid = False
                        break

            if valid:
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        repuesto = form.cleaned_data['repuesto']
                        cantidad = form.cleaned_data['cantidad']
                        Repuesto.objects.filter(pk=repuesto.pk).update(cantidad=F('cantidad') - cantidad)
                        RetiroRepuesto.objects.create(
                            trabajador=trabajador,
                            empresa=empresa,
                            area=area,
                            repuesto=repuesto,
                            cantidad=cantidad
                        )
                messages.success(request, '¡Retiros registrados correctamente!')
                return redirect('registro_RetiroRepuesto')
        else:
            messages.error(request, 'Corrige los errores del formulario.')

    else:
        info_form = InfoGeneralRetiroForm()
        formset = RetiroFormSet(queryset=RetiroRepuesto.objects.none())

    return render(request, 'app/registro_RetiroRepuesto.html', {
        'info_form': info_form,
        'formset': formset,
    })


@login_required
def registro_RetiroRepuesto_success(request):
    messages.success(request, 'El retiro de repuesto se ha registrado correctamente.')
    return render(request, 'app/registro_RetiroRepuesto.html', {'form': RetiroRepuestoForm(), 'success_message': messages.get_messages(request)})


from django.db.models import Q
@login_required
def lista_RetiroRepuesto(request):
    search_term = request.GET.get('buscar', '')
    retirorepuestos = RetiroRepuesto.objects.all()

    if search_term:
        retirorepuestos = retirorepuestos.filter(
            Q(trabajador__nombre__icontains=search_term) |   # Ajusta 'nombre' si tu modelo Obrero usa otro campo
            Q(empresa__nombre__icontains=search_term) |      # Ajusta 'nombre' si tu modelo Empresa usa otro campo
            Q(repuesto__nombre__icontains=search_term) |     # Ajusta 'nombre' si tu modelo Repuesto usa otro campo
            Q(area__icontains=search_term) |
            Q(cantidad__icontains=search_term) |
            Q(fecha_retiro__icontains=search_term)
        )

    # Paginación (opcional)
    from django.core.paginator import Paginator
    paginator = Paginator(retirorepuestos, 10)
    page_number = request.GET.get('page')
    retirorepuestos = paginator.get_page(page_number)

    context = {
        'retirorepuestos': retirorepuestos,
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





from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Utilesaseo

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from .models import Utilesaseo

@login_required
def lista_utilesaseo(request):
    search_term = request.GET.get('buscar', '').strip()
    producto_term = request.GET.get('producto', '').strip()
    utilesaseos_list = Utilesaseo.objects.all()

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            utilesaseos_list = utilesaseos_list.filter(fecha_creacion=search_date)
        except ValueError:
            text_search = (
                Q(mes__icontains=search_term) |
                Q(detalles__producto__nombre__icontains=search_term) |
                Q(detalles__cantidad__icontains=search_term) |
                Q(nombre_solicitante__nombre__icontains=search_term) |
                Q(empresa__nombre__icontains=search_term) |
                Q(fecha_creacion__icontains=search_term) |
                Q(run__icontains=search_term)
            )
            utilesaseos_list = utilesaseos_list.filter(text_search).distinct()

    if producto_term:
        utilesaseos_list = utilesaseos_list.filter(detalles__producto__nombre__icontains=producto_term).distinct()

    utilesaseos_list = utilesaseos_list.order_by('-fecha_creacion')
    paginator = Paginator(utilesaseos_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'utilesaseos': page_obj,
        'search_term': search_term,
        'producto_term': producto_term,
    }
    return render(request, 'app/lista_utilesaseo.html', context)







@login_required
def registro_utilesaseo(request):
    if request.method == 'POST':
        form = UtilesaseoForm(request.POST)
        formset = UtilAseoDetalleFormSet(request.POST, queryset=UtilAseoDetalle.objects.none())
        if form.is_valid() and formset.is_valid():
            mes = form.cleaned_data['mes']
            nombre_solicitante = form.cleaned_data['nombre_solicitante']
            empresa = form.cleaned_data['empresa']
            año_actual = datetime.now().year

            productos_en_form = []
            errores = []

            # Validar productos ya registrados
            for detalle_form in formset:
                if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                    producto = detalle_form.cleaned_data['producto']
                    productos_en_form.append(producto)

                    existe = UtilAseoDetalle.objects.filter(
                        utilesaseo__mes=mes,
                        utilesaseo__fecha_creacion__year=año_actual,
                        utilesaseo__nombre_solicitante=nombre_solicitante,
                        utilesaseo__empresa=empresa,
                        producto=producto
                    ).exists()

                    if existe:
                        errores.append(f"Ya se ha registrado {producto.nombre} en {mes} para este trabajador.")

            # Validar productos repetidos dentro del mismo formset
            if len(productos_en_form) != len(set(productos_en_form)):
                errores.append("No puedes repetir productos en el mismo formulario.")

            if errores:
                for error in errores:
                    messages.error(request, error)
            else:
                utilesaseo = form.save()
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalle = detalle_form.save(commit=False)
                        detalle.utilesaseo = utilesaseo
                        detalle.save()
                messages.success(request, "Registro de útiles realizado correctamente.")
                return redirect('registro_utilesaseo')  # Ajusta con la vista correcta
    else:
        form = UtilesaseoForm()
        formset = UtilAseoDetalleFormSet(queryset=UtilAseoDetalle.objects.none())

    return render(request, 'app/registro_utilesaseo.html', {'form': form, 'formset': formset})



from django.db.models import Q

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.defaultfilters import date
from django.db.models import Q
from django.contrib.staticfiles import finders
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import ParagraphStyle
from django.utils.dateparse import parse_datetime
from app.models import Utilesaseo  # Assuming this is your model

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

from django.contrib.staticfiles import finders
from dateutil.parser import parse as parse_datetime
import qrcode
from reportlab.lib.utils import ImageReader
from .models import Utilesaseo  
from django.db.models.functions import Cast
from django.db.models import CharField


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from django.contrib.staticfiles import finders
from io import BytesIO
from django.utils.dateparse import parse_datetime
import qrcode

from .models import Utilesaseo  # Ajusta esto si tu modelo tiene otro nombre


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, white, HexColor
from io import BytesIO
import qrcode
from django.utils.dateparse import parse_datetime
from .models import Utilesaseo


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from django.contrib.staticfiles import finders
from django.utils.dateparse import parse_datetime
from io import BytesIO
import qrcode
from .models import Utilesaseo


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from django.contrib.staticfiles import finders
from django.utils.dateparse import parse_datetime
from io import BytesIO
import qrcode
from .models import Utilesaseo
import uuid



from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.contrib.staticfiles import finders

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, white, HexColor
import qrcode
from io import BytesIO
import uuid

from .models import Utilesaseo


@login_required
def generar_pdf_utiles_aseo(request):
    search_term = request.GET.get('buscar', '').strip()
    producto_term = request.GET.get('producto', '').strip()  # <-- ¡AGREGADO!

    empresa_id = request.GET.get('empresa_id')
    utilesaseos = Utilesaseo.objects.all()

    # Filtrado por empresa si corresponde
    if empresa_id:
        utilesaseos = utilesaseos.filter(empresa_id=empresa_id)
    if search_term:
        try:
            search_datetime = parse_datetime(search_term)
            if search_datetime:
                search_date = search_datetime.date()
                utilesaseos = utilesaseos.filter(fecha_creacion__date=search_date)
            else:
                raise ValueError()
        except ValueError:
            text_search = Q(mes__icontains=search_term) | \
                          Q(productos__nombre__icontains=search_term) | \
                          Q(detalles__cantidad__icontains=search_term) | \
                          Q(nombre_solicitante__nombre__icontains=search_term) | \
                          Q(empresa__nombre__icontains=search_term) | \
                          Q(fecha_creacion__icontains=search_term) | \
                          Q(run__icontains=search_term)
            utilesaseos = utilesaseos.filter(text_search).distinct()

    if producto_term:
        utilesaseos = utilesaseos.filter(detalles__producto__nombre__icontains=producto_term).distinct()

    # Si no se encontraron registros, devolver respuesta vacía
    if not utilesaseos.exists():
        return HttpResponse("No se encontraron registros para el filtro aplicado.", status=404)

    # SIEMPRE generar un nuevo número de reporte único y asignarlo SOLO a los registros filtrados
    import uuid
    while True:
        numero_reporte = f"UA-{uuid.uuid4().hex[:8].upper()}"
        if not Utilesaseo.objects.filter(numero_reporte=numero_reporte).exists():
            break
    utilesaseos.update(numero_reporte=numero_reporte)

    # ... Resto del código para generar el PDF ...
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="UTILES_ASEO.pdf"'
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Logo
    logo_path = finders.find('app/imgenes/Logo.png')
    if not logo_path:
        raise FileNotFoundError(f'Logo no encontrado en: {logo_path}')
    logo = Image(logo_path, width=200, height=50)

    # QR
    qr_image = None
    if numero_reporte:
        verificacion_url = request.build_absolute_uri(f"/verificar-utiles/{numero_reporte}/")
        qr_img = qrcode.make(verificacion_url)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        qr_image = Image(qr_buffer, width=80, height=80)

    # Logo + QR juntos
    if qr_image:
        logo_qr_table = Table([[logo, qr_image]], colWidths=[250, 100])
    else:
        logo_qr_table = Table([[logo]])

    logo_qr_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(logo_qr_table)

    # Título
    title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        alignment=1,
        textColor=black,
        fontName='Helvetica-Bold',
        fontSize=18
    )
    elements.append(Paragraph("ENTREGA DE UTILES DE ASEO", title_style))

    # Número de reporte
    if numero_reporte:
        reporte_style = ParagraphStyle(
            'Reporte',
            parent=getSampleStyleSheet()['Normal'],
            alignment=1,
            fontSize=12,
            textColor=black,
            spaceAfter=6
        )
        elements.append(Paragraph(f"N° REPORTE: {numero_reporte}", reporte_style))

    elements.append(Spacer(1, 12))

    data = [[ 'RUN', 'TRABAJADOR', 'EMPRESA', 'MES', 'PRODUCTO', 'CANT', 'FECHA']]
    for utilesaseo in utilesaseos:
        run = utilesaseo.run or ''
        trabajador = utilesaseo.nombre_solicitante.nombre if utilesaseo.nombre_solicitante else ''
        empresa = utilesaseo.empresa.nombre if utilesaseo.empresa else ''
        mes = utilesaseo.mes
        fecha = utilesaseo.fecha_creacion.strftime("%d/%m/%Y")
        for detalle in utilesaseo.detalles.all():
            producto = detalle.producto.nombre
            cantidad = detalle.cantidad
            if not producto_term or producto_term.lower() in producto.lower():
                data.append([
                    run,
                    trabajador,
                    empresa,
                    mes,
                    producto,
                    cantidad,
                    fecha
                ])


    table = Table(data)
    table._argW[0] = 70  # RUN
    table._argW[1] = 140 # TRABAJADOR
    table._argW[2] = 130 # EMPRESA
    table._argW[3] = 60  # MES
    table._argW[4] = 150 # PRODUCTO
    table._argW[5] = 50  # CANTIDAD
    table._argW[6] = 70  # FECHA

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, black),
    ]))
    elements.append(table)

    # Firma
    elements.append(Spacer(1, 24))
    signature_style = ParagraphStyle(
        'Signature',
        parent=getSampleStyleSheet()['Normal'],
        alignment=1,
        textColor=black,
        fontSize=12,
        leading=16
    )
    elements.append(Paragraph("Firma: ____________________________________________", signature_style))

    # Generar y enviar el PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response







@login_required
def verificar_utiles(request, numero_reporte):
    empresa_id = request.GET.get('empresa_id')
    producto_term = request.GET.get('producto', '').strip().lower()  # <--- NUEVO

    utiles_list = Utilesaseo.objects.filter(numero_reporte=numero_reporte)

    if empresa_id:
        utiles_list = utiles_list.filter(empresa_id=empresa_id)

    if not utiles_list.exists():
        return HttpResponse("No se encontraron registros", status=404)

    # Filtrar detalles dentro del contexto (opcional, también puedes hacerlo en la plantilla)
    for utiles in utiles_list:
        detalles_filtrados = utiles.detalles.all()
        if producto_term:
            detalles_filtrados = detalles_filtrados.filter(producto__nombre__icontains=producto_term)
        utiles.detalles_filtrados = detalles_filtrados  # <--- NUEVO atributo temporal

    # Obtener trabajadores y empresas únicos SOLO de los registros filtrados
    trabajadores_unicos = list({u.nombre_solicitante.nombre for u in utiles_list})
    empresas_unicas = list({(u.empresa.id, u.empresa.nombre) for u in utiles_list})

    return render(request, 'verificacionqr/verificacion_utiles.html', {
        'utiles_list': utiles_list,
        'trabajadores_unicos': trabajadores_unicos,
        'empresas_unicas': empresas_unicas,
        'filtro_aplicado': "numero_reporte",
        'valor_filtro': numero_reporte,
        'empresa_id': empresa_id,
        'producto_term': producto_term,  # <--- Opcional si lo usas en el template
    })




from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from .models import RetiroRepuesto
from datetime import datetime
from reportlab.lib.units import inch
import os
from django.conf import settings

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.urls import reverse
import qrcode
from reportlab.lib.utils import ImageReader
from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.conf import settings
from django.http import HttpResponse
from .models import RetiroRepuesto, Obrero, ReporteRetiroRepuesto  # Asegúrate de tener este modelo
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def generar_pdf_retiro(request, obrero_id=None):
    # === Datos ===
    if obrero_id:
        data = RetiroRepuesto.objects.filter(trabajador_id=obrero_id).order_by('fecha_retiro')
    else:
        data = RetiroRepuesto.objects.all().order_by('fecha_retiro')

    # === Generar número de reporte y crear objeto ReporteRetiroRepuesto ===
    fecha_hoy = datetime.now().strftime('%Y%m%d%H%M%S')
    numero_reporte = f"RR-{fecha_hoy}"
    reporte, created = ReporteRetiroRepuesto.objects.get_or_create(
        numero_reporte=numero_reporte,
        defaults={
            'filtro': str(obrero_id) if obrero_id else 'Todos',
            'trabajador': Obrero.objects.get(id=obrero_id) if obrero_id else None
        }
    )

    # Asignar el reporte a cada retiro filtrado
    for retiro in data:
        retiro.reporte = reporte
        retiro.save()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_retiros_{numero_reporte}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    margin = 50
    page_num = 1

    # === Rutas imágenes ===
    logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Logo.png')
    minera_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'minera.png')

    # === Estilos ===
    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=0,
        wordWrap='CJK',
    )

    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ])

    # === Encabezado con QR ===
    def draw_header(canvas_obj, title, user_name, page_num):
        logo_width = 100
        logo_height = 40
        minera_width = 100
        minera_height = 80

        logo_x = margin
        logo_y = height - margin - logo_height
        minera_x = width - margin - minera_width
        minera_y = logo_y

        # Logo izquierdo
        if os.path.exists(logo_path):
            canvas_obj.drawImage(logo_path, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

        # Logo derecho
        if os.path.exists(minera_path):
            canvas_obj.drawImage(minera_path, minera_x, minera_y, width=minera_width, height=minera_height, mask='auto')

        # QR generado con link de verificación
        url_verificacion = request.build_absolute_uri(reverse('verificar_reporte_retiro', args=[numero_reporte, obrero_id]))
        qr = qrcode.make(url_verificacion)
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        qr_io.seek(0)
        qr_img = ImageReader(qr_io)
        qr_size = 60
        qr_x = logo_x + logo_width + 10
        qr_y = logo_y
        canvas_obj.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size, mask='auto')
        canvas_obj.setFont("Helvetica", 7)
        canvas_obj.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "Escanee el QR")

        # Título
        title_x = width / 2
        title_y = height - margin - (logo_height / 4)
        canvas_obj.setFont("Helvetica-Bold", 14)
        canvas_obj.drawCentredString(title_x, title_y, title)

        # Info usuario y número de página
        canvas_obj.setFont("Helvetica", 10)
        canvas_obj.drawCentredString(width / 2, height - margin - logo_height - 10, f"PAÑOLERO: {user_name}")
        canvas_obj.drawRightString(width - margin - minera_width - 10, height - margin - minera_height - 10, f"PÁGINA: {page_num}")

        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.drawCentredString(width / 2, title_y - 15, f"N° REPORTE: {numero_reporte}")

        # Línea separadora
        line_y = height - margin - logo_height - 20
        canvas_obj.line(margin, line_y, width - margin, line_y)

    # === Tabla ===
    table_data = [['FECHA', 'TRABAJADOR', 'EMPRESA', 'REPUESTO', 'CANT']]
    for retiro in data:
        table_data.append([
            retiro.fecha_retiro.strftime('%d/%m/%Y %H:%M'),
            Paragraph(str(retiro.trabajador), styleN),
            Paragraph(str(retiro.empresa), styleN),
            Paragraph(str(retiro.repuesto), styleN),
            str(retiro.cantidad),
        ])

    column_widths = [90, 110, 180, 180, 50]
    current_data = table_data[1:]

    while current_data:
        draw_header(p, "RETIRO DE REPUESTOS", request.user.username, page_num)
        y_position = height - margin - 100
        max_rows_per_page = int((y_position - margin) / 15)
        page_data = [table_data[0]] + current_data[:max_rows_per_page]
        current_data = current_data[max_rows_per_page:]

        table = Table(page_data, colWidths=column_widths)
        table.setStyle(style_table)
        table_width, table_height = table.wrap(0, 0)
        x_centered = (width - table_width) / 2
        table.drawOn(p, x_centered, y_position - table_height)

        if current_data:
            p.showPage()
            page_num += 1

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from .models import RetiroRepuesto
from datetime import datetime
import os
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from datetime import datetime
from io import BytesIO
import os
import qrcode

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader

from app.models import RetiroRepuesto


def parse_date(search_term):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(search_term, fmt).date()
        except ValueError:
            continue
    return None


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.dateparse import parse_date
from io import BytesIO
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os
import qrcode

from .models import RetiroRepuesto
from django.conf import settings
from django.urls import reverse
from .models import ReporteRetiroRepuesto
from datetime import datetime
from reportlab.lib.colors import HexColor

@login_required
def generar_pdf_retiros_general(request):
    search_term = request.GET.get('buscar', '').strip()
    retiros = RetiroRepuesto.objects.all()

    if search_term:
        retiros = retiros.filter(
            Q(trabajador__nombre__icontains=search_term) |
            Q(empresa__nombre__icontains=search_term) |
            Q(repuesto__nombre__icontains=search_term) |
            Q(area__icontains=search_term) |
            Q(cantidad__icontains=search_term) |
            Q(fecha_retiro__icontains=search_term)
        )

  
  

    fecha_hoy = datetime.now().strftime('%Y%m%d%H%M%S')
    numero_reporte = f"RR-{fecha_hoy}"
    reporte, created = ReporteRetiroRepuesto.objects.get_or_create(
        numero_reporte=numero_reporte,
        defaults={'filtro': search_term}
    )

    # === Generar PDF ===
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="retiros_{numero_reporte}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Logos
    logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Logo.png')
    minera_logo_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'imgenes', 'Minera.png')

    # Estilos
    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=10,
        alignment=0,
        wordWrap='CJK',
    )

    margin = 50
    logo_x, logo_y = margin, height - margin - 40
    minera_x, minera_y = width - margin - 80, height - margin - 60

    if os.path.exists(logo_path):
        p.drawImage(logo_path, logo_x, logo_y, width=80, height=30, mask='auto')
    if os.path.exists(minera_logo_path):
        p.drawImage(minera_logo_path, minera_x, minera_y, width=80, height=60, mask='auto')

    p.setFont("Helvetica-Bold", 14)
    titulo_y = max(logo_y + 40, minera_y + 60) + 10
    p.drawCentredString(width / 2, titulo_y, "RETIRO DE REPUESTOS")

    p.setFont("Helvetica", 10)
    info_y = titulo_y - 15
    p.drawCentredString(width / 2, info_y, f"PAÑOLERO: {request.user.username}    |    FECHA REPORTE: {datetime.now().strftime('%d/%m/%Y')}")
    p.drawCentredString(width / 2, info_y - 15, f"N° REPORTE: {numero_reporte}")

    line_y = info_y - 50
    p.line(margin, line_y, width - margin, line_y)

    data = [['FECHA', 'TRABAJADOR', 'EMPRESA', 'REPUESTO', 'CANTIDAD', 'AREA']]
    for retiro in retiros:
        data.append([
            retiro.fecha_retiro.strftime("%d/%m/%Y %H:%M"),
            Paragraph(str(retiro.trabajador.nombre), styleN),
            Paragraph(str(retiro.empresa.nombre), styleN),
            Paragraph(str(retiro.repuesto.nombre), styleN),
            str(retiro.cantidad),
            retiro.area or '',
        ])

    if len(data) == 1:
        data.append(['No hay registros', '', '', '', '', ''])

    column_widths = [90, 100, 120, 120, 60, 100]
    table = Table(data, colWidths=column_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#0d6efd")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table_width, table_height = table.wrap(0, 0)
    x_centered = (width - table_width) / 2
    y_position = line_y - 30
    table.drawOn(p, x_centered, y_position - table_height)

    # === QR code con link único de verificación ===
    from django.urls import reverse
    import qrcode
    from reportlab.lib.utils import ImageReader

    url_verificacion = request.build_absolute_uri(
        reverse('verificar_reporte_retiros', args=[numero_reporte])
    )
    qr = qrcode.make(url_verificacion)
    qr_io = BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_img = ImageReader(qr_io)
    qr_size = 70
    qr_size = 60
    qr_x = logo_x + 90  # justo al lado derecho del logo
    qr_y = logo_y       # misma altura que el logo

    p.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size, mask='auto')
    p.setFont("Helvetica", 7)
    p.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "Escanee el QR para verificar")


    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response






def verificar_reporte_retiros(request, numero_reporte):
    reporte = get_object_or_404(ReporteRetiroRepuesto, numero_reporte=numero_reporte)
    # Aplica el filtro guardado si quieres mostrar los mismos retiros
    retiros = RetiroRepuesto.objects.all()
    if reporte.filtro:
        retiros = retiros.filter(
            Q(trabajador__nombre__icontains=reporte.filtro) |
            Q(empresa__nombre__icontains=reporte.filtro) |
            Q(repuesto__nombre__icontains=reporte.filtro) |
            Q(area__icontains=reporte.filtro) |
            Q(cantidad__icontains=reporte.filtro) |
            Q(fecha_retiro__icontains=reporte.filtro)
        )
    context = {
        'retiros': retiros,
        'numero_reporte': numero_reporte,
        'fecha_reporte': reporte.fecha_generacion,
    }
    return render(request, 'verificacionqr/verificacion_retiros.html', context)


from django.shortcuts import render, get_object_or_404
from .models import RetiroRepuesto, Obrero, ReporteRetiroRepuesto
from datetime import datetime

def verificar_reporte_retiro(request, numero_reporte, obrero_id):
    reporte = get_object_or_404(ReporteRetiroRepuesto, numero_reporte=numero_reporte)
    trabajador = get_object_or_404(Obrero, id=obrero_id)
    retiros = RetiroRepuesto.objects.filter(reporte=reporte, trabajador=trabajador).order_by('fecha_retiro')
    return render(request, 'verificacionqr/verificacion_retiro.html', {
        'numero_reporte': reporte.numero_reporte,
        'fecha_reporte': reporte.fecha_generacion.strftime('%d/%m/%Y %H:%M'),
        'retiros': retiros,
        'trabajador': trabajador,
    })





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


def calcular_totales_dia(pedidos, fecha_seleccionada):
    insumos_totales = {}

    for pedido in pedidos:
        for pedido_insumo in pedido.pedidoinsumo_set.all():
            insumo = pedido_insumo.insumos.nombre
            fecha_pedido = pedido.fecha_pedido.date()
            cantidad = pedido_insumo.cantidad

            if fecha_pedido != fecha_seleccionada:
                continue

            if insumo not in insumos_totales:
                insumos_totales[insumo] = {'total': 0}

            insumos_totales[insumo]['total'] += cantidad

    return insumos_totales


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def pedidos_dia(request):
    # Obtener y validar la fecha
    fecha_seleccionada_str = request.GET.get('fecha')
    if not fecha_seleccionada_str:
        return HttpResponse("Por favor, seleccione una fecha válida.", status=400)

    try:
        fecha_seleccionada = datetime.strptime(fecha_seleccionada_str, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponse("Fecha inválida. Asegúrese de usar el formato YYYY-MM-DD.", status=400)

    # Filtrar pedidos
    pedidos = Pedido.objects.filter(fecha_pedido__date=fecha_seleccionada)
    if not pedidos.exists():
        return HttpResponse(f"No se encontraron pedidos para la fecha {fecha_seleccionada}.", status=404)

    # Calcular totales
    insumos_totales = calcular_totales_dia(pedidos, fecha_seleccionada)

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{fecha_seleccionada}.pdf"'

    # PDF y dimensiones
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Título principal
    mes_espanol = traducir_mes_en_espanol(fecha_seleccionada)
    fecha_formateada = fecha_seleccionada.strftime(f'%d {mes_espanol} %Y')
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 40, f"INFORME DE INSUMOS - {fecha_formateada}")

    # Tabla de datos
    data = [['NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    for insumo, totales in insumos_totales.items():
        data.append([insumo, str(totales['total'])])

    # Estilo tabla
    table = Table(data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Calcular posición centrada
    table_width, table_height = table.wrap(0, 0)
    x_pos = (width - table_width) / 2
    y_pos = height - 100 - table_height  # Debajo del título

    table.drawOn(p, x_pos, y_pos)

    # Guardar el PDF
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def calcular_totales_semana(pedidos, fecha_inicio, fecha_fin):
    insumos_totales = {}

    for pedido in pedidos:
        for pedido_insumo in pedido.pedidoinsumo_set.all():
            insumo = pedido_insumo.insumos.nombre
            cantidad = pedido_insumo.cantidad
            fecha_pedido = pedido.fecha_pedido.date()  # Convertir a datetime.date

            if not (fecha_inicio <= fecha_pedido <= fecha_fin):
                continue  # Solo procesar pedidos dentro del rango de fechas

            if insumo not in insumos_totales:
                insumos_totales[insumo] = {
                    'total': 0,
                    'totales_por_periodo': {
                        'semana': 0,
                        'mes': 0,
                        'año': 0,
                    }
                }

            insumos_totales[insumo]['totales_por_periodo']['semana'] += cantidad
            insumos_totales[insumo]['total'] += cantidad

    return insumos_totales


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def pedidos_semana(request):
    # Validar fecha de inicio
    fecha_inicio_str = request.GET.get('fecha_inicio')
    if not fecha_inicio_str:
        return HttpResponse("Por favor, seleccione una fecha de inicio.", status=400)

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = fecha_inicio + timedelta(days=6 - fecha_inicio.weekday())
    except ValueError:
        return HttpResponse("Fecha inválida. Asegúrese de usar el formato YYYY-MM-DD.", status=400)

    # Filtrar pedidos
    pedidos = Pedido.objects.filter(fecha_pedido__date__range=(fecha_inicio, fecha_fin))
    if not pedidos.exists():
        return HttpResponse(f"No se encontraron pedidos entre {fecha_inicio} y {fecha_fin}.", status=404)

    # Calcular totales
    insumos_totales = calcular_totales_semana(pedidos, fecha_inicio, fecha_fin)

    # Configurar respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PEDIDOS_{fecha_inicio}_a_{fecha_fin}.pdf"'

    # Crear PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Título del reporte
    mes_espanol = traducir_mes_en_espanol(fecha_inicio)
    fecha_formateada_inicio = fecha_inicio.strftime(f'%d {mes_espanol} %Y')
    fecha_formateada_fin = fecha_fin.strftime(f'%d {mes_espanol} %Y')
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 40, f"INFORME DE INSUMOS - {fecha_formateada_inicio} a {fecha_formateada_fin}")

    # Construir datos de tabla
    data = [['NOMBRE DEL PRODUCTO', 'CANTIDAD TOTAL']]
    for insumo, totales in insumos_totales.items():
        data.append([insumo, str(totales['total'])])

    # Crear tabla y estilo
    table = Table(data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Centrar la tabla
    table_width, table_height = table.wrap(0, 0)
    x_pos = (width - table_width) / 2
    y_pos = height - 100 - table_height
    table.drawOn(p, x_pos, y_pos)

    # Subtítulo adicional
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "INFORME DE INSUMOS POR SEMANA")

    # Guardar y retornar PDF
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Informe
from django.template.loader import get_template
from weasyprint import HTML
from datetime import datetime
from django.templatetags.static import static
import os
from django.conf import settings
import qrcode
import base64
from io import BytesIO


@login_required
def generar_pdf_informes_por_dia(request):
    fecha_str = request.GET.get('fecha')
    if not fecha_str:
        return HttpResponse('Debe proporcionar una fecha.', status=400)

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse('Formato de fecha inválido.', status=400)

    informes = Informe.objects.filter(fecha=fecha).order_by('hora_inicio')
    if not informes.exists():
        return HttpResponse('No hay informes para la fecha seleccionada.', status=404)

    # Generar QR con un texto (puede ser la fecha, una URL, o lo que desees)
    numero_reporte = f"VR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    qr_url = request.build_absolute_uri(reverse('verificar_reporte_informe', args=[numero_reporte]))

    
    qr = qrcode.make(qr_url)

    VerificacionInforme.objects.create(
    numero_reporte=numero_reporte,
    fecha=fecha
    )
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    qr_img = f'data:image/png;base64,{qr_base64}'

    image_path = os.path.join(settings.BASE_DIR, 'app','static', 'app', 'imgenes', 'minera.png')

    # Convertir la imagen a base64
    with open(image_path, 'rb') as img_file:
        minera_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    minera_img = f'data:image/png;base64,{minera_base64}'

    header_html = f'''
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
        <div style="flex: 0 0 auto;">
            <img src="{qr_img}" style="width: 60px; height: 60px;">
        </div>
        <div style="text-align: center; flex: 1;">
            <h1 style="font-size: 22px; margin-bottom: 5px;">INFORME DIA {fecha.strftime('%d-%m-%Y')}</h1>
            <p style="margin: 0;font-size: 12px;">PAÑOLERO: {request.user.username}</p>
        </div>
        <div style="flex: 0 0 auto;">
            <img src="{minera_img}" style="width: 60px; height: 60px;">
        </div>
    </div>
    '''



    # Renderizar cada informe y acumular HTML
    html_parts = []
    for informe in informes:
        template = get_template(f'informes/pdf/caso_{informe.caso}.html')
        html = template.render({'informe': informe})
        html_parts.append(html)

    # Unir encabezado y contenido
    full_html = f'''
    <html>
        <head><meta charset="utf-8"></head>
        <body>
            {header_html}
            {"".join(html_parts)}
        </body>
    </html>
    '''

    pdf = HTML(string=full_html, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informes_{fecha}.pdf"'
    return response

from django.shortcuts import render, get_list_or_404
from .models import Informe

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError
from .models import VerificacionInforme, Informe

def verificar_reporte_informe(request, numero_reporte):
    try:
        verificacion = get_object_or_404(VerificacionInforme, numero_reporte=numero_reporte)
        informes = Informe.objects.filter(fecha=verificacion.fecha)

        return render(request, 'verificacionqr/verificar_reporte_informe.html', {
            'numero_reporte': numero_reporte,
            'fecha_reporte': verificacion.fecha,
            'informes': informes
        })

    except Exception as e:
        # Log interno si deseas (no en producción con print)
        print(f"[ERROR] Verificación fallida para {numero_reporte}: {e}")
        return HttpResponseServerError("Error interno del servidor.")



def mi_error_404(request, exception):
    return render(request, 'app/404.html', status=404)

def mi_error_500(request):
    return render(request, 'app/500.html', status=500)


def verificar_informes_fecha(request, fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Fecha inválida", status=400)

    informes = Informe.objects.filter(fecha=fecha).order_by('hora_inicio')
    return render(request, 'verificacionqr/verificar_informes_fecha.html', {
        'fecha': fecha,
        'informes': informes
    })


def listar_informes(request):
    informes = Informe
   
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


def calcular_totales_mes(pedidos, fecha_inicio, fecha_fin):
    """
    Calcula los totales por mes para cada insumo en los pedidos.
    """
    insumos_totales = {}

    for pedido in pedidos:
        for pedido_insumo in pedido.pedidoinsumo_set.all():
            insumo = pedido_insumo.insumos.nombre
            cantidad = pedido_insumo.cantidad

            if insumo not in insumos_totales:
                insumos_totales[insumo] = {
                    'total': 0,
                }

            # Total general
            insumos_totales[insumo]['total'] += cantidad

    return insumos_totales



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
    p.setFont("Helvetica-Bold", 14)
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

def generate_pdf(request, personal=None, empresa=None):
    personal = personal or request.GET.get('personal')
    empresa = empresa or request.GET.get('empresa')

    # Ruta absoluta a la imagen
    image_path = os.path.join(settings.STATIC_ROOT, 'app/imgenes/minera.png')

    congelados = congelado.objects.all()
    if personal:
        congelados = congelados.filter(personal=personal)
    if empresa:
        congelados = congelados.filter(empresa=empresa)

    personas = congelados.values_list('personal', flat=True).distinct()

    merger = PdfMerger()

    for persona in personas:
        congelados_persona = congelados.filter(personal=persona)
        max_filas = 16
        filas_vacias = max_filas - congelados_persona.count()
        vacias_filas = [{}] * filas_vacias

        context = {
            'congelados': congelados_persona,
            'date': timezone.now().strftime("%d/%m/%Y"),
            'vacias_filas': vacias_filas,
            'logo_url': request.build_absolute_uri(static('app/imgenes/logo.png')),
            'logo_url1': request.build_absolute_uri(static('app/imgenes/minera.png')),
        }

        pdf = render_to_pdf('app/pdf_template.html', context)
        if pdf:
            merger.append(BytesIO(pdf))
        else:
            return HttpResponse("Error al generar el PDF para persona: {}".format(persona), status=500)

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
def crear_informe(request):
    if request.method == 'POST':
        caso = request.POST.get('caso')
        if caso in ['2', '3', '4', '5']:
            form_map = {
                '2': InformeCaso2Form,
                '3': InformeCaso3Form,
                '4': InformeCaso4Form,
                '5': InformeCaso5Form,
            }
            form_class = form_map[caso]
            form_caso = form_class(request.POST, request.FILES)
            form = InformeForm()
            form_caso2 = InformeCaso2Form() if caso != '2' else form_caso
            form_caso3 = InformeCaso3Form() if caso != '3' else form_caso
            form_caso4 = InformeCaso4Form() if caso != '4' else form_caso
            form_caso5 = InformeCaso5Form() if caso != '5' else form_caso
            imagen_formset = ImagenInformeFormSet(request.POST, request.FILES)
            imagen_solo_formset = ImagenSoloImagenFormSet()
            if form_caso.is_valid() and imagen_formset.is_valid():
                informe = form_caso.save()
                imagen_formset.instance = informe
                imagen_formset.save()
                return redirect('listar_informes')
        elif caso == '6':
            form = InformeForm()
            form_caso2 = InformeCaso2Form()
            form_caso3 = InformeCaso3Form()
            form_caso4 = InformeCaso4Form()
            form_caso5 = InformeCaso5Form()
            form_caso6 = InformeCaso6Form(request.POST, request.FILES)
            imagen_formset = ImagenInformeFormSet()
            imagen_solo_formset = ImagenSoloImagenFormSet(request.POST, request.FILES)
            if form_caso6.is_valid() and imagen_solo_formset.is_valid():
                informe = form_caso6.save()
                imagen_solo_formset.instance = informe
                imagen_solo_formset.save()
                return redirect('listar_informes')
        else:
            form = InformeForm(request.POST, request.FILES)
            form_caso2 = InformeCaso2Form()
            form_caso3 = InformeCaso3Form()
            form_caso4 = InformeCaso4Form()
            form_caso5 = InformeCaso5Form()
            form_caso6 = InformeCaso6Form()
            imagen_formset = ImagenInformeFormSet()
            imagen_solo_formset = ImagenSoloImagenFormSet()
            if form.is_valid():
                form.save()
                return redirect('listar_informes')
    else:
        form = InformeForm()
        form_caso2 = InformeCaso2Form()
        form_caso3 = InformeCaso3Form()
        form_caso4 = InformeCaso4Form()
        form_caso5 = InformeCaso5Form()
        form_caso6 = InformeCaso6Form()
        imagen_formset = ImagenInformeFormSet()
        imagen_solo_formset = ImagenSoloImagenFormSet()
    return render(request, 'app/registrar_informe.html', {
        'form': form,
        'form_caso2': form_caso2,
        'form_caso3': form_caso3,
        'form_caso4': form_caso4,
        'form_caso5': form_caso5,
        'form_caso6': form_caso6,
        'imagen_formset': imagen_formset,
        'imagen_solo_formset': imagen_solo_formset,
    })

def extraer_tabla_html(html):
    """Extrae solo el bloque <table>...</table> del HTML renderizado."""
    start = html.find('<table')
    end = html.find('</table>')
    if start != -1 and end != -1:
        return html[start:end+8]
    return ''

from weasyprint import HTML
from django.template.loader import get_template
import base64
import os
# ...existing imports...

@login_required
def generar_pdf_informes_tablas_unidas(request):
    from .models import Informe
    from datetime import datetime

    fecha_str = request.GET.get('fecha')
    if not fecha_str:
        return HttpResponse('Debe proporcionar una fecha.', status=400)
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse('Formato de fecha inválido.', status=400)

    informes = Informe.objects.filter(fecha=fecha).order_by('hora_inicio')
    if not informes.exists():
        return HttpResponse('No hay informes para la fecha seleccionada.', status=404)

    tablas_html = []
    for informe in informes:
        template = get_template(f'informes/pdf/caso_{informe.caso}.html')
        html_render = template.render({'informe': informe})
        tabla = extraer_tabla_html(html_render)
        tablas_html.append(tabla)

    # Convertir logos a base64
    def img_to_base64(path):
        try:
            with open(path, 'rb') as img_file:
                ext = os.path.splitext(path)[1].lower()
                mime = 'image/png' if ext == '.png' else 'image/svg+xml' if ext == '.svg' else 'image/jpeg'
                return f"data:{mime};base64," + base64.b64encode(img_file.read()).decode()
        except Exception as e:
            return ''

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_izq_path = os.path.join(base_dir, 'app', 'static','app', 'imgenes', 'Logo.png')
    logo_der_path = os.path.join(base_dir, 'app', 'static','app', 'imgenes', 'minera.png')
    logo_izq_b64 = img_to_base64(logo_izq_path)
    logo_der_b64 = img_to_base64(logo_der_path)

    context = {
        'tablas_html': tablas_html,
        'fecha': fecha,
        'logo_izq_b64': logo_izq_b64,
        'logo_der_b64': logo_der_b64,
    }
    html_string = get_template('informes/pdf/informes_tablas_unidas.html').render(context)

    # Guardar el HTML generado para depuración
    with open(os.path.join(base_dir, 'html_generado_para_pdf.html'), 'w', encoding='utf-8') as f:
        f.write(html_string)

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=\"informes_tablas_unidas_{fecha}.pdf\"'
    return response

def listar_informes(request):
    informes = Informe.objects.all().order_by('-fecha')
    return render(request, 'informes/listar.html', {'informes': informes})

from django.template.loader import get_template
from weasyprint import HTML
from .models import Informe
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def generar_pdf_informe(request, informe_id):
    informe = Informe.objects.get(id=informe_id)
    template = get_template(f'informes/pdf/caso_{informe.caso}.html')
    html_string = template.render({'informe': informe}, request)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="informe_{informe.id}.pdf"'
    return response

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Informe, ImagenInforme
import os
from django.contrib.auth.decorators import login_required

@login_required
def eliminar_informe(request, informe_id):
    informe = get_object_or_404(Informe, id=informe_id)
    if request.method == 'POST':
        # Eliminar imágenes asociadas (ImagenInforme)
        for imagen in informe.imagenes.all():
            if imagen.imagen and os.path.isfile(imagen.imagen.path):
                os.remove(imagen.imagen.path)
        # Eliminar imagen_antes y imagen_despues si existen
        if informe.imagen_antes and os.path.isfile(informe.imagen_antes.path):
            os.remove(informe.imagen_antes.path)
        if informe.imagen_despues and os.path.isfile(informe.imagen_despues.path):
            os.remove(informe.imagen_despues.path)
        informe.delete()
        messages.success(request, 'Informe y sus imágenes eliminados correctamente.')
        return redirect('listar_informes')
    return render(request, 'informes/confirmar_eliminar.html', {'informe': informe})    




from django.shortcuts import render, get_object_or_404

from django.db.models import Q
from datetime import datetime


from django.core.paginator import Paginator

def verificar_reporte(request, codigo):
    try:
        reporte = ReportePedido.objects.get(codigo_reporte=codigo)
        insumos_guardados = ReporteInsumo.objects.filter(reporte=reporte)

        tabla_datos = []

        for item in insumos_guardados:
            tabla_datos.append({
                'fecha': item.pedido.fecha_pedido.strftime("%d/%m/%Y %H:%M"),
                'trabajador': item.trabajador.nombre,
                'empresa': item.pedido.compañia.nombre,
                'insumo': item.insumo.nombre,
                'cantidad': item.cantidad,
                'area': item.area,
            })

        page_number = request.GET.get('page')
        paginator = Paginator(tabla_datos, 10)
        page_obj = paginator.get_page(page_number)

        return render(request, 'verificacionqr/verificacion_reporte.html', {
            'reporte': reporte,
            'tabla_datos': tabla_datos,
            'page_obj': page_obj,
        })

    except ReportePedido.DoesNotExist:
        return render(request, 'verificacionqr/verificacion_reporte.html', {
            'error': "No se encontró el reporte con el código proporcionado."
        })



from django.shortcuts import render, get_object_or_404
from .models import PedidoInsumo, Pedido, Obrero
from django.db.models import Q
from datetime import datetime

def verificar_reporte_personal(request, codigo_unico, obrero_id):
    search_term = request.GET.get('buscar')

    pedido_insumos = PedidoInsumo.objects.filter(
        pedido__codigo_unico=codigo_unico,
        pedido__solicitante_id=obrero_id
    )

    if search_term:
        try:
            search_date = datetime.strptime(search_term, "%d/%m/%Y").date()
            pedido_insumos = pedido_insumos.filter(
                Q(pedido__fecha_pedido__date=search_date) |
                Q(pedido__solicitante__nombre__icontains=search_term) |
                Q(pedido__compañia__nombre__icontains=search_term) |
                Q(insumos__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(pedido__area__icontains=search_term)
            )
        except ValueError:
            pedido_insumos = pedido_insumos.filter(
                Q(pedido__solicitante__nombre__icontains=search_term) |
                Q(pedido__compañia__nombre__icontains=search_term) |
                Q(insumos__nombre__icontains=search_term) |
                Q(cantidad__icontains=search_term) |
                Q(pedido__area__icontains=search_term)
            )

    trabajador = get_object_or_404(Obrero, pk=obrero_id)

    context = {
        'pedido_insumos': pedido_insumos.order_by('-pedido__fecha_pedido'),
        'trabajador': trabajador,
        'codigo_unico': codigo_unico,
        'search_term': search_term,
    }

    return render(request, 'verificacionqr/verificacion_reporte1.html', context)



from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from collections import defaultdict
from .models import Pedido, PedidoInsumo





from django.shortcuts import render

def mi_error_404(request, excption):
    return render(request, 'app/404.html', status=404)

def mi_error_500(request):
    return render(request, 'app/500.html', status=500)




