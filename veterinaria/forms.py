from django import forms
from .models import Boi, ColetaSemen, FotoBoi, SaidaSemen

class SaidaSemenForm(forms.ModelForm):
    class Meta:
        model = SaidaSemen
        fields = ['coleta', 'data_saida', 'quantidade', 'motivo', 'destino', 'observacoes']
        widgets = {
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 2}),
        }

    # Esta função permite-nos filtrar as coletas na caixa de seleção
    def __init__(self, *args, **kwargs):
        boi_id = kwargs.pop('boi_id', None) # Recebemos o ID do boi da view
        super().__init__(*args, **kwargs)
        
        if boi_id:
            # Mostra apenas coletas deste boi que tenham mais de 0 doses
            self.fields['coleta'].queryset = ColetaSemen.objects.filter(boi_id=boi_id, quantidade_doses__gt=0)
            # Formata o texto que aparece na caixa de seleção para facilitar a vida ao operador
            self.fields['coleta'].label_from_instance = lambda obj: f"Lote {obj.lote} | Estoque: {obj.quantidade_doses} doses"

class BoiForm(forms.ModelForm):
    class Meta:
        model = Boi
        # Adicionamos os novos campos na lista
        fields = [
            'nome', 'brinco_id', 'raca', 'registro_genealogico', 'data_nascimento', 
            'peso', 'circunferencia_escrotal', 'data_exame_andrologico', 
            'status', 'localizacao', 'descricao'
        ]
        
        # Colocamos o calendário bonitinho para as novas datas
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_exame_andrologico': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class ColetaForm(forms.ModelForm):
    class Meta:
        model = ColetaSemen
        # Note que não colocamos o "boi" aqui, pois o sistema vai preencher isso automaticamente
        fields = ['data_coleta', 'motilidade', 'vigor', 'motilidade_pos', 'vigor_pos', 'quantidade_doses', 'data_validade', 'observacoes']
        
        # O widget 'type': 'date' faz o navegador mostrar aquele calendário bonitinho
        widgets = {
            'data_coleta': forms.DateInput(attrs={'type': 'date'}),
            'data_validade': forms.DateInput(attrs={'type': 'date'}),
        }

class FotoBoiForm(forms.ModelForm):
    class Meta:
        model = FotoBoi
        # O campo 'boi' será preenchido automaticamente na view,
        # então só mostramos o campo para fazer o upload da imagem.
        fields = ['imagem']