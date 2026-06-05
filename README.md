# MoneyWise

MoneyWise é uma aplicação web para controle financeiro pessoal. O sistema permite registrar receitas e despesas, acompanhar saldo, consultar histórico financeiro e visualizar estatísticas por usuário autenticado.

O projeto também demonstra uma esteira DevOps completa com Docker, Docker Compose, Jenkins em container, testes automatizados, cobertura acima de 90%, publicação de imagem no Docker Hub e notificação de pipeline por e-mail.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Stack Técnica](#stack-técnica)
- [Arquitetura DevOps](#arquitetura-devops)
- [Como Executar](#como-executar)
- [Pipeline Jenkins](#pipeline-jenkins)
- [Imagens Docker Hub](#imagens-docker-hub)
- [Relatórios e Artefatos](#relatórios-e-artefatos)
- [Uso de IA e SDD](#uso-de-ia-e-sdd)
- [O que não foi feito por IA](#o-que-não-foi-feito-por-ia)
- [Validação](#validação)

## Funcionalidades

- Cadastro, login e autenticação de usuários com JWT.
- Registro, edição, listagem e remoção de transações financeiras.
- Separação de dados por usuário autenticado.
- Dashboard com receitas, despesas, saldo e estatísticas financeiras.
- Recuperação de senha e envio de mensagens de contato.
- Testes unitários e de integração para regras de domínio, rotas Flask e persistência.

## Stack Técnica

| Área                 | Tecnologias                                      |
| -------------------- | ------------------------------------------------ |
| Backend              | Python, Flask, Flask-SQLAlchemy, Flask-Migrate   |
| Banco de dados       | PostgreSQL                                       |
| Autenticação         | Flask-JWT-Extended, Flask-Bcrypt                 |
| Formulários e e-mail | Flask-WTF, Flask-Mail                            |
| Testes               | pytest, pytest-mock, pytest-cov                  |
| DevOps               | Docker, Docker Compose, Jenkins, Docker Hub      |
| Relatórios CI        | JUnit XML, Coverage XML, HTML Publisher, Mailpit |

## Arquitetura DevOps

O ambiente é orquestrado por Docker Compose e possui múltiplos containers:

| Serviço        | Finalidade                                      |
| -------------- | ----------------------------------------------- |
| `app`          | Aplicação Flask MoneyWise                       |
| `db_container` | Banco PostgreSQL                                |
| `jenkins`      | Jenkins em container para executar a pipeline   |
| `pgadmin`      | Interface de administração do PostgreSQL        |
| `mailpit`      | SMTP local para capturar notificações de e-mail |

O Jenkins executa o pipeline definido no `Jenkinsfile`. As etapas da pipeline ficam versionadas no repositório, atendendo ao requisito de não criar etapas manualmente pela interface gráfica do Jenkins.

## Como Executar

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/S07B-S107B-Moneywise/Moneywise-DevOps.git
cd Moneywise-DevOps
```

Crie o arquivo de ambiente local:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Preencha no `.env` os valores locais de banco, secrets e variáveis de DevOps. O arquivo `.env` não deve ser commitado.

Suba o ambiente:

```bash
docker-compose up -d --build
```

Acessos locais:

| Serviço   | URL                     |
| --------- | ----------------------- |
| Aplicação | `http://localhost:3000` |
| Jenkins   | `http://localhost:8080` |
| pgAdmin   | `http://localhost:5050` |
| Mailpit   | `http://localhost:8025` |

Para parar o ambiente:

```bash
docker-compose down
```

## Pipeline Jenkins

A pipeline automatizada realiza:

1. Checkout do repositório.
2. Validação das ferramentas necessárias.
3. Build da imagem Docker da aplicação.
4. Execução dos testes unitários e de integração em container isolado.
5. Geração dos relatórios JUnit, Coverage XML e HTML de cobertura.
6. Empacotamento da imagem Docker como artefato `.tar`.
7. Publicação opcional da imagem da aplicação no Docker Hub.
8. Notificação por e-mail via script Python e variáveis de ambiente.
9. Arquivamento dos pacotes e relatórios como artefatos do Jenkins.

As credenciais sensíveis ficam fora do repositório:

- GitHub token: configurado no Jenkins Credentials para checkout.
- Docker Hub token: configurado no Jenkins Credentials para publicação da imagem.
- Secrets da aplicação: definidos em `.env` local ou ambiente seguro.

## Imagens Docker Hub

Imagens publicadas para entrega DevOps:

| Imagem                    | Finalidade                                                          |
| ------------------------- | ------------------------------------------------------------------- |
| `jmsz1/moneywise`         | Imagem da aplicação Flask publicada pela pipeline                   |
| `jmsz1/moneywise-jenkins` | Imagem customizada do Jenkins com plugins e ferramentas necessárias |

Links:

- Aplicação: `https://hub.docker.com/r/jmsz1/moneywise`
- Jenkins customizado: `https://hub.docker.com/r/jmsz1/moneywise-jenkins`

A imagem da aplicação não contém banco de dados nem secrets. Ela deve receber configuração por variáveis de ambiente e depende de um PostgreSQL acessível em runtime.

A imagem do Jenkins não contém jobs nem credenciais. Ela contém Jenkins LTS, Docker CLI, Python 3 e plugins necessários para executar a pipeline versionada no `Jenkinsfile`.

## Relatórios e Artefatos

Durante a execução, a pipeline gera e arquiva:

- `dist/`: pacote da imagem Docker exportada em `.tar`.
- `reports/tests/`: resultado dos testes em formato JUnit XML.
- `reports/coverage/`: relatório HTML e XML de cobertura.
- `reports/notification/`: cópia da notificação enviada por e-mail.

O relatório HTML de cobertura usa configuração em `.coveragerc` e estilo customizado em `coverage_custom.css`, tornando a visualização mais legível para apresentação.

## Uso de IA e SDD

O projeto utilizou IA de forma assistida, com revisão humana, principalmente para especificação, planejamento, implementação DevOps, debugging e documentação. As ferramentas utilizadas durante o desenvolvimento foram GitHub Copilot no VS Code e o Codex via OpenAI API para prompts mais complexos e organização de artefatos com o GPT 5.5.

Também foi utilizado o conceito de SDD (Spec-Driven Development) com apoio do Spec Kit. O SDD trata especificações como artefatos centrais do desenvolvimento: primeiro são definidos requisitos, critérios de aceite, plano técnico e tarefas; depois a implementação segue esses documentos.

No projeto, essa abordagem aparece em `Doc/specs/001-backend-unit-integration-tests/`, com os seguintes artefatos:

| Artefato        | Papel no processo                                                                          |
| --------------- | ------------------------------------------------------------------------------------------ |
| `spec.md`       | Requisitos, histórias de usuário, critérios de aceite e casos de borda para testes backend |
| `plan.md`       | Plano técnico, stack, estrutura esperada e estratégia de implementação                     |
| `research.md`   | Decisões e contexto técnico pesquisado antes da implementação                              |
| `quickstart.md` | Comandos e cenários de validação                                                           |
| `tasks.md`      | Lista de tarefas incrementais, fases, dependências e itens paralelizáveis                  |

O Spec Kit foi usado como referência metodológica para organizar prompts e artefatos de especificação. O fluxo seguido foi inspirado nos comandos e conceitos de SDD:

- especificar o que precisava ser entregue antes de alterar código;
- transformar requisitos em plano técnico;
- quebrar o plano em tarefas executáveis;
- validar implementação contra critérios de aceite;
- manter documentação, testes e pipeline alinhados.

Exemplos de uso de IA no projeto:

- interpretar o PRD DevOps e mapear requisitos obrigatórios;
- revisar `Dockerfile`, `Dockerfile.jenkins`, `docker-compose.yml` e `Jenkinsfile`;
- diagnosticar erro de container causado por line ending `CRLF` no `wait-for-it.sh`;
- estruturar pipeline Jenkins com testes, cobertura, artefatos, publicação Docker Hub e notificação;
- organizar variáveis de ambiente para evitar senhas e tokens hardcoded;
- configurar Mailpit como SMTP local para demonstração;
- melhorar documentação técnica do README;
- apoiar a criação e revisão dos artefatos de SDD: specs, plan, research, quickstart e tasks.

Exemplos reais de prompts usados durante o desenvolvimento:

- "Por que minha aplicação não está subindo no container?"
- "Leia o PRD-DevOps e verifique o projeto, Docker, docker-compose, Dockerfile.jenkins e Jenkinsfile."
- "Remova variáveis sensíveis hardcoded e deixe o pipeline funcional."
- "Configure a parte de e-mail, Docker Hub e demais variáveis necessárias na env."
- "Publique a imagem, configure a notificação por e-mail e coloque uma parte do pipeline rodando em paralelo."
- "As variáveis do environment não podem ficar expostas; continue deixando funcional."
- "Pesquise e instale estes plugins do Jenkins no Dockerfile.jenkins."
- "O que é fallback?"
- "Para que serve `TEST_DATABASE_URL`?"
- "O que é o Mailpit?"
- "Explique as tags do Docker Hub e por que aparecem metadados `unknown/unknown`."
- "Leia o documento `PRD-DevOps.md` e foque apenas no tópico 7."

## O que não foi feito por IA

- Criação de contas externas do GitHub, Docker Hub ou serviços de e-mail.
- Geração, exposição ou armazenamento de tokens e senhas reais.
- Elaboração inicial do `requirements.txt` e definição das dependências principais do projeto.
- Configuração real do banco de dados local, incluindo nome do banco, usuário, senha, portas e credenciais administrativas.
- Preenchimento final do `.env` com valores reais de ambiente, credenciais e secrets.
- Decisão final sobre credenciais, usuários, nomes de repositórios e imagens publicadas.
- Execução da defesa ou validação oral do projeto.
- Aprovação final das alterações no repositório.

## Validação

Comandos utilizados para validar a configuração:

```bash
docker-compose config --quiet
docker build -f Dockerfile.jenkins -t moneywise-jenkins-devops-review .
python -m py_compile scripts/ci/send_notification.py
git diff --check
```

O pipeline Jenkins também valida a aplicação ao executar testes unitários e de integração com cobertura mínima de 90%.
