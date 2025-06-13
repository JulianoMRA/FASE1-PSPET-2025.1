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
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f'ESC{Escola.objects.count() + 1:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo or self.id} - {self.nome}'

# -------------------------
# Modelo Participante
# -------------------------
class Participante(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nome = models.CharField(max_length=64)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f'PART{Participante.objects.count() + 1:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo or self.id} - {self.nome}'

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ano = models.CharField(max_length=4, choices=ANO_CHOICES, default='2024')
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='Iniciacao A')
    fase = models.CharField(max_length=10, choices=FASE_CHOICES, default='Fase 1')
    gabarito = models.CharField(max_length=20)
    codigo = models.CharField(max_length=10, unique=True, null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f'PROVA{Prova.objects.count() + 1:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo or self.id} - Gabarito: {self.gabarito}'

# -------------------------
# Modelo GabaritoLido
# -------------------------
class GabaritoLido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True)
    gabarito_lido = models.CharField(max_length=20)
    nota = models.FloatField(default=0.0)
    codigo = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo = GabaritoLido.objects.all().order_by('-id').first()
            proximo_num = (ultimo.id + 1) if ultimo else 1
            self.codigo = f'GBR{proximo_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo or self.id} - Gabarito Lido: {self.gabarito_lido} - Nota: {self.nota}'

# Fim do arquivo de modelos
