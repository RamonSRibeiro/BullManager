"""
seed_data.py — Insere 5 touros com situações distintas para teste.

Como usar:
    python manage.py shell < seed_data.py
    
    ou via runscript se tiver django-extensions:
    python manage.py runscript seed_data
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from datetime import date
from veterinaria.models import Boi, ColetaSemen, SaidaSemen

print("=" * 55)
print("  Iniciando inserção de dados de teste...")
print("=" * 55)

# ---------------------------------------------------------------
# Touro 1 — ATIVO, estoque alto, coletas recentes
# Situação ideal: em plena produção, tudo ok
# ---------------------------------------------------------------
boi1, criado = Boi.objects.get_or_create(
    brinco_id='BTB-001',
    defaults=dict(
        nome='Imperador da Serra',
        raca='Nelore',
        data_nascimento=date(2019, 3, 15),
        registro_genealogico='ABCZ-00123',
        circunferencia_escrotal=42.5,
        peso=980.0,
        data_exame_andrologico=date(2026, 1, 10),
        status='ativo',
        localizacao='Piquete 01 - Reprodutores',
        descricao='Touro elite, aprovado no exame andrológico com classificação Apto. Alto potencial genético.',
    )
)
if criado:
    # Coleta 1 — recente, bom estoque, longe do vencimento
    c1a = ColetaSemen.objects.create(
        boi=boi1,
        data_coleta=date(2026, 4, 10),
        motilidade=85,
        vigor=4,
        motilidade_pos=72,
        vigor_pos=4,
        quantidade_doses=120,
        data_validade=date(2028, 4, 10),
        observacoes='Coleta excelente. Morfologia 92% normais.',
    )
    # Coleta 2 — coleta anterior com algumas saídas já registradas
    c1b = ColetaSemen.objects.create(
        boi=boi1,
        data_coleta=date(2025, 11, 20),
        motilidade=80,
        vigor=4,
        motilidade_pos=68,
        vigor_pos=3,
        quantidade_doses=45,
        data_validade=date(2027, 11, 20),
    )
    SaidaSemen.objects.create(
        coleta=c1b,
        data_saida=date(2026, 2, 5),
        quantidade=30,
        motivo='venda',
        destino='Fazenda Boa Vista - Botijão 02',
        observacoes='Venda para programa de melhoramento genético.',
    )
    SaidaSemen.objects.create(
        coleta=c1b,
        data_saida=date(2026, 3, 18),
        quantidade=10,
        motivo='inseminacao',
        destino='Lote Matrizes A - Curral Central',
    )
    print(f"[OK] Touro 1 criado: {boi1.nome} — Ativo, estoque alto")
else:
    print(f"[--] Touro 1 já existe: {boi1.nome}")

# ---------------------------------------------------------------
# Touro 2 — ATIVO, estoque CRÍTICO (menos de 2 doses)
# Situação de alerta: precisa de nova coleta urgente
# ---------------------------------------------------------------
boi2, criado = Boi.objects.get_or_create(
    brinco_id='BTB-002',
    defaults=dict(
        nome='Furacão do Vale',
        raca='Angus',
        data_nascimento=date(2020, 7, 22),
        registro_genealogico='ABBA-00456',
        circunferencia_escrotal=39.0,
        peso=870.0,
        data_exame_andrologico=date(2025, 8, 5),
        status='ativo',
        localizacao='Piquete 02 - Reprodutores',
        descricao='Touro de corte com DEPs de destaque para ganho de peso.',
    )
)
if criado:
    # Coleta quase zerada — vai disparar o alerta de estoque crítico
    c2 = ColetaSemen.objects.create(
        boi=boi2,
        data_coleta=date(2025, 9, 14),
        motilidade=78,
        vigor=3,
        motilidade_pos=60,
        vigor_pos=3,
        quantidade_doses=1,
        data_validade=date(2027, 9, 14),
        observacoes='Estoque crítico. Agendar nova coleta.',
    )
    print(f"[OK] Touro 2 criado: {boi2.nome} — Ativo, estoque CRÍTICO")
else:
    print(f"[--] Touro 2 já existe: {boi2.nome}")

# ---------------------------------------------------------------
# Touro 3 — ATIVO, lote com validade vencendo em menos de 30 dias
# Situação de alerta: doses prestes a vencer
# ---------------------------------------------------------------
boi3, criado = Boi.objects.get_or_create(
    brinco_id='BTB-003',
    defaults=dict(
        nome='Trovão Dourado',
        raca='Brahman',
        data_nascimento=date(2018, 5, 3),
        registro_genealogico='ABCB-00789',
        circunferencia_escrotal=44.0,
        peso=1050.0,
        data_exame_andrologico=date(2026, 2, 20),
        status='ativo',
        localizacao='Piquete 01 - Reprodutores',
        descricao='Touro zebuíno de alto padrão. Excelente adaptação ao clima tropical.',
    )
)
if criado:
    # Lote com bom estoque mas vencendo em ~15 dias a partir de hoje
    from datetime import timedelta
    vencimento_proximo = date.today() + timedelta(days=15)
    c3 = ColetaSemen.objects.create(
        boi=boi3,
        data_coleta=date(2024, 6, 20),
        motilidade=82,
        vigor=4,
        motilidade_pos=70,
        vigor_pos=3,
        quantidade_doses=35,
        data_validade=vencimento_proximo,
        observacoes=f'ATENÇÃO: lote vence em 15 dias ({vencimento_proximo}). Priorizar uso.',
    )
    print(f"[OK] Touro 3 criado: {boi3.nome} — Ativo, lote vencendo em 15 dias")
else:
    print(f"[--] Touro 3 já existe: {boi3.nome}")

# ---------------------------------------------------------------
# Touro 4 — EM DESCANSO, histórico de coletas com descarte
# Situação: afastado temporariamente após exame
# ---------------------------------------------------------------
boi4, criado = Boi.objects.get_or_create(
    brinco_id='BTB-004',
    defaults=dict(
        nome='Rei das Gerais',
        raca='Senepol',
        data_nascimento=date(2017, 11, 9),
        registro_genealogico='ABCS-00321',
        circunferencia_escrotal=38.5,
        peso=920.0,
        data_exame_andrologico=date(2026, 3, 1),
        status='descanso',
        localizacao='Pasto de Descanso - Gleba B',
        descricao='Em período de recuperação após diagnóstico de degeneração testicular leve. Reavaliação prevista para 90 dias.',
    )
)
if criado:
    # Coleta antiga com boa quantidade
    c4a = ColetaSemen.objects.create(
        boi=boi4,
        data_coleta=date(2025, 6, 10),
        motilidade=75,
        vigor=3,
        motilidade_pos=58,
        vigor_pos=3,
        quantidade_doses=60,
        data_validade=date(2027, 6, 10),
    )
    # Coleta mais recente com qualidade ruim — descartada
    c4b = ColetaSemen.objects.create(
        boi=boi4,
        data_coleta=date(2026, 3, 1),
        motilidade=35,
        vigor=2,
        motilidade_pos=20,
        vigor_pos=1,
        quantidade_doses=0,
        data_validade=date(2028, 3, 1),
        observacoes='Coleta descartada — parâmetros abaixo do padrão CBRA. Motivo do afastamento.',
    )
    SaidaSemen.objects.create(
        coleta=c4a,
        data_saida=date(2025, 10, 12),
        quantidade=15,
        motivo='inseminacao',
        destino='Lote Matrizes C - Pasto Norte',
    )
    print(f"[OK] Touro 4 criado: {boi4.nome} — Em descanso, coleta descartada")
else:
    print(f"[--] Touro 4 já existe: {boi4.nome}")

# ---------------------------------------------------------------
# Touro 5 — APOSENTADO, sem coletas ativas, apenas histórico
# Situação: animal ainda no plantel mas fora de produção
# ---------------------------------------------------------------
boi5, criado = Boi.objects.get_or_create(
    brinco_id='BTB-005',
    defaults=dict(
        nome='Pioneiro JBS',
        raca='Simmental',
        data_nascimento=date(2012, 2, 28),
        registro_genealogico='ABSS-00654',
        circunferencia_escrotal=36.0,
        peso=1120.0,
        data_exame_andrologico=date(2024, 6, 15),
        status='aposentado',
        localizacao='Pasto de Aposentados - Gleba A',
        descricao='Animal aposentado após 10 anos de serviço. Mantido no plantel por valor histórico e genético. Mais de 2.000 doses produzidas ao longo da vida.',
    )
)
if criado:
    # Histórico de coletas antigas — todas zeradas (estoque esgotado ao longo dos anos)
    c5a = ColetaSemen.objects.create(
        boi=boi5,
        data_coleta=date(2023, 3, 8),
        motilidade=65,
        vigor=3,
        motilidade_pos=50,
        vigor_pos=2,
        quantidade_doses=0,
        data_validade=date(2025, 3, 8),
        observacoes='Última coleta antes da aposentadoria. Qualidade reduzida pela idade.',
    )
    SaidaSemen.objects.create(
        coleta=c5a,
        data_saida=date(2023, 5, 20),
        quantidade=80,
        motivo='venda',
        destino='Central de Reprodução Minas Sul Ltda.',
        observacoes='Venda do estoque remanescente.',
    )
    print(f"[OK] Touro 5 criado: {boi5.nome} — Aposentado, estoque zerado")
else:
    print(f"[--] Touro 5 já existe: {boi5.nome}")

# ---------------------------------------------------------------
# Resumo final
# ---------------------------------------------------------------
print()
print("=" * 55)
print(f"  Total de touros no banco: {Boi.objects.count()}")
print(f"  Total de coletas:         {ColetaSemen.objects.count()}")
print(f"  Total de saídas:          {SaidaSemen.objects.count()}")
print("=" * 55)
print("  Pronto! Acesse http://127.0.0.1:8000 para ver.")
print("=" * 55)
