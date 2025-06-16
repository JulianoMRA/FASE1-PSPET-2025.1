from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Escola, Participante, Prova, GabaritoLido
from .serializers import EscolaSerializer, ParticipanteSerializer, ProvaSerializer, GabaritoLidoSerializer

# =========================
# ViewSets da API REST
# =========================
# Cada ViewSet abaixo define as operações CRUD para um modelo,
# restringindo o acesso aos objetos do usuário autenticado.

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.none()  # QuerySet padrão vazio (será sobrescrito)
    serializer_class = EscolaSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar
    def get_queryset(self):
        # Retorna apenas as escolas do usuário autenticado
        return Escola.objects.filter(user=self.request.user)

class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.none()
    serializer_class = ParticipanteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Retorna apenas os participantes do usuário autenticado
        return Participante.objects.filter(user=self.request.user)

class ProvaViewSet(viewsets.ModelViewSet):
    queryset = Prova.objects.none()
    serializer_class = ProvaSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Retorna apenas as provas do usuário autenticado
        return Prova.objects.filter(user=self.request.user)

class GabaritoLidoViewSet(viewsets.ModelViewSet):
    queryset = GabaritoLido.objects.none()
    serializer_class = GabaritoLidoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Retorna apenas os gabaritos lidos do usuário autenticado
        return GabaritoLido.objects.filter(user=self.request.user)