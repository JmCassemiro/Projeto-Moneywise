# Quickstart: Backend Unit and Integration Tests

Este guia descreve como executar a suite planejada para testes unitarios e de integracao do backend MoneyWise depois que as tasks forem implementadas.

## 1. Preparar ambiente Python

Ative a virtualenv do projeto:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
. .\.venv\Scripts\Activate.ps1
```

Instale dependencias:

```powershell
pip install -r requirements.txt
```

## 2. Conferir variaveis de teste

A configuracao de teste usa `TEST_DATABASE_URL` em `config.py`.

Exemplo para execucao dentro do Docker:

```text
TEST_DATABASE_URL=postgresql://postgres:senha@db_container:5432/moneywise_test
```

Exemplo para execucao local fora do Docker:

```text
TEST_DATABASE_URL=postgresql://postgres:senha@localhost:5432/moneywise_test
```

Use um banco dedicado a testes. Nunca aponte `TEST_DATABASE_URL` para desenvolvimento ou producao.

## 3. Executar testes unitarios

```powershell
pytest tests/unit
```

Resultado esperado:

- Nao depende de banco.
- Nao envia email real.
- Valida regras puras, validacoes, tokens, erros e calculos.

## 4. Executar testes de integracao

```powershell
pytest tests/integration
```

Resultado esperado:

- Usa `create_app('testing')`.
- Usa banco definido em `TEST_DATABASE_URL`.
- Cria e limpa dados entre testes.
- Valida repositories, services e rotas Flask.

## 5. Executar todos os testes backend com cobertura

```powershell
pytest tests/unit tests/integration --cov=app
```

Resultado esperado:

- Relatorio de cobertura sobre o pacote `app`.
- Testes Playwright nao sao executados por este comando.

## 6. Validacoes manuais de qualidade

Antes de considerar a implementacao pronta:

- Confirmar que `pytest tests/unit` passa duas vezes seguidas.
- Confirmar que `pytest tests/integration` passa duas vezes seguidas.
- Confirmar que nenhum email real foi enviado.
- Confirmar que dados de teste nao ficaram no banco apos a execucao.
- Confirmar que arquivos Playwright em `tests/specs/`, `tests/fixtures/` e `tests/page-objects/` nao foram alterados.

## 7. Problemas comuns

### Banco `db_container` nao resolve localmente

Se os testes estiverem rodando fora do Docker, troque o host de `TEST_DATABASE_URL` para `localhost` e a porta publicada do PostgreSQL.

### CSRF bloqueando POSTs

Confirme que `WTF_CSRF_ENABLED` esta falso no ambiente de teste.

### Pytest tentando coletar TypeScript

Configure o pytest para coletar apenas arquivos Python `test_*.py` nas pastas `tests/unit` e `tests/integration`, ou execute sempre os comandos com diretorios explicitos.
