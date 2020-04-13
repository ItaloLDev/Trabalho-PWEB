from django import forms

from .models import Partida
from .models import Aposta

class CadastrarPartidaForm(forms.ModelForm):

    class Meta:
        model = Partida
        fields = ('codigoPartida', 'time1', 'time2', 'qtdGols_time1', 'qtdGols_time2', 'placar', 'campeonato' ,  'isValidoParaAposta')

class ApostarForm(forms.ModelForm):

    class Meta:
        model = Aposta
        fields = ('placar', 'resultado')
       