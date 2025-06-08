# backend/core/views.py

from django.shortcuts import render, redirect # Importa render e redirect
from django.contrib.auth import authenticate, login, logout # Importa funções de autenticação (authenticate, login, e logout)
from django.contrib import messages # Importa o módulo de mensagens para feedback ao usuário
from django.urls import reverse
from datetime import date, timedelta # Importa date (data atual) e timedelta (para cálculo de datas)

from veiculos.models import Veiculo # Importa o modelo Veiculo para poder contar carros e buscar alertas


def login_view(request):
    """
    Esta view gerencia a exibição e o processamento do formulário de login.
    - Se a requisição for POST, tenta autenticar o usuário.
    - Se a autenticação for bem-sucedida, faz o login e redireciona para o dashboard.
    - Caso contrário, exibe uma mensagem de erro e mantém o usuário na página de login.
    - Se a requisição for GET, simplesmente exibe o formulário de login.
    """
    if request.method == 'POST': # Verifica se a requisição é um POST (envio do formulário)
        username = request.POST.get('username') # Obtém o valor do campo 'username' do formulário
        password = request.POST.get('password') # Obtém o valor do campo 'password' do formulário

        # Tenta autenticar o usuário com as credenciais fornecidas
        user = authenticate(request, username=username, password=password)

        if user is not None: # Se a autenticação for bem-sucedida (usuário encontrado e senha correta)
            login(request, user) # Faz o login do usuário na sessão do Django
            # Adiciona uma mensagem de sucesso para exibir ao usuário
            messages.success(request, f'Bem-vindo, {user.username}!')
            # Redireciona para a URL do dashboard
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
    - Verifica se o usuário está autenticado.
    - Busca e exibe a quantidade de carros ativos.
    - Busca e exibe alertas de seguros próximos ao vencimento (próximos 60 dias).
    """
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))

    # Contagem de carros ativos
    quantidade_carros = Veiculo.objects.filter(ativo=True).count()

    # Lógica para Alertas de Vencimento
    today = date.today() # Obtém a data de hoje
    # Calcula a data limite para o alerta (hoje + 60 dias)
    alert_date_limit = today + timedelta(days=60) 

    # Busca veículos ativos cujo vencimento do seguro está entre hoje e a data limite de alerta
    # .select_related('empresa') para otimizar o acesso à razão social no template
    alertas_vencimento = Veiculo.objects.filter(
        ativo=True, # Apenas veículos ativos
        data_vencimento_seguro__gte=today, # Vencimento maior ou igual a hoje
        data_vencimento_seguro__lte=alert_date_limit # Vencimento menor ou igual à data limite
    ).order_by('data_vencimento_seguro') # Ordena pela data de vencimento (mais próximos primeiro)

    context = {
        'quantidade_carros': quantidade_carros,
        'alertas_vencimento': alertas_vencimento, # Passa a lista de veículos com alertas
        'total_alertas': alertas_vencimento.count(), # Passa a quantidade de alertas
    }

    return render(request, 'core/dashboard.html', context)

def logout_view(request):
    """
    Esta view realiza o logout do usuário.
    - Desloga o usuário da sessão.
    - Adiciona uma mensagem de sucesso.
    - Redireciona para a página de login.
    """
    logout(request) # Função do Django para deslogar o usuário da sessão
    messages.info(request, 'Você foi desconectado com sucesso.') # Adiciona uma mensagem de informação
    return redirect(reverse('core:login')) # Redireciona para a página de login