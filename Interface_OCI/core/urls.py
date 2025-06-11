from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# Este arquivo define as URLs da aplicação Interface_OCI.
# As URLs são usadas para mapear requisições HTTP para as views correspondentes.

urlpatterns = [
    path('', views.index, name='index'),
    path('lista_escolas/', views.lista_escolas, name='lista_escolas'),
    path('lista_participantes/', views.lista_participantes, name='lista_participantes'),
    path('lista_provas/', views.lista_provas, name='lista_provas'),
    path('cadastrar_participante/', views.cadastrar_participante, name='cadastrar_participante'),
    path('cadastrar_escola/', views.cadastrar_escola, name='cadastrar_escola'),
    path('cadastrar_prova/', views.cadastrar_prova, name='cadastrar_prova'),


    # Autenticação e Autorização
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
