# backend/veiculos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Decorador para exigir login
from django.contrib import messages # Para exibir mensagens de sucesso/erro
from django.urls import reverse
from django.db.models import Q # Importa Q para realizar buscas complexas (OR)

from .models import Veiculo, Empresa
from .forms import VeiculoForm, EmpresaForm


@login_required # Garante que apenas usuários logados possam acessar esta view
def registrar_empresa(request):
    """
    Esta view gerencia o formulário de registro de novas empresas.
    - Se a requisição for POST, tenta salvar uma nova empresa no banco de dados.
    - Se o formulário for válido, salva a empresa e redireciona para a lista de empresas.
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe um formulário vazio para registro.
    """
    if request.method == 'POST':
        form = EmpresaForm(request.POST) # Instancia o formulário com os dados POST
        if form.is_valid():
            form.save() # Salva a nova empresa no banco de dados
            messages.success(request, 'Empresa registrada com sucesso!')
            return redirect(reverse('veiculos:listar_empresas')) # Redireciona para a lista de empresas
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
    - Se o formulário for válido, salva o veículo e redireciona para a lista de veículos.
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe um formulário vazio para registro.
    """
    if request.method == 'POST': # Verifica se a requisição é um POST (envio do formulário)
        # Instancia o formulário com os dados enviados via POST
        form = VeiculoForm(request.POST) 
        if form.is_valid(): # Verifica se os dados do formulário são válidos
            form.save() # Salva o novo veículo no banco de dados
            messages.success(request, 'Veículo registrado com sucesso!')
            return redirect(reverse('veiculos:listar_carros')) # Redireciona para a lista de veículos
        else:
            # Se o formulário for inválido, adiciona uma mensagem de erro
            messages.error(request, 'Erro ao registrar veículo. Verifique os campos.')
    else:
        # Se a requisição for GET, cria um formulário vazio
        form = VeiculoForm()
    
    # Renderiza o template com o formulário
    # is_edit=False indica que estamos no modo de registro, não edição
    return render(request, 'veiculos/registrar_carro.html', {'form': form, 'is_edit': False})


@login_required
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
        'query': query # Passa o termo de busca de volta para o template para manter no campo
    }
    return render(request, 'veiculos/listar_carros.html', context)


@login_required # Garante que apenas usuários logados possam acessar esta view
def excluir_carro(request, pk):
    """
    Esta view realiza a exclusão lógica (desativação) de um veículo.
    - Busca o veículo pelo ID (pk).
    - Altera o status 'ativo' para False.
    - Redireciona para a lista de veículos com mensagem de sucesso.
    - Se a requisição não for POST, renderiza uma página de confirmação (opcional).
    """
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if request.method == 'POST': # Garante que a ação seja via POST para segurança (formulário ou AJAX)
        veiculo.ativo = False # Define o status do veículo como inativo
        veiculo.save() # Salva a mudança no banco de dados

        messages.success(request, f'Veículo com placa {veiculo.placa} desativado com sucesso.')
        return redirect(reverse('veiculos:listar_carros'))

    # Se a requisição não for POST (ex: GET direto na URL), renderiza uma página de confirmação
    return render(request, 'veiculos/confirmar_exclusao.html', {'veiculo': veiculo})


@login_required # Garante que apenas usuários logados possam acessar esta view
def editar_carro(request, pk): # Recebe o PK (Primary Key) do veículo a ser editado
    """
    Esta view gerencia o formulário de edição de veículos.
    - Busca o veículo pelo ID (pk).
    - Se a requisição for POST, tenta atualizar o veículo no banco de dados.
    - Se o formulário for válido, salva as alterações e redireciona para a lista de veículos com mensagem de sucesso.
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe o formulário pré-preenchido com os dados do veículo.
    """
    veiculo = get_object_or_404(Veiculo, pk=pk)

    if request.method == 'POST':
        # Instancia o formulário com os dados enviados via POST
        # e passa a instância 'veiculo' para que o formulário atualize esse objeto existente
        form = VeiculoForm(request.POST, instance=veiculo) 
        if form.is_valid(): # Verifica se os dados do formulário são válidos
            form.save() # Salva as alterações no veículo existente
            messages.success(request, f'Veículo com placa {veiculo.placa} atualizado com sucesso!')
            return redirect(reverse('veiculos:listar_carros')) # Redireciona para a lista de veículos
        else:
            messages.error(request, 'Erro ao atualizar veículo. Verifique os campos.')
    else:
        # Se a requisição for GET, cria um formulário pré-preenchido com os dados do veículo
        form = VeiculoForm(instance=veiculo)
    
    # Renderiza o template com o formulário e o objeto veiculo
    context = {
        'form': form,
        'veiculo': veiculo, # Passa o objeto veiculo para o template (útil para títulos, etc.)
        'is_edit': True, # Indica que estamos no modo de edição (útil para mudar o título do formulário)
    }
    return render(request, 'veiculos/registrar_carro.html', context) # Reutiliza o template de registro


@login_required
def listar_empresas(request):
    """
    Lista todas as empresas cadastradas, com opção de busca por razão social ou CNPJ.
    """
    empresas = Empresa.objects.all().order_by('razao_social') # Ordena por razão social
    query = request.GET.get('q') # Obtém o termo de busca

    if query:
        # Filtra empresas usando Q objects para buscar em razão social ou CNPJ
        empresas = empresas.filter(
            Q(razao_social__icontains=query) |
            Q(cnpj__icontains=query)
        ).distinct() # distinct() para evitar duplicatas se um termo corresponder a ambos os campos

        messages.info(request, f"Exibindo resultados para a busca por empresa: '{query}'")

    context = {
        'empresas': empresas,
        'query': query, # Passa o termo de busca de volta para o template
    }
    return render(request, 'veiculos/listar_empresas.html', context)


@login_required
def excluir_empresa(request, pk):
    """
    Exclui uma empresa do banco de dados.  **CUIDADO: ESTA EXCLUSÃO É PERMANENTE.**
    Todos os veículos associados a esta empresa também serão excluídos devido ao CASCADE.
    É recomendável ter uma confirmação visual robusta no template.
    """
    empresa = get_object_or_404(Empresa, pk=pk)
    
    if request.method == 'POST':
        empresa.delete() # Exclui a empresa do banco de dados
        messages.success(request, f'Empresa "{empresa.razao_social}" excluída permanentemente.')
        return redirect(reverse('veiculos:listar_empresas')) # Redireciona para a lista de empresas

    # Se a requisição não for POST, exibe a página de confirmação
    return render(request, 'veiculos/confirmar_excluir_empresa.html', {'empresa': empresa})