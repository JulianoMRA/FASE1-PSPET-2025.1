from django.db import models
from django.contrib.auth.models import User

# Este arquivo define os modelos do Django para a aplicação Interface_OCI.
# Os modelos representam as tabelas do banco de dados e são usados para interagir com os dados.
# Importante: Certifique-se de que o Django esteja configurado corretamente para usar este modelo.
# Definindo os modelos para a aplicação Interface_OCI
class Escola(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome
    
class Participante(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nome = models.CharField(max_length=64)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Prova(models.Model):

    ANO_CHOICES = [(str(ano), str(ano)) for ano in range(2011, 2026)]
    NIVEL_CHOICES = [
        ('Iniciacao A', 'Iniciação A'),
        ('Iniciacao B', 'Iniciação B'),
        ('Programacao', 'Programação'),
    ]
    FASE_CHOICES = [
        ('Fase 1', 'Fase 1'),
        ('Fase 2', 'Fase 2'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ano = models.CharField(max_length=4, choices=ANO_CHOICES, default='2024')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='Iniciacao A')
    fase = models.CharField(max_length=10, choices=FASE_CHOICES, default='Fase 1')
    gabarito = models.CharField(max_length=20)

    def __str__(self):
        return f'Prova {self.id} - Gabarito: {self.gabarito}'
