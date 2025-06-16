# FASE1-PSPET-2025.1 - Backend

## Descrição

Este repositório contém o back-end do sistema **Interface OCI**, desenvolvido em Django, para gerenciamento de escolas, participantes, provas e leitura/correção de gabaritos.

---

## Requisitos

- Python 3.10+
- Django 4.x
- Django REST Framework

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/FASE1-PSPET-2025.1.git
   cd FASE1-PSPET-2025.1/Interface_OCI
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # Ative o ambiente:
   # No Windows:
   venv\Scripts\activate
   # No Linux/macOS:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

---

## Estrutura do Projeto

```
Interface_OCI/
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── urls_api.py
│   ├── views_api.py
│   └── templates/core/
│       └── ... (templates HTML)
├── manage.py
└── requirements.txt
```

---

## Funcionalidades

- Cadastro, edição e exclusão de escolas, participantes e provas
- Upload, leitura e correção de gabaritos
- Dashboard principal com tabelas de dados
- API REST autenticada para integração com frontend

---

## Endpoints Principais

### Web

- `/` — Dashboard principal (requer login)
- `/login/` — Login de usuário
- `/logout/` — Logout
- `/signup/` — Cadastro de usuário
- `/escolas/novo/` — Cadastro de escola
- `/participantes/novo/` — Cadastro de participante
- `/provas/novo/` — Cadastro de prova
- `/ler_gabarito/` — Leitura/correção de gabarito

### API REST

- `/api/escolas/`
- `/api/participantes/`
- `/api/provas/`
- `/api/gabaritos/`

Todos os endpoints da API exigem autenticação.

---

## Autenticação

- O sistema utiliza autenticação padrão do Django (sessão).
- Para acessar a API, é necessário estar autenticado.

---

## Como rodar o projeto completo (Back-end + Front-end)

### Passo 1: Rode o servidor do Back-end (Django)

No diretório do back-end (`Interface_OCI`):

```bash
# Ative o ambiente virtual, se necessário
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# Execute as migrações (se ainda não fez)
python manage.py migrate

# Rode o servidor Django
python manage.py runserver
```

O back-end estará disponível em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

### Passo 2: Rode o servidor do Front-end (Vite)

Abra um novo terminal, navegue até o diretório do front-end (por exemplo, `FASE1-PSPET-2025.1-Frontend`) e execute:

```bash
# Instale as dependências (apenas na primeira vez)
npm install

# Rode o servidor de desenvolvimento
npm run dev
```

O front-end estará disponível em [http://localhost:5173/](http://localhost:5173/)

---

### Observações

- O front-end se comunica com o back-end via API REST.
- Certifique-se de que ambos os servidores estejam rodando ao mesmo tempo.
- Se necessário, ajuste as URLs da API no front-end para apontar para `http://127.0.0.1:8000/`.
- Para autenticação funcionar corretamente, ambos devem rodar no mesmo computador ou configurar CORS no Django.

---

## Observações

- As bibliotecas nativas para leitura de gabarito devem estar presentes no diretório do projeto.
- O sistema foi desenvolvido para fins acadêmicos.

---
