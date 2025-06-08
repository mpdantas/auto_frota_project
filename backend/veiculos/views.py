# backend/veiculos/views.py

from django.shortcuts import render, redirect, get_object_or_404 # Importa render, redirect, e get_object_or_404
from django.contrib.auth.decorators import login_required # Decorador para exigir login
from django.contrib import messages # Para exibir mensagens de sucesso/erro
from django.urls import reverse # Para gerar URLs por nome

from .models import Veiculo, Empresa # Importa os modelos Veiculo e Empresa
from .forms import VeiculoForm # Importa o formulário que criamos para o Veículo

@login_required # Garante que apenas usuários logados possam acessar esta view
def registrar_carro(request):
    """
    Esta view gerencia o formulário de registro de veículos.
    - Se a requisição for POST, tenta salvar um novo veículo no banco de dados.
    - Se o formulário for válido, salva o veículo e redireciona para o dashboard com mensagem de sucesso.
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe um formulário vazio para registro.
    """
    if request.method == 'POST':
        # Instancia o formulário com os dados enviados via POST
        form = VeiculoForm(request.POST) 
        if form.is_valid(): # Verifica se os dados do formulário são válidos
            form.save() # Salva o novo veículo no banco de dados
            messages.success(request, 'Veículo registrado com sucesso!') # Adiciona mensagem de sucesso
            return redirect(reverse('core:dashboard')) # Redireciona para o dashboard
        else:
            # Se o formulário for inválido, adiciona uma mensagem de erro
            messages.error(request, 'Erro ao registrar veículo. Verifique os campos.')
    else:
        # Se a requisição for GET, cria um formulário vazio
        form = VeiculoForm()
    
    # Renderiza o template com o formulário
    return render(request, 'veiculos/registrar_carro.html', {'form': form})

@login_required # Garante que apenas usuários logados possam acessar esta view
def listar_carros(request):
    """
    Esta view busca e exibe uma lista de todos os veículos ativos registrados no sistema.
    Ela também pode ser usada para contar o total de carros.
    """
    # Busca todos os veículos que estão marcados como 'ativo=True'
    # .select_related('empresa') otimiza a consulta para buscar dados da empresa de uma vez
    veiculos = Veiculo.objects.filter(ativo=True).select_related('empresa').order_by('placa')
    
    # Adiciona a contagem de carros ativos ao contexto
    quantidade_carros = veiculos.count() 

    context = {
        'veiculos': veiculos, # Lista de veículos para exibir no template
        'quantidade_carros': quantidade_carros, # Quantidade total de carros ativos
    }
    # Renderiza o template 'listar_carros.html' com os dados dos veículos e a contagem
    return render(request, 'veiculos/listar_carros.html', context)

@login_required # Garante que apenas usuários logados possam acessar esta view
def excluir_carro(request, pk): # Recebe o PK (Primary Key) do veículo a ser excluído
    """
    Esta view realiza a exclusão lógica (desativação) de um veículo.
    - Busca o veículo pelo ID (pk).
    - Altera o status 'ativo' para False.
    - Redireciona para a lista de veículos com mensagem de sucesso.
    - Se a requisição não for POST, renderiza uma página de confirmação (opcional).
    """
    # Tenta obter o objeto Veiculo pelo ID (pk). Se não encontrar, retorna um erro 404.
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if request.method == 'POST': # Garante que a ação seja via POST para segurança (formulário ou AJAX)
        veiculo.ativo = False # Define o status do veículo como inativo
        veiculo.save() # Salva a mudança no banco de dados

        messages.success(request, f'Veículo com placa {veiculo.placa} desativado com sucesso.')
        return redirect(reverse('veiculos:listar_carros')) # Redireciona para a lista de carros

    # Se a requisição não for POST (ex: GET direto na URL), renderiza uma página de confirmação
    return render(request, 'veiculos/confirmar_exclusao.html', {'veiculo': veiculo})