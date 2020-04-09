from django.urls import path
from . import views

urlpatterns = [
    path('', views.tabela_partidas, name='tabela_partidas'),
]