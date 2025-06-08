# backend/veiculos/urls.py

from django.urls import path
from . import views

app_name = 'veiculos'

urlpatterns = [
    # URLs para Gestão de Empresas
    path('empresa/registrar/', views.registrar_empresa, name='registrar_empresa'),
    path('empresas/lista/', views.listar_empresas, name='listar_empresas'),
    path('empresas/excluir/<int:pk>/', views.excluir_empresa, name='excluir_empresa'),

    # URLs para Gestão de Veículos
    path('registrar/', views.registrar_carro, name='registrar_carro'),
    path('lista/', views.listar_carros, name='listar_carros'),
    path('excluir/<int:pk>/', views.excluir_carro, name='excluir_carro'),
    # NOVA URL para editar um veículo
    path('editar/<int:pk>/', views.editar_carro, name='editar_carro'), 
]