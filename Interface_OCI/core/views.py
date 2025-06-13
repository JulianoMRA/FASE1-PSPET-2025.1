"""
Views da aplicação Interface_OCI.
Responsáveis por processar requisições HTTP e retornar respostas apropriadas.
"""

# =========================
# IMPORTAÇÕES
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Escola, Participante, Prova, GabaritoLido
from .forms import ParticipanteForm, ProvaForm, EscolaForm
import ctypes
from ctypes import *

# =========================
# CARREGAMENTO DAS BIBLIOTECAS NATIVAS
# =========================
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

# =========================
# AUTENTICAÇÃO E PÁGINA INICIAL
# =========================

def signup(request):
    """Cadastro de novo usuário."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def index(request):
    """Página inicial da aplicação."""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'core/index.html')

# =========================
# DASHBOARD DE CADASTROS (Centralizado)
# =========================

@login_required
def dashboard_cadastros(request):
    """
    Dashboard para cadastros rápidos de escola, participante e prova.
    """
    escola_form = EscolaForm(prefix='escola')
    participante_form = ParticipanteForm(prefix='participante')
    prova_form = ProvaForm(prefix='prova')

    if request.method == 'POST':
        if 'escola-submit' in request.POST:
            escola_form = EscolaForm(request.POST, prefix='escola')
            if escola_form.is_valid():
                escola = escola_form.save(commit=False)
                escola.user = request.user
                escola.save()
                return redirect('dashboard_cadastros')
        elif 'participante-submit' in request.POST:
            participante_form = ParticipanteForm(request.POST, prefix='participante')
            if participante_form.is_valid():
                participante = participante_form.save(commit=False)
                participante.user = request.user
                participante.save()
                return redirect('dashboard_cadastros')
        elif 'prova-submit' in request.POST:
            prova_form = ProvaForm(request.POST, prefix='prova')
            if prova_form.is_valid():
                prova = prova_form.save(commit=False)
                prova.user = request.user
                prova.save()
                return redirect('dashboard_cadastros')

    return render(request, 'core/dashboard_cadastros.html', {
        'escola_form': escola_form,
        'participante_form': participante_form,
        'prova_form': prova_form,
    })

# =========================
# DASHBOARD CENTRALIZADO DE LISTAGEM/EDIÇÃO/EXCLUSÃO
# =========================

@login_required
def dashboard(request):
    """
    Dashboard centralizado com todas as listas (escolas, participantes, provas, gabaritos lidos).
    """
    escolas = Escola.objects.filter(user=request.user)
    participantes = Participante.objects.filter(user=request.user)
    provas = Prova.objects.filter(user=request.user)
    gabaritos = GabaritoLido.objects.filter(user=request.user).select_related('prova', 'participante')
    return render(request, 'core/dashboard.html', {
        'escolas': escolas,
        'participantes': participantes,
        'provas': provas,
        'gabaritos': gabaritos,
    })

# =========================
# LEITURA E CORREÇÃO DE GABARITO
# =========================

@login_required
def ler_gabarito(request):
    """
    Upload, leitura e correção de gabarito.
    Permite informar pesos especiais para cada questão.
    """
    provas = Prova.objects.filter(user=request.user)
    participantes = Participante.objects.filter(user=request.user)
    if request.method == 'POST':
        file = request.FILES['imagem']
        pesos_input = request.POST.get('pesos', '').strip()
        prova_id = request.POST.get('prova_id')
        participante_id = request.POST.get('participante_id')
        codigo = request.POST.get('codigo')  
        prova = Prova.objects.filter(id=prova_id, user=request.user).first()
        participante = Participante.objects.filter(id=participante_id, user=request.user).first()

        # Parse dos pesos: por padrão, todas as questões têm peso 1
        pesos = [1] * 20
        if pesos_input:
            try:
                for par in pesos_input.split(','):
                    if ':' in par:
                        idx, peso = par.split(':')
                        idx = int(idx.strip()) - 1  # questões começam em 1
                        peso = float(peso.strip())
                        if 0 <= idx < 20:
                            pesos[idx] = peso
            except Exception:
                pass  # Se houver erro, ignora e usa pesos padrão

        if file and prova and participante and codigo:
            dados = file.read()
            tipo = b'.' + file.name.split('.')[-1].encode()
            array_type = ctypes.c_ubyte * len(dados)
            array_instance = array_type.from_buffer_copy(dados)

            resultado = leitor.read_image_data(tipo, array_instance, len(dados))
            gabarito_lido = resultado.leitura.decode('utf-8')

            nota = 0
            peso_total = sum(pesos)
            for i in range(20):
                if gabarito_lido[i] == prova.gabarito[i]:
                    nota += pesos[i]

            nota_final = (nota / peso_total) * 10
            nota_final = round(nota_final, 2)

            GabaritoLido.objects.create(
                user=request.user,
                prova=prova,
                participante=participante,
                gabarito_lido=gabarito_lido,
                nota=nota_final,
                codigo=codigo  # salva o código informado
            )

            return render(request, 'core/ler_gabarito.html', {
                'gabarito_lido': gabarito_lido,
                'nota': nota_final,
                'prova_gabarito': prova.gabarito,
                'provas': provas,
                'participantes': participantes
            })

    return render(request, 'core/ler_gabarito.html', {'provas': provas, 'participantes': participantes})

# =========================
# EXCLUSÃO DE REGISTROS
# =========================

@login_required
def excluir_prova(request, prova_id):
    """Exclui uma prova cadastrada."""
    prova = get_object_or_404(Prova, id=prova_id, user=request.user)
    prova.delete()
    return redirect('dashboard')

@login_required
def excluir_participante(request, participante_id):
    """Exclui um participante cadastrado."""
    participante = get_object_or_404(Participante, id=participante_id, user=request.user)
    participante.delete()
    return redirect('dashboard')

@login_required
def excluir_escola(request, escola_id):
    """Exclui uma escola cadastrada."""
    escola = get_object_or_404(Escola, id=escola_id, user=request.user)
    escola.delete()
    return redirect('dashboard')

@login_required
def excluir_gabarito_lido(request, gabarito_id):
    """Exclui um gabarito lido cadastrado."""
    gabarito = get_object_or_404(GabaritoLido, id=gabarito_id, user=request.user)
    gabarito.delete()
    return redirect('dashboard')

# =========================
# EDIÇÃO DE REGISTROS
# =========================

@login_required
def editar_escola(request, escola_id):
    """Edita uma escola cadastrada."""
    escola = get_object_or_404(Escola, id=escola_id, user=request.user)
    if request.method == 'POST':
        form = EscolaForm(request.POST, instance=escola)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EscolaForm(instance=escola)
    return render(request, 'core/editar_escola.html', {'form': form, 'escola': escola})

@login_required
def editar_participante(request, participante_id):
    """Edita um participante cadastrado."""
    participante = get_object_or_404(Participante, id=participante_id, user=request.user)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, instance=participante)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ParticipanteForm(instance=participante)
    return render(request, 'core/editar_participante.html', {'form': form, 'participante': participante})

@login_required
def editar_prova(request, prova_id):
    """Edita uma prova cadastrada."""
    prova = get_object_or_404(Prova, id=prova_id, user=request.user)
    if request.method == 'POST':
        form = ProvaForm(request.POST, instance=prova)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProvaForm(instance=prova)
    return render(request, 'core/editar_prova.html', {'form': form, 'prova': prova})

@login_required
def editar_gabarito_lido(request, gabarito_id):
    """Edita um gabarito lido cadastrado (nota e participante)."""
    gabarito = get_object_or_404(GabaritoLido, id=gabarito_id, user=request.user)
    if request.method == 'POST':
        if 'nota' in request.POST and 'participante_id' in request.POST:
            gabarito.nota = float(request.POST['nota'])
            participante_id = request.POST['participante_id']
            if participante_id:
                gabarito.participante_id = participante_id
            gabarito.save()
            return redirect('dashboard')
    participantes = Participante.objects.filter(user=request.user)
    return render(request, 'core/editar_gabarito_lido.html', {'gabarito': gabarito, 'participantes': participantes})

# Fim do arquivo de views
