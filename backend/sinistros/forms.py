# backend/sinistros/forms.py

from django import forms
from .models import Sinistro
from veiculos.models import Veiculo # Importa Veiculo para o campo 'veiculo'

class SinistroForm(forms.ModelForm):
    """
    Formulário baseado no modelo Sinistro para registro de novos sinistros.
    """
    class Meta:
        model = Sinistro
        # Inclui todos os campos editáveis do modelo
        fields = [
            'veiculo',
            'data_sinistro',
            'tipo_sinistro',
            'descricao',
            'status_sinistro',
        ]
        labels = {
            'veiculo': 'Veículo Sinistrado',
            'data_sinistro': 'Data do Sinistro',
            'tipo_sinistro': 'Tipo de Sinistro',
            'descricao': 'Descrição Detalhada',
            'status_sinistro': 'Status do Sinistro',
        }
        widgets = {
            'data_sinistro': forms.DateInput(attrs={'type': 'date'}), # Seletor de data HTML5
            'descricao': forms.Textarea(attrs={'rows': 4}), # Aumenta a altura do campo de texto
        }
        help_texts = {
            'veiculo': 'Selecione o veículo envolvido no sinistro.',
            'descricao': 'Descreva o ocorrido (local, danos, etc.).',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona a opção padrão para o dropdown de veículos
        # Filtra apenas veículos ativos para seleção, se desejar
        self.fields['veiculo'].empty_label = "--- Selecione o Veículo ---"
        self.fields['veiculo'].queryset = Veiculo.objects.filter(ativo=True).order_by('placa')