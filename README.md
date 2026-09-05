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
- adicionar comentários com autor, conteúdo e data/hora persistidos;
- acompanhar comentários e mudanças de status em uma timeline unificada, do evento mais antigo ao mais recente;
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

Esse comando remove os incidentes, históricos e comentários existentes e recria exatamente os três incidentes obrigatórios:

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
GET    /api/incidents/<id>/comments/
POST   /api/incidents/<id>/comments/
GET    /api/incidents/<id>/timeline/
```

### Comentários e timeline — Change Request #1

O Change Request #1 chegou às 14:00, após a implementação original e o redesign. Na tela de detalhes, o formulário exige autor (até 255 caracteres) e conteúdo. Valores vazios ou somente espaços são rejeitados. Após salvar, o formulário é limpo e a timeline é recarregada; falhas da API são apresentadas na interface.

`POST /api/incidents/<id>/comments/` recebe:

```json
{"author": "Ana", "content": "Provider contacted."}
```

A resposta `201` contém `id`, `author`, `content` e `created_at`. O incidente é definido pela URL e o timestamp pelo servidor. `GET` no mesmo endereço lista os comentários em ordem crescente de criação e ID. Entradas inválidas retornam `400`; incidente inexistente retorna `404`.

`GET /api/incidents/<id>/timeline/` retorna uma lista com `id`, `type` e `occurred_at`. Eventos `status_change` incluem `previous_status` e `new_status`; eventos `comment` incluem `author` e `content`. A ordem é cronológica crescente; em timestamps iguais, mudanças de status vêm antes de comentários, e o ID desempata dentro de cada tipo. A identidade do evento é o par `type` + `id`.

O endpoint `/history/` mantém seu contrato anterior. Comentários são armazenados em SQLite pela migration `0002_incidentcomment`; não modificam o status nem o `updated_at` do incidente. Refresh e reinício leem os mesmos registros persistidos. O seed continua sendo um reset explícito e também remove comentários por cascata.

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
- seed reproduzível, incluindo remoção de comentários e rollback;
- criação e persistência de comentários no incidente correto;
- autor/conteúdo obrigatórios, espaços rejeitados e limite do autor;
- múltiplos comentários e isolamento entre incidentes;
- timeline mista em ordem cronológica, com desempate determinístico;
- compatibilidade do histórico e preservação da regra Critical com comentários.

Validação automatizada pós-Change Request #1 executada pelo Codex: **34 testes passaram**, `python manage.py check` sem problemas, `python manage.py makemigrations --check --dry-run` sem alterações e `npm run build` concluído. A migration foi aplicada no banco local. A regressão manual pós-mudança, incluindo refresh/reinício com comentários, permanece pendente.

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

## Validação manual realizada antes do Change Request #1

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

## Validação manual pendente após o Change Request #1

- Adicionar vários comentários intercalados com mudanças de status e conferir autor, conteúdo e horários na timeline.
- Verificar campos vazios/somente espaços, falhas da API, limpeza após sucesso e nova tentativa de carregar a timeline.
- Atualizar a página e reiniciar o backend sem executar o seed; confirmar que os comentários permanecem.
- Repetir criação, listagem, filtros, detalhes, dashboard e fluxo Critical, incluindo a tentativa bloqueada `Open → Resolved`.
- Conferir responsividade, acessibilidade e conteúdo longo/multilinha na tela de detalhes.

## Limitações conhecidas

- Não existe autenticação.
- Não existem níveis de permissão.
- Não existem organizações ou múltiplos tenants.
- O responsável pelo incidente e o autor do comentário são armazenados como texto simples, sem identidade autenticada.
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