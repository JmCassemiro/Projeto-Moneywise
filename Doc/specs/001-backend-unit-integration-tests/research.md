# Research: Backend Unit and Integration Tests

## Decision 1: Test runner

**Decision**: Usar `pytest` como runner principal.

**Rationale**: O projeto Flask se beneficia de fixtures para app, client, banco, usuarios, transacoes e mocks. `pytest` reduz repeticao em comparacao com `unittest` e permite separar suites por diretorio.

**Alternatives considered**:

- `unittest`: disponivel na biblioteca padrao, mas gera mais boilerplate para fixtures e parametrizacao.
- `pytest-flask`: util, mas opcional. O app factory atual permite criar fixtures com Flask test client diretamente.

## Decision 2: Dependencies

**Decision**: Adicionar dependencias de teste Python no momento da implementacao.

Recommended dependencies:

- `pytest`: runner e fixtures.
- `pytest-mock`: mocks integrados ao pytest.
- `pytest-cov`: relatorio de cobertura.

Optional dependency:

- `pytest-flask`: usar somente se simplificar fixtures sem esconder comportamento importante.

## Decision 3: Test directory structure

**Decision**: Manter a pasta `tests/` existente e adicionar subpastas Python separadas.

```text
tests/
├── conftest.py
├── unit/
└── integration/
```

**Rationale**: A estrutura preserva os testes Playwright existentes em `tests/specs/`, `tests/fixtures/` e `tests/page-objects/`, enquanto cria uma separacao clara para testes backend Python.

## Decision 4: Integration database

**Decision**: Usar PostgreSQL de teste via `TEST_DATABASE_URL`.

**Rationale**: A aplicacao usa PostgreSQL, SQLAlchemy e migracoes Alembic. A integracao deve validar comportamento de queries, ordenacao, filtros, constraints e relacionamentos no banco mais proximo possivel do real.

**Fallback**: SQLite em memoria pode ser considerado somente para testes locais rapidos, mas nao deve substituir a suite de integracao principal.

## Decision 5: App factory and config

**Decision**: Criar fixture `app` com `create_app('testing')`.

**Rationale**: O projeto ja possui app factory e `TestingConfig`. Isso evita servidor real e permite usar Flask test client, contexto de aplicacao, extensoes e blueprints reais.

## Decision 6: Database lifecycle

**Decision**: Usar fixtures para criar schema antes dos testes de integracao e limpar dados entre testes.

Recommended approach:

- Inicializar app em modo testing.
- Usar `db.create_all()` ou migracoes em banco de teste conforme decisao de implementacao.
- Limpar tabelas entre testes ou usar transacoes com rollback.
- Garantir que cada teste tenha estado independente.

## Decision 7: Email and external effects

**Decision**: Mockar `mail.send` nos testes unitarios e capturar/verificar chamada nos testes de integracao quando necessario.

**Rationale**: Testes nao devem enviar email real. O valor do teste esta em validar destinatario, assunto, corpo e fluxo de erro/sucesso.

## Decision 8: Authentication helpers

**Decision**: Criar helper de cliente autenticado para testes de rotas protegidas.

**Rationale**: Varias rotas usam JWT em cookies. Um helper reduz repeticao e garante consistencia ao configurar cookies de acesso nos testes.

## Decision 9: Coverage strategy

**Decision**: Cobertura inicial orientada por risco, nao por porcentagem absoluta.

Priority order:

1. Transacoes e isolamento por usuario.
2. Autenticacao, perfil e reset de senha.
3. Estatisticas financeiras.
4. Erros e rotas publicas.
5. Casos adicionais de borda.

## Risks

- `TEST_DATABASE_URL` usa `db_container`, que funciona dentro do Docker. Em execucao local Windows fora do Docker, pode ser necessario configurar host/porta local.
- Fixtures de banco mal isoladas podem causar testes flakey.
- Testes de rota podem depender de textos de template se forem escritos de forma fragil; preferir status, redirecionamentos, cookies, JSON e estado persistido.
- CSRF pode bloquear POSTs em testes se `WTF_CSRF_ENABLED` nao estiver falso no ambiente testing.
