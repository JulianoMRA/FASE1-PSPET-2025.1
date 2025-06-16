from django.apps import AppConfig

# Esta classe configura o aplicativo 'core' do Django.
# O nome 'core' deve coincidir com o nome da pasta do app.
# O default_auto_field define o tipo padrão de campo auto-incremental para os modelos.
class WebpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
