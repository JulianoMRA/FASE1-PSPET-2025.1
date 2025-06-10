from django.contrib import admin
from .models import Escola, Participante, Prova

# Este arquivo registra os modelos do Django no painel de administração.
# Isso permite que os modelos sejam gerenciados através da interface administrativa do Django.

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id_participante', 'nome', 'escola')
    search_fields = ('nome', 'id_participante')
    list_filter = ('escola',)

@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ('id_prova', 'gabarito')
    search_fields = ('id_prova',)
