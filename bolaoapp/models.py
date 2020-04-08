from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.functions import Concat


class Partida(models.Model):
    codigoPartida = models.CharField(max_length=8)
    time1 = models.CharField(max_length=25)
    time2 = models.CharField(max_length=25)
    time1_gols = models.IntegerField()
    time2_gols = models.IntegerField()
    placar = models.CharField(max_length=6, blank=True)

    def cadastrar(self):
        self.save()

    def getPlacar(self):
        return self.placar

    def getVencedor(self):
        if(self.time1_gols > self.time2_gols):
            return self.time1
        elif(self.time2_gols > self.time1_gols):
            return self.time2
        else:
            return "Empate"