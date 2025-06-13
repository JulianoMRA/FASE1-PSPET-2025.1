from django.db import models
from django.contrib.auth.models import User

# =========================
# Modelos da aplicação Interface_OCI
# =========================
# Estes modelos representam as tabelas do banco de dados e suas relações.

# -------------------------
# Modelo Escola
# -------------------------
class Escola(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome

# -------------------------
# Modelo Participante
# -------------------------
class Participante(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nome = models.CharField(max_length=64)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# -------------------------
# Modelo Prova
# -------------------------
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

    id_prova = models.CharField(max_length=3, unique=True, default='001')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ano = models.CharField(max_length=4, choices=ANO_CHOICES, default='2024')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='Iniciacao A')
    fase = models.CharField(max_length=10, choices=FASE_CHOICES, default='Fase 1')
    gabarito = models.CharField(max_length=20)

    def __str__(self):
        return f'Prova {self.id} - Gabarito: {self.gabarito}'

# -------------------------
# Modelo GabaritoLido
# -------------------------
class GabaritoLido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    gabarito_lido = models.CharField(max_length=20)
    nota = models.FloatField(default=0.0)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Gabarito Lido: {self.gabarito_lido} - Nota: {self.nota}'

# Fim do arquivo de modelos
