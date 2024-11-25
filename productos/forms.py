from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Producto, Venta

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'stock']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Producto.objects.filter(nombre=nombre).exists():  # Validación para evitar duplicados
            raise forms.ValidationError('Ya existe un producto con este nombre.')
        return nombre

class VentaForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), widget=forms.CheckboxSelectMultiple)
    cantidades = forms.CharField(widget=forms.HiddenInput)  # Vamos a manejar las cantidades como un campo oculto.

    
    def clean_cantidades(self):
        cantidades_str = self.cleaned_data['cantidades']
        cantidades = [int(cant.strip()) for cant in cantidades_str.split(',')]
        return cantidades



