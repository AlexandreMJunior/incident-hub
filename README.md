# Incident Hub

Incident Hub é uma aplicação web simples para registro e acompanhamento de incidentes operacionais.

A solução foi desenvolvida como parte do **AI Engineering Hackathon** e tem como foco funcionalidade, confiabilidade, clareza e facilidade de reprodução local.

## Funcionalidades

A aplicação permite:

- criar incidentes;
- listar incidentes;
- filtrar por status e severidade;
- visualizar detalhes;
- alterar status;
- consultar o histórico de alterações de status;
- visualizar um dashboard resumido;
- persistir os dados localmente;
- carregar/resetar dados iniciais de demonstração.

Também implementa a seguinte **regra de negócio crítica**:

> Um incidente com severidade `Critical` não pode passar diretamente de `Open` para `Resolved`.

Nesse caso, o fluxo obrigatório é:

```
Open → In Progress → Resolved
```

## Stack

### Frontend

- Angular 21.2.22
- TypeScript
- SCSS
- Angular HttpClient

### Backend

- Python 3.12
- Django 6.1.1
- Django REST Framework 3.18.0
- django-cors-headers 4.9.0

### Persistência

- SQLite

## Estrutura do projeto

```text
incident-hub/
├── backend/
│   ├── config/
│   ├── incidents/
│   └── manage.py
├── frontend/
├── AI_LOG.md
├── FINAL_REPORT.md
├── PLAN.md
├── README.md
├── START.md
└── requirements.txt
```

O projeto é dividido em duas aplicações principais:

- **backend**: API Django responsável por persistência, validações e regras de negócio;
- **frontend**: aplicação Angular responsável pela interface e pelo consumo da API.

## Pré-requisitos

Para executar a aplicação localmente, é necessário possuir:

- Python 3.12 ou compatível;
- python3-venv;
- Node.js compatível com Angular 21;
- npm;
- Git.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/AlexandreMJunior/incident-hub.git
cd incident-hub
```

Crie o ambiente virtual Python:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Instale as dependências do backend:

```bash
pip install -r requirements.txt
```

Entre na pasta do backend:

```bash
cd backend
```

Aplique as migrations:

```bash
python manage.py migrate
```

## Dados iniciais

A aplicação possui um management command para criar ou resetar os dados de demonstração.

Dentro da pasta `backend`, execute:

```bash
python manage.py seed_incidents
```

Esse comando remove os incidentes e históricos existentes e recria exatamente os três incidentes obrigatórios:

| Incidente | Severity | Owner | Status |
|---|---|---|---|
| Payment API instability | Critical | Ana | Open |
| Reconciliation delay | High | Bruno | In Progress |
| Incorrect customer notification | Medium | Carla | Resolved |

O comando pode ser executado novamente sempre que for necessário restaurar os dados iniciais.

## Execução

A aplicação precisa de dois processos em execução: **backend** e **frontend**.

### Backend

Com o ambiente virtual ativo:

```bash
cd backend
python manage.py runserver
```

O backend estará disponível em:

```
http://127.0.0.1:8000/
```

A API utiliza o prefixo:

```
http://127.0.0.1:8000/api/
```

### Frontend

Em outro terminal, a partir da raiz do projeto:

```bash
cd frontend
npm install
npm start
```

O frontend estará disponível em:

```
http://localhost:4200/
```

## Rotas do frontend

| Rota | Descrição |
|---|---|
| `/` | Dashboard |
| `/incidents` | Lista de incidentes |
| `/incidents/new` | Criar incidente |
| `/incidents/:id` | Detalhes do incidente |

## Endpoints da API

### Incidentes

```
GET    /api/incidents/
POST   /api/incidents/
GET    /api/incidents/<id>/
PATCH  /api/incidents/<id>/status/
GET    /api/incidents/<id>/history/
```

### Dashboard

```
GET /api/dashboard/
```

A listagem de incidentes aceita filtros opcionais por:

- `status`
- `severity`

## Testes

### Backend

Com o ambiente virtual ativo:

```bash
cd backend
python manage.py test
```

Também é possível validar a configuração Django com:

```bash
python manage.py check
```

A suíte atual cobre comportamentos como:

- criação de incidentes;
- validação de campos obrigatórios;
- status inicial `Open`;
- timestamps;
- listagem;
- filtros;
- detalhes;
- mudanças válidas de status;
- bloqueio de Critical: `Open → Resolved`;
- histórico;
- ausência de histórico duplicado;
- rollback em falhas;
- dashboard;
- atualização do dashboard;
- seed reproduzível.

### Frontend

Para validar a compilação:

```bash
cd frontend
npm run build
```

## Arquitetura

A solução utiliza uma arquitetura simples, com frontend e backend separados.

### Backend

O Django é responsável por:

- persistência;
- validação;
- regras de negócio;
- API REST;
- histórico de status;
- dashboard;
- dados iniciais.

A regra de alteração de status está centralizada no backend, evitando dependência exclusiva da interface.

A principal regra de negócio é implementada no serviço responsável pela alteração de status.

### Frontend

O Angular é responsável por:

- dashboard;
- listagem;
- filtros;
- formulário de criação;
- detalhes;
- histórico;
- alteração de status;
- feedback de erros.

O acesso à API é centralizado em um serviço Angular utilizando `HttpClient`.

## Persistência

Os dados são armazenados em SQLite.

O arquivo local do banco não é versionado no Git.

Para preparar o banco em uma nova instalação:

```bash
python manage.py migrate
python manage.py seed_incidents
```

## Regra de negócio crítica

Incidentes `Critical` não podem realizar a seguinte transição:

```
Open → Resolved
```

A aplicação rejeita essa operação.

O fluxo permitido é:

```
Open → In Progress → Resolved
```

Alterações válidas geram histórico contendo:

- status anterior;
- novo status;
- data/hora da alteração.

## Validação manual realizada

Os principais fluxos foram validados com frontend e backend executando simultaneamente:

- carregamento do dashboard;
- listagem de incidentes;
- filtros;
- criação de incidente;
- visualização de detalhes;
- alteração de status;
- bloqueio da transição inválida de incidentes Critical;
- exibição de mensagem de erro compreensível;
- histórico;
- atualização do dashboard;
- persistência após reinicialização.

## Limitações conhecidas

- Não existe autenticação.
- Não existem níveis de permissão.
- Não existem organizações ou múltiplos tenants.
- O responsável pelo incidente é armazenado como texto simples.
- A aplicação utiliza SQLite e foi planejada para execução local e pequena escala.
- Não há atualização em tempo real entre múltiplos usuários.
- O frontend não utiliza biblioteca visual externa; o redesign foi implementado utilizando a estrutura Angular existente e estilos próprios da aplicação.
- A suíte automatizada não simula reinicialização do processo do backend; a persistência após reinicialização foi validada manualmente.
- Deploy público não foi implementado, pois não é requisito obrigatório do desafio.

## Documentação adicional

O repositório também contém:

- `START.md` — registro inicial do desafio;
- `PLAN.md` — planejamento, estratégia de implementação, decisões técnicas e evolução do plano;
- `AI_LOG.md` — registro das principais interações com IA;
- `FINAL_REPORT.md` — retrospectiva e relatório final do desenvolvimento.