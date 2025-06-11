from django import forms
from .models import Participante, Prova

# Este arquivo define os formulários da aplicação Interface_OCI.
# Os formulários são usados para validar e processar dados de entrada do usuário.

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'escola']

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Participante.escola.field.related_model
        fields = ['nome']

class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = ['ano', 'nivel', 'fase', 'gabarito']
