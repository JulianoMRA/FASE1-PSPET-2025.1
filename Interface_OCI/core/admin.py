from django.contrib import admin
from .models import Escola, Participante, Prova, GabaritoLido

# =========================
# Configuração do Django Admin para cada modelo
# =========================

# Administração de Escola
@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nome')
    search_fields = ('nome', 'codigo')
    list_filter = ('codigo',)
    ordering = ('codigo',)

# Administração de Participante
@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nome', 'escola')
    search_fields = ('nome', 'codigo')
    list_filter = ('escola', 'codigo')
    ordering = ('codigo',)

# Administração de Prova
@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'ano', 'nivel', 'fase', 'gabarito')
    search_fields = ('id_prova', 'codigo')
    list_filter = ('codigo', 'ano', 'nivel', 'fase')
    ordering = ('codigo',)

# Administração de Gabarito Lido
@admin.register(GabaritoLido)
class GabaritoLidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'user', 'participante', 'prova', 'gabarito_lido', 'nota')
    search_fields = ('gabarito_lido', 'codigo')
    list_filter = ('codigo', 'user', 'prova')
    ordering = ('codigo',)

# Fim do arquivo de administração
