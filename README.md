# Gerenciador Bovino

## Descrição

O **Gerenciador Bovino** é uma aplicação web desenvolvida em Django para o gerenciamento de bovinos em um contexto veterinário. O sistema permite o cadastro de animais, controle de coletas de sêmen, rastreamento de estoque e validade dos lotes, além de funcionalidades para registro de saídas e alertas automáticos.

### Funcionalidades Principais

- **Cadastro de Bovinos**: Adicione, edite e visualize detalhes dos animais, incluindo fotos, raça, data de nascimento e exames andrológicos.
- **Controle de Coletas de Sêmen**: Registre coletas com dados laboratoriais (motilidade, vigor), gere códigos de lote automaticamente e monitore o estoque.
- **Rastreamento de Saídas**: Registre saídas de sêmen para inseminação própria, vendas ou descartes, com controle de destino e observações.
- **Dashboard com Alertas**: Visualize o estoque total, alertas de estoque crítico e lotes próximos ao vencimento (30 dias).
- **Importação de Dados**: Importe bovinos em massa via arquivo Excel.
- **Busca e Filtros**: Pesquise animais por nome ou ID.
- **Relatórios**: Gere relatórios detalhados para cada bovino.

## Tecnologias Utilizadas

- **Backend**: Django 6.0.3
- **Banco de Dados**: SQLite
- **Bibliotecas Python**:
  - pandas: Para manipulação de dados e importação de Excel
  - openpyxl: Suporte para arquivos Excel
  - Pillow: Processamento de imagens para upload de fotos
- **Frontend**: HTML/CSS (templates Django)

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd gerenciador_bovino
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto com:
     ```
     SECRET_KEY=sua-chave-secreta-aqui
     DEBUG=True
     ```

5. **Execute as migrações do banco de dados**:
   ```bash
   python manage.py migrate
   ```

6. **Inicie o servidor**:
   ```bash
   python manage.py runserver
   ```

   Acesse a aplicação em `http://127.0.0.1:8000/`.

## Uso

- **Página Inicial**: Lista todos os bovinos com dashboard de alertas.
- **Adicionar Bovino**: Use o formulário para cadastrar novos animais.
- **Detalhes do Bovino**: Visualize informações completas, fotos e histórico de coletas.
- **Registrar Coleta**: Adicione novas coletas de sêmen com dados laboratoriais.
- **Registrar Saída**: Controle as saídas de sêmen.
- **Importar Bovinos**: Faça upload de um arquivo Excel para importar múltiplos animais.

## Estrutura do Projeto

```
gerenciador_bovino/
├── core/                 # Configurações principais do Django
├── veterinaria/          # App principal
│   ├── models.py         # Modelos de dados (Boi, ColetaSemen, etc.)
│   ├── views.py          # Lógica das views
│   ├── forms.py          # Formulários Django
│   ├── templates/        # Templates HTML
│   └── migrations/       # Migrações do banco
├── media/                # Arquivos de mídia (fotos)
├── db.sqlite3            # Banco de dados
├── manage.py             # Script de gerenciamento Django
└── requirements.txt      # Dependências Python
```

