# backend/veiculos/admin.py

from django.contrib import admin # Importa o módulo admin do Django
from .models import Empresa, Veiculo # Importa os modelos Empresa e Veiculo do mesmo diretório ('.')

# Registra o modelo Empresa no painel de administração
@admin.register(Empresa) # Decorador que registra o modelo Empresa no admin
class EmpresaAdmin(admin.ModelAdmin):
    """
    Define as opções de exibição e interação para o modelo Empresa no painel administrativo.
    """
    list_display = ('razao_social', 'cnpj', 'data_cadastro') # Campos a serem exibidos na lista de empresas
    search_fields = ('razao_social', 'cnpj') # Habilita busca por Razão Social e CNPJ
    list_filter = ('data_cadastro',) # Permite filtrar empresas pela data de cadastro
    # readonly_fields = ('data_cadastro',) # Opcional: Torna o campo somente leitura no formulário de edição

# Registra o modelo Veiculo no painel de administração
@admin.register(Veiculo) # Decorador que registra o modelo Veiculo no admin
class VeiculoAdmin(admin.ModelAdmin):
    """
    Define as opções de exibição e interação para o modelo Veiculo no painel administrativo.
    """
    # Campos a serem exibidos na lista de veículos
    list_display = (
        'placa', 'modelo', 'empresa', 'seguradora', 'data_vencimento_seguro',
        'ativo', 'classe_bonus'
    )
    # Habilita busca pelos campos indicados
    search_fields = ('placa', 'chassi', 'renavam', 'modelo', 'empresa__razao_social')
    # Permite filtrar veículos por campos específicos
    list_filter = ('ativo', 'marca', 'seguradora', 'classe_bonus', 'zero_kilometro', 'empresa')
    # Campos que se tornam links para a página de detalhes do item
    list_display_links = ('placa', 'modelo',)
    # Campos que podem ser editados diretamente na lista (cuidado ao usar com muitos campos)
    # list_editable = ('ativo',)
    # Campos para preenchimento automático (slugs, etc. - não se aplica diretamente aqui, mas é útil saber)
    # prepopulated_fields = {"slug": ("title",)}
    # Campo para seleção de FK que vira um dropdown de busca
    raw_id_fields = ('empresa',) # Mostra um campo de busca para a empresa, útil para muitas empresas
    # Agrupamento de campos no formulário de edição para melhor organização
    fieldsets = (
        (None, { # Primeiro grupo, sem título
            'fields': (('empresa', 'numero_registro'),) # Tupla para colocar campos na mesma linha
        }),
        ('Dados do Veículo', {
            'fields': (
                ('marca', 'modelo'),
                ('placa', 'chassi', 'renavam'),
                ('ano_fabricacao', 'ano_modelo', 'zero_kilometro'),
                'nome_condutor',
            )
        }),
        ('Dados do Seguro', {
            'fields': (
                ('seguradora', 'classe_bonus'),
                ('franquia', 'data_vencimento_seguro'),
            ),
            'description': 'Informações relativas ao seguro do veículo.'
        }),
        ('Status do Sistema', {
            'fields': (('data_cadastro', 'ativo'),),
            'classes': ('collapse',), # Faz o grupo ser retrátil
        }),
    )
    # Torna certos campos somente leitura
    readonly_fields = ('numero_registro', 'data_cadastro',)