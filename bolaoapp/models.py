from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.functions import Concat
from django.contrib.auth.models import User



class Partida(models.Model):
    time1 = models.CharField("TIME 1", max_length=25, blank=False)
    time2 = models.CharField("TIME 2",max_length=25, blank=False)
    qtdGols_time1 = models.IntegerField("GOLS DO TIME 1")
    qtdGols_time2 = models.IntegerField("GOLS DO TIME 2")
    isValidoParaAposta = models.BooleanField(default=True)
    campeonato = models.CharField(max_length=25, blank=False)

    def cadastrar(self):
        self.save()
    
    def getResultado(self):
        if(self.qtdGols_time1 > self.qtdGols_time2):
            return 1
        elif(self.qtdGols_time2 > self.qtdGols_time1):
            return 2
        else:
            return "Empate"
        
class Jogador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credito = models.DecimalField(max_digits=5, decimal_places=2)

    def getCredito(self):
        return self.credito

    def addCredito(self, credito_adicional):
        self.credito +=credito_adicional
        ##TERMINAR O METODO PARA ADICIONAR CREDITO

    def salvar(self):
        self.save()

class Aposta(models.Model):
    qtdGols_time1 = models.IntegerField(blank=False)
    qtdGols_time2 = models.IntegerField(blank=False)
    apostador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, default="")
    valor_aposta = models.DecimalField(max_digits=5, decimal_places=2)

    def apostar(self):
        self.save()

    def getResultado(self):
        if(self.qtdGols_time1 > self.qtdGols_time2):
            return 1
        elif(self.qtdGols_time2 > self.qtdGols_time1):
            return 2
        else:
            return "Empate"
    
