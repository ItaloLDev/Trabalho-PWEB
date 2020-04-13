from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.functions import Concat
from django.contrib.auth.models import User



class Partida(models.Model):
    codigoPartida = models.CharField(max_length=8)
    time1 = models.CharField(max_length=25)
    time2 = models.CharField(max_length=25)
    qtdGols_time1 = models.IntegerField()
    qtdGols_time2 = models.IntegerField()
    placar = models.CharField(max_length=6, blank=True)
    isValidoParaAposta = models.BooleanField(default=True)
    campeonato = models.CharField(max_length=25)

    def cadastrar(self):
        self.save()
    
    def getResultado(self):
        if(self.qtdGols_time1 > self.qtdGols_time2):
            return self.time1
        elif(self.qtdGols_time2 > self.qtdGols_time1):
            return self.time2
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
    placar = models.CharField(max_length=6, blank=True)
    resultado = models.CharField(max_length=25, blank=True)
    apostador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, default="")
    valor_aposta = models.DecimalField(max_digits=5, decimal_places=2)

    def apostar(self):
        self.save()
    
