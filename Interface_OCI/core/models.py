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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Usuário dono da escola
    nome = models.CharField(max_length=64)  # Nome da escola
    codigo = models.CharField(max_length=10, null=True, blank=True)  # Código único da escola

    class Meta:
        unique_together = ('codigo', 'user')

    def save(self, *args, **kwargs):
        # Gera um código automático se não for informado
        if not self.codigo:
            self.codigo = f'ESC{Escola.objects.count() + 1:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        # Exibe o código e nome ao representar o objeto
        return f'{self.codigo or self.id} - {self.nome}'

# -------------------------
# Modelo Participante
# -------------------------
class Participante(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Usuário dono do participante
    nome = models.CharField(max_length=64)  # Nome do participante
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)  # Escola do participante
    codigo = models.CharField(max_length=10, null=True, blank=True)  # Código único do participante

    class Meta:
        unique_together = ('codigo', 'user')

    def save(self, *args, **kwargs):
        # Gera um código automático se não for informado
        if not self.codigo:
            self.codigo = f'PART{Participante.objects.count() + 1:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        # Exibe o código e nome ao representar o objeto
        return f'{self.codigo or self.id} - {self.nome}'

# -------------------------
# Modelo Prova
# -------------------------
class Prova(models.Model):
    # Opções de ano, nível e fase
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Usuário dono da prova
    ano = models.CharField(max_length=4, choices=ANO_CHOICES, default='2024')  # Ano da prova
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='Iniciacao A')  # Nível da prova
    fase = models.CharField(max_length=10, choices=FASE_CHOICES, default='Fase 1')  # Fase da prova
    gabarito = models.CharField(max_length=20)  # Gabarito oficial da prova
    codigo = models.CharField(max_length=10, null=True, blank=True)  # Código único da prova

    class Meta:
        unique_together = ('codigo', 'user')

    def save(self, *args, **kwargs):
        # Gera um código automático se não for informado
        if not self.codigo:
            self.codigo = f'PROVA{Prova.objects.count() + 1:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        # Exibe o código e o gabarito ao representar o objeto
        return f'{self.codigo or self.id} - Gabarito: {self.gabarito}'

# -------------------------
# Modelo GabaritoLido
# -------------------------
class GabaritoLido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuário dono do gabarito lido
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)  # Prova relacionada
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, null=True, blank=True)  # Participante relacionado
    gabarito_lido = models.CharField(max_length=20)  # Gabarito lido do participante
    nota = models.FloatField(default=0.0)  # Nota obtida
    codigo = models.CharField(max_length=15, null=True, blank=True)  # Código único do gabarito lido

    class Meta:
        unique_together = ('codigo', 'user')

    def save(self, *args, **kwargs):
        # Gera um código automático se não for informado
        if not self.codigo:
            ultimo = GabaritoLido.objects.all().order_by('-id').first()
            proximo_num = (ultimo.id + 1) if ultimo else 1
            self.codigo = f'GBR{proximo_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        # Exibe o código, gabarito lido e nota ao representar o objeto
        return f'{self.codigo or self.id} - Gabarito Lido: {self.gabarito_lido} - Nota: {self.nota}'

# Fim do arquivo de modelos
