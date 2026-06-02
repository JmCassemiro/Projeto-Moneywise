# MoneyWise

## 📖 Visão Geral

O **MoneyWise** é uma aplicação web de controle financeiro pessoal, criada para registrar receitas e despesas de maneira simples e intuitiva. Cadastre‑se e tenha acesso a um painel personalizado, onde você acompanha seu fluxo de caixa em tempo real. Com gráficos interativos, visualize suas entradas, saídas e saldo disponível, identifique tendências e alcance suas metas econômicas com facilidade — tudo num só lugar!

- 📥 **Registrar** entradas (salários, vendas, investimentos) e saídas (contas, compras, serviços)
- 📊 **Visualizar** o saldo em tempo real através de dashboards claros
- 🔍 **Analisar** tendências diárias, semanais, mensais e anuais

### Objetivos

- Fornecer uma ferramenta leve e escalável para finanças pessoais
- Garantir segurança com autenticação JWT
- Assegurar precisão de cálculos usando PostgreSQL
- Oferecer flexibilidade: categorias customizadas e relatórios dinâmicos

## 📋 Conteúdo

- [Demos Highlights](#-demos-highlights-)
- [Funcionalidades Principais](#-funcionalidades-principais-)
- [Tech Stack](#-tech-stack-)
- [Instalação & Uso](#-instalação--uso-)
- [DevOps / Jenkins](#-devops--jenkins)
- [Uso de IA](#-uso-de-ia)
- [Contribuição](#-contribuição-)

## 🌟 Pricipais Demos de evolução do Projeto

- **Demo 3:** Segurança JWT, transações dinâmicas Front↔Back e filtragem por usuário
- **Demo 4:** Interfaces Figma-driven, gráficos com Plotly.py e testes E2E com Playwright
- **Demo 5:** Containerização com Docker (app, DB, Nginx), VPS Hostinger e HTTPS via Let's Encrypt

## 🚀 Funcionalidades Principais

1. **Autenticação & Usuários**
   - Login/Registro com JWT (header ou cookie)
   - Perfis com avatar e data de nascimento

2. **Transações CRUD**
   - Registrar receitas, despesas e recorrências (diárias a anuais)
   - Integração Jinja2 + JS para cálculos dinâmicos sem recarga de página
   - Filtragem por usuário (user_id)

3. **Dashboard & Relatórios**
   - Visão mensal de receitas, despesas e saldo
   - Gráficos de histórico financeiro (1, 3, 6 e 12 meses) usando Plotly
   - Metas financeiras configuráveis com alertas

4. **Categorias Personalizadas**
   - CRUD de categorias via SQLAlchemy

5. **Testes & QA**
   - Playwright para testes de Home, Auth, Perfil e Transações

## ⚙️ Tech Stack

- **Back-end:** Python 3.x, Flask 3.x
- **Banco:** PostgreSQL, Flask-SQLAlchemy e Flask-Migrate
- **Autenticação:** Flask-JWT-Extended
- **Front-end:** Jinja2, HTML5, CSS3, JavaScript
- **Gráficos:** Plotly.py
- **Contêineres:** Docker, Docker Compose

## 💻 Instalação & Uso

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/MoneyWise.git
   cd MoneyWise
   ```

2. Instale dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Aplique migrações:

   ```bash
   flask db upgrade
   ```

4. Execute a aplicação:

   ```bash
   flask run
   ```

Ou, usando Docker:

```bash
cp .env.example .env
docker-compose up --build
```

No Windows PowerShell, use `Copy-Item .env.example .env` antes de preencher as variaveis locais.

Para recriar o banco do zero durante a refatoração:

```bash
docker-compose down -v
docker-compose up --build
```

Acesse em `http://localhost:3000`.

## 🔧 DevOps / Jenkins

O Jenkins roda em container pelo `docker-compose.yml` e executa as etapas definidas no `Jenkinsfile`: checkout, preparo de ferramentas, build da imagem, testes com cobertura, empacotamento, publicacao opcional no Docker Hub e notificacao.

Variaveis sensiveis devem ficar apenas no `.env` local ou no Jenkins Credentials. O arquivo `.env` esta ignorado pelo Git; use `.env.example` como referencia.

Para publicar a imagem no Docker Hub pela pipeline:

1. Crie no Jenkins uma credencial do tipo username/password ou token com ID `dockerhub-credentials`, ou defina outro ID em `DOCKERHUB_CREDENTIALS_ID`.
2. Configure `DOCKERHUB_IMAGE` no `.env` ou no ambiente do job, por exemplo usando o formato `<usuario-dockerhub>/<imagem>`.
3. Recrie o Jenkins quando alterar a imagem base: `docker-compose up -d --build jenkins`.

Para notificar por e-mail pela pipeline, configure no `.env` local as variaveis `NOTIFICATION_EMAIL` e `NOTIFICATION_FROM`, ou reutilize `MAIL_CONTACT_RECIPIENT` e `MAIL_DEFAULT_SENDER`. As credenciais SMTP devem ficar em `SMTP_USERNAME`/`SMTP_PASSWORD` ou `MAIL_USERNAME`/`MAIL_PASSWORD`. Se essas variaveis nao estiverem preenchidas, a pipeline continua funcional e salva o conteudo da notificacao como artefato.

Os relatorios de testes e cobertura sao arquivados no Jenkins; quando os plugins estiverem instalados, o HTML Publisher mostra o relatorio HTML de cobertura e o plugin Coverage processa o `coverage.xml`.

## 🤖 Uso de IA

Este projeto utilizou IA como apoio de pair programming, revisao tecnica e debugging durante a etapa DevOps. A ferramenta utilizada foi o GitHub Copilot no VS Code.

### Como a IA foi utilizada

- Analise dos requisitos do PRD DevOps para identificar entregaveis pendentes: pipeline Jenkins, Docker Hub, notificacao por e-mail, artefatos, cobertura e uso de Docker Compose com multiplos containers.
- Revisao dos arquivos `Dockerfile`, `Dockerfile.jenkins`, `docker-compose.yml`, `Jenkinsfile`, `.env.example` e scripts auxiliares.
- Debugging da aplicacao no container, incluindo a identificacao do problema de line ending `CRLF` no `wait-for-it.sh`, que causava o erro `env: 'bash\r': No such file or directory`.
- Apoio na configuracao dos plugins Jenkins necessarios para pipeline, Docker, relatorios HTML, cobertura e visualizacao de stages.
- Refatoracao do `Jenkinsfile` para manter o pipeline funcional, publicar artefatos, publicar relatorio de cobertura, adicionar etapa paralela e preparar publicacao opcional no Docker Hub.
- Organizacao de variaveis de ambiente para evitar senhas, tokens, chaves secretas e e-mails fixos no codigo versionado.
- Criacao de um fluxo de notificacao por e-mail via script Python e variaveis de ambiente.
- Adicao do Mailpit como SMTP local para demonstrar notificacoes sem depender de credenciais reais de Gmail, Outlook ou outro provedor externo.

### Exemplos de prompts utilizados

- "Por que minha aplicacao nao esta subindo no container?"
- "Pesquise e instale estes plugins do Jenkins no Dockerfile.jenkins."
- "Leia o PRD-DevOps e verifique o projeto, Docker, docker-compose, Dockerfile.jenkins e Jenkinsfile."
- "Remova variaveis sensiveis hardcoded e deixe o pipeline funcional."
- "Configure a parte de e-mail, Docker Hub e demais variaveis necessarias na env."
- "Adicione uma sessao no README falando como a IA foi utilizada nessas modificacoes."

### Decisoes tomadas com apoio da IA

- Manter `.env` fora do Git e criar `.env.example` apenas como modelo sem segredos.
- Usar Jenkins Credentials para usuario/token do Docker Hub, mantendo `DOCKERHUB_IMAGE` como variavel nao sensivel.
- Usar Mailpit para notificacao local, permitindo demonstrar o requisito de e-mail em ambiente Docker sem expor credenciais reais.
- Deixar a publicacao no Docker Hub condicional: quando `DOCKERHUB_IMAGE` estiver configurado e a credencial existir, o push ocorre; caso contrario, o pipeline continua executando as demais etapas.
- Rodar empacotamento e publicacao da imagem em paralelo no Jenkinsfile.
- Salvar pacotes, relatorios de teste, cobertura e notificacao como artefatos do Jenkins.

### Validacoes realizadas

- `docker-compose config --quiet` para validar a configuracao do Compose.
- `docker build -f Dockerfile.jenkins ...` para validar a imagem Jenkins com plugins e dependencias.
- `python -m py_compile scripts/ci/send_notification.py` para validar o script de notificacao.
- `git diff --check` para verificar problemas mecanicos de diff e line endings.
- Execucao local do Mailpit e envio de uma notificacao de teste capturada na interface web.

### O que nao foi feito por IA

- Criacao de contas externas.
- Geracao ou exposicao de senhas, tokens e credenciais reais.
- Publicacao efetiva da imagem no Docker Hub sem credencial configurada pelo responsavel do projeto.
- Decisao final sobre valores reais de ambiente, como usuario Docker Hub, e-mails reais e tokens.

## 🤝 Contribuição

- Ajude-nos a sempre melhorar!

1. Fork este repositório
2. Crie uma branch (`git checkout -b feature/nova-coisa`)
3. Commit suas alterações (`git commit -m 'Adiciona xyz'`)
4. Push para a branch (`git push origin feature/nova-coisa`)
5. Abra um Pull Request

---

> Simplificando sua jornada financeira! Escolha MoneyWise💡
