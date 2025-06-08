# backend/sinistros/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Decorador para exigir login
from django.contrib import messages # Para exibir mensagens de sucesso/erro
from django.urls import reverse
from django.db.models import Q # Para busca

from .models import Sinistro # Importa o modelo Sinistro
from .forms import SinistroForm # Importa o formulário que acabamos de criar


@login_required
def registrar_sinistro(request):
    """
    View para registrar um novo sinistro.
    - Se a requisição for POST, tenta salvar um novo sinistro no banco de dados.
    - Se o formulário for válido, salva o sinistro e redireciona para a lista de sinistros com mensagem de sucesso.
    - Se o formulário for inválido, exibe os erros no formulário.
    - Se a requisição for GET, exibe um formulário vazio para registro.
    """
    if request.method == 'POST':
        form = SinistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sinistro registrado com sucesso!')
            return redirect(reverse('sinistros:listar_sinistros')) # Redireciona para a lista de sinistros
        else:
            messages.error(request, 'Erro ao registrar sinistro. Verifique os campos.')
    else:
        form = SinistroForm()
    
    return render(request, 'sinistros/registrar_sinistro.html', {'form': form})


@login_required
def listar_sinistros(request):
    """
    View para listar todos os sinistros.
    Permite busca por tipo de sinistro, placa do veículo ou status.
    """
    # Inicializa a queryset com todos os sinistros, ordenados por data de sinistro mais recente
    # select_related('veiculo', 'veiculo__empresa') otimiza a consulta para buscar dados relacionados
    sinistros = Sinistro.objects.all().select_related('veiculo', 'veiculo__empresa').order_by('-data_sinistro')
    
    query = request.GET.get('q') # Termo de busca

    if query:
        # Filtra sinistros usando Q objects para buscar em múltiplos campos
        sinistros = sinistros.filter(
            Q(tipo_sinistro__icontains=query) | # Busca por tipo de sinistro
            Q(status_sinistro__icontains=query) | # Busca por status
            Q(veiculo__placa__icontains=query) | # Busca por placa do veículo
            Q(veiculo__modelo__icontains=query) # Busca por modelo do veículo
        ).distinct() # distinct() para evitar duplicatas em casos de OR em campos relacionados

        messages.info(request, f"Exibindo resultados para a busca por sinistro: '{query}'")

    context = {
        'sinistros': sinistros,
        'query': query,
        'total_sinistros': sinistros.count(),
    }
    return render(request, 'sinistros/listar_sinistros.html', context)

# backend/sinistros/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from .models import Sinistro
from .forms import SinistroForm


# ... (código existente para registrar_sinistro e listar_sinistros) ...


@login_required # Garante que apenas usuários logados possam acessar esta view
def excluir_sinistro(request, pk): # Recebe o PK (Primary Key) do sinistro a ser excluído
    """
    Exclui um sinistro do banco de dados. **CUIDADO: ESTA EXCLUSÃO É PERMANENTE.**
    É recomendável adicionar uma confirmação extra no template.
    """
    # Tenta obter o objeto Sinistro pelo ID (pk). Se não encontrar, retorna um erro 404.
    sinistro = get_object_or_404(Sinistro, pk=pk)

    if request.method == 'POST': # Garante que a ação seja via POST para segurança
        sinistro.delete() # Exclui o sinistro do banco de dados
        messages.success(request, f'Sinistro do veículo {sinistro.veiculo.placa} excluído permanentemente.')
        return redirect(reverse('sinistros:listar_sinistros')) # Redireciona para a lista de sinistros

    # Se a requisição não for POST, exibe a página de confirmação
    return render(request, 'sinistros/confirmar_excluir_sinistro.html', {'sinistro': sinistro})