from django.shortcuts import render, redirect
from .models import Boi, ColetaSemen
from .forms import BoiForm, ColetaForm, FotoBoiForm, FotoBoi
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import date, timedelta
from .forms import BoiForm, ColetaForm, FotoBoiForm, SaidaSemenForm
from .models import Boi, ColetaSemen, FotoBoi, SaidaSemen, models
import pandas as pd
from django.contrib import messages

def lista_bois(request):
    search_query = request.GET.get('q')
    bois = Boi.objects.all()
    
    if search_query:
        bois = bois.filter(
            models.Q(nome__icontains=search_query) | 
            models.Q(brinco_id__icontains=search_query)
        )

    hoje = date.today()
    trinta_dias = hoje + timedelta(days=30) # Calcula a data de daqui a 30 dias

    # --- DADOS DO DASHBOARD ---
    total_bois_ativos = bois.filter(status='ativo').count()
    estoque_total_valido = 0
    
    alertas_estoque = []
    doses_vencendo = []
    
    for boi in bois:
        if boi.status not in ['obito', 'aposentado']:
            estoque_boi = 0
            
            for coleta in boi.coletas.all():
                # Ignora sêmen já vencido no cálculo total
                if coleta.data_validade and coleta.data_validade < hoje:
                    continue 
                
                estoque_boi += coleta.quantidade_doses
                estoque_total_valido += coleta.quantidade_doses

                # Verifica se o lote tem estoque E vai vencer nos próximos 30 dias
                if coleta.quantidade_doses > 0 and coleta.data_validade and hoje <= coleta.data_validade <= trinta_dias:
                    doses_vencendo.append({
                        'boi': boi.nome,
                        'doses': coleta.quantidade_doses,
                        'vencimento': coleta.data_validade
                    })
            
            # Alerta de estoque crítico
            if estoque_boi < 2:
                alertas_estoque.append(f"{boi.nome} (ID: {boi.brinco_id}) - Apenas {estoque_boi} dose(s)")
    # --------------------------

    return render(request, 'veterinaria/lista_bois.html', {
        'bois': bois, 
        'search_query': search_query,
        'total_bois_ativos': total_bois_ativos,
        'estoque_total_valido': estoque_total_valido,
        'alertas_estoque': alertas_estoque,
        'doses_vencendo': doses_vencendo
    })

def registrar_inseminacao(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    hoje = date.today()
    
    if request.method == 'POST':
        # Busca coletas do boi que tenham mais de 0 doses
        # E exclui as que estão com a validade menor que hoje (vencidas)
        coletas_validas = boi.coletas.filter(quantidade_doses__gt=0).exclude(data_validade__lt=hoje)
        
        if coletas_validas.exists():
            # Pega a coleta válida mais antiga (para usar o sêmen mais velho primeiro)
            coleta_usar = coletas_validas.order_by('data_validade').first()
            
            # Desconta 1 dose e salva no banco
            coleta_usar.quantidade_doses -= 1
            coleta_usar.save()
            
    # Redireciona de volta para os detalhes do boi
    return redirect('detalhes_boi', pk=pk)

def criar_boi(request):
    if request.method == 'POST':
        # Se o usuário enviou dados, preenchemos o formulário com eles
        form = BoiForm(request.POST)
        if form.is_valid(): # Verifica se os dados estão corretos (ex: brinco_id não está duplicado)
            form.save() # Salva no banco de dados
            return redirect('lista_bois') # Redireciona de volta para a tela inicial
    else:
        # Se for só um acesso normal à página, cria um formulário vazio
        form = BoiForm()

    # Envia o formulário para o template HTML
    return render(request, 'veterinaria/criar_boi.html', {'form': form})

def detalhes_boi(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    
    # Pegamos apenas as 5 últimas coletas (ordenadas da mais nova para a mais velha)
    coletas_recentes = boi.coletas.all().order_by('-data_coleta')[:5]
    
    # Pegamos apenas as 5 últimas saídas
    saidas_recentes = SaidaSemen.objects.filter(coleta__boi=boi).order_by('-data_saida')[:5]
    
    return render(request, 'veterinaria/detalhes_boi.html', {
        'boi': boi, 
        'coletas': coletas_recentes, 
        'saidas': saidas_recentes
    })

def editar_boi(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    
    if request.method == 'POST':
        # Aqui a mágica acontece: passamos o 'instance=boi' para o formulário saber que 
        # estamos atualizando um boi existente, e não criando um novo.
        form = BoiForm(request.POST, instance=boi)
        if form.is_valid():
            form.save()
            return redirect('detalhes_boi', pk=boi.pk) # Volta para a tela de detalhes dele
    else:
        # Carrega o formulário já preenchido com os dados atuais do boi
        form = BoiForm(instance=boi)

    return render(request, 'veterinaria/editar_boi.html', {'form': form, 'boi': boi})


def deletar_boi(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    
    if request.method == 'POST':
        # Se o usuário confirmou na tela, nós deletamos e voltamos para a lista principal
        boi.delete()
        return redirect('lista_bois')
        
    # Se ele só acessou o link, mostramos a tela perguntando "Tem certeza?"
    return render(request, 'veterinaria/confirmar_delecao.html', {'boi': boi})

def registrar_coleta(request, pk):
    # Buscamos o boi específico
    boi = get_object_or_404(Boi, pk=pk)
    
    if request.method == 'POST':
        form = ColetaForm(request.POST)
        if form.is_valid():
            # commit=False salva os dados na memória, mas não envia pro banco ainda
            coleta = form.save(commit=False)
            coleta.boi = boi # Preenchemos o campo "boi" que estava faltando
            coleta.save() # Agora sim salvamos no banco!
            return redirect('detalhes_boi', pk=boi.pk)
    else:
        form = ColetaForm()
        
    return render(request, 'veterinaria/registrar_coleta.html', {'form': form, 'boi': boi})

def adicionar_foto(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    
    if request.method == 'POST':
        # IMPORTANTE: Passamos request.POST E request.FILES
        form = FotoBoiForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.boi = boi # Vincula a foto ao boi atual
            foto.save()
            return redirect('detalhes_boi', pk=boi.pk)
    else:
        form = FotoBoiForm()
        
    return render(request, 'veterinaria/adicionar_foto.html', {'form': form, 'boi': boi})

# ... (suas importações e views anteriores continuam aqui) ...

def deletar_foto(request, pk_boi, pk_foto):
    # Busca a foto específica ou retorna 404
    foto = get_object_or_404(FotoBoi, pk=pk_foto)
    
    # Se for uma confirmação de POST, deletamos a foto
    if request.method == 'POST':
        foto.delete()
        # Após deletar, volta para a tela de detalhes do boi
        return redirect('detalhes_boi', pk=pk_boi)
        
    # Se for um GET, mostramos uma tela de confirmação
    # (reaproveitaremos a mesma lógica do confirmar_delecao.html do boi)
    return render(request, 'veterinaria/confirmar_delecao_foto.html', {'foto': foto, 'pk_boi': pk_boi})

def registrar_saida(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    
    if request.method == 'POST':
        form = SaidaSemenForm(request.POST, boi_id=boi.pk)
        if form.is_valid():
            saida = form.save(commit=False)
            coleta = saida.coleta
            
            # Validação extra: garantir que não retiram mais doses do que o stock existente
            if saida.quantidade <= coleta.quantidade_doses:
                # Desconta o stock da coleta e guarda na base de dados
                coleta.quantidade_doses -= saida.quantidade
                coleta.save()
                saida.save() # Guarda o registo da saída
                return redirect('detalhes_boi', pk=boi.pk)
            else:
                form.add_error('quantidade', f'Erro: Tentou retirar {saida.quantidade} doses, mas este lote só tem {coleta.quantidade_doses}.')
    else:
        form = SaidaSemenForm(boi_id=boi.pk)
        
    return render(request, 'veterinaria/registrar_saida.html', {'form': form, 'boi': boi})

def relatorio_boi(request, pk):
    boi = get_object_or_404(Boi, pk=pk)
    
    # Aqui pegamos TUDO (sem o [:5]) para o relatório completo
    todas_coletas = boi.coletas.all().order_by('-data_coleta')
    todas_saidas = SaidaSemen.objects.filter(coleta__boi=boi).order_by('-data_saida')
    
    return render(request, 'veterinaria/relatorio_boi.html', {
        'boi': boi,
        'coletas': todas_coletas,
        'saidas': todas_saidas
    })

import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect

def importar_bois(request):
    if request.method == 'POST' and request.FILES.get('arquivo_excel'):
        arquivo = request.FILES['arquivo_excel']
        
        try:
            # O Pandas lê o arquivo Excel
            df = pd.read_excel(arquivo)
            
            bois_criados = 0
            bois_ignorados = 0

            # Percorre cada linha da planilha
            for index, row in df.iterrows():
                # Campos de Texto (se for NaN/vazio, transforma em string vazia)
                nome = str(row.get('Nome', '')).strip()
                brinco = str(row.get('Brinco', '')).strip()
                
                # Se a linha estiver completamente vazia de nome/brinco, pula
                if nome == 'nan' or not nome or brinco == 'nan' or not brinco:
                    continue

                raca = str(row.get('Raça', '')).strip()
                raca = '' if raca == 'nan' else raca
                
                registro = str(row.get('Registro', '')).strip()
                registro = '' if registro == 'nan' else registro
                
                localizacao = str(row.get('Localização', '')).strip()
                localizacao = '' if localizacao == 'nan' else localizacao

                status = str(row.get('Status', 'ativo')).lower().strip()
                if status not in ['ativo', 'descanso', 'aposentado', 'obito']:
                    status = 'ativo'

                # Tratamento seguro para Data de Nascimento
                nascimento_raw = row.get('Nascimento')
                data_nascimento = None
                if pd.notna(nascimento_raw):
                    try:
                        data_nascimento = pd.to_datetime(nascimento_raw).date()
                    except:
                        pass # Se digitar texto em vez de data, ignora

                # Tratamento seguro para Números (Peso e Circunferência)
                peso_raw = row.get('Peso')
                try:
                    peso = float(peso_raw) if pd.notna(peso_raw) else None
                except ValueError:
                    peso = None

                circ_raw = row.get('Circunferência Escrotal')
                try:
                    circunferencia = float(circ_raw) if pd.notna(circ_raw) else None
                except ValueError:
                    circunferencia = None

                # Cadastra no banco de dados
                if not Boi.objects.filter(brinco_id=brinco).exists():
                    Boi.objects.create(
                        nome=nome,
                        brinco_id=brinco,
                        raca=raca,
                        registro_genealogico=registro,
                        localizacao=localizacao,
                        status=status,
                        data_nascimento=data_nascimento,
                        peso=peso,
                        circunferencia_escrotal=circunferencia
                    )
                    bois_criados += 1
                else:
                    bois_ignorados += 1
            
            messages.success(request, f'Importação concluída! {bois_criados} bois cadastrados e {bois_ignorados} ignorados (já existiam).')
            return redirect('lista_bois')

        except Exception as e:
            messages.error(request, f'Erro ao ler a planilha: {e}. Verifique se o formato está correto.')
            return redirect('importar_bois')

    return render(request, 'veterinaria/importar_bois.html')