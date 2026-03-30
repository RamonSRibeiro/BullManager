# BullManager

Sistema desenvolvido em Django para gerenciamento veterinário.

## 🚀 Pré-requisitos

Antes de começar, você precisa ter instalado em sua máquina:

- [Python 3.10+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (opcional, mas recomendado)
- Git

## 📦 Instalação

1. Clone o repositório:
git clone https://github.com/seuusuario/BullManager.git
cd BullManager-main

   
2- Crie e ative um ambiente virtual:
python -m venv venv
# Windows (PowerShell)
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

3- Instale as dependências:

pip install -r requirements.txt

4- Para gerar uma chave secreta segura:

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

⚙️ Configuração inicia
1- Execute as migrações:
python manage.py migrate

2-Crie um superusuário para acessar o painel administrativo:
python manage.py createsuperuser

3- Inicie o servidor de desenvolvimento:
python manage.py runserver

4- Acesse no navegador:
http://127.0.0.1:8000/

📂 Estrutura do projeto
- core/ → Configurações principais do Django
- veterinaria/ → Aplicação veterinária
- manage.py → Utilitário para comandos Django
- .env → Variáveis de ambiente (não deve ser versionado)
🛠️ Ambiente de produção
- Defina DEBUG=False no .env
- Configure ALLOWED_HOSTS com o domínio ou IP do servidor
- Use um servidor WSGI/ASGI (ex: Gunicorn, Daphne) atrás de um servidor web (ex: Nginx)

✅ Checklist rápido
- [ ] Criar .env com SECRET_KEY, DEBUG, ALLOWED_HOSTS
- [ ] Instalar dependências
- [ ] Rodar migrate
- [ ] Criar superusuário
- [ ] Rodar runserver

Feito isso, o sistema estará pronto para uso!





