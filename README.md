# ECOPA-system

Sistema desktop para gestão de pontos de coleta de materiais recicláveis: cadastro de gerentes, coletas, estoque (lotes), destinações e pedidos de remessa.

## Funcionalidades

- **Login de gerente** — autenticação por nome de usuário e senha
- **Dashboard** — resumo de coletas, gráficos e métricas de desempenho
- **Cadastros** — gerentes, pontos de coleta, coletas, destinações e pedidos
- **Estoque (lotes)** — controle de lotes gerados a partir de coletas realizadas
- **Distribuição de estoque** — consumo de lotes por pedidos (`pedido_lote`)
- **Relatórios** — consultas com filtro por data e status
- **Cache em memória** — consultas frequentes com TTL para melhorar performance

## Tecnologias

- Python 3.x
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) — interface gráfica
- MySQL — banco de dados (`mysql-connector-python`)
- matplotlib — gráficos do dashboard
- python-dotenv — variáveis de ambiente
- pywinstyles — efeitos visuais da janela (Windows)

## Pré-requisitos

- Python 3.10 ou superior
- MySQL Server (8.0 recomendado)
- MySQL Workbench (opcional, para administrar o banco)

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ECOPA-system.git
cd ECOPA-system

# 2. Crie um ambiente virtual
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
copy .env.example .env   # Windows
cp .env.example .env     # Linux/macOS
```

Edite o arquivo `.env` com os dados da sua conexão:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=ecopa_system
```

## Configuração do banco de dados

Importe o script de criação do schema no MySQL:

```bash
mysql -u root -p < database/database.sql
```

Ou no MySQL Workbench: **File → Open SQL Script** → selecione `database/database.sql` → **Execute**.

O script cria o schema `ecopa_system` com as tabelas:

- `gerente` — usuários do sistema
- `ponto_de_coleta` — pontos de coleta
- `horario_ponto` — horários de funcionamento dos pontos
- `coleta` — coletas realizadas nos pontos
- `lote` — estoque gerado a partir das coletas
- `destinacao` — centros de destino do material
- `pedido` — remessas para destinações
- `pedido_lote` — relação N:N entre pedidos e lotes

- use sempre aspas simples (`'`) para valores de string no MySQL. Aspas duplas (`"`) são interpretadas como nomes de colunas.

## Executando

```bash
python main.py
```

## Gerar executável e instalador

### 1. Gerar o executável (.exe) com PyInstaller

```bash
pyinstaller --name ECOPA --icon assets/icone.ico --onefile --windowed --add-data "assets;assets" --add-data "database.sql;." --add-data ".env;." main.py
```

O executável será gerado em `dist/ECOPA.exe`.

### 2. Criar o instalador com Inno Setup

1. Baixe e instale o [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Abra o arquivo `ECOPA-setup.iss` no Inno Setup
3. Pressione `Ctrl+F9` (ou vá em **Build > Compile**)
4. O instalador será gerado em `installer/ECOPA-Setup.exe`

### Configuração do Inno Setup

O arquivo `ECOPA-setup.iss` já está configurado no projeto. Ele inclui:

- Instalação na pasta `Program Files\ECOPA`
- Atalho na área de trabalho
- Atalho no menu iniciar
- Ícone personalizado

## Estrutura do projeto

```
├── main.py                   # Ponto de entrada
├── requirements.txt          # Dependências
├── ECOPA-setup.iss           # Script do Inno Setup (instalador)
├── .env.example              # Modelo de configuração
├── database/
│   ├── database.sql          # Script de criação do schema
│   ├── conecta_database.py   # Pool de conexões MySQL
│   └── cache.py              # Cache em memória (TTL)
├── controllers/              # Lógica de negócio
├── models/                   # Acesso ao banco (CRUD)
├── views/                    # Telas da interface (customtkinter)
└── assets/                   # Imagens e ícones
```
