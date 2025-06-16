from rest_framework import serializers
from .models import Escola, Participante, Prova, GabaritoLido

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = ['id', 'codigo', 'nome']

class ParticipanteSerializer(serializers.ModelSerializer):
    escola = EscolaSerializer()
    class Meta:
        model = Participante
        fields = ['id', 'codigo', 'nome', 'escola']

class ProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prova
        fields = ['id', 'codigo', 'ano', 'nivel', 'fase']

class GabaritoLidoSerializer(serializers.ModelSerializer):
    participante = ParticipanteSerializer()
    prova = ProvaSerializer()
    class Meta:
        model = GabaritoLido
        fields = ['id', 'codigo', 'participante', 'prova', 'nota']
        