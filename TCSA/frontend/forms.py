from django import forms

class Cargar_datos(forms.Form):
    file = forms.FileField(label="archivo")

class Form_cliente(forms.Form):
    nombre = forms.CharField(label="nombre")
    nit = forms.CharField(label="nit")
    usuario = forms.CharField(label="nit")
    clave = forms.CharField(label="password", required = False)
    direccion = forms.CharField(label="direccion")
    email = forms.EmailField(label="email")

class Form_recurso(forms.Form):
    nombre = forms.CharField(label="nombre")
    id_recurso = forms.CharField(label="Id")
    abrev = forms.CharField(label="abrev")
    metrica = forms.CharField(label="metrica")
    precio = forms.DecimalField(label="precio")
