# backend/veiculos/urls.py

from django.urls import path
from . import views

app_name = 'veiculos' # O namespace 'veiculos' é crucial!

urlpatterns = [
    # URL para registrar empresa
    path('empresa/registrar/', views.registrar_empresa, name='registrar_empresa'), # <-- VERIFIQUE ESTA LINHA

    # URLs existentes para veículos
    path('registrar/', views.registrar_carro, name='registrar_carro'),
    path('lista/', views.listar_carros, name='listar_carros'),
    path('excluir/<int:pk>/', views.excluir_carro, name='excluir_carro'),
]