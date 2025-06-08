# backend/veiculos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Veiculo, Empresa # Já importado
from .forms import VeiculoForm, EmpresaForm # NOVO: Importa EmpresaForm

@login_required # Garante que apenas usuários logados possam acessar esta view
def registrar_empresa(request):
    """
    Esta view gerencia o formulário de registro de novas empresas.
    - Se a requisição for POST, tenta salvar uma nova empresa no banco de dados.
    - Se o formulário for válido, salva a empresa e redireciona para a lista de veículos (ou dashboard).
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe um formulário vazio para registro.
    """
    if request.method == 'POST':
        form = EmpresaForm(request.POST) # Instancia o formulário com os dados POST
        if form.is_valid():
            form.save() # Salva a nova empresa no banco de dados
            messages.success(request, 'Empresa registrada com sucesso!')
            return redirect(reverse('veiculos:listar_carros')) # Redireciona para a lista de veículos
        else:
            messages.error(request, 'Erro ao registrar empresa. Verifique os campos.')
    else:
        form = EmpresaForm() # Cria um formulário vazio para requisições GET

    return render(request, 'veiculos/registrar_empresa.html', {'form': form})

@login_required # Garante que apenas usuários logados possam acessar esta view
def registrar_carro(request):
    """
    Esta view gerencia o formulário de registro de veículos.
    - Se a requisição for POST, tenta salvar um novo veículo no banco de dados.
    - Se o formulário for válido, salva o veículo e redireciona para o dashboard com mensagem de sucesso.
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe um formulário vazio para registro.
    """
    if request.method == 'POST': # Verifica se a requisição é um POST (envio do formulário)
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
    Permite busca por placa do veículo.
    """
    # Inicializa a queryset com todos os veículos ativos
    veiculos = Veiculo.objects.filter(ativo=True).select_related('empresa')

    # Obtém o termo de busca da requisição GET (se houver)
    query = request.GET.get('q') # 'q' será o nome do campo de busca no HTML

    if query:
        # Se houver um termo de busca, filtra os veículos.
        from django.db.models import Q # Importa Q aqui, para ter certeza que está disponível
        veiculos = veiculos.filter(
            Q(placa__icontains=query) | # Busca por placa
            Q(modelo__icontains=query) | # Opcional: buscar também por modelo para uma busca mais ampla
            Q(chassi__icontains=query)   # Opcional: buscar também por chassi
        )
        messages.info(request, f"Exibindo resultados para a busca: '{query}'")

    # Ordena a lista de veículos (após a busca, se houver)
    veiculos = veiculos.order_by('placa')

    # Adiciona a contagem de carros ativos (ou filtrados) ao contexto
    quantidade_carros = veiculos.count() 

    context = {
        'veiculos': veiculos,
        'quantidade_carros': quantidade_carros,
        'query': query
    }
    return render(request, 'veiculos/listar_carros.html', context)

@login_required # Garante que apenas usuários logados possam acessar esta view
def excluir_carro(request, pk):
    """
    Esta view realiza a exclusão lógica (desativação) de um veículo.
    """
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if request.method == 'POST':
        veiculo.ativo = False
        veiculo.save()
        messages.success(request, f'Veículo com placa {veiculo.placa} desativado com sucesso.')
        return redirect(reverse('veiculos:listar_carros'))

    return render(request, 'veiculos/confirmar_exclusao.html', {'veiculo': veiculo})