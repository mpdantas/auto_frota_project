# backend/sinistros/models.py

from django.db import models
from veiculos.models import Veiculo # Importa o modelo Veiculo do app 'veiculos' (necessário para ForeignKey)

class Sinistro(models.Model):
    """
    Modelo para registrar e detalhar eventos de sinistro.
    Cada sinistro é associado a um veículo específico.
    """
    # Relacionamento com o Veículo (Chave Estrangeira)
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE, # Se o veículo for excluído, seus sinistros associados também serão
        related_name='sinistros', # Permite acessar sinistros a partir de um veículo (ex: meu_veiculo.sinistros.all())
        verbose_name="Veículo Sinistrado"
    )

    # Dados do Sinistro
    data_sinistro = models.DateField(
        verbose_name="Data do Sinistro"
    )
    
    # Opções para o tipo de sinistro (usando um dropdown)
    TIPO_SINISTRO_CHOICES = [
        ('colisao', 'Colisão'),
        ('roubo', 'Roubo'),
        ('furto', 'Furto'),
        ('incendio', 'Incêndio'),
        ('danos_terceiros', 'Danos a Terceiros'),
        ('fenomeno_natureza', 'Fenômeno da Natureza'),
        ('outros', 'Outros'),
    ]
    tipo_sinistro = models.CharField(
        max_length=50,
        choices=TIPO_SINISTRO_CHOICES,
        default='colisao',
        verbose_name="Tipo de Sinistro"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição Detalhada"
    )
    
    # Opções para o status do sinistro
    STATUS_SINISTRO_CHOICES = [
        ('em_analise', 'Em Análise'),
        ('aberto', 'Aberto'),
        ('concluido_com_indenizacao', 'Concluído com Indenização'),
        ('concluido_sem_indenizacao', 'Concluído sem Indenização'),
        ('negado', 'Negado'),
        ('cancelado', 'Cancelado'),
    ]
    status_sinistro = models.CharField(
        max_length=50,
        choices=STATUS_SINISTRO_CHOICES,
        default='em_analise',
        verbose_name="Status do Sinistro"
    )

    # Metadados do Registro
    data_registro_sistema = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro no Sistema"
    )

    class Meta:
        verbose_name = "Sinistro"
        verbose_name_plural = "Sinistros"
        # Ordena por data do sinistro (mais recente primeiro) e depois pela placa do veículo
        ordering = ['-data_sinistro', 'veiculo__placa']

    def __str__(self):
        return f"{self.tipo_sinistro} - {self.veiculo.placa} ({self.data_sinistro.strftime('%d/%m/%Y')})"