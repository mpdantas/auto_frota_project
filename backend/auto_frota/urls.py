"""
URL configuration for auto_frota project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# backend/auto_frota/urls.py

from django.contrib import admin
from django.urls import path, include # Importa 'include' para incluir URLs de outros apps

urlpatterns = [
    path('admin/', admin.site.urls), # URL para o painel de administração do Django
    path('', include('core.urls')),  # Inclui as URLs do aplicativo 'core'.
                                     # Quando o path está vazio (''), significa que 'core'
                                     # gerenciará as URLs a partir da raiz do projeto.
                                     # Por exemplo, 'http://127.0.0.1:8000/login/'
]
