# Incident Hub — Frontend

Estrutura inicial Angular com componentes standalone, routing e SCSS.

## Executar localmente

Dentro de `frontend`, instale as dependências com `npm ci` e execute `npm start`.
A aplicação estará disponível em http://localhost:4200/.

## Backend

A URL base está em `src/environments/environment.ts`:
`http://localhost:8000/api/`.

O `HttpClient` está registrado em `src/app/app.config.ts`. Os futuros serviços
podem importar `environment` e usar `environment.apiBaseUrl` nas requisições.
O backend Django deve estar em execução na porta 8000.

## Rotas e telas

As futuras rotas de dashboard, lista, criação e detalhes serão definidas em
`src/app/app.routes.ts`. Histórico e alteração de status poderão ser integrados
à tela de detalhes. Nesta etapa, existe apenas a página inicial mínima e o
`router-outlet`; as telas de negócio ainda não foram implementadas.

## Build

Execute `npm run build`. Os arquivos gerados ficam em `dist/frontend/`.
