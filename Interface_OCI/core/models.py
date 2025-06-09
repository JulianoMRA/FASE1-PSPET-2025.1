from django.db import models

# Create your models here.

class Escola(models.Model):
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome
    
class Participante(models.Model):
    id_participante = models.IntegerField(unique=True)
    nome = models.CharField(max_length=64)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Prova(models.Model):
    id_prova = models.IntegerField(unique=True)
    gabarito = models.CharField(max_length=20)

    def __str__(self):
        return f'Prova {self.id_prova} - Gabarito: {self.gabarito}'
