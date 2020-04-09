from django.shortcuts import render
from .models import Partida

def tabela_partidas(request):
    tabela = Partida.objects.order_by('-codigoPartida') 
    return render(request, 'bolaoapp/tabela_partidas.html', {'tabela': tabela})
