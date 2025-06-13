from django import forms
from .models import Participante, Prova, Escola, GabaritoLido

# =========================
# Formulários da aplicação Interface_OCI
# =========================
# Estes formulários são usados para validar e processar dados de entrada do usuário
# para as entidades Participante, Escola e Prova.

# Formulário para Escola
class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['codigo', 'nome']

# Formulário para Participante
class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['codigo', 'nome', 'escola']

# Formulário para Prova
class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['codigo', 'ano', 'nivel', 'fase', 'gabarito']

# Formulário para Gabarito Lido
class GabaritoLidoForm(forms.ModelForm):
    class Meta:
        model = GabaritoLido
        fields = ['codigo', 'prova', 'participante', 'gabarito_lido', 'nota']

# Fim do módulo de formulários
