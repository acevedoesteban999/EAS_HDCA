from django import forms
from .models import I2C

class I2CForm(forms.ModelForm):

    class Meta:
        model=I2C
        fields = 'slug','addr'
        widgets = {
            'slug': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'addr': forms.NumberInput(attrs={'class':'form-control','placeholder': 'Ingrese una direccion'}),

        }
        