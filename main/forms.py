from django import forms
from .models import Roteiro


class RoteiroForm(forms.ModelForm):
    class Meta:
        model = Roteiro
        fields = ["destino", "data_ida", "data_volta", "quantidade_pessoas"]
        widgets = {
            "destino": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Destino"}
            ),
            "data_ida": forms.TextInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "data_volta": forms.TextInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "quantidade_pessoas": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Quantidade de pessoas"}
            ),
        }
