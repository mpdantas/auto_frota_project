# backend/veiculos/models.py

from django.db import models # Importa o módulo models do Django
import uuid # Importa o módulo UUID para gerar números de registro únicos

# --- Modelo Empresa ---
class Empresa(models.Model):
    """
    Modelo para representar as empresas/clientes da corretora.
    Cada empresa pode ter uma ou mais frotas de veículos associadas.
    """
    razao_social = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Razão Social"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['razao_social']

    def __str__(self):
        return self.razao_social

# --- Opções para o campo 'marca' ---
# Definindo as opções de marcas aqui no arquivo models.py
MARCA_CHOICES = [
    ('chevrolet', 'Chevrolet'),
    ('fiat', 'Fiat'),
    ('ford', 'Ford'),
    ('honda', 'Honda'),
    ('hyundai', 'Hyundai'),
    ('jeep', 'Jeep'),
    ('mercedes-benz', 'Mercedes-Benz'),
    ('mitsubishi', 'Mitsubishi'),
    ('nissan', 'Nissan'),
    ('peugeot', 'Peugeot'),
    ('renault', 'Renault'),
    ('toyota', 'Toyota'),
    ('volkswagen', 'Volkswagen'),
    ('volvo', 'Volvo'),
    ('bmw', 'BMW'),
    ('audi', 'Audi'),
    # Adicione mais marcas conforme a necessidade da corretora
]

# --- Opções para o campo 'seguradora' ---
# Definindo as opções de seguradoras aqui no arquivo models.py
SEGURADORA_CHOICES = [
    ('porto_seguro', 'Porto Seguro'),
    ('bradesco_seguros', 'Bradesco Seguros'),
    ('sulamerica', 'SulAmérica'),
    ('tokio_marine', 'Tokio Marine'),
    ('allianz', 'Allianz'),
    ('liberty', 'Liberty'),
    ('itau_seguros', 'Itaú Seguros'),
    ('mapfre', 'Mapfre'),
    ('zurich', 'Zurich'),
    ('hdi', 'HDI'),
    ('sompo', 'Sompo'),
    ('alfa', 'Alfa'),
    ('axa', 'AXA'),
    ('azul_seguros', 'Azul Seguros'), # Adicionando Azul Seguros, conforme solicitado anteriormente
    # Adicione mais seguradoras conforme necessário
]


# --- Modelo Veiculo ---
class Veiculo(models.Model):
    """
    Modelo para representar um veículo individual dentro da frota de uma empresa.
    Cada veículo é associado a uma empresa e contém detalhes sobre o veículo e seu seguro.
    """
    # Relacionamento com a Empresa (Chave Estrangeira)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='veiculos',
        verbose_name="Empresa Proprietária"
    )

    # Identificação Única do Veículo no Sistema
    numero_registro = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Número de Registro"
    )

    # Campo Marca: Agora usa 'choices' definidos acima (MARCA_CHOICES)
    marca = models.CharField(
        max_length=50,
        choices=MARCA_CHOICES, # <-- ESSENCIAL para o dropdown de MARCA
        verbose_name="Marca",
        help_text="Selecione a marca da montadora."
    )
    
    modelo = models.CharField(
        max_length=100,
        verbose_name="Modelo do Veículo"
    )
    placa = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Placa"
    )
    chassi = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="Chassi"
    )
    renavam = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="Renavam"
    )
    ano_fabricacao = models.IntegerField(
        verbose_name="Ano de Fabricação"
    )
    ano_modelo = models.IntegerField(
        verbose_name="Ano do Modelo"
    )
    zero_kilometro = models.BooleanField(
        default=False,
        verbose_name="Zero Quilômetro"
    )
    nome_condutor = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Nome do Condutor"
    )

    # Opções para a classe de bônus (0 a 10)
    class_bonus_choices = [(i, str(i)) for i in range(11)] 
    classe_bonus = models.IntegerField(
        choices=class_bonus_choices,
        default=0,
        verbose_name="Classe de Bônus"
    )
    
    # Campo Seguradora: Agora usa 'choices' definidos acima (SEGURADORA_CHOICES)
    seguradora = models.CharField(
        max_length=100,
        choices=SEGURADORA_CHOICES, # <-- ESSENCIAL para o dropdown de SEGURADORA
        verbose_name="Seguradora",
        help_text="Selecione a seguradora."
    )
    
    franquia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor da Franquia"
    )
    data_vencimento_seguro = models.DateField(
        verbose_name="Data de Vencimento do Seguro"
    )

    # Metadados do Registro
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro no Sistema"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo no Sistema"
    )

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['placa']

    def __str__(self):
        return f"{self.placa} - {self.modelo} ({self.empresa.razao_social})"