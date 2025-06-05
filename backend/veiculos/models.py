# backend/veiculos/models.py

from django.db import models # Importa o módulo models do Django para definir modelos de banco de dados

class Empresa(models.Model):
    """
    Modelo para representar as empresas/clientes da corretora.
    Cada empresa pode ter uma ou mais frotas de veículos associadas.
    """
    razao_social = models.CharField(
        max_length=200,  # Define o tamanho máximo para o campo de texto
        unique=True,     # Garante que não haverá duas empresas com a mesma razão social
        verbose_name="Razão Social" # Nome amigável para exibição no painel administrativo
    )
    cnpj = models.CharField(
        max_length=18,   # Tamanho para CNPJ (XX.XXX.XXX/YYYY-ZZ)
        unique=True,     # Garante que cada CNPJ seja único no sistema
        verbose_name="CNPJ"
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True, # Preenche automaticamente com a data e hora da criação do registro
        verbose_name="Data de Cadastro"
    )

    class Meta:
        """
        Classe Meta interna para definir metadados do modelo.
        """
        verbose_name = "Empresa"        # Nome singular para exibição no painel administrativo
        verbose_name_plural = "Empresas" # Nome plural para exibição
        ordering = ['razao_social']     # Ordena os registros por razão social por padrão

    def __str__(self):
        """
        Método que retorna uma representação em string do objeto.
        É o que será exibido no painel administrativo do Django e em logs.
        """
        return self.razao_social
    
    # backend/veiculos/models.py

from django.db import models # Importa o módulo models do Django para definir modelos de banco de dados
import uuid # Importa o módulo UUID para gerar números de registro únicos

# --- Modelo Empresa (já existente) ---
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

# --- Novo Modelo Veiculo ---
class Veiculo(models.Model):
    """
    Modelo para representar um veículo individual dentro da frota de uma empresa.
    Cada veículo é associado a uma empresa e contém detalhes sobre o veículo e seu seguro.
    """
    # Relacionamento com a Empresa (Chave Estrangeira)
    empresa = models.ForeignKey(
        Empresa,           # Indica que este campo se relaciona com o modelo Empresa
        on_delete=models.CASCADE, # Se a empresa for excluída, todos os seus veículos também serão (ou mudar para SET_NULL, PROTECT dependendo da regra de negócio)
        related_name='veiculos', # Nome inverso para acessar os veículos a partir de uma empresa (ex: empresa.veiculos.all())
        verbose_name="Empresa Proprietária"
    )

    # Identificação Única do Veículo no Sistema
    numero_registro = models.UUIDField(
        default=uuid.uuid4, # Gera um UUID (Universal Unique Identifier) único por padrão
        unique=True,        # Garante que cada número de registro seja único
        editable=False,     # Não permite edição após a criação
        verbose_name="Número de Registro"
    )

    # Dados Básicos do Veículo
    marca = models.CharField(
        max_length=50,
        verbose_name="Marca",
        help_text="Ex: Fiat, Chevrolet, Volkswagen" # Ajuda para o usuário no painel administrativo
    )
    modelo = models.CharField(
        max_length=100,
        verbose_name="Modelo do Veículo"
    )
    placa = models.CharField(
        max_length=10, # Considerando formatos de placa atuais e futuros
        unique=True,   # Placa deve ser única para evitar duplicidade de veículos
        verbose_name="Placa"
    )
    chassi = models.CharField(
        max_length=17, # Chassi padrão tem 17 caracteres
        unique=True,   # Chassi é um identificador único global
        verbose_name="Chassi"
    )
    renavam = models.CharField(
        max_length=11, # Renavam padrão tem 11 dígitos
        unique=True,   # Renavam também é único
        verbose_name="Renavam"
    )
    ano_fabricacao = models.IntegerField(
        verbose_name="Ano de Fabricação"
    )
    ano_modelo = models.IntegerField(
        verbose_name="Ano do Modelo"
    )
    zero_kilometro = models.BooleanField(
        default=False, # Valor padrão é False (não é zero km)
        verbose_name="Zero Quilômetro"
    )
    nome_condutor = models.CharField(
        max_length=150,
        blank=True,    # Permite que o campo seja vazio
        null=True,     # Permite que o campo seja NULL no banco de dados
        verbose_name="Nome do Condutor"
    )

    # Dados do Seguro
    class_bonus_choices = [(i, str(i)) for i in range(11)] # Cria escolhas de 0 a 10
    classe_bonus = models.IntegerField(
        choices=class_bonus_choices, # Usa as escolhas definidas
        default=0,                   # Valor padrão para classe de bônus
        verbose_name="Classe de Bônus"
    )
    seguradora = models.CharField(
        max_length=100,
        verbose_name="Seguradora",
        help_text="Ex: Porto Seguro, Tokio Marine, Azul Seguros"
    )
    franquia = models.DecimalField(
        max_digits=10,    # Total de dígitos (ex: 99999999.99)
        decimal_places=2, # Número de casas decimais
        verbose_name="Valor da Franquia"
    )
    data_vencimento_seguro = models.DateField(
        verbose_name="Data de Vencimento do Seguro"
    )

    # Metadados do Registro
    data_cadastro = models.DateTimeField(
        auto_now_add=True, # Preenche automaticamente com a data e hora da criação
        verbose_name="Data de Cadastro no Sistema"
    )
    ativo = models.BooleanField(
        default=True, # Por padrão, o veículo é considerado ativo
        verbose_name="Ativo no Sistema"
    )

    class Meta:
        """
        Classe Meta interna para definir metadados do modelo.
        """
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['placa'] # Ordena os veículos pela placa por padrão

    def __str__(self):
        """
        Método que retorna uma representação em string do objeto Veiculo.
        Útil para exibição no painel administrativo e em logs.
        """
        return f"{self.placa} - {self.modelo} ({self.empresa.razao_social})"