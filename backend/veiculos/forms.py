# backend/veiculos/forms.py

from django import forms # Importa o módulo forms do Django
from .models import Veiculo, Empresa # Importa os modelos Veiculo e Empresa

class VeiculoForm(forms.ModelForm):
    """
    Formulário baseado no modelo Veiculo para registro e edição.
    Ele gera automaticamente campos para a maioria dos atributos do modelo,
    incluindo os dropdowns 'marca' e 'seguradora' que agora estão configurados no modelo.
    """
    class Meta:
        model = Veiculo
        # Lista dos campos do modelo Veiculo que o formulário deve incluir.
        # 'marca' e 'seguradora' estão aqui na ordem desejada.
        fields = [
            'empresa',
            'marca',
            'modelo',
            'placa',
            'chassi',
            'renavam',
            'ano_fabricacao',
            'ano_modelo',
            'zero_kilometro',
            'nome_condutor',
            'classe_bonus',
            'seguradora', # Agora configurada como dropdown no model
            'franquia',
            'data_vencimento_seguro',
            'ativo'
        ]
        
        # Opcional: Personalizar labels dos campos se forem diferentes do verbose_name no model
        labels = {
            'empresa': 'Empresa Proprietária',
            'marca': 'Marca do Veículo',
            'modelo': 'Modelo do Veículo',
            'placa': 'Placa do Veículo',
            'chassi': 'Chassi',
            'renavam': 'Renavam',
            'ano_fabricacao': 'Ano de Fabricação',
            'ano_modelo': 'Ano do Modelo',
            'zero_kilometro': 'Zero Quilômetro',
            'nome_condutor': 'Nome do Condutor',
            'classe_bonus': 'Classe de Bônus',
            'seguradora': 'Seguradora',
            'franquia': 'Franquia',
            'data_vencimento_seguro': 'Vencimento do Seguro',
            'ativo': 'Ativo no Sistema',
        }
        
        # Opcional: Widgets para personalizar a apresentação dos campos HTML
        widgets = {
            'data_vencimento_seguro': forms.DateInput(attrs={'type': 'date'}),
        }
    
    # Este método é executado quando o formulário é instanciado.
    # Usamos ele para adicionar a opção vazia (empty_label) aos dropdowns.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adiciona a opção "Escolha a Marca" como a primeira no dropdown de marca
        if 'marca' in self.fields: # Verifica se o campo 'marca' existe no formulário
            self.fields['marca'].empty_label = "--- Escolha a Marca ---"
        
        # Adiciona a opção "Escolha a Seguradora" como a primeira no dropdown de seguradora
        if 'seguradora' in self.fields: # Verifica se o campo 'seguradora' existe no formulário
            self.fields['seguradora'].empty_label = "--- Escolha a Seguradora ---"
            
        # Adiciona a opção "Escolha a Empresa" como a primeira no dropdown de empresa
        if 'empresa' in self.fields: # Verifica se o campo 'empresa' existe no formulário
            self.fields['empresa'].empty_label = "--- Escolha a Empresa ---"