from django.contrib import admin
from .models import Escola, Participante, Prova

# Register your models here.
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('id_participante', 'nome', 'escola')
    search_fields = ('nome', 'id_participante')
    list_filter = ('escola',)

class ProvaAdmin(admin.ModelAdmin):
    list_display = ('id_prova', 'gabarito')
    search_fields = ('id_prova')
