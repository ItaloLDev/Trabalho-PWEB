from django.shortcuts import render
from .models import Partida
from django.shortcuts import render, get_object_or_404
from .forms import CadastrarPartidaForm
from .forms import DefinirResultadoForm
from .forms import ApostarForm
from django.shortcuts import redirect
from .models import Jogador
from .models import Aposta
from django.contrib.auth.models import User
from django.db.models import Sum
import decimal
from django.contrib import messages

def tabela_partidas(request):
    tabela = Partida.objects.order_by('-id') 
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'bolaoapp/tabela_partidas.html', {'tabela': tabela})
        jogador = Jogador.objects.get(user=User.objects.get(username=request.user.username))
        return render(request, 'bolaoapp/tabela_partidas.html', {'tabela': tabela, 'jogador': jogador})
    return render(request, 'bolaoapp/tabela_partidas.html', {'tabela': tabela})
    
def listar_apostas(request, pk):
    apostas = Aposta.objects.filter(partida=get_object_or_404(Partida, pk=pk))
    partida = Partida.objects.get(pk=pk) 
    return render(request, 'bolaoapp/listar_apostas.html', {'apostas': apostas, 'partida':partida})

def fazer_aposta(request, pk):
    jogador = Jogador.objects.get(user=User.objects.get(username=request.user.username))
    partida = Partida.objects.get(pk=pk) 
    try:
       check = Aposta.objects.get(apostador=jogador, partida=partida) 
    except Aposta.DoesNotExist:
        check = None
    if jogador.credito < decimal.Decimal(5):
        messages.error(request, 'Créditos insuficientes!')
        return redirect('tabela_partidas') 
    if not check:
        if request.method == "POST":
            form = ApostarForm(request.POST)
            if form.is_valid():
                aposta = form.save(commit=False)
                aposta.apostador = jogador
                aposta.valor_aposta = decimal.Decimal(5)
                aposta.partida = partida
                aposta.apostar()
                jogador.credito = decimal.Decimal(jogador.credito) - decimal.Decimal(5)
                jogador.save(update_fields=["credito"]) 
                return render(request, 'bolaoapp/confirmacao_aposta.html', {'aposta': aposta}) #supostamente nossa tela de confirmação
        else:
            form = ApostarForm()
        return render(request, 'bolaoapp/fazer_aposta.html', {'form': form, 'partida': partida}) #a tela onde carrega o formulario
    return render(request, 'bolaoapp/confirmacao_aposta.html', {'aposta': check}) #supostamente nossa tela de confirmação

def cadastrar_partida(request):
    if request.method == "POST":
         form = CadastrarPartidaForm(request.POST)
         if form.is_valid():
            partida = Partida()
            partida.time1 = str(form.cleaned_data["time1"])
            partida.time2 = str(form.cleaned_data["time2"])
            partida.campeonato = str(form.cleaned_data["campeonato"])
            partida.qtdGols_time1 = -1
            partida.qtdGols_time2 = -1
            partida.cadastrar()
            return redirect('tabela_partidas')
    else:
        form = CadastrarPartidaForm()
    return render(request, 'bolaoapp/cadastrar_partida.html', {'form': form})

def definir_resultado(request, pk):
    partida = Partida.objects.get(pk=pk) 
    if not partida.isValidoParaAposta:
        messages.error(request, 'Essa partida já teve o resultado definido. Não é possível editar seu resultado.')
        return redirect('tabela_partidas') 
    else:   
        if request.method == "POST":
            form = DefinirResultadoForm(request.POST, instance=partida)
            if form.is_valid():
                partida = form.save(commit=False)
                apostas = Aposta.objects.filter(partida=get_object_or_404(Partida, pk=pk))
                valor_geral = apostas.aggregate(Sum('valor_aposta'))
                distribuir(partida, apostas,valor_geral)
                partida.isValidoParaAposta = False
                partida.save()
                return redirect('tabela_partidas')
        else:
            messages.warning(request, 'Atenção! Partidas finalizadas não podem ser excluídas ou editadas. Após definido o resultado, não será possível modifica-lo. ')
            form = DefinirResultadoForm(instance=partida)
            form.qtdGols_time1 = 0
            form.qtdGols_time2 = 0
        return render(request, 'bolaoapp/definir_resultado.html', {'form': form})
        
def excluir_partida(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    apostas = Aposta.objects.filter(partida=get_object_or_404(Partida, pk=pk))
    if partida.isValidoParaAposta == True:
        for aposta in apostas:
            jogador = Jogador.objects.get(pk=aposta.apostador.pk)
            jogador.credito += aposta.valor_aposta
            jogador.save(update_fields=['credito'])
        partida.delete()
        return render(request, 'bolaoapp/excluir_partida.html', )
    else:
        messages.error(request, 'Não é permitido excluir partidas já finalizadas.')
        return redirect('tabela_partidas') 

def login(request):
    template = loader.get_template('login.html')
    user_info = Jogador.objects.get(user=User.objects.get(username=request.user.username))
    context = RequestContext(request, {'credito':user_info.credito,})
    return HttpResponse(template.render(context))
     
def distribuir(partida, apostas, valor_geral):
    try: 
        resultado = partida.getResultado()
        print(resultado)
        if apostas:
            apostas_corretas_placar = apostas.filter(qtdGols_time1=partida.qtdGols_time1, qtdGols_time2=partida.qtdGols_time2)
            print('uiui')
            apostas_corretas_resultado = []
            apostas_corretas_resultado = getApostasPorResultado(apostas, resultado)
            print('antes')
            if apostas_corretas_placar:
                print('placar')
                valor_dividido = valor_geral['valor_aposta__sum'] / apostas_corretas_placar.count()
                print(valor_dividido)
                for aposta in apostas_corretas_placar:
                    jogador = Jogador.objects.get(pk=aposta.apostador.pk)
                    jogador.credito += valor_dividido
                    jogador.save(update_fields=['credito'])
            elif apostas_corretas_resultado:
                print('resultado')
                valor_dividido = valor_geral['valor_aposta__sum'] / len(apostas_corretas_resultado)
                for aposta in apostas_corretas_resultado:
                    jogador = Jogador.objects.get(pk=aposta.apostador.pk)
                    jogador.credito += valor_dividido
                    jogador.save(update_fields=['credito'])
            else:
                for aposta in apostas:
                    jogador = Jogador.objects.get(pk=aposta.apostador.pk)
                    jogador.credito += aposta.valor_aposta
                    jogador.save(update_fields=['credito'])
    except Exception:
        return 

def ranking(request):
    jogadores = Jogador.objects.all().order_by('-credito')
    return render(request, 'bolaoapp/ranking.html', {'jogadores': jogadores})

def getApostasPorResultado(apostas, resultado):
    print('entrou')
    lista = []
    for aposta in apostas:
        if aposta.getResultado() == resultado:
            print('entrou2')
            lista.append(aposta)
    print(len(lista))
    return lista


