# backend/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Página de login (agora na raiz do site)
    path('', views.login_view, name='login'),
    # Página do dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Nova URL para a função de logout
    path('logout/', views.logout_view, name='logout'), # Nova URL para logout
]