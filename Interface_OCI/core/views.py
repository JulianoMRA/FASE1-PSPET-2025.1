"""
Views da aplicação Interface_OCI.
Responsáveis por processar requisições HTTP e retornar respostas apropriadas.
"""

# =========================
# IMPORTAÇÕES
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from .models import Escola, Participante, Prova, GabaritoLido
from .forms import EscolaForm, ParticipanteForm, ProvaForm
import ctypes
import json
from ctypes import *

# =========================
# CARREGAMENTO DAS BIBLIOTECAS NATIVAS
# =========================
# Carrega as bibliotecas nativas necessárias para leitura de gabaritos
ctypes.CDLL('./libraylib.so.550', mode=RTLD_GLOBAL)
ctypes.CDLL('./libZXing.so.3', mode=RTLD_GLOBAL)
leitor = ctypes.CDLL('./libleitor.so')

# Estrutura para receber o resultado da leitura do gabarito
class Reading(Structure):
    _fields_ = [
        ('erro', ctypes.c_int),
        ('id_prova', ctypes.c_int),
        ('id_participante', ctypes.c_int),
        ('leitura', ctypes.c_char_p)
    ]

# Define os tipos de argumentos e retorno da função de leitura
leitor.read_image_data.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
leitor.read_image_data.restype = Reading

# =========================
# AUTENTICAÇÃO E PÁGINA INICIAL
# =========================

@csrf_exempt
def signup(request):
    """Cadastro de novo usuário."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Usuario criado com sucesso'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    # Retorna erro para métodos diferentes de POST
    return JsonResponse({'error': 'Metodo nao permitido'})

@csrf_exempt
def api_login(request):
    """Realiza login via API (usado pelo frontend)."""
    username = request.POST.get('username')
    password = request.POST.get('password1')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Credenciais inválidas'}, status=401)

@ensure_csrf_cookie
def get_csrf(request):
    """Endpoint para garantir que o cookie CSRF está setado."""
    return JsonResponse({'message': 'CSRF cookie set'})

def index(request):
    """Página inicial da aplicação (dashboard principal)."""
    if not request.user.is_authenticated:
        return redirect('login')

    # Busca todos os registros do usuário autenticado
    escolas = list(Escola.objects.filter(user=request.user))
    participantes = list(Participante.objects.filter(user=request.user))
    provas = list(Prova.objects.filter(user=request.user))
    gabaritos = list(GabaritoLido.objects.filter(user=request.user).select_related('prova', 'participante'))

    # Função auxiliar para ordenar pelo campo 'codigo'
    def codigo_key(obj):
        try:
            return int(obj.codigo)
        except (ValueError, TypeError, AttributeError):
            return 0

    escolas.sort(key=codigo_key)
    participantes.sort(key=codigo_key)
    provas.sort(key=codigo_key)
    gabaritos.sort(key=codigo_key)

    return render(request, 'core/index.html', {
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
    View para upload, leitura e correção de gabarito.
    Possui dois passos: upload/extração e confirmação/salvamento.
    """
    provas = Prova.objects.filter(user=request.user)
    participantes = Participante.objects.filter(user=request.user)

    if request.method == 'POST':
        # Passo 1: Upload e leitura da imagem
        if 'imagem' in request.FILES:
            file = request.FILES['imagem']
            prova_id = request.POST.get('prova_id')
            participante_id = request.POST.get('participante_id')
            codigo = request.POST.get('codigo')
            pesos_input = request.POST.get('pesos', '').strip()
            prova = Prova.objects.filter(id=prova_id, user=request.user).first()
            participante = Participante.objects.filter(id=participante_id, user=request.user).first()

            # Parse dos pesos (caso informado)
            pesos = [1] * 20
            if pesos_input:
                try:
                    for par in pesos_input.split(','):
                        if ':' in par:
                            idx, peso = par.split(':')
                            idx = int(idx.strip()) - 1
                            peso = float(peso.strip())
                            if 0 <= idx < 20:
                                pesos[idx] = peso
                except Exception:
                    pass

            # Leitura do gabarito usando biblioteca nativa
            dados = file.read()
            tipo = b'.' + file.name.split('.')[-1].encode()
            array_type = ctypes.c_ubyte * len(dados)
            array_instance = array_type.from_buffer_copy(dados)
            resultado = leitor.read_image_data(tipo, array_instance, len(dados))
            gabarito_lido = resultado.leitura.decode('utf-8')

            # Mostra para o usuário editar/confirmar antes de salvar
            return render(request, 'core/ler_gabarito.html', {
                'gabarito_lido': gabarito_lido,
                'prova_gabarito': prova.gabarito if prova else '',
                'provas': provas,
                'participantes': participantes,
                'prova_id': prova_id,
                'participante_id': participante_id,
                'codigo': codigo,
                'pesos': pesos_input,
                'step': 2  # indica que está no passo de edição/validação
            })

        # Passo 2: Edição/validação e salvamento
        elif 'gabarito_lido' in request.POST:
            gabarito_lido = request.POST.get('gabarito_lido')
            prova_id = request.POST.get('prova_id')
            participante_id = request.POST.get('participante_id')
            codigo = request.POST.get('codigo')
            pesos_input = request.POST.get('pesos', '').strip()
            prova = Prova.objects.filter(id=prova_id, user=request.user).first()
            participante = Participante.objects.filter(id=participante_id, user=request.user).first()

            # Parse dos pesos
            pesos = [1] * 20
            if pesos_input:
                try:
                    for par in pesos_input.split(','):
                        if ':' in par:
                            idx, peso = par.split(':')
                            idx = int(idx.strip()) - 1
                            peso = float(peso.strip())
                            if 0 <= idx < 20:
                                pesos[idx] = peso
                except Exception:
                    pass

            # Calcula a nota do participante
            nota = 0
            peso_total = sum(pesos)
            for i in range(20):
                if gabarito_lido[i] == prova.gabarito[i]:
                    nota += pesos[i]
            nota_final = (nota / peso_total) * 10
            nota_final = round(nota_final, 2)

            # Salva o gabarito lido no banco de dados
            GabaritoLido.objects.create(
                user=request.user,
                prova=prova,
                participante=participante,
                gabarito_lido=gabarito_lido,
                nota=nota_final,
                codigo=codigo
            )

            return render(request, 'core/ler_gabarito.html', {
                'gabarito_lido': gabarito_lido,
                'nota': nota_final,
                'prova_gabarito': prova.gabarito if prova else '',
                'provas': provas,
                'participantes': participantes,
                'success': True
            })

    # GET ou início do POST
    return render(request, 'core/ler_gabarito.html', {
        'provas': provas,
        'participantes': participantes
    })

# =========================
# EXCLUSÃO DE REGISTROS
# =========================

@login_required
def excluir_prova(request, prova_id):
    """Exclui uma prova cadastrada."""
    prova = get_object_or_404(Prova, id=prova_id, user=request.user)
    prova.delete()
    return redirect('index')

@login_required
def excluir_participante(request, participante_id):
    """Exclui um participante cadastrado."""
    participante = get_object_or_404(Participante, id=participante_id, user=request.user)
    participante.delete()
    return redirect('index')

@login_required
def excluir_escola(request, escola_id):
    """Exclui uma escola cadastrada."""
    escola = get_object_or_404(Escola, id=escola_id, user=request.user)
    escola.delete()
    return redirect('index')

@login_required
def excluir_gabarito_lido(request, gabarito_id):
    """Exclui um gabarito lido cadastrado."""
    gabarito = get_object_or_404(GabaritoLido, id=gabarito_id, user=request.user)
    gabarito.delete()
    return redirect('index')

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
            return JsonResponse({'message': 'Dados editados'})
    return JsonResponse({'error': 'Metodo nao permitido'})

@login_required
def editar_participante(request, participante_id):
    """Edita um participante cadastrado."""
    participante = get_object_or_404(Participante, id=participante_id, user=request.user)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, instance=participante)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Dados editados'})
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
            return JsonResponse({'message': 'Dados editados'})
    else:
        form = ProvaForm(instance=prova)
    return render(request, 'core/editar_prova.html', {'form': form, 'prova': prova})

@login_required
def editar_gabarito_lido(request, gabarito_id):
    """Edita um gabarito lido cadastrado (código e participante)."""
    gabarito = get_object_or_404(GabaritoLido, id=gabarito_id, user=request.user)
    participantes = Participante.objects.filter(user=request.user)
    if request.method == 'POST':
        novo_codigo = request.POST.get('codigo')
        participante_id = request.POST.get('participante_id')
        if novo_codigo:
            gabarito.codigo = novo_codigo
        if participante_id:
            gabarito.participante_id = participante_id
        gabarito.save()
        return redirect('index')
    return render(request, 'core/editar_gabarito_lido.html', {'gabarito': gabarito, 'participantes': participantes})

# =========================
# CADASTRO DE NOVOS REGISTROS
# =========================

@login_required
def cadastrar_escola(request):
    """Cadastra uma nova escola."""
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            escola = form.save(commit=False)
            escola.user = request.user
            escola.save()
            return JsonResponse({'message': 'Escola cadastrada'})
        else:
            return JsonResponse({'error': 'Dados invalidos'})
    return JsonResponse({'error': 'Metodo nao permitido'})

@login_required
def cadastrar_participante(request):
    """Cadastra um novo participante."""
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.user = request.user
            participante.save()
            return JsonResponse({'message': 'Participante cadastrado'})
        else:
            return JsonResponse({'error': 'Dados invalidos'})
    return JsonResponse({'error': 'Metodo nao permitido'})

@login_required
def cadastrar_prova(request):
    """Cadastra uma nova prova."""
    if request.method == 'POST':
        form = ProvaForm(request.POST)
        if form.is_valid():
            prova = form.save(commit=False)
            prova.user = request.user
            prova.save()
            return JsonResponse({'message': 'Prova cadastrada'})
        else:
            return JsonResponse({'error': 'Dados invalidos'})
    return JsonResponse({'error': 'Metodo nao permitido'})

# Fim do arquivo de views
