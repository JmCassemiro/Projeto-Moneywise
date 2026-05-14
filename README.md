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

2. Crie o arquivo `.env` com suas credenciais:

   ```ini
   FLASK_APP=app
   FLASK_CONFIG=development
   DEBUG=true
   TESTING=true
   WTF_CSRF_ENABLED=false
   DB_HOST=localhost
   DB_PORT=5433
   DOCKER_DB_HOST=db_container
   DOCKER_DB_PORT=5432
   DB_PUBLIC_PORT=5433
   DB_NAME=moneywise
   DB_USER=postgres
   DB_PASSWORD=meritopg
   SQLALCHEMY_TRACK_MODIFICATIONS=false
   SECRET_KEY=uma_chave_secreta
   JWT_SECRET_KEY=uma_chave_secreta
   SECURITY_PASSWORD_SALT=um_salt_seguro
   JWT_TOKEN_LOCATION=headers,cookies
   JWT_COOKIE_SECURE=false
   JWT_COOKIE_SAMESITE=Lax
   JWT_COOKIE_CSRF_PROTECT=false
   JWT_COOKIE_NAME=access_token_cookie
   JWT_ACCESS_COOKIE_PATH=/
   JWT_REFRESH_COOKIE_PATH=/auth/refresh
   JWT_ACCESS_TOKEN_MINUTES=30
   MAIL_SERVER=localhost
   MAIL_PORT=1025
   MAIL_USE_TLS=false
   MAIL_USE_SSL=false
   MAIL_USERNAME=
   MAIL_PASSWORD=
   MAIL_DEFAULT_SENDER=noreply@moneywise.local
   MAIL_CONTACT_RECIPIENT=contact@moneywise.local
   ```

3. Instale dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Aplique migrações:

   ```bash
   flask db upgrade
   ```

5. Execute a aplicação:

   ```bash
   flask run
   ```

Ou, usando Docker:

```bash
docker-compose up --build
```

Para recriar o banco do zero durante a refatoração:

```bash
docker-compose down -v
docker-compose up --build
```

Acesse em `http://localhost:3000`.

## 🤝 Contribuição

- Ajude-nos a sempre melhorar!

1. Fork este repositório
2. Crie uma branch (`git checkout -b feature/nova-coisa`)
3. Commit suas alterações (`git commit -m 'Adiciona xyz'`)
4. Push para a branch (`git push origin feature/nova-coisa`)
5. Abra um Pull Request

---

> Simplificando sua jornada financeira! Escolha MoneyWise💡
