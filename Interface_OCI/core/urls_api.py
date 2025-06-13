from rest_framework import routers
from .views_api import EscolaViewSet, ParticipanteViewSet, ProvaViewSet, GabaritoLidoViewSet

router = routers.DefaultRouter()
router.register(r'escolas', EscolaViewSet)
router.register(r'participantes', ParticipanteViewSet)
router.register(r'provas', ProvaViewSet)
router.register(r'gabaritos', GabaritoLidoViewSet)

urlpatterns = router.urls
