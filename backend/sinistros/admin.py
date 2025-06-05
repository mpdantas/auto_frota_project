# backend/sinistros/admin.py

from django.contrib import admin # Importa o módulo admin do Django
from .models import Sinistro # Importa o modelo Sinistro
from veiculos.models import Veiculo # Importa o modelo Veiculo, pois Sinistro se relaciona com ele

@admin.register(Sinistro) # Registra o modelo Sinistro no painel de administração
class SinistroAdmin(admin.ModelAdmin):
    """
    Define as opções de exibição e interação para o modelo Sinistro no painel administrativo.
    """
    # Campos a serem exibidos na lista de sinistros
    list_display = (
        'veiculo_placa', # Usa um método customizado para exibir a placa do veículo
        'tipo_sinistro',
        'data_sinistro',
        'status_sinistro',
        'data_registro_sistema'
    )
    # Habilita busca pelos campos indicados
    search_fields = (
        'tipo_sinistro', 'descricao', 'veiculo__placa', # Busca também pela placa do veículo relacionado
        'veiculo__modelo'
    )
    # Permite filtrar sinistros por campos específicos
    list_filter = ('tipo_sinistro', 'status_sinistro', 'data_sinistro', 'veiculo__empresa')
    # Campo para seleção de FK que vira um dropdown de busca
    raw_id_fields = ('veiculo',) # Útil para muitos veículos
    # Agrupamento de campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('veiculo',)
        }),
        ('Detalhes do Sinistro', {
            'fields': (
                ('data_sinistro', 'tipo_sinistro'),
                'descricao',
                'status_sinistro',
            )
        }),
        ('Informações do Registro', {
            'fields': ('data_registro_sistema',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('data_registro_sistema',) # Torna o campo somente leitura

    # Método customizado para exibir a placa do veículo diretamente na lista de sinistros
    def veiculo_placa(self, obj):
        return obj.veiculo.placa
    veiculo_placa.short_description = 'Placa do Veículo' # Nome da coluna no admin
    veiculo_placa.admin_order_field = 'veiculo__placa' # Permite ordenar por este campo