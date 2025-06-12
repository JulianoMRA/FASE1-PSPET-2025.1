from django.contrib import admin
from .models import Escola, Participante, Prova, GabaritoLido

# Este arquivo registra os modelos do Django no painel de administração.
# Isso permite que os modelos sejam gerenciados através da interface administrativa do Django.

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'escola')
    search_fields = ('nome', 'id_participante')
    list_filter = ('escola',)

@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_prova', 'ano', 'nivel', 'fase', 'gabarito')
    search_fields = ('id',)

@admin.register(GabaritoLido)
class GabaritoLidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'participante', 'prova', 'gabarito_lido', 'nota')
    search_fields = ('gabarito_lido',)
