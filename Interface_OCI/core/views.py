from django.shortcuts import render, redirect
from .models import Escola, Participante, Prova
from .forms import ParticipanteForm, ProvaForm, EscolaForm

# Este arquivo define as views da aplicação Interface_OCI.
# As views são responsáveis por processar as requisições HTTP e retornar as respostas apropriadas.

def lista_escolas(request):
    escolas = Escola.objects.all()
    return render(request, 'core/lista_escolas.html', {'escolas': escolas})

def lista_participantes(request):
    participantes = Participante.objects.all()
    return render(request, 'core/lista_participantes.html', {'participantes': participantes})

def lista_provas(request):
    provas = Prova.objects.all()
    return render(request, 'core/lista_provas.html', {'provas': provas})

def cadastrar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_participantes')
    else:
        form = ParticipanteForm()
    return render(request, 'core/cadastrar_participante.html', {'form': form})

def cadastrar_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_escolas')
    else:
        form = EscolaForm()
    return render(request, 'core/cadastrar_escola.html', {'form': form})

def cadastrar_prova(request):
    if request.method == 'POST':
        form = ProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_provas')
    else:
        form = ProvaForm()
    return render(request, 'core/cadastrar_prova.html', {'form': form})
