from django.shortcuts import render, redirect
## from django.views.decorators.csrf import csrf_exempt
from .models import Escola, Participante, Prova
from .forms import ParticipanteForm, ProvaForm, EscolaForm

import ctypes
from ctypes import *

ctypes.CDLL('./libraylib.so.550', mode=RTLD_GLOBAL)
ctypes.CDLL('./libZXing.so.3', mode=RTLD_GLOBAL)

leitor = ctypes.CDLL('./core/libleitor.so')

class Reading(Structure):
    _fields_ = [
        ('erro', ctypes.c_int),
        ('id_prova', ctypes.c_int),
        ('id_participante', ctypes.c_int),
        ('leitura', ctypes.c_char_p)
    ]

leitor.read_image_data.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
leitor.read_image_data.restype = Reading

# Este arquivo define as views da aplicação Interface_OCI.
# As views são responsáveis por processar as requisições HTTP e retornar as respostas apropriadas.

def index(request):
    return render(request, 'core/index.html')

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

## @csrf_exempt
def ler_gabarito(request):
    if request.method == 'POST':
        file = request.FILES['imagem']

        if file:
            dados = file.read()
            tipo = b'.' + file.name.split('.')[-1].encode()

            array_type = ctypes.c_ubyte * len(dados)
            array_instance = array_type.from_buffer_copy(dados)

            resultado = leitor.read_image_data(tipo, array_instance, len(dados))

            print(f"Erro: {resultado.erro}")
            print(f"ID Prova: {resultado.id_prova}")
            print(f"ID Participante: {resultado.id_participante}")
            print(f"Leitura: {resultado.leitura.decode('utf-8')}")
    return render(request, 'core/index.html')
