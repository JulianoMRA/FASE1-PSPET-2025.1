from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Escola, Participante, Prova, GabaritoLido
from .serializers import EscolaSerializer, ParticipanteSerializer, ProvaSerializer, GabaritoLidoSerializer

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer
    permission_classes = [IsAuthenticated]

class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer
    permission_classes = [IsAuthenticated]

class ProvaViewSet(viewsets.ModelViewSet):
    queryset = Prova.objects.all()
    serializer_class = ProvaSerializer
    permission_classes = [IsAuthenticated]

class GabaritoLidoViewSet(viewsets.ModelViewSet):
    queryset = GabaritoLido.objects.all()
    serializer_class = GabaritoLidoSerializer
    permission_classes = [IsAuthenticated]
