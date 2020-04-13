from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.tabela_partidas, name='tabela_partidas'),
    path('apostas/<int:pk>/', views.fazer_aposta, name='fazer_aposta'),
    path('partida/cadastrar/', views.cadastrar_partida, name='cadastrar_partida'),
    path('partida/<int:pk>/definir_resultado/', views.definir_resultado, name='definir_resultado'),
    path('partida/<int:pk>/excluir_partida/', views.excluir_partida, name='excluir_partida'),
    path('partida/<int:pk>/listar_apostas/', views.listar_apostas, name='listar_apostas'),
    path('login/', include('django.contrib.auth.urls')), 
    path('raking', views.ranking, name='ranking'),
]