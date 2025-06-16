from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Escola, Participante, Prova, GabaritoLido
from .serializers import EscolaSerializer, ParticipanteSerializer, ProvaSerializer, GabaritoLidoSerializer


import ctypes
from ctypes import *

ctypes.CDLL('./libraylib.so.550', mode=RTLD_GLOBAL)
ctypes.CDLL('./libZXing.so.3', mode=RTLD_GLOBAL)
leitor = ctypes.CDLL('./libleitor.so')

class Reading(Structure):
    _fields_ = [
        ('erro', ctypes.c_int),
        ('id_prova', ctypes.c_int),
        ('id_participante', ctypes.c_int),
        ('leitura', ctypes.c_char_p)
    ]

leitor.read_image_data.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
leitor.read_image_data.restype = Reading

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
    
class LerGabaritoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # PASSO 2: Salvar gabarito e calcular nota
        if 'gabarito_lido' in request.data and not request.FILES.get('imagem'):
            prova_id = request.POST.get('prova_id')
            participante_id = request.POST.get('participante_id')
            codigo = request.POST.get('codigo')
            pesos_input = request.POST.get('pesos', '').strip()
            gabarito_lido = request.POST.get('gabarito_lido')

            prova = Prova.objects.filter(id=prova_id, user=request.user).first()
            participante = Participante.objects.filter(id=participante_id, user=request.user).first()
            if not prova or not participante:
                return Response({'erro': 'Prova ou participante inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            # Parse dos pesos
            pesos = [1] * 20
            if pesos_input:
                try:
                    for par in pesos_input.split(','):
                        if ':' in par:
                            idx, peso = par.split(':')
                            idx = int(idx.strip()) - 1
                            peso = float(peso.strip())
                            if 0 <= idx < 20:
                                pesos[idx] = peso
                except Exception:
                    pass

            # Calcule a nota
            gabarito_oficial = prova.gabarito.lower()
            gabarito_lido = gabarito_lido.lower()
            acertos = 0
            total_peso = 0
            for i, (resp, oficial) in enumerate(zip(gabarito_lido, gabarito_oficial)):
                peso = pesos[i] if i < len(pesos) else 1
                total_peso += peso
                if resp == oficial:
                    acertos += peso
            nota = round((acertos / total_peso) * 10, 2) if total_peso else 0

            # Salve o GabaritoLido
            GabaritoLido.objects.create(
                codigo=codigo,
                prova=prova,
                participante=participante,
                gabarito_lido   =gabarito_lido,
                nota=nota,
                user=request.user
            )

            return Response({'nota': nota}, status=status.HTTP_200_OK)

        # PASSO 1: Leitura da imagem
        file = request.FILES.get('imagem')
        prova_id = request.POST.get('prova_id')
        participante_id = request.POST.get('participante_id')
        codigo = request.POST.get('codigo')
        pesos_input = request.POST.get('pesos', '').strip()

        if not file or not prova_id or not participante_id or not codigo:
            return Response({'erro': 'Dados obrigatórios não enviados.'}, status=status.HTTP_400_BAD_REQUEST)

        prova = Prova.objects.filter(id=prova_id, user=request.user).first()
        participante = Participante.objects.filter(id=participante_id, user=request.user).first()
        if not prova or not participante:
            return Response({'erro': 'Prova ou participante inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse dos pesos (caso informado)
        pesos = [1] * 20
        if pesos_input:
            try:
                for par in pesos_input.split(','):
                    if ':' in par:
                        idx, peso = par.split(':')
                        idx = int(idx.strip()) - 1
                        peso = float(peso.strip())
                        if 0 <= idx < 20:
                            pesos[idx] = peso
            except Exception:
                pass

        # Leitura do gabarito usando biblioteca nativa
        dados = file.read()
        tipo = b'.' + file.name.split('.')[-1].encode()
        array_type = ctypes.c_ubyte * len(dados)
        array_instance = array_type.from_buffer_copy(dados)
        resultado = leitor.read_image_data(tipo, array_instance, len(dados))
        gabarito_lido = resultado.leitura.decode('utf-8')

        return Response({
            'gabarito_lido': gabarito_lido,
            'prova_gabarito': prova.gabarito if prova else ''
        }, status=status.HTTP_200_OK)