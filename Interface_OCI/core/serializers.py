from rest_framework import serializers
from .models import Escola, Participante, Prova, GabaritoLido

# Serializador para o modelo Escola
class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = ['id', 'codigo', 'nome']  # Campos expostos na API

# Serializador para o modelo Participante, incluindo dados da escola relacionada
class ParticipanteSerializer(serializers.ModelSerializer):
    escola = EscolaSerializer()  # Serializa o objeto Escola relacionado
    class Meta:
        model = Participante
        fields = ['id', 'codigo', 'nome', 'escola']

# Serializador para o modelo Prova
class ProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prova
        fields = ['id', 'codigo', 'ano', 'nivel', 'fase', 'gabarito']

# Serializador para o modelo GabaritoLido, incluindo participante e prova relacionados
class GabaritoLidoSerializer(serializers.ModelSerializer):
    participante = ParticipanteSerializer()  # Serializa o objeto Participante relacionado
    prova = ProvaSerializer()                # Serializa o objeto Prova relacionado
    class Meta:
        model = GabaritoLido
        fields = ['id', 'codigo', 'participante', 'prova', 'nota', 'gabarito_lido']
