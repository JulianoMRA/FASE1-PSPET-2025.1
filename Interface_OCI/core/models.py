from django.db import models

# Este arquivo define os modelos do Django para a aplicação Interface_OCI.
# Os modelos representam as tabelas do banco de dados e são usados para interagir com os dados.
# Importante: Certifique-se de que o Django esteja configurado corretamente para usar este modelo.
# Definindo os modelos para a aplicação Interface_OCI
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
