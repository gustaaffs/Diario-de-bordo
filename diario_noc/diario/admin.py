from django.contrib import admin
from .models import EntradaDiario

@admin.register(EntradaDiario)
class EntradaDiarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'autor', 'data_criacao')
    search_fields = ('titulo', 'conteudo')
    list_filter = ('tipo', 'data_criacao')