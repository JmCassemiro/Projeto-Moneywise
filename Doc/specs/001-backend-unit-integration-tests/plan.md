# Implementation Plan: Backend Unit and Integration Tests

**Branch**: `001-backend-unit-integration-tests` | **Date**: 2026-05-14 | **Spec**: `Doc/specs/001-backend-unit-integration-tests/spec.md`

**Input**: Feature specification from `Doc/specs/001-backend-unit-integration-tests/spec.md`

## Summary

Adicionar uma suite Python de testes unitarios e de integracao para o backend Flask do MoneyWise. A implementacao deve usar pytest, app factory em modo testing, fixtures para banco e cliente Flask, mocks para email e separacao clara entre `tests/unit/` e `tests/integration/`. O escopo nao inclui Playwright, frontend ou mudancas de produto.

## Technical Context

**Language/Version**: Python 3.x usado pela virtualenv atual do projeto.

**Primary Dependencies**: Flask 3.1.0, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.40, Flask-JWT-Extended 4.7.1, Flask-WTF 1.2.2, Flask-Mail 0.10.0, Flask-Bcrypt 1.0.1.

**Storage**: PostgreSQL via `DATABASE_URL` e `TEST_DATABASE_URL`.

**Testing**: pytest, pytest-mock, pytest-cov. pytest-flask opcional.

**Target Platform**: Backend web Flask executado localmente, em Docker ou em ambiente CI futuro.

**Project Type**: Web application backend.

**Performance Goals**: Testes unitarios devem executar rapidamente sem banco. Testes de integracao devem priorizar determinismo e isolamento.

**Constraints**: Nao alterar testes Playwright existentes. Nao enviar emails reais. Nao usar banco de desenvolvimento/producao. Evitar abstracoes novas alem de fixtures/helpers de teste.

**Scale/Scope**: Cobertura inicial dos modulos `transactions`, `users_authentication`, `statistics`, `home`, `errors` e `exceptions`.

## Constitution Check

_GATE: Must pass before implementation and re-check after fixtures are designed._

- [x] Specification-first: PRD, spec, research, plan e tasks existem antes da implementacao.
- [x] Scope control: somente testes unitarios e de integracao backend.
- [x] No product behavior change: codigo de produto so muda se necessario para testabilidade ou bug revelado.
- [x] Test-first: tarefas priorizam criar testes antes de qualquer ajuste de implementacao.
- [x] Integration realism: integracao usa app factory real, blueprints reais e banco de teste.
- [x] Simplicity: sem framework novo alem do necessario para pytest/cobertura.
- [x] Isolation: fixtures devem limpar estado entre testes.

## Project Structure

### Documentation (this feature)

```text
Doc/
├── PRD.md
└── specs/
    └── 001-backend-unit-integration-tests/
        ├── spec.md
        ├── research.md
        ├── plan.md
        ├── quickstart.md
        └── tasks.md
```

### Source Code (repository root)

```text
app/
├── home/
├── statistics/
├── transactions/
└── users_authentication/

tests/
├── conftest.py
├── unit/
│   ├── test_transaction_service.py
│   ├── test_statistics_service.py
│   ├── test_user_service.py
│   ├── test_password_reset_service.py
│   ├── test_forms.py
│   ├── test_tokens.py
│   └── test_errors.py
├── integration/
│   ├── test_user_repository_and_service.py
│   ├── test_transaction_repository_and_service.py
│   ├── test_statistics_integration.py
│   ├── test_auth_routes.py
│   ├── test_transaction_routes.py
│   ├── test_statistics_routes.py
│   └── test_home_routes.py
├── specs/              # Existing Playwright E2E tests, unchanged
├── fixtures/           # Existing Playwright fixtures, unchanged
└── page-objects/       # Existing Playwright page objects, unchanged
```

**Structure Decision**: Usar a pasta `tests/` existente, adicionando `unit/`, `integration/` e `conftest.py`. Os arquivos TypeScript de Playwright permanecem no local atual sem alteracao.

## Implementation Approach

1. Adicionar dependencias de teste Python.
2. Configurar pytest para ignorar ou nao coletar arquivos TypeScript.
3. Criar fixtures base para app, db, client, usuario, transacao, cliente autenticado e mail mockado.
4. Implementar testes unitarios de regras puras.
5. Implementar testes de integracao de banco.
6. Implementar testes de integracao de rotas Flask.
7. Rodar comandos de validacao e ajustar somente bugs reais encontrados.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --------- | ---------- | ------------------------------------ |
| None      | N/A        | N/A                                  |
