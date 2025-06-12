from django import forms
from .models import Participante, Prova, Escola

# Este arquivo define os formulários da aplicação Interface_OCI.
# Os formulários são usados para validar e processar dados de entrada do usuário.

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'escola']

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = ['nome']

class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['id_prova', 'ano', 'nivel', 'fase', 'gabarito']
