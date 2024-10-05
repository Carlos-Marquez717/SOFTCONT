# en trabajadores/forms.py
from django_select2.forms import Select2Widget
from django_select2.forms import ModelSelect2Widget
from django import forms
from .models import Trabajador,Empresa, Obrero, Pedido, Material, Herramienta, Prestamo, Repuesto, RetiroRepuesto,Utilesaseo,Producto

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        self.fields['solicitante'].widget.attrs.update({'class': 'select2'})
        self.fields['compañia'].widget.attrs.update({'class': 'select2'})
        self.fields['insumo'].widget.attrs.update({'class': 'select2'})



class LoginForm(AuthenticationForm):
    # Agrega campos personalizados si es necesario
    email = forms.CharField(max_length=100, required=True, help_text='Ingresa tu email.')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Puedes personalizar el aspecto de los campos aquí si es necesario
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
        super(HerramientaForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()           


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['nombre_solicitante', 'empresa', 'herramienta', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica Select2 a los campos nombre_solicitante, empresa y herramienta
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
        fields = ['nombre', 'cantidad']

    def __init__(self, *args, **kwargs):
        super(RepuestoForm, self).__init__(*args, **kwargs)
        
        # Cambiar a mayúsculas los títulos de los campos
        self.fields['nombre'].label = 'NOMBRE'.upper()       
        self.fields['cantidad'].label = 'CANTIDAD'.upper()            


class RetiroRepuestoForm(forms.ModelForm):
    class Meta:
        model = RetiroRepuesto
        fields = ['trabajador', 'empresa', 'repuesto', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica Select2 a los campos trabajador, empresa y repuesto
        self.fields['trabajador'].widget.attrs.update({'class': 'select2'})
        self.fields['empresa'].widget.attrs.update({'class': 'select2'})
        self.fields['repuesto'].widget.attrs.update({'class': 'select2'})   



class UtilesaseoForm(forms.ModelForm):
    class Meta:
        model = Utilesaseo
        fields = '__all__'
        widgets = {
            'Producto': forms.CheckboxSelectMultiple,  # Utiliza CheckboxSelectMultiple para múltiples selecciones
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
