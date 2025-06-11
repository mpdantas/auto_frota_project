# backend/veiculos/forms.py

from django import forms # Importa o módulo forms do Django
from .models import Veiculo, Empresa # Importa os modelos Veiculo e Empresa
import re # Importa o módulo de expressões regulares para validação de CNPJ e Placa

# --- Formulário para o Modelo Empresa ---
class EmpresaForm(forms.ModelForm):
    """
    Formulário baseado no modelo Empresa para registro de novas empresas.
    Inclui validação de formato para o CNPJ.
    """
    class Meta:
        model = Empresa # Define que este formulário é baseado no modelo Empresa
        fields = ['razao_social', 'cnpj'] # Campos que o formulário deve incluir (data_cadastro é auto_now_add)
        labels = {
            'razao_social': 'Razão Social',
            'cnpj': 'CNPJ',
        }
        help_texts = {
            # Atualiza o texto de ajuda para ser mais explícito
            'cnpj': 'Digite o CNPJ no formato XX.XXX.XXX/YYYY-ZZ (somente números serão aceitos).',
        }
        error_messages = {
            'razao_social': {
                'unique': 'Já existe uma empresa com esta Razão Social cadastrada.',
            },
            'cnpj': {
                'unique': 'Já existe uma empresa com este CNPJ cadastrado.',
            },
        }

    # Método para limpar e validar o campo CNPJ
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj') # Obtém o valor do CNPJ já limpo pelos validadores básicos

        if cnpj: # Se o CNPJ não estiver vazio
            # Remove qualquer caracter que não seja dígito para padronizar
            cnpj_numerico = re.sub(r'[^0-9]', '', cnpj)

            # Valida se o CNPJ numérico tem 14 dígitos
            if len(cnpj_numerico) != 14:
                raise forms.ValidationError('O CNPJ deve conter exatamente 14 dígitos.')

            # Expressão regular para validar o formato XX.XXX.XXX/YYYY-ZZ
            cnpj_pattern = r'^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$'

            # Se o CNPJ original não está no formato, ele o formata
            if not re.match(cnpj_pattern, cnpj):
                cnpj_formatado = f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"
                # Retorna o CNPJ formatado
                return cnpj_formatado
            
        # Se já estava no formato correto ou vazio, retorna o valor original
        return cnpj

# --- Formulário para o Modelo Veiculo ---
class VeiculoForm(forms.ModelForm):
    """
    Formulário baseado no modelo Veiculo para registro e edição.
    Ele gera automaticamente campos para a maioria dos atributos do modelo,
    incluindo os dropdowns 'marca' e 'seguradora' que agora estão configurados no modelo.
    """
    class Meta:
        model = Veiculo
        # Lista dos campos do modelo Veiculo que o formulário deve incluir.
        # A ordem aqui define a ordem no formulário.
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
            'seguradora',
            'franquia',
            'data_vencimento_seguro',
            'ativo' # Mantido para permitir ativar/desativar se necessário via formulário
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
            'data_vencimento_seguro': forms.DateInput(attrs={'type': 'date'}), # Renderiza como um seletor de data HTML5
        }

        # Opcional: Textos de ajuda personalizados para campos
        help_texts = {
            'chassi': 'O chassi deve conter 17 caracteres alfanuméricos.',
            'renavam': 'O RENAVAM deve conter 11 dígitos.',
            'zero_kilometro': 'Marque se o veículo é zero quilômetro.',
            'placa': 'Use o padrão AAA-1234 (antigo) ou AAA0A00 (Mercosul).'
        }

        # Opcional: Mensagens de erro personalizadas para validação
        error_messages = {
            'placa': {
                'unique': 'Já existe um veículo cadastrado com esta placa. Por favor, verifique.',
            },
            'chassi': {
                'unique': 'Já existe um veículo cadastrado com este chassi. Por favor, verifique.',
            },
            'renavam': {
                'unique': 'Já existe um veículo cadastrado com este RENAVAM. Por favor, verifique.',
            },
        }
    
    # Método para limpar e validar o campo Placa
    def clean_placa(self):
        placa = self.cleaned_data.get('placa') # Obtém o valor da placa

        if placa: # Se a placa não estiver vazia
            placa_limpa = placa.replace('-', '').upper() # Remove hífen e converte para maiúsculas para validação

            # Padrão para placa Mercosul: AAA0A00 (3 letras, 1 número, 1 letra, 2 números)
            # Ex: ABC1E23
            mercosul_pattern = r'^[A-Z]{3}\d[A-Z]\d{2}$'
            
            # Padrão para placa Antiga: AAA-0000 (3 letras, hífen, 4 números)
            # Ex: ABC-1234
            antiga_pattern = r'^[A-Z]{3}-\d{4}$'

            # Primeiro, tenta validar o formato com hífen ou sem e padroniza
            if re.match(antiga_pattern, placa):
                # Se já está no formato antigo (com hífen), aceita como está
                return placa
            elif re.match(mercosul_pattern, placa_limpa): # Verifica o Mercosul sem hífen
                # Se está no formato Mercosul (sem hífen), aceita o valor limpo
                return placa_limpa 
            else:
                # Se não corresponde a nenhum dos padrões válidos
                raise forms.ValidationError('Formato de placa inválido. Use AAA-1234 ou AAA0A00.')
        
        return placa # Retorna a placa (se vazia ou já validada)

    # Este método é executado quando o formulário é instanciado.
    # Usamos ele para adicionar a opção vazia (empty_label) aos dropdowns.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adiciona a opção "Escolha a Marca" como a primeira no dropdown de marca
        if 'marca' in self.fields:
            self.fields['marca'].empty_label = "--- Escolha a Marca ---"
        
        # Adiciona a opção "Escolha a Seguradora" como a primeira no dropdown de seguradora
        if 'seguradora' in self.fields:
            self.fields['seguradora'].empty_label = "--- Escolha a Seguradora ---"
            
        # Adiciona a opção "Escolha a Empresa" como a primeira no dropdown de empresa
        if 'empresa' in self.fields:
            self.fields['empresa'].empty_label = "--- Escolha a Empresa ---"