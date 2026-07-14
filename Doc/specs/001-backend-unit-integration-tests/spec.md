# Feature Specification: Backend Unit and Integration Tests

**Feature Branch**: `001-backend-unit-integration-tests`
**Created**: 2026-05-14
**Status**: Draft
**Input**: Criar PRD, specs e tasks para adicionar somente testes unitarios e de integracao ao backend MoneyWise.

## User Scenarios & Testing

### User Story 1 - Verificar regras de dominio com testes unitarios (Priority: P1)

Como pessoa mantenedora do MoneyWise, eu quero uma suite de testes unitarios para regras puras do backend, para receber feedback rapido quando validacoes, calculos ou formatos forem alterados.

**Why this priority**: Regras de transacao, autenticacao, estatisticas e erro sao o nucleo da aplicacao. Elas devem falhar rapidamente sem exigir banco, browser ou servidor real.

**Independent Test**: Executar `pytest tests/unit` deve validar regras de servicos, modelos, formularios, tokens, erros e helpers com mocks quando necessario.

**Acceptance Scenarios**:

1. **Given** dados validos de transacao, **When** o servico limpa e converte o formulario, **Then** valores monetarios, datas, horarios, recorrencia e tipo sao normalizados corretamente.
2. **Given** dados invalidos de transacao, **When** campos obrigatorios, valor, data, hora ou tipo forem processados, **Then** uma excecao de validacao clara e retornada.
3. **Given** uma lista de transacoes em memoria, **When** o dashboard estatistico for calculado, **Then** receitas, despesas, saldo, categorias, meses e top 5 despesas ficam corretos.
4. **Given** regras de senha e token, **When** senha fraca, token invalido ou token expirado forem avaliados, **Then** o comportamento esperado e validado sem envio real de email.
5. **Given** excecoes da aplicacao, **When** forem serializadas, **Then** status e mensagens seguem o contrato esperado.

---

### User Story 2 - Verificar persistencia e isolamento com testes de integracao (Priority: P2)

Como pessoa mantenedora do MoneyWise, eu quero testes de integracao com banco de teste para confirmar que repositories e services persistem, filtram e isolam dados corretamente.

**Why this priority**: O sistema lida com dados financeiros por usuario. Erros de query ou isolamento podem expor dados ou produzir relatorios incorretos.

**Independent Test**: Executar `pytest tests/integration` com `TEST_DATABASE_URL` deve criar, consultar, atualizar e remover dados em banco de teste limpo.

**Acceptance Scenarios**:

1. **Given** dois usuarios com transacoes distintas, **When** transacoes forem listadas para um usuario, **Then** apenas dados daquele usuario sao retornados.
2. **Given** transacoes com datas, tipos, categorias, valores e metodos diferentes, **When** filtros forem aplicados, **Then** a consulta retorna apenas registros correspondentes e na ordenacao esperada.
3. **Given** uma operacao de criacao, atualizacao ou exclusao valida, **When** o servico executar a operacao, **Then** o banco reflete o novo estado.
4. **Given** erro de persistencia, **When** a operacao falhar, **Then** rollback e excecao de validacao sao aplicados.
5. **Given** transacoes persistidas, **When** estatisticas forem calculadas, **Then** os agregados usam somente os dados do usuario autenticado.

---

### User Story 3 - Verificar fluxos Flask com testes de integracao de rotas (Priority: P3)

Como pessoa mantenedora do MoneyWise, eu quero testes de integracao usando Flask test client para garantir que rotas publicas, protegidas e autenticadas respondam corretamente.

**Why this priority**: As rotas conectam formularios, cookies JWT, flashes, templates e servicos. Elas precisam ser verificadas sem depender de Playwright.

**Independent Test**: Executar os testes de rotas em `tests/integration` deve validar status HTTP, redirecionamentos, cookies, payloads JSON e protecao de paginas.

**Acceptance Scenarios**:

1. **Given** cliente nao autenticado, **When** acessar rotas protegidas, **Then** o usuario e redirecionado para signin e cookies JWT sao limpos.
2. **Given** usuario valido, **When** fizer signin, **Then** recebe cookie JWT e redirecionamento para transacoes.
3. **Given** usuario autenticado, **When** criar, editar ou excluir transacao via rota, **Then** o comportamento HTTP e o estado do banco ficam corretos.
4. **Given** usuario autenticado, **When** atualizar perfil ou excluir conta, **Then** respostas JSON/redirecionamentos seguem o contrato.
5. **Given** erro no carregamento de estatisticas, **When** a rota `/statistics/` for acessada, **Then** flash e redirecionamento seguro sao aplicados.

## Edge Cases

- Valor monetario com virgula, ponto, texto invalido, vazio ou nulo.
- Data e hora vazias, em formato invalido ou fora do formato esperado.
- Tipo de transacao diferente de `income` e `expense`.
- Transacao recorrente com numero de parcelas ausente ou invalido.
- Usuario inexistente, email duplicado e nome duplicado.
- Senha incorreta ao excluir conta.
- Senha fraca em cadastro ou reset.
- Token de reset invalido, expirado ou de usuario inexistente.
- JWT ausente, expirado ou invalido em pagina protegida.
- Historico de transacoes vazio.
- Tentativa de acessar transacao pertencente a outro usuario.
- Respostas 404 e 500 para clientes HTML e JSON.
- Falha de envio de email sem envio real em teste.

## Requirements

### Functional Requirements

- **FR-001**: A suite MUST incluir testes unitarios para regras de transacoes, usuarios, estatisticas, tokens, formularios e erros.
- **FR-002**: A suite MUST incluir testes de integracao para repositories e services que dependem de banco.
- **FR-003**: A suite MUST incluir testes de integracao para rotas Flask publicas e protegidas.
- **FR-004**: A suite MUST manter testes Playwright/E2E fora do escopo desta feature.
- **FR-005**: Testes unitarios MUST evitar banco real, servidor real e envio real de email.
- **FR-006**: Testes de integracao MUST usar configuracao de teste e banco separado de desenvolvimento/producao.
- **FR-007**: Fixtures MUST limpar dados entre testes para garantir determinismo.
- **FR-008**: Rotas protegidas MUST ser testadas com usuario autenticado e nao autenticado.
- **FR-009**: Operacoes financeiras MUST validar isolamento por usuario.
- **FR-010**: Comandos de execucao MUST permitir rodar unitarios, integracao e cobertura separadamente.

### Key Entities

- **User**: Conta autenticavel com email, nome, senha, aniversario e relacionamento com transacoes.
- **Transaction**: Registro financeiro com valor, tipo, categoria, metodo, datas, recorrencia e usuario dono.
- **Dashboard Statistics**: Agregados derivados de transacoes por usuario, incluindo saldos, categorias, series mensais e top despesas.
- **Reset Token**: Token temporario usado para recuperacao de senha.
- **App Error**: Erro de dominio serializavel com mensagem e status HTTP.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `pytest tests/unit` executa com sucesso sem depender de banco.
- **SC-002**: `pytest tests/integration` executa com sucesso usando `TEST_DATABASE_URL`.
- **SC-003**: Pelo menos transacoes, usuarios, estatisticas, reset de senha e erros possuem cobertura inicial.
- **SC-004**: Testes de integracao provam que um usuario nao acessa transacoes de outro usuario.
- **SC-005**: Emails sao mockados/capturados e nenhum email real e enviado durante testes.
- **SC-006**: A suite pode ser repetida duas vezes seguidas sem falha por estado residual.

## Assumptions

- O projeto continuara usando Flask, Flask-SQLAlchemy, Flask-JWT-Extended e PostgreSQL.
- `TestingConfig` sera reutilizado por `create_app('testing')`.
- `TEST_DATABASE_URL` apontara para banco descartavel ou dedicado a testes.
- Dependencias de teste podem ser adicionadas a `requirements.txt`.
- Mudancas funcionais so serao feitas se forem necessarias para permitir testabilidade ou corrigir bug revelado pela suite.
