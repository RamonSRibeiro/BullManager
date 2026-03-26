from django.db import models
from datetime import date
import uuid

class Boi(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo (Em Coleta)'),
        ('descanso', 'Em Descanso'),
        ('aposentado', 'Aposentado'),
        ('obito', 'Óbito'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do Boi")
    brinco_id = models.CharField(max_length=50, unique=True, verbose_name="ID/Brinco")
    
    raca = models.CharField(max_length=50, blank=True, null=True, verbose_name="Raça")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    registro_genealogico = models.CharField(max_length=50, blank=True, null=True, verbose_name="Registro (Pedigree)")
    
    circunferencia_escrotal = models.FloatField(blank=True, null=True, verbose_name="Circunferência Escrotal (cm)")
    peso = models.FloatField(blank=True, null=True, verbose_name="Peso Atual (kg)")
    data_exame_andrologico = models.DateField(blank=True, null=True, verbose_name="Último Exame Andrológico")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo', verbose_name="Status")
    localizacao = models.CharField(max_length=100, blank=True, null=True, verbose_name="Localização/Lote")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} (ID: {self.brinco_id})"


class FotoBoi(models.Model):
    # Relacionamento 1 para N: Um boi pode ter várias fotos
    boi = models.ForeignKey(Boi, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='fotos_bois/')
    
    def __str__(self):
        return f"Foto de {self.boi.nome}"


class ColetaSemen(models.Model):
    boi = models.ForeignKey(Boi, related_name='coletas', on_delete=models.CASCADE)
    
    # --- RASTREABILIDADE ---
    lote = models.CharField(max_length=30, unique=True, blank=True, verbose_name="Código do Lote")
    data_coleta = models.DateField(verbose_name="Data da Coleta")
    
    # --- DADOS LABORATORIAIS (Padrão CBRA) ---
    motilidade = models.IntegerField(verbose_name="Motilidade Progressiva (%)", help_text="Ex: 80")
    vigor = models.IntegerField(verbose_name="Vigor (0 a 5)", help_text="Ex: 4")
    
    motilidade_pos = models.IntegerField(verbose_name="Motilidade Pós-Descongelamento (%)", blank=True, null=True)
    vigor_pos = models.IntegerField(verbose_name="Vigor Pós-Descongelamento (0 a 5)", blank=True, null=True)
    
    # --- ESTOQUE E VALIDADE ---
    quantidade_doses = models.IntegerField(verbose_name="Quantidade em Estoque (Doses/Palhetas)", default=0)
    data_validade = models.DateField(verbose_name="Data de Validade", blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    @property
    def is_vencida(self):
        if self.data_validade and self.data_validade < date.today():
            return True
        return False

    def save(self, *args, **kwargs):
        # Se o lote estiver vazio (nova coleta), gera um código único automático
        if not self.lote:
            # Pega a data (ex: 20260318) e junta com 4 letras/números aleatórios
            data_str = self.data_coleta.strftime('%Y%m%d') if self.data_coleta else date.today().strftime('%Y%m%d')
            codigo_aleatorio = uuid.uuid4().hex[:4].upper()
            self.lote = f"L-{data_str}-{codigo_aleatorio}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lote {self.lote} - {self.boi.nome} - Estoque: {self.quantidade_doses}"

class SaidaSemen(models.Model):
    MOTIVOS_CHOICES = [
        ('inseminacao', 'Uso Próprio (Inseminação)'),
        ('venda', 'Venda para Terceiros'),
        ('descarte', 'Descarte/Perda'),
    ]

    coleta = models.ForeignKey(ColetaSemen, related_name='saidas', on_delete=models.CASCADE)
    data_saida = models.DateField(default=date.today, verbose_name="Data da Saída")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade de Doses")
    motivo = models.CharField(max_length=20, choices=MOTIVOS_CHOICES, verbose_name="Motivo da Saída")
    
    # Transformamos o destino em OBRIGATÓRIO (retiramos o blank=True, null=True)
    destino = models.CharField(max_length=150, verbose_name="Destino / Transporte (Ex: Botijão 04 - Fazenda X)")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"{self.quantidade} doses - {self.get_motivo_display()}"