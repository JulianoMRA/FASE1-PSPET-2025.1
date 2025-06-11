from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Escola, Participante, Prova
from .forms import ParticipanteForm, ProvaForm, EscolaForm
from django.db.models import Max

# Este arquivo define as views da aplicação Interface_OCI.
# As views são responsáveis por processar as requisições HTTP e retornar as respostas apropriadas.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'core/index.html')

@login_required
def lista_escolas(request):
    escolas = Escola.objects.filter(user=request.user)
    return render(request, 'core/lista_escolas.html', {'escolas': escolas})

@login_required
def lista_participantes(request):
    participantes = Participante.objects.filter(user=request.user)
    return render(request, 'core/lista_participantes.html', {'participantes': participantes})

@login_required
def lista_provas(request):
    provas = Prova.objects.filter(user=request.user)
    return render(request, 'core/lista_provas.html', {'provas': provas})

@login_required
def cadastrar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.user = request.user
            participante.save()
            return redirect('lista_participantes')
    else:
        form = ParticipanteForm()
    return render(request, 'core/cadastrar_participante.html', {'form': form})

@login_required
def cadastrar_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            escola = form.save(commit=False)
            escola.user = request.user
            escola.save()
            return redirect('lista_escolas')
    else:
        form = EscolaForm()
    return render(request, 'core/cadastrar_escola.html', {'form': form})

@login_required
def cadastrar_prova(request):
    if request.method == 'POST':
        form = ProvaForm(request.POST)
        if form.is_valid():
            prova = form.save(commit=False)
            prova.user = request.user
            prova.save()
            return redirect('lista_provas')
    else:
        form = ProvaForm()
    return render(request, 'core/cadastrar_prova.html', {'form': form})

