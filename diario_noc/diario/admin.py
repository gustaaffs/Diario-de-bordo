from django.contrib import admin
from .models import EntradaDiario, AuditoriaEntrada, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(EntradaDiario)
class EntradaDiarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'autor', 'data_criacao')
    search_fields = ('titulo', 'conteudo')
    list_filter = ('tipo', 'data_criacao')


@admin.register(AuditoriaEntrada)
class AuditoriaEntradaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'entrada', 'data')
    search_fields = ('detalhes',)
    list_filter = ('acao', 'usuario', 'data')