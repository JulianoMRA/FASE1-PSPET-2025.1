from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# =========================
# URLs da aplicação Interface_OCI
# =========================
# Este arquivo define as rotas que mapeiam requisições HTTP para as views correspondentes.

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),
    
    # Cadastro individual
    path('escolas/novo/', views.cadastrar_escola, name='cadastrar_escola'),
    path('participantes/novo/', views.cadastrar_participante, name='cadastrar_participante'),
    path('provas/novo/', views.cadastrar_prova, name='cadastrar_prova'),

    # Leitura de gabarito
    path('ler_gabarito/', views.ler_gabarito, name='ler_gabarito'),

    # Edição
    path('editar_escola/<int:escola_id>/', views.editar_escola, name='editar_escola'),
    path('editar_participante/<int:participante_id>/', views.editar_participante, name='editar_participante'),
    path('editar_prova/<int:prova_id>/', views.editar_prova, name='editar_prova'),
    path('editar_gabarito_lido/<int:gabarito_id>/', views.editar_gabarito_lido, name='editar_gabarito_lido'),

    # Exclusão
    path('excluir_prova/<int:prova_id>/', views.excluir_prova, name='excluir_prova'),
    path('excluir_participante/<int:participante_id>/', views.excluir_participante, name='excluir_participante'),
    path('excluir_escola/<int:escola_id>/', views.excluir_escola, name='excluir_escola'),
    path('excluir_gabarito_lido/<int:gabarito_id>/', views.excluir_gabarito_lido, name='excluir_gabarito_lido'),

    # Autenticação
    path('login/', views.api_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('csrf/', views.get_csrf, name='get_csrf')
]

# Fim do arquivo de URLs da aplicação Interface_OCI
