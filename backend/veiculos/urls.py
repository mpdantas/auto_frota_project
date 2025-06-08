# backend/veiculos/urls.py
from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    path('registrar/', views.registrar_carro, name='registrar_carro'),
    path('lista/', views.listar_carros, name='listar_carros'),
    path('excluir/<int:pk>/', views.excluir_carro, name='excluir_carro'),
]