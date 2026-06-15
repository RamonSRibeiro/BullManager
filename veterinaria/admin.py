from django.contrib import admin
from .models import Boi, FotoBoi, ColetaSemen, SaidaSemen


class FotoBoiInline(admin.TabularInline):
    model = FotoBoi
    extra = 0
    readonly_fields = ('imagem',)


class ColetaSemenInline(admin.TabularInline):
    model = ColetaSemen
    extra = 0
    fields = ('lote', 'data_coleta', 'quantidade_doses', 'data_validade', 'motilidade', 'vigor')
    readonly_fields = ('lote',)


@admin.register(Boi)
class BoiAdmin(admin.ModelAdmin):
    list_display = ('nome', 'brinco_id', 'raca', 'status', 'localizacao', 'data_cadastro')
    list_filter = ('status', 'raca')
    search_fields = ('nome', 'brinco_id', 'registro_genealogico')
    ordering = ('nome',)
    inlines = [FotoBoiInline, ColetaSemenInline]


class SaidaSemenInline(admin.TabularInline):
    model = SaidaSemen
    extra = 0
    fields = ('data_saida', 'quantidade', 'motivo', 'destino')


@admin.register(ColetaSemen)
class ColetaSemenAdmin(admin.ModelAdmin):
    list_display = ('lote', 'boi', 'data_coleta', 'quantidade_doses', 'data_validade', 'motilidade', 'vigor')
    list_filter = ('boi', 'data_coleta')
    search_fields = ('lote', 'boi__nome', 'boi__brinco_id')
    ordering = ('-data_coleta',)
    readonly_fields = ('lote',)
    inlines = [SaidaSemenInline]


@admin.register(SaidaSemen)
class SaidaSemenAdmin(admin.ModelAdmin):
    list_display = ('coleta', 'data_saida', 'quantidade', 'motivo', 'destino')
    list_filter = ('motivo', 'data_saida')
    search_fields = ('coleta__lote', 'coleta__boi__nome', 'destino')
    ordering = ('-data_saida',)


@admin.register(FotoBoi)
class FotoBoiAdmin(admin.ModelAdmin):
    list_display = ('boi', 'imagem')
    search_fields = ('boi__nome',)
