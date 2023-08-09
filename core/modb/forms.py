from django import forms
from .models import ModBus,MODB_TYPE

class ModBusForm(forms.ModelForm):
    ip=forms.GenericIPAddressField(initial="0.0.0.0",widget=forms.TextInput(attrs={'class':'form-control'}))
    #type=forms.ChoiceField(choices=MODB_TYPE)
    class Meta:
        model=ModBus
        fields = 'slug','ip','type'
        widgets = {
            'slug': forms.TextInput(attrs={'class':'form-control','placeholder': 'Ingrese un nombre'}),
            'type':forms.Select(attrs={'class':'form-control'}),
        }
        