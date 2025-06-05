# backend/core/views.py

from django.shortcuts import render, redirect # Importa render e AGORA TAMBÉM redirect
from django.contrib.auth import authenticate, login # Importa funções de autenticação do Django
from django.contrib import messages # Importa o módulo de mensagens para feedback ao usuário
from django.urls import reverse # Importa reverse para gerar URLs por nome

def login_view(request):
    """
    Esta view gerencia a exibição e o processamento do formulário de login.
    - Se a requisição for POST, tenta autenticar o usuário.
    - Se a autenticação for bem-sucedida, redireciona para o dashboard.
    - Caso contrário, exibe uma mensagem de erro e mantém o usuário na página de login.
    - Se a requisição for GET, simplesmente exibe o formulário de login.
    """
    if request.method == 'POST': # Verifica se a requisição é um POST (envio do formulário)
        username = request.POST.get('username') # Obtém o valor do campo 'username' do formulário
        password = request.POST.get('password') # Obtém o valor do campo 'password' do formulário

        # Tenta autenticar o usuário com as credenciais fornecidas
        # 'authenticate' verifica o usuário e senha contra o banco de dados do Django
        user = authenticate(request, username=username, password=password)

        if user is not None: # Se a autenticação for bem-sucedida (usuário encontrado e senha correta)
            login(request, user) # Faz o login do usuário na sessão do Django
            # Adiciona uma mensagem de sucesso para exibir ao usuário (opcional)
            messages.success(request, f'Bem-vindo, {user.username}!')
            # Redireciona para a URL do dashboard (que ainda vamos definir)
            # reverse('core:dashboard') gera a URL 'http://127.0.0.1:8000/dashboard/'
            return redirect(reverse('core:dashboard'))
        else: # Se a autenticação falhar
            # Adiciona uma mensagem de erro para exibir ao usuário
            messages.error(request, 'Nome de usuário ou senha inválidos.')
            # Mantém o usuário na página de login
            return render(request, 'core/login.html')
            
    # Se a requisição for GET (apenas para exibir a página), renderiza o template de login
    return render(request, 'core/login.html')

def dashboard_view(request):
    """
    Esta view será responsável por exibir a página do dashboard.
    No futuro, ela buscará dados relevantes para o dashboard.
    Por enquanto, apenas renderiza um template simples.
    """
    # Verifica se o usuário está autenticado. Se não estiver, redireciona para o login.
    # Isso é uma forma básica de proteger a página.
    if not request.user.is_authenticated:
        return redirect(reverse('core:login')) # Redireciona para o login se não estiver logado

    return render(request, 'core/dashboard.html') # Renderiza o arquivo 'dashboard.html'