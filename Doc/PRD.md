# PRD: Testes Unitarios e de Integracao Backend MoneyWise

**Data**: 2026-05-14
**Status**: Draft
**Escopo**: Somente testes unitarios e testes de integracao do backend Flask

## Objetivo

Criar uma base de testes automatizados para o backend do MoneyWise que valide regras de dominio, persistencia, autenticacao, fluxos de rotas Flask e tratamento de erros sem alterar funcionalidades de produto. O projeto atualmente possui testes E2E com Playwright, mas nao possui uma suite Python dedicada a testes unitarios e de integracao.

## Problema

A aplicacao possui regras importantes em servicos, repositorios, formularios, tokens, autenticacao JWT, estatisticas financeiras e transacoes monetarias. Sem testes unitarios e de integracao, mudancas futuras podem quebrar validacoes, filtros, isolamento por usuario, persistencia e respostas HTTP sem feedback rapido.

## Objetivos de Produto

- Garantir que regras criticas do backend sejam verificadas de forma rapida e repetivel.
- Separar claramente testes unitarios, testes de integracao e testes E2E existentes.
- Permitir evolucao segura das features de usuarios, transacoes e estatisticas.
- Criar uma base de fixtures reutilizavel para testes futuros.
- Validar integracao real com Flask, SQLAlchemy e banco de teste.

## Fora de Escopo

- Criar ou alterar testes Playwright/E2E.
- Criar testes de frontend, CSS, acessibilidade visual ou snapshots de UI.
- Alterar regras de negocio da aplicacao.
- Refatorar arquitetura alem do necessario para testabilidade.
- Criar pipelines CI/CD neste momento.

## Estado Atual

- Backend Flask com app factory em `app/__init__.py`.
- Configuracao de teste existente em `config.py` via `TestingConfig`.
- Variavel `TEST_DATABASE_URL` ja prevista para banco de teste.
- Persistencia com Flask-SQLAlchemy e migracoes Alembic.
- Testes existentes sao TypeScript/Playwright em `tests/specs/`.
- Nao existe estrutura Python para `tests/unit/` ou `tests/integration/`.
- `requirements.txt` ainda nao lista ferramentas de teste Python como `pytest`, `pytest-mock` e `pytest-cov`.

## Areas Prioritarias de Cobertura

1. Transacoes
   - Validacao e parsing de formulario.
   - Valores monetarios, datas, horarios, recorrencia e tipos de transacao.
   - Filtros por usuario, periodo, valor, categoria, metodo de pagamento e texto.
   - Criacao, edicao, exclusao e isolamento entre usuarios.

2. Usuarios e Autenticacao
   - Cadastro com email/nome duplicados.
   - Autenticacao por email e senha.
   - Atualizacao de perfil.
   - Exclusao de conta com confirmacao de senha.
   - Cookies JWT e redirecionamentos de paginas protegidas.

3. Reset de Senha
   - Geracao e confirmacao de token.
   - Token invalido ou expirado.
   - Envio de email mockado.
   - Atualizacao efetiva da senha.

4. Estatisticas
   - Somatorios de receitas e despesas.
   - Agrupamento por categoria.
   - Series mensais.
   - Top 5 despesas.
   - Historico vazio.

5. Erros e Excecoes
   - Conversao de `AppError` para JSON.
   - Respostas 404 e 500 para clientes HTML e JSON.
   - Mensagens de validacao consistentes.

6. Home e Contato
   - Renderizacao basica das paginas publicas.
   - Envio de mensagem de contato com mail mockado.

## Requisitos Funcionais

- RF-001: A suite deve separar testes unitarios em `tests/unit/` e testes de integracao em `tests/integration/`.
- RF-002: Testes unitarios devem validar funcoes e servicos sem depender de banco, rede ou servidor real.
- RF-003: Testes de integracao devem usar o app Flask criado por `create_app('testing')`.
- RF-004: Testes de integracao com persistencia devem usar banco de teste configurado por `TEST_DATABASE_URL`.
- RF-005: Fixtures devem criar e limpar dados para evitar vazamento entre testes.
- RF-006: Rotas protegidas devem ser verificadas com e sem autenticacao JWT.
- RF-007: Operacoes de transacao devem garantir isolamento por usuario.
- RF-008: Emails devem ser mockados ou capturados em ambiente de teste, sem envio real.
- RF-009: A suite deve produzir comandos claros para execucao separada de unitarios, integracao e cobertura.
- RF-010: Testes existentes de Playwright devem permanecer inalterados.

## Requisitos Nao Funcionais

- RNF-001: Testes unitarios devem ser rapidos e independentes de banco.
- RNF-002: Testes de integracao devem ser deterministas e limpar o estado do banco.
- RNF-003: A estrutura deve ser simples e aderente ao padrao atual do projeto Flask.
- RNF-004: A cobertura inicial deve priorizar modulos de maior risco antes de atingir cobertura ampla.
- RNF-005: A documentacao deve permitir que outro agente implemente a suite sem reler todo o projeto.

## Criterios de Sucesso

- CS-001: `pytest tests/unit` executa somente testes unitarios do backend.
- CS-002: `pytest tests/integration` executa somente testes de integracao do backend.
- CS-003: `pytest tests/unit tests/integration --cov=app` gera relatorio de cobertura do backend.
- CS-004: Transacoes, usuarios, estatisticas, reset de senha e erros possuem cobertura inicial.
- CS-005: Nenhum teste E2E/Playwright e modificado por esta iniciativa.
- CS-006: Cada teste pode ser executado repetidamente sem depender de estado anterior.

## Entregaveis SDD

- `Doc/PRD.md`: este PRD.
- `Doc/specs/001-backend-unit-integration-tests/spec.md`: especificacao da feature de testes.
- `Doc/specs/001-backend-unit-integration-tests/research.md`: decisoes tecnicas.
- `Doc/specs/001-backend-unit-integration-tests/plan.md`: plano de implementacao.
- `Doc/specs/001-backend-unit-integration-tests/quickstart.md`: guia de execucao.
- `Doc/specs/001-backend-unit-integration-tests/tasks.md`: tarefas executaveis.

## Premissas

- O banco PostgreSQL de teste estara disponivel via `TEST_DATABASE_URL`.
- O ambiente local pode rodar a aplicacao com a virtualenv existente.
- Testes podem instalar dependencias Python de desenvolvimento no `requirements.txt`.
- O objetivo inicial e criar cobertura de seguranca, nao cobertura total de 100%.
