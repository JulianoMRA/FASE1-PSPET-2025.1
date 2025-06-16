from rest_framework import routers
from django.urls import path
from .views_api import EscolaViewSet, ParticipanteViewSet, ProvaViewSet, GabaritoLidoViewSet, LerGabaritoAPIView

# Cria um roteador padrão do Django REST Framework para registrar as rotas da API
router = routers.DefaultRouter()
router.register(r'escolas', EscolaViewSet)           # Endpoint para Escola (/api/escolas/)
router.register(r'participantes', ParticipanteViewSet) # Endpoint para Participante (/api/participantes/)
router.register(r'provas', ProvaViewSet)             # Endpoint para Prova (/api/provas/)
router.register(r'gabaritos', GabaritoLidoViewSet)   # Endpoint para GabaritoLido (/api/gabaritos/)

# As URLs geradas pelo roteador serão usadas pelo Django
urlpatterns = router.urls + [
    path('ler-gabarito/', LerGabaritoAPIView.as_view(), name='ler-gabarito'),
]
