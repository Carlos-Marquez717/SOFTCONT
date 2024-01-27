# en trabajadores/forms.py
from django_select2.forms import Select2Widget
from django_select2.forms import ModelSelect2Widget
from django import forms
from .models import Trabajador,Empresa, Obrero, Pedido, Material, Herramienta, Prestamo, Repuesto, RetiroRepuesto

from django.contrib.auth.forms import AuthenticationForm

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'empresa']

    def __init__(self, *args, **kwargs):
        super(TrabajadorForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()
        self.fields['empresa'].label = 'EMPRESA'.upper()
        self.fields['empresa'].widget.attrs['class'] = 'select2'

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()        

class ObreroForm(forms.ModelForm):
    class Meta:
        model = Obrero
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(ObreroForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()        
      

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['solicitante', 'compañia', 'insumo', 'cantidad', 'area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica Select2 a los campos solicitante, compañia e insumo
        self.fields['solicitante'].widget.attrs['class'] = 'select2'
        self.fields['compañia'].widget.attrs['class'] = 'select2'
        self.fields['insumo'].widget.attrs['class'] = 'select2'



class LoginForm(AuthenticationForm):
    # Agrega campos personalizados si es necesario
    email = forms.CharField(max_length=100, required=True, help_text='Ingresa tu email.')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Puedes personalizar el aspecto de los campos aquí si es necesario
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'



class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombre']

    def __init__(self, *args, **kwargs):
        super(HerramientaForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()           


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['nombre_solicitante', 'empresa', 'herramienta', 'status']



class PrestamoEditForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['status']        


class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['nombre', 'cantidad']

    def __init__(self, *args, **kwargs):
        super(RepuestoForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()       
        self.fields['cantidad'].label = 'CANTIDAD'.upper()            


class RetiroRepuestoForm(forms.ModelForm):
    class Meta:
        model = RetiroRepuesto
        fields = ['trabajador', 'empresa', 'repuesto', 'cantidad']  # Ajustar los campos necesarios

    def __init__(self, *args, **kwargs):
        super(RetiroRepuestoForm, self).__init__(*args, **kwargs)
        # Puedes personalizar las etiquetas aquí si es necesario
        self.fields['trabajador'].label = 'trabajador'.upper()
        self.fields['empresa'].label = 'Empresa'.upper()
        self.fields['repuesto'].label = 'Repuesto'.upper()
        self.fields['cantidad'].label = 'Cantidad'.upper()     