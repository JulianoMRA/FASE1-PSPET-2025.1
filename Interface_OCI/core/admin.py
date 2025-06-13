from django.contrib import admin
from .models import Escola, Participante, Prova, GabaritoLido

# =========================
# Configuração do Django Admin para cada modelo
# =========================

# Administração de Escola
@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# Administração de Participante
@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'escola')
    search_fields = ('nome',)
    list_filter = ('escola',)

# Administração de Prova
@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_prova', 'ano', 'nivel', 'fase', 'gabarito')
    search_fields = ('id_prova',)

# Administração de Gabarito Lido
@admin.register(GabaritoLido)
class GabaritoLidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'participante', 'prova', 'gabarito_lido', 'nota')
    search_fields = ('gabarito_lido',)

# Fim do arquivo de administração
