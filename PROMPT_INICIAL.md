# Prompt Base — Template de Projeto FastAPI

Use este prompt no início de qualquer projeto pessoal para gerar a estrutura completa.
Substitua os valores entre `{{}}` pelo domínio do seu projeto.

---

## Prompt

```
Aja como um especialista em Python e FastAPI. Use boas práticas de programação.

## Projeto
CRUD completo de {{DOMÍNIO}} (ex: personagens, produtos, tarefas).
Propriedades da entidade:
- {{PROPRIEDADE_1}} ({{TIPO}})
- {{PROPRIEDADE_2}} ({{TIPO}})
- {{PROPRIEDADE_3}} ({{TIPO}})
- ...

## Stack
- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy ORM
- PostgreSQL (via Docker)
- Pydantic para schemas/DTOs
- pydantic-settings para configuração (.env)

## Arquitetura
Separação por domínio com camadas explícitas (inspirado em Clean Architecture simplificada).
Cada domínio segue a mesma estrutura de pastas:

```

app.py # Entry point — FastAPI, exception handler global, registro de routers
config.py # Settings via pydantic-settings (lê do .env)
database.py # Engine, SessionLocal, Base, get_db (generator de session por request)
.env # DATABASE_URL
requirements.txt # Dependências
common/
├── **init**.py
└── api_response.py # ApiResponse[T] genérico — wrapper padrão de toda resposta
{{dominio}}/
├── **init**.py
├── {{dominio}}.py # Entidade de domínio (dataclass pura, sem dependência de framework)
├── {{dominio}}\_schema.py # DTOs Pydantic: Create, Update, Response (contrato HTTP)
├── {{dominio}}\_model.py # Modelo ORM SQLAlchemy (representa a tabela no banco)
├── router/
│ ├── **init**.py
│ └── {{dominio}}\_router.py # Endpoints FastAPI — recebe request, chama service, retorna response
├── service/
│ ├── **init**.py
│ └── {{dominio}}\_service.py # Regras de negócio — orquestra operações, converte schema → entidade
├── repository/
│ ├── **init**.py
│ └── {{dominio}}\_repository.py # Acesso a dados — CRUD via SQLAlchemy Session
└── exceptions/
├── **init**.py
└── {{dominio}}\_exception.py # Exceção de domínio — lançada pelo service, capturada pelo router

```

## Convenções

### Nomenclatura
- Tudo em snake_case (arquivos, variáveis, funções) — padrão Python.
- Classes em PascalCase.
- Toda pasta que é importável tem __init__.py.

### ApiResponse genérico
- Todas as respostas (sucesso e erro) seguem o formato: { "message": "...", "data": ... }
- Usar Generic[T] do Pydantic para tipar o data.
- Exception handler global no app.py intercepta HTTPException e retorna no mesmo formato.

### Separação de representações da entidade
- {{Dominio}} (dataclass)       → entidade de domínio pura
- {{Dominio}}Schema (Pydantic)  → DTOs de entrada/saída da API
- {{Dominio}}Model (SQLAlchemy) → mapeamento ORM para o banco

### Fluxo de uma request
Request HTTP
  → router (valida com schema, injeta service via Depends)
    → service (aplica regras de negócio, chama repository)
      → repository (persiste/consulta via ORM, retorna entidade de domínio)
    ← retorna entidade
  ← envolve em ApiResponse, serializa com schema de response
Response HTTP

### Injeção de dependência
- Usar Depends() do FastAPI.
- Factory get_service() no router monta a cadeia: Session → Repository → Service.
- O repository recebe a Session do banco via construtor.
- O service recebe o repository via construtor.

### Exceções de domínio
- Cada domínio tem sua própria exceção (ex: {{Dominio}}Exception) dentro de exceptions/.
- O service lança exceções de domínio — nunca HTTPException (sem acoplamento com o framework HTTP).
- O router captura a exceção de domínio e traduz para HTTPException com o status code adequado (ex: 400).
- Isso mantém o service reutilizável fora do contexto HTTP (CLI, workers, scripts, etc.).

### Status codes explícitos
- POST   → 201 Created
- GET    → 200 OK
- PUT    → 200 OK
- DELETE → 200 OK (retorna ApiResponse com message, não 204)
- Erros  → HTTPException com status adequado (404, 400, etc.)

### Banco de dados
- PostgreSQL via SQLAlchemy.
- URL de conexão no .env, lida pelo pydantic-settings.
- Base.metadata.create_all no app.py para criar tabelas (em produção, usar Alembic).
- Session gerenciada por generator (get_db) com yield + finally close.
- Repository converte Model ↔ Entidade de domínio internamente (_to_entity).

## Gere todos os arquivos de uma vez seguindo essa estrutura.
```

---

## Exemplo preenchido

```
Projeto: CRUD de personagens.
Domínio: character
Propriedades:
- name (str)
- health_points (int)
- attack (int)
- defense (int)
```
