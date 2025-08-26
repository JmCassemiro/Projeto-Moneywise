# 📊 Dashboard de Controle de Gastos — Moneywise

## Sumário

* [Visão Geral](#visão-geral)
* [Arquitetura de Produção](#arquitetura-de-produção)
* [Stack Tecnológica](#stack-tecnológica)
* [Estrutura de Pastas](#estrutura-de-pastas)
* [Configuração por Ambiente](#configuração-por-ambiente)
* [Autenticação e Autorização (JWT)](#autenticação-e-autorização-jwt)
* [Módulos Funcionais](#módulos-funcionais)

  * [Usuários](#usuários)
  * [Controle de Gastos](#controle-de-gastos)
* [Banco de Dados](#banco-de-dados)
* [Camada Web (Templates e Estáticos)](#camada-web-templates-e-estáticos)
* [Observabilidade e Logs](#observabilidade-e-logs)
* [Padrões de Erro e Respostas](#padrões-de-erro-e-respostas)
* [Containerização e Orquestração](#containerização-e-orquestração)
* [Segurança](#segurança)
* [Testes](#testes)

  * [Playwright (E2E/UI)](#playwright-e2eui)
  * [Postman (API)](#postman-api)
* [Manutenção e Operação](#manutenção-e-operação)
* [Anexos](#anexos)

---

## Visão Geral

A aplicação é uma **Dashboard de Controle de Gastos** construída em **Flask** (Python), com **PostgreSQL** como banco de dados relacional. A autenticação é baseada em **JWT** (via *Flask-JWT-Extended*). A solução roda em contêineres **Docker** e é exposta por um **proxy reverso Nginx** com **HTTPS** (certificados válidos).

**Principais capacidades em produção:**

* Cadastro, autenticação e gerenciamento de usuários (JWT).
* Gestão de perfil do usuário (atualização de dados e exclusão de conta mediante confirmação de senha).
* Módulo de **controle de gastos** (cadastro/edição/exclusão/consulta) com visualização na dashboard.
* Templates HTML (Jinja2) e mensagens de feedback ao usuário.
* Persistência de dados em PostgreSQL com volume dedicado.
* Orquestração por Docker Compose, isolando *web*, *db* e *edge* (proxy).

---

## Arquitetura de Produção

**Componentes:**

* **App Web (Flask)**: expõe rotas HTTP (públicas e protegidas por JWT), renderiza templates e serve endpoints para o front-end.
* **Banco de Dados (PostgreSQL)**: armazena usuários e dados de gastos (e metadados correlatos). Persistência via volume Docker.
* **Proxy Reverso (Nginx)**: termina TLS (HTTPS) e encaminha o tráfego para o serviço *web*.
* **Certificados TLS válidos** (Let's Encrypt): arquivos montados no proxy para habilitar HTTPS em produção.

**Fluxo simplificado de requisição:**

1. Cliente → **HTTPS** → Nginx (camada edge)
2. Nginx → upstream → Flask (*web*)
3. Flask acessa **PostgreSQL** via rede interna

**Redes e isolamento:**

* Rede interna de aplicação conectando *web* ↔ *db* (não exposta ao público).
* Rede de borda (*edge*) conectando *nginx* ↔ *web* (exposta nas portas 80/443 do host).

**Volumes persistentes:**

* Dados do PostgreSQL.
* Diretório de certificados (TLS).

---

## Stack Tecnológica

* **Linguagem / Framework**: Python 3.11+, **Flask**
* **Autenticação**: **Flask-JWT-Extended** (tokens Bearer; suporte a refresh)
* **Banco de Dados**: **PostgreSQL 15**
* **Templates**: Jinja2 (HTML/CSS)
* **Proxy/Edge**: **Nginx** (terminação TLS e proxy para o *web*)
* **Containerização**: **Docker** + **Docker Compose**
* **Sistema Operacional (produção)**: Linux (Ubuntu Server)

---

## Estrutura de Pastas

```
meu_app/
├─ app/                          # Código da aplicação Flask
│  ├─ __init__.py                # Fábrica da aplicação, inicializações e registro de blueprints
│  ├─ config.py                  # Configurações centralizadas (lidas de variáveis de ambiente)
│  ├─ routes.py                  # Rotas públicas/gerais (se aplicável)
│  ├─ models.py                  # Modelos de domínio (se aplicável ao padrão adotado)
│  ├─ user_db.py                 # Camada de acesso a dados (usuários / queries ao Postgres)
│  ├─ auth/                      # Módulo de autenticação JWT
│  │  ├─ __init__.py
│  │  ├─ routes.py               # Rotas /auth (login, register, refresh, logout se aplicável)
│  │  └─ utils.py                # Funções utilitárias (hash de senha, geração/validação de tokens)
│  ├─ expenses/                  # Módulo de gastos (dashboard)
│  │  ├─ __init__.py
│  │  ├─ routes.py               # CRUD de gastos, filtros, resumo para dashboard
│  │  └─ services.py             # Regras de negócio/calculadoras/relatórios
│  ├─ templates/                 # Templates Jinja2
│  │  ├─ base.html
│  │  ├─ auth/
│  │  │  ├─ login.html
│  │  │  └─ register.html
│  │  ├─ expenses/
│  │  │  ├─ index.html           # Dashboard de gastos (cards, gráficos, tabelas)
│  │  │  └─ form.html            # Formulário de criação/edição
│  │  └─ profile.html
│  └─ static/                    # Arquivos estáticos
│     ├─ css/
│     ├─ js/
│     └─ img/
│
├─ docker/                       # Materiais de infraestrutura (sem expor conteúdo neste README)
│  ├─ nginx/
│  │  └─ nginx.conf              # Configuração do proxy reverso (produção)
│  └─ certs/                     # Estrutura para certificados TLS
│
├─ scripts/
│  └─ wait-for-it.sh             # Utilitário p/ orquestração entre web↔db
│
├─ tests/                        # Testes automatizados
│  ├─ e2e/                       # Testes E2E com Playwright
│  │  ├─ specs/                  # Casos de teste (login, fluxo de gastos, etc.)
│  │  ├─ fixtures/               # Utilidades, dados de teste, auth helpers
│  │  └─ playwright.config.ts    # Config E2E (baseURL, timeouts, reporter)
│  └─ postman/                   # Testes de API (coleção + ambiente)
│     ├─ collection.json         # Coleção de requests (auth, gastos, usuários)
│     └─ environment.json        # Variáveis (baseUrl, tokens, ids)
│
├─ .env.example                  # Exemplo de variáveis de ambiente para execução
├─ Dockerfile                    # Build do serviço web (Flask)
├─ docker-compose.yml            # Orquestração: web, db, proxy, certificados (produção)
└─ README.md                     # Este documento
```

> **Observação:** nomes de arquivos/pastas podem variar levemente; a estrutura acima representa a organização **em produção** e os papéis de cada componente.

---

## Configuração por Ambiente

A aplicação lê configurações via **variáveis de ambiente**. *Chaves típicas utilizadas em produção*:

* `FLASK_ENV=production` — modo produção
* `SECRET_KEY` — chave da aplicação Flask
* `JWT_SECRET_KEY` — chave para assinar tokens JWT
* `DATABASE_URL` — string de conexão (ex.: `postgresql://usuario:senha@db:5432/banco`)
* (Opcional) `JWT_ACCESS_TOKEN_EXPIRES` — duração do token de acesso
* (Opcional) `JWT_REFRESH_TOKEN_EXPIRES` — duração do token de refresh

As variáveis sensíveis **não** são commitadas; um arquivo **`.env.example`** documenta o formato esperado.

---

## Autenticação e Autorização (JWT)

* **Padrão**: *Bearer Token* no cabeçalho `Authorization`.
* **Geração de token**: após credenciais válidas, um **Access Token** (e opcionalmente um **Refresh Token**) é emitido.
* **Proteção de rotas**: decoradores/middlewares exigem token válido para acessar recursos da API e páginas protegidas.
* **Revogação/Logout**: invalidação lógica do token (estratégia conforme política adotada — por ex., *blacklist* em memória/DB quando necessário).
* **Hash de senha**: armazenamento seguro (ex.: *bcrypt* ou *werkzeug.security*), sem senhas em texto puro.

---

## Módulos Funcionais

### Usuários

* **Cadastro**: criação de conta com validações de entrada.
* **Login (JWT)**: emissão de `access_token` (e `refresh_token` se habilitado).
* **Perfil**: consulta e atualização de dados (atributos permitidos).
* **Exclusão de conta**: exige confirmação de senha.
* **Recuperação de acesso**: fluxo de redefinição (token temporário + nova senha).

### Controle de Gastos

* **Cadastro/edição/exclusão** de lançamentos de gasto.
* **Consulta** com filtros (por período, categoria e/ou status, conforme telas do projeto).
* **Dashboard** com visão consolidada (saldos, somatórios por período/categoria e lista paginada).
* **Validações** de domínio (valores numéricos, datas, categorias permitidas, etc.).

> Observação: a *UI* usa templates HTML (Jinja2) com **mensagens de feedback** (flash) para operações de sucesso/erro.

---

## Banco de Dados

* **Motor**: PostgreSQL 15.
* **Conexão**: via URL unificada (`DATABASE_URL`).
* **Persistência**: dados preservados em **volume** dedicado.
* **Camada de acesso**: abstraída em módulos Python (ex.: `user_db.py` e serviços do domínio de gastos), garantindo **separação entre regras de negócio e queries**.
* **Índices e integridade**: chaves primárias, estrangeiras e índices funcionais onde aplicável às consultas críticas.

> A evolução de esquema segue a estratégia do projeto (ex.: versionamento de *scripts SQL* e/ou migrações). Em produção, o schema publicado cobre usuários, autenticação e gastos.

---

## Camada Web (Templates e Estáticos)

* **Templates (Jinja2)** com herança a partir de `base.html`.
* **Páginas principais**: autenticação, dashboard de gastos, formulário de lançamento, perfil de usuário.
* **Componentes de UI**: formulários com validação do lado do servidor, modais de confirmação para ações sensíveis.
* **Mensagens flash**: feedback imediato para operações (create/update/delete, autenticação, etc.).
* **Estáticos**: CSS/JS/Imagens servidos pela pasta `static/` (minificação/empacotamento de acordo com as práticas do projeto).

---

## Observabilidade e Logs

* **Logs de aplicação**: `stdout/stderr` do serviço *web* (capturados pelo runtime de contêineres).
* **Níveis**: `INFO` para trilha de uso, `WARNING/ERROR` para exceções e falhas de integração.
* **Correlação**: identificação por request (ex.: inclusão de *request id* nos logs quando aplicável).
* **Auditoria básica**: eventos-chave (login, exclusão de conta, operações críticas) registrados para acompanhamento operacional.

---

## Padrões de Erro e Respostas

* **API**: respostas JSON com estrutura consistente (ex.: `{ "message": str, "data": any, "errors": list }`).
* **Códigos HTTP**: 2xx para sucesso; 4xx para falhas do cliente (ex.: `401` para token inválido/ausente, `403` para acesso negado, `404` quando não encontrado); 5xx para falhas internas.
* **Páginas HTML**: templates de erro dedicados (`4xx`/`5xx`) quando aplicável.

---

## Containerização e Orquestração

> **Sem expor arquivos de configuração.** Abaixo, apenas os **conceitos em produção**.

* **Serviços**:

  * `web`: aplicação Flask (porta interna 5000).
  * `db`: PostgreSQL (porta interna 5432; não exposto publicamente).
  * `edge`: Nginx (exposição 80/443; termina TLS e encaminha ao `web`).
* **Redes**: separação entre rede interna (*web↔db*) e rede de borda (*edge↔web*).
* **Volumes**: persistência de dados do Postgres e armazenamento de certificados TLS.
* **Dependências**: inicialização coordenada para garantir que o banco esteja disponível antes do *web* (uso de *wait-for-it.sh*).

---

## Segurança

* **JWT** assinado com `JWT_SECRET_KEY` (segredo não versionado).
* **Senhas**: hash seguro e *salting* (sem armazenamento em texto claro).
* **HTTPS** de ponta a ponta entre cliente e proxy.
* **Proteções de formulário** e validação de entrada do lado do servidor.
* **Segregação de redes** (banco não exposto externamente).
* **Princípio do menor privilégio** na conexão ao banco (usuário de aplicação com permissões restritas).

---

## Testes

### Playwright (E2E/UI)

* **Objetivo**: validar os fluxos críticos de interface em navegador real.
* **Abrangência principal**:

  * Autenticação: login válido/ inválido; registro de usuário.
  * Fluxo de gastos: criação, edição, exclusão e listagem com filtros.
  * Perfil: atualização de dados e exclusão de conta com confirmação.
  * Regressões: verificação de mensagens flash e estados pós-ação.
* **Organização**:

  * `tests/e2e/specs/` concentra cenários (arquivos `*.spec.ts`).
  * `tests/e2e/fixtures/` guarda utilitários e *helpers* (ex.: funções para obter token via API, *seeding* mínimo, dados mockados).
  * `tests/e2e/playwright.config.ts` define `baseURL`, *timeouts*, *reporters* e *projects* (browsers alvo).
* **Execução típica**:

  * Preparar variáveis/ambiente de teste (baseURL local ou staging).
  * Rodar `npx playwright test` (com *report* HTML disponível conforme config).

### Postman (API)

* **Objetivo**: garantir a consistência das rotas de API e contratos de resposta.
* **Coleção**: `tests/postman/collection.json` cobre endpoints de autenticação, usuários e gastos.
* **Ambiente**: `tests/postman/environment.json` contém variáveis como `{{baseUrl}}`, `{{accessToken}}`, `{{userId}}` etc.
* **Automação**:

  * *Pre-request scripts* para obter token e populá-lo em `Authorization: Bearer {{accessToken}}`.
  * *Tests* por request validando `status`, *schema* básico e campos obrigatórios (ex.: `message`, `data.id`).
* **Uso**: importar coleção e ambiente no Postman, selecionar o ambiente e executar via *Runner*.

---

## Manutenção e Operação

* **Backup**: política de backup dos volumes de banco (rotina operacional do time/infra).
* **Rotinas administrativas**: criação de usuários administrativos e rotação periódica de segredos (conforme política interna).
* **Escalabilidade**: suporte à verticalização (CPU/RAM/IO) e replicação de serviços via orquestração.

---

## Anexos

* **`.env.example`**: referência de variáveis necessárias na aplicação.
* **Diagramas (opcional)**: representação do fluxo *edge → web → db* e fronteiras de rede.
* **Especificação de endpoints (opcional)**: tabela de rotas e contratos JSON exportada a partir da coleção Postman.
