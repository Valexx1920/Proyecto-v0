from django import forms
from .models import Objeto

class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['nombre', 'descripcion', 'latitud', 'longitud', 'imagen', 'gramos']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'descripcion': forms.Textarea(attrs={'required': True}),
            'latitud': forms.NumberInput(),
            'longitud': forms.NumberInput(),
            'gramos': forms.NumberInput(attrs={'step': '0.01'}),  
        }

