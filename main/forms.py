from django import forms
from .models import Atleta, Agente

class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['modalidade', 'regiao', 'foto']


class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        fields = ['area_atuacao', 'regiao', 'descricao', 'foto']
