from rest_framework import serializers
from .models import Escola, Participante, Prova, GabaritoLido

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'

class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'

class ProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prova
        fields = '__all__'

class GabaritoLidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GabaritoLido
        fields = '__all__'
        