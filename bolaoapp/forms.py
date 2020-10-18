from django import forms

from .models import Partida
from .models import Aposta

class DefinirResultadoForm(forms.ModelForm):

    class Meta:
        model = Partida
        fields = ('time1', 'time2', 'qtdGols_time1', 'qtdGols_time2','campeonato')

class CadastrarPartidaForm(forms.Form):

    time1 = forms.CharField(max_length = 200) 
    time2 = forms.CharField(max_length = 200) 
    campeonato = forms.CharField(max_length = 200) 


class ApostarForm(forms.ModelForm):

    class Meta:
        model = Aposta
        fields = ('qtdGols_time1', 'qtdGols_time2')
       