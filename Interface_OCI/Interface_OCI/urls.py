"""
URL configuration for Interface_OCI project.

O arquivo urlpatterns abaixo faz o roteamento das URLs principais do projeto.
- URLs do admin do Django.
- URLs da aplicação principal 'core' (incluindo todas as rotas definidas em core/urls.py).
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin do Django
    path('admin/', admin.site.urls),

    # Inclui todas as URLs da aplicação 'core'
    path('', include('core.urls')),

    # URLs da API da aplicação 'core'
    path('api/', include('core.urls_api')),
]

# Fim do arquivo de URLs do projeto
