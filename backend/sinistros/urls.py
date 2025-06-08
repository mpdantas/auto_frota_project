# backend/sinistros/urls.py

from django.urls import path
from . import views

app_name = 'sinistros'

urlpatterns = [
    path('registrar/', views.registrar_sinistro, name='registrar_sinistro'),
    path('lista/', views.listar_sinistros, name='listar_sinistros'),
    # NOVA URL para excluir um sinistro
    path('excluir/<int:pk>/', views.excluir_sinistro, name='excluir_sinistro'),
]