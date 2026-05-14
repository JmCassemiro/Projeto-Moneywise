# PRD — Projeto DevOps MoneyWise (S07 - NP2)

## 1. Visão Geral

Demonstrar domínio de práticas DevOps modernas:

- Containerização com Docker
- Automação de CI/CD com Jenkins (em container)
- Orquestração de múltiplos serviços com Docker Compose

O sistema pode ser de autoria própria ou hipotético, desde que não seja o utilizado pelo professor nas aulas.

## 2. Objetivos do Projeto

- Pipeline automatizado com cobertura de testes ≥ 90%
- Infraestrutura definida como código (IaC)
- Colaboração efetiva de todos os membros do grupo

## 3. Requisitos Funcionais

- Sistema inédito (não pode ser o do professor)
- Repositório público no GitHub do time
- Cobertura de testes (unitários, integração e/ou interface) ≥ 90%
- Jenkins rodando em container (não instalado direto na máquina)
- Não utilizar GitHub Actions
- Interface gráfica do Jenkins permitida apenas para checkout do código; etapas do pipeline devem estar no Jenkinsfile
- Commits relevantes de todos os membros

## 4. Requisitos Não Funcionais

- README completo: instalação, execução, uso, funcionalidades e seção "Uso de IA"
- Entrega via Teams com link do GitHub (repositório público)
- Link para imagem publicada no Docker Hub
- Defesa do projeto em até 20 minutos (formato Q&A)

## 5. Critérios Técnicos e de Aceite

### 5.1 Dockerfile e Pipeline Jenkins

- Pipeline com etapas obrigatórias:
  - Execução dos testes
  - Build/empacotamento
  - Notificação de usuários (e-mail, via script e variável de ambiente)
- Pacote e relatório de testes armazenados como artefatos no Jenkins
- Softwares necessários instalados via script ou Dockerfile
- Proibido criar etapas do pipeline via interface gráfica do Jenkins

### 5.2 Docker Hub

- Criar imagem a partir do Dockerfile
- Publicar imagem no Docker Hub
- Entregar link da imagem junto ao repositório

### 5.3 Docker Compose (mínimo 4 containers)

- Subir a imagem do Docker Hub e executar pipeline completo
- Mínimo de 4 containers
- Comunicação entre pelo menos 2 containers
- Um container definido via Dockerfile local, outro puxado do Docker Hub
- Uso de volumes para persistência de dados relevantes

## 6. Apresentação e Defesa

- Formato: perguntas e respostas (Q&A)
- Todos os integrantes devem conhecer o sistema como um todo
- Professor pode pedir para navegar pelo repositório, mostrar Jenkinsfile, executar pipeline ao vivo
- Respostas devem ser concretas, com evidências (arquivo, commit, log, artefato)

## 7. Uso de Inteligência Artificial

- Uso de IA permitido e incentivado, desde que declarado de forma transparente
- Seção obrigatória "Uso de IA" no README, contendo:
  - Modelos utilizados (ex: Copilot, ChatGPT, Gemini, etc.)
  - Para quê foram usados (ex: geração de Dockerfile, Jenkinsfile, scripts, testes, documentação, debugging, brainstorming, etc.)
  - Exemplos reais de prompts e respostas
  - Dinâmica de uso (individual, pair programming, revisão, etc.)
  - O que não foi feito por IA

---

**Referências:**

- [awesome-compose](https://github.com/docker/awesome-compose)
- [Docker Hub](https://hub.docker.com/)

**Observação:**
Revisar o repositório, Jenkinsfile e docker-compose.yml em grupo antes da defesa.
