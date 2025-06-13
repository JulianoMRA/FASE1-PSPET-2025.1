from django import forms
from .models import Participante, Prova, Escola

# =========================
# Formulários da aplicação Interface_OCI
# =========================
# Estes formulários são usados para validar e processar dados de entrada do usuário
# para as entidades Participante, Escola e Prova.

# Formulário para Participante
class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'escola']

# Formulário para Escola
class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome']

# Formulário para Prova
class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['id_prova', 'ano', 'nivel', 'fase', 'gabarito']

# Fim do módulo de formulários
