# Este arquivo define as views da aplicação Interface_OCI.
# As views são responsáveis por processar as requisições HTTP e retornar as respostas apropriadas.


# Importando as bibliotecas necessárias
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Escola, Participante, Prova
from .forms import ParticipanteForm, ProvaForm, EscolaForm
from django.db.models import Max
import ctypes
from ctypes import *


# Carregando as bibliotecas compartilhadas necessárias
# As bibliotecas devem estar no mesmo diretório que este script ou em um diretório acessível pelo sistema.
# As bibliotecas são carregadas com o modo RTLD_GLOBAL para que suas funções possam ser acessadas globalmente.
# As bibliotecas são necessárias para a leitura de imagens e processamento de dados.
# As bibliotecas devem ser compiladas para a arquitetura correta do sistema (x86_64, ARM, etc.).
# As bibliotecas devem ser compatíveis com a versão do Python utilizada.
# As bibliotecas devem ser instaladas no sistema ou no ambiente virtual utilizado pelo Django.


ctypes.CDLL('./libraylib.so.550', mode=RTLD_GLOBAL)
ctypes.CDLL('./libZXing.so.3', mode=RTLD_GLOBAL)

leitor = ctypes.CDLL('./libleitor.so')

class Reading(Structure):
    _fields_ = [
        ('erro', ctypes.c_int),
        ('id_prova', ctypes.c_int),
        ('id_participante', ctypes.c_int),
        ('leitura', ctypes.c_char_p)
    ]

leitor.read_image_data.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
leitor.read_image_data.restype = Reading

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

@login_required
def ler_gabarito(request):
    provas = Prova.objects.filter(user=request.user)  
    if request.method == 'POST':
        file = request.FILES['imagem']
        pesos = request.POST.get('pesos')
        pont_max = 10
    
        if pesos:
            pesos = pesos.split(';')
            for i in range(len(pesos)):
                pont_max+=(int(pesos[i].split('_')[1])-1)*0.5
        
        prova_id = request.POST.get('prova_id')  
        prova = Prova.objects.filter(id=prova_id, user=request.user).first()
        print('prova: ', prova)

        if file and prova:
            dados = file.read()
            tipo = b'.' + file.name.split('.')[-1].encode()
            array_type = ctypes.c_ubyte * len(dados)
            array_instance = array_type.from_buffer_copy(dados)

            resultado = leitor.read_image_data(tipo, array_instance, len(dados))

            gabarito_lido = resultado.leitura.decode('utf-8')

            nota = 0
            peso_index = 0
            for i in range(20):
                # mantendo a questao ponderada a ser checada >= que a questao sendo checada no gabarito
                if pesos and i > int(pesos[peso_index].split('_')[0]) and peso_index < len(pesos)-1:
                    peso_index += 1
                if gabarito_lido[i] == prova.gabarito[i]:
                    if pesos and i == int(pesos[peso_index].split('_')[0]):
                        nota+=int(pesos[peso_index].split('_')[1])*0.5
                    else:
                        nota+=.5
                        
            nota_final = (nota/pont_max)*10
            nota_final = round(nota_final, 2)
            return render(request, 'core/ler_gabarito.html', {
                'gabarito_lido': gabarito_lido,
                'nota': nota_final,
                'prova_gabarito': prova.gabarito,
                'provas': provas
            })
    
    return render(request, 'core/ler_gabarito.html', {'provas': provas})

@login_required
def excluir_prova(request, prova_id):
    prova = get_object_or_404(Prova, id=prova_id, user=request.user)
    prova.delete()
    return redirect('lista_provas')

@login_required
def excluir_participante(request, participante_id):
    participante = get_object_or_404(Participante, id=participante_id, user=request.user)
    participante.delete()
    return redirect('lista_participantes')

@login_required
def excluir_escola(request, escola_id):
    escola = get_object_or_404(Escola, id=escola_id, user=request.user)
    escola.delete()
    return redirect('lista_escolas')
