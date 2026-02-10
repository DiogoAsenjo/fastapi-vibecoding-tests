# CRUD — FastAPI

Projeto criado com o intuido de entender um pouco mais de FastAPI, criado utilizando IA tentando manter boas práticas de código e separação de responsabilidades, além de poder ser reutilizado em outros projetos simples.

## Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop/)

## Como rodar

### 1. Subir o banco de dados

```bash
docker-compose up -d
```

Isso sobe um PostgreSQL 16 na porta `5432` com as credenciais:

| Campo   | Valor       |
| ------- | ----------- |
| Host    | `localhost` |
| Porta   | `5432`      |
| Usuário | `postgres`  |
| Senha   | `postgres`  |
| Banco   | `database`  |

### 2. Criar e ativar o virtual environment

```bash
python -m venv venv
```

**Windows (PowerShell):**

```bash
.\venv\Scripts\Activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar o servidor

```bash
uvicorn app:app --reload
```

O servidor sobe em **http://localhost:8000**.

## Documentação da API

Com o servidor rodando, acesse:

- **Swagger UI:** http://localhost:8000/docs

## Estrutura do projeto

```
├── app.py                                  # Entry point — FastAPI + exception handler global
├── config.py                               # Settings via pydantic-settings (.env)
├── database.py                             # Engine, Session, Base (SQLAlchemy)
├── docker-compose.yml                      # PostgreSQL 16
├── .env                                    # Variáveis de ambiente
├── requirements.txt                        # Dependências
├── common/
│   └── api_response.py                     # ApiResponse[T] — wrapper padrão de resposta
└── character/
    ├── character.py                        # Entidade de domínio (dataclass)
    ├── character_schema.py                 # DTOs Pydantic (Create, Update, Response)
    ├── character_model.py                  # Modelo ORM (tabela no banco)
    ├── router/
    │   └── character_router.py             # Endpoints FastAPI
    ├── service/
    │   └── character_service.py            # Regras de negócio
    └── repository/
        └── character_repository.py         # Acesso a dados
```
