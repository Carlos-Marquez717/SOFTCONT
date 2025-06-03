from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, modelformset_factory
from .models import ImagenInforme

from .models import (
    Trabajador, Empresa, Obrero, Pedido, PedidoInsumo, 
    Material, Herramienta, Prestamo, Repuesto, RetiroRepuesto, 
    Utilesaseo, Producto, Informe
)

# ===================== FORMULARIOS PERSONALIZADOS =====================

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'empresa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'NOMBRE'
        self.fields['empresa'].label = 'EMPRESA'
        self.fields['empresa'].widget.attrs.update({'class': 'select2'})


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'NOMBRE'


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'NOMBRE'


class ObreroForm(forms.ModelForm):
    class Meta:
        model = Obrero
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'NOMBRE'


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['solicitante', 'compañia', 'area']
        widgets = {
            'solicitante': Select2Widget,
            'compañia': Select2Widget,
        }

class PedidoInsumoForm(forms.ModelForm):
    class Meta:
        model = PedidoInsumo
        fields = ['insumos', 'cantidad']
        widgets = {
            'insumos': Select2Widget,
        }

# Formset para los insumos asociados a un pedido (sin trabajador ni área)
PedidoInsumoInlineFormset = inlineformset_factory(
    Pedido, PedidoInsumo,
    form=PedidoInsumoForm,
    fields=['insumos', 'cantidad'],
    extra=1,
    can_delete=False
)

class LoginForm(AuthenticationForm):
    email = forms.CharField(max_length=100, required=True, help_text='Ingresa tu email.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data


class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'NOMBRE'


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['nombre_solicitante', 'empresa', 'herramienta', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_solicitante'].widget.attrs.update({'class': 'select2'})
        self.fields['empresa'].widget.attrs.update({'class': 'select2'})
        self.fields['herramienta'].widget.attrs.update({'class': 'select2'})


class PrestamoEditForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['status']


class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['nombre', 'cantidad', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'NOMBRE'
        self.fields['cantidad'].label = 'CANTIDAD'
        self.fields['ubicacion'].label = 'UBICACIÓN'


class InfoGeneralRetiroForm(forms.Form):
    trabajador = forms.ModelChoiceField(queryset=Obrero.objects.all(),  widget=Select2Widget(attrs={'class': 'select2'}))
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), widget=Select2Widget(attrs={'class': 'select2'}))

    area = forms.CharField(max_length=100)


class RetiroRepuestoForm(forms.ModelForm):
    class Meta:
        model = RetiroRepuesto
        fields = ['repuesto', 'cantidad']
        widgets = {
            'repuesto': Select2Widget(attrs={'class': 'select2'}),
        }

RetiroRepuestoFormSet = modelformset_factory(
    RetiroRepuesto,
    form=RetiroRepuestoForm,
    extra=1,
    can_delete=True
)


class UtilesaseoForm(forms.ModelForm):
    class Meta:
        model = Utilesaseo
        fields = '__all__'
        widgets = {
            'Producto': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mes'].widget.attrs.update({'class': 'select2'})
        self.fields['productos'].widget.attrs.update({'class': 'select2'})
        self.fields['nombre_solicitante'].widget.attrs.update({'class': 'select2'})
        self.fields['empresa'].widget.attrs.update({'class': 'select2'})


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email



class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [
            'caso',
            'area',
            'hora_inicio',
            'hora_culm',
            'descripcion',
            'fecha',
            'imagen_antes',
            'imagen_despues',
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_culm': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class InformeCaso2Form(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [
            'caso',
            'area',
            'hora_inicio',
            'hora_culm',
            'descripcion',
            'fecha',
           
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_culm': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InformeCaso3Form(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [
            'caso',
            'area',
            'hora_inicio',
            'hora_culm',
            'descripcion',
            'fecha',
            
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_culm': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            
        }


class InformeCaso4Form(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [
            'caso',
            'area',
            'hora_inicio',
            'hora_culm',
            'descripcion',
            'fecha',
            
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_culm': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InformeCaso5Form(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [
            'caso',
            'area',
            'hora_inicio',
            'hora_culm',
            'descripcion',
            'fecha',
            
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_culm': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InformeCaso6Form(forms.ModelForm):
    class Meta:
        model = Informe
        fields = [
            'caso',
            'area',
            'hora_inicio',
            'hora_culm',
            'descripcion',
            'piezas',
            'fecha',
            'imagen_antes',
            'imagen_despues',
        ]
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_culm': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'piezas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

ImagenInformeFormSet = inlineformset_factory(
    Informe, ImagenInforme,
    fields=("ot", "imagen"),  # Solo ot e imagen
    extra=1,
    can_delete=True
)

# Formset para imágenes sin OT (caso 6)
ImagenSoloImagenFormSet = inlineformset_factory(
    Informe, ImagenInforme,
    fields=("imagen",),  # Solo imagen
    extra=1,
    can_delete=True
)
