from django import forms
from .models import Objeto

class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['nombre', 'descripcion', 'latitud', 'longitud', "imagen"]
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'descripcion': forms.Textarea(attrs={'required': True}),
            'latitud': forms.HiddenInput(),   # <- oculto
            'longitud': forms.HiddenInput(),  # <- oculto
        }
