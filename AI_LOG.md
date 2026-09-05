# AI_LOG.md

## Visão geral

Durante o desenvolvimento do Incident Hub, utilizei ferramentas de Inteligência Artificial exclusivamente em modalidades gratuitas disponíveis ao público, conforme as regras do hackathon.

Nenhum plano pago, assinatura premium, crédito pago de API, conta corporativa com capacidade superior à gratuita ou recurso premium de IA foi utilizado durante o desafio.

As ferramentas efetivamente utilizadas foram:

- ChatGPT Free;
- Codex utilizando exclusivamente acesso gratuito;
- Lovable utilizando exclusivamente acesso gratuito.

No `START.md`, Claude Free e Gemini Free foram registradas como alternativas inicialmente planejadas. Durante a execução, nenhuma das duas foi necessária e, portanto, não foram utilizadas. Codex e Lovable foram incorporados posteriormente à estratégia e aparecem neste documento por terem sido efetivamente utilizados durante o desenvolvimento.

As ferramentas de IA foram utilizadas para:

- planejamento;
- decomposição do trabalho;
- geração e alteração de código;
- configuração técnica;
- investigação de problemas;
- revisão;
- validação;
- exploração visual;
- redesign da interface.

A estratégia adotada foi trabalhar de forma incremental: dividir o problema em partes menores, fornecer contexto específico à IA, executar e validar o resultado e somente depois avançar para a próxima etapa.

---

# 1. Definição da stack e planejamento inicial

## Ferramenta

ChatGPT Free

## Objetivo

Definir uma abordagem técnica adequada ao escopo do desafio e ao tempo disponível.

## Contexto

O desafio permitia liberdade de escolha da stack.

Tenho familiaridade prévia com Angular e Django. Utilizar uma tecnologia desconhecida durante um desafio com tempo limitado aumentaria o risco de retrabalho e adaptação.

## Instrução

Solicitei à IA auxílio para estruturar o planejamento inicial considerando:

- Angular no frontend;
- Django no backend;
- Django REST Framework para API;
- SQLite para persistência;
- arquitetura simples;
- prioridade para requisitos obrigatórios;
- testes das regras de negócio críticas.

## Resultado

Foi definida a seguinte stack:

- Angular;
- Django;
- Django REST Framework;
- SQLite.

Também foi definido que a solução deveria evitar complexidade desnecessária e priorizar:

1. correção;
2. completude;
3. simplicidade;
4. confiabilidade;
5. funcionalidades adicionais.

## Validação

Comparei o planejamento produzido com os requisitos apresentados no Challenge Pack e confirmei que os principais requisitos estavam contemplados.

## Decisão

Manter Angular + Django devido à familiaridade com a stack e ao menor risco técnico durante o tempo limitado do hackathon.

---

# 2. Preparação do ambiente Python

## Ferramenta

ChatGPT Free

## Objetivo

Criar corretamente o ambiente virtual Python e instalar as dependências necessárias para o backend.

## Contexto

Na primeira tentativa, a criação do ambiente virtual foi interrompida.

Como consequência:

- `.venv/bin/activate` não existia;
- o ambiente virtual não estava ativo;
- o `pip` tentou realizar instalação no Python global;
- o Ubuntu bloqueou a operação devido ao ambiente gerenciado externamente.

A mensagem de erro completa do terminal foi fornecida à IA.

## Instrução

Solicitei à IA que analisasse o erro e orientasse uma correção sem utilizar instalação global ou mecanismos que pudessem comprometer o ambiente Python do sistema.

## Resultado

A IA identificou que o ambiente virtual havia sido criado apenas parcialmente.

Foi orientado:

- remover `.venv` incompleto;
- instalar/verificar `python3-venv` e `python3-full`;
- recriar o ambiente virtual;
- ativar o ambiente;
- atualizar o pip;
- instalar as dependências dentro do ambiente virtual.

Foram instalados:

- Django;
- Django REST Framework;
- django-cors-headers.

## Validação

O ambiente virtual foi criado e ativado corretamente.

As dependências foram instaladas com sucesso dentro de `.venv`.

## Decisão

Utilizar exclusivamente o ambiente virtual local para as dependências Python do projeto.

---

# 3. Criação inicial do backend Django

## Ferramenta

ChatGPT Free

## Objetivo

Criar a estrutura inicial do backend Django.

## Contexto

O ambiente Python já estava configurado e as dependências necessárias estavam disponíveis.

## Instrução

Solicitei instruções para:

- criar o projeto Django;
- criar o app `incidents`;
- aplicar as migrations iniciais;
- executar o servidor de desenvolvimento.

## Resultado

Foi criada a estrutura inicial do backend, incluindo:

- projeto Django `config`;
- app `incidents`;
- banco SQLite;
- migrations padrão do Django.

## Validação

Foi executado:

`python manage.py migrate`

As migrations foram aplicadas corretamente.

Em seguida:

`python manage.py runserver`

O servidor iniciou em:

`http://127.0.0.1:8000/`

A página inicial padrão do Django foi aberta no navegador com sucesso.

## Decisão

Prosseguir para a configuração do Django REST Framework, CORS e do app principal.

---

# 4. Configuração do Django REST Framework e CORS

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Configurar o projeto Django para utilizar Django REST Framework, CORS e o app `incidents`.

## Contexto

O projeto Django já existia e executava corretamente.

As dependências:

- djangorestframework;
- django-cors-headers;

já estavam instaladas.

## Instrução

Solicitei ao Codex que:

- adicionasse `rest_framework` em `INSTALLED_APPS`;
- adicionasse `corsheaders`;
- adicionasse `incidents`;
- configurasse `CorsMiddleware`;
- permitisse requisições de `http://localhost:4200`;
- preservasse SQLite;
- não criasse modelos;
- não criasse endpoints;
- não implementasse regras de negócio;
- não alterasse configurações desnecessárias.

## Resultado

O arquivo:

`backend/config/settings.py`

foi alterado somente com as configurações necessárias.

## Validação

Foi executado:

`python manage.py check`

Resultado:

`System check identified no issues (0 silenced).`

## Decisão

Considerar a configuração inicial concluída e avançar para a modelagem do domínio.

---

# 5. Criação do requirements.txt

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Registrar de forma reproduzível as dependências Python necessárias para o backend.

## Contexto

As dependências necessárias já estavam instaladas no ambiente virtual.

## Instrução

Solicitei ao Codex que criasse um `requirements.txt` na raiz do repositório contendo somente as dependências realmente utilizadas e suas versões instaladas.

## Resultado

Foi criado:

`requirements.txt`

com:

- Django==6.1.1
- djangorestframework==3.18.0
- django-cors-headers==4.9.0

## Validação

Comparei o arquivo gerado com as versões efetivamente instaladas no ambiente virtual.

## Decisão

Manter o arquivo mínimo, sem adicionar dependências não utilizadas.

---

# 6. Configuração do .gitignore

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Evitar que arquivos locais e artefatos desnecessários fossem enviados ao repositório.

## Contexto

O Git identificou `.venv` e outros arquivos locais como não monitorados.

## Instrução

Solicitei ao Codex a criação de um `.gitignore` contendo pelo menos:

- `.venv/`;
- `__pycache__/`;
- `*.pyc`;
- `db.sqlite3`.

## Resultado

O `.gitignore` foi criado na raiz do repositório.

## Validação

Executei `git status` e confirmei que os arquivos locais esperados deixaram de aparecer para versionamento.

## Decisão

Manter o banco SQLite local e o ambiente virtual fora do controle de versão.

---

# 7. Modelagem de Incident e histórico de status

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Representar os incidentes e o histórico persistente das alterações de status.

## Contexto

O desafio exige que um incidente possua:

- identificador;
- título;
- descrição;
- severidade;
- responsável;
- status;
- data/hora de criação;
- data/hora da última atualização.

Também exige histórico das mudanças de status.

## Instrução

Solicitei ao Codex a criação dos modelos:

- `Incident`;
- `IncidentStatusHistory`.

Requisitos fornecidos:

- severity com choices:
  - Low;
  - Medium;
  - High;
  - Critical;
- status com choices:
  - Open;
  - In Progress;
  - Resolved;
- status inicial `Open`;
- timestamps automáticos;
- associação do histórico ao incidente;
- histórico com status anterior, novo status e timestamp;
- nenhuma regra de negócio ainda;
- nenhuma API ainda.

## Resultado

Foram criados os modelos:

- `Incident`;
- `IncidentStatusHistory`.

Também foi criada:

`backend/incidents/migrations/0001_initial.py`

## Validação

Foram executados:

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py check`

Todos os comandos concluíram com sucesso.

## Decisão

Manter a estrutura simples e implementar a lógica de alteração de status separadamente.

---

# 8. Implementação da regra de alteração de status

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Implementar a principal regra de negócio do desafio.

## Contexto

Um incidente com severidade `Critical` não pode realizar diretamente:

`Open → Resolved`

Ele precisa passar primeiro por:

`Open → In Progress → Resolved`

A regra deveria existir no backend e não depender do frontend.

## Instrução

Solicitei ao Codex que centralizasse a lógica de alteração de status em um único ponto.

A implementação deveria:

- validar o novo status;
- bloquear `Critical: Open → Resolved`;
- atualizar o status;
- atualizar `updated_at`;
- criar histórico;
- não criar histórico quando não houver mudança;
- utilizar uma transação;
- retornar erro de validação compreensível;
- não criar endpoints ainda.

## Resultado

Foi criada a função:

`change_incident_status(incident, new_status)`

em:

`backend/incidents/services.py`

A regra de negócio ficou centralizada nesse serviço.

## Validação

Foram criados testes cobrindo:

- status válido;
- status inválido;
- bloqueio de Critical;
- histórico;
- repetição do mesmo status;
- rollback em caso de falha.

Resultado:

**6 testes passaram.**

Também foi executado:

`python manage.py check`

Resultado:

`System check identified no issues (0 silenced).`

## Decisão

Manter a regra de negócio centralizada no service e exigir que qualquer alteração de status futura reutilize esse ponto.

---

# 9. Implementação da API

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Expor através de API os fluxos necessários para o frontend.

## Contexto

Os modelos e a regra de alteração de status já estavam implementados.

## Instrução

Solicitei ao Codex a criação dos endpoints necessários para:

- listar incidentes;
- filtrar por status;
- filtrar por severity;
- criar incidente;
- visualizar detalhes;
- alterar status;
- visualizar histórico;
- visualizar dashboard.

Também solicitei que:

- a alteração de status utilizasse obrigatoriamente `change_incident_status`;
- erros de validação retornassem mensagens compreensíveis;
- fossem criados testes automatizados;
- não fosse adicionada autenticação;
- não fosse adicionada paginação desnecessária.

## Resultado

Foram criados os endpoints:

- `GET /api/incidents/`
- `POST /api/incidents/`
- `GET /api/incidents/<id>/`
- `PATCH /api/incidents/<id>/status/`
- `GET /api/incidents/<id>/history/`
- `GET /api/dashboard/`

Foram criados ou alterados:

- `backend/config/urls.py`;
- `backend/incidents/views.py`;
- `backend/incidents/serializers.py`;
- `backend/incidents/urls.py`;
- `backend/incidents/test_api.py`.

## Validação

Foram executados todos os testes.

Resultado:

**23 testes passaram**, sendo:

- 17 testes relacionados à API;
- 6 testes relacionados ao serviço.

Também foi executado:

`python manage.py check`

Resultado sem problemas.

## Decisão

Considerar a API funcional e avançar para os dados iniciais obrigatórios.

---

# 10. Criação dos dados iniciais

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Disponibilizar de forma simples e reproduzível os três incidentes iniciais exigidos pelo desafio.

## Contexto

O avaliador deve conseguir utilizar a aplicação sem cadastrar manualmente vários registros.

Os três incidentes obrigatórios são:

1. Payment API instability — Critical — Ana — Open
2. Reconciliation delay — High — Bruno — In Progress
3. Incorrect customer notification — Medium — Carla — Resolved

## Instrução

Solicitei ao Codex a criação de um management command Django:

`python manage.py seed_incidents`

O comando deveria:

- limpar incidentes e históricos existentes;
- recriar exatamente os três incidentes obrigatórios;
- não acumular duplicações;
- funcionar de forma previsível;
- ser atômico;
- possuir testes automatizados.

## Resultado

Foi criado o comando:

`seed_incidents`

e seus respectivos testes.

## Validação

O comando foi executado.

Resultado:

- 3 incidentes criados;
- dados corretos;
- 26 testes passando;
- `python manage.py check` sem problemas.

## Decisão

Utilizar `seed_incidents` como mecanismo oficial de inicialização e reset dos dados de demonstração.

---

# 11. Revisão da cobertura de testes do backend

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Verificar se algum requisito importante do backend ainda estava sem cobertura automatizada.

## Contexto

Já existiam 26 testes passando.

## Instrução

Solicitei ao Codex que revisasse a cobertura atual sem criar testes redundantes e sem alterar a lógica da aplicação sem necessidade.

## Resultado

Foram identificadas duas lacunas:

- validação dos campos obrigatórios retornados pela listagem;
- atualização do dashboard após mudança de status.

Essas verificações foram adicionadas aos testes existentes.

Nenhuma lógica da aplicação foi alterada.

## Validação

A suíte completa foi executada novamente.

Resultado:

**26 testes passaram.**

Também foi executado:

`python manage.py check`

sem problemas.

## Decisão

Considerar a cobertura automatizada do backend suficiente para o escopo do desafio.

---

# 12. Criação da estrutura inicial do frontend Angular

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Criar a base do frontend Angular.

## Contexto

O backend e a API já estavam funcionais.

A interface exigida pelo desafio precisava ser funcional e clara, sem necessidade de sofisticação visual.

## Instrução

Solicitei ao Codex a criação de um projeto Angular em `frontend`, com:

- routing;
- SCSS;
- HttpClient;
- configuração da URL da API;
- estrutura mínima;
- nenhuma autenticação;
- nenhuma biblioteca visual externa.

## Resultado

Foi criado o frontend com:

- Angular 21.2.22;
- Angular CLI 21.2.23;
- routing;
- SCSS;
- HttpClient;
- `environment.ts`.

A base da API foi configurada como:

`http://localhost:8000/api/`

## Validação

Foi executado:

`npm run build`

Resultado:

**build concluído sem erros.**

## Decisão

Prosseguir com a camada de models e acesso HTTP antes da criação das telas.

---

# 13. Models e service do frontend

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Criar uma camada tipada para representar os dados da API e centralizar as requisições HTTP.

## Contexto

Os endpoints do backend já estavam definidos e estáveis.

## Instrução

Solicitei ao Codex:

- interfaces para Incident;
- tipos para Severity;
- tipos para Status;
- interface para histórico;
- interface para dashboard;
- tipos para criação;
- tipos para mudança de status;
- filtros;
- criação de um `IncidentService`.

O serviço deveria expor métodos para:

- listar incidentes;
- criar incidente;
- buscar detalhes;
- alterar status;
- consultar histórico;
- consultar dashboard.

## Resultado

Foram criados:

- `incident.models.ts`;
- `incident.service.ts`.

O serviço passou a possuir:

- `listIncidents`;
- `createIncident`;
- `getIncident`;
- `changeIncidentStatus`;
- `getIncidentHistory`;
- `getDashboard`.

## Validação

Foi executado:

`npm run build`

O build passou sem erros.

## Decisão

Prosseguir para a implementação das telas.

---

# 14. Implementação do dashboard

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Criar a visão resumida exigida pelo desafio.

## Contexto

O backend já disponibilizava:

`GET /api/dashboard/`

e o `IncidentService` já possuía `getDashboard()`.

## Instrução

Solicitei a criação de um dashboard simples na rota `/`, mostrando:

- incidentes Open;
- incidentes Critical ainda não resolvidos;
- incidentes Resolved.

Também deveria tratar:

- carregamento;
- erro de requisição;
- valores iguais a zero.

## Resultado

O dashboard foi implementado na rota `/`.

## Validação

Foi executado:

`npm run build`

O build passou sem erros.

Posteriormente, durante a validação integrada, o dashboard apresentou corretamente os dados do seed:

- Open: 1;
- Critical não resolvido: 1;
- Resolved: 1.

## Decisão

Prosseguir para os demais fluxos obrigatórios do frontend.

---

# 15. Implementação agrupada das telas restantes

## Ferramenta

Codex — acesso exclusivamente gratuito

## Objetivo

Implementar:

- lista + filtros;
- criação;
- detalhes;
- histórico;
- alteração de status.

## Contexto

A ferramenta de IA utilizada possui limites de uso no acesso gratuito.

Para reduzir o consumo de interações sem perder o controle do escopo, decidi agrupar funcionalidades relacionadas em uma única solicitação detalhada.

## Instrução

Solicitei ao Codex, em uma única tarefa, a implementação de:

### Lista

Rota:

`/incidents`

Com:

- título;
- severity;
- owner;
- status;
- filtro por status;
- filtro por severity;
- filtros combinados;
- limpeza de filtros;
- loading;
- erro;
- lista vazia.

### Criação

Rota:

`/incidents/new`

Campos:

- title;
- description;
- severity;
- owner.

Sem permitir seleção de status.

### Detalhes

Rota:

`/incidents/:id`

Com:

- dados completos do incidente;
- histórico;
- mudança de status;
- mensagens de erro retornadas pela API.

A regra de:

`Critical: Open → Resolved`

não deveria ser duplicada no frontend.

## Resultado

Foram implementadas as rotas:

- `/`;
- `/incidents`;
- `/incidents/new`;
- `/incidents/:id`.

Foram implementados:

- lista;
- filtros;
- criação;
- detalhes;
- histórico;
- alteração de status;
- tratamento de erros;
- navegação.

## Validação

Foi executado:

`npm run build`

Resultado:

**build concluído sem erros.**

A validação funcional foi deixada para a etapa integrada.

## Decisão

Executar frontend e backend simultaneamente e validar todos os fluxos no navegador.

---

# 16. Validação integrada da aplicação

## Ferramenta

ChatGPT Free para orientação da sequência de validação.

A validação da aplicação foi realizada manualmente por mim no navegador.

## Objetivo

Confirmar que frontend e backend funcionavam juntos e que os principais requisitos do desafio estavam realmente atendidos.

## Contexto

Backend e frontend já compilavam e possuíam testes próprios, mas ainda era necessário testar a aplicação integrada.

## Instrução

Foi definida uma sequência de validação contendo:

1. dashboard;
2. lista de incidentes;
3. filtros;
4. criação de incidente;
5. detalhes;
6. alteração de status;
7. tentativa inválida de `Critical: Open → Resolved`;
8. histórico;
9. atualização do dashboard;
10. persistência após reinicialização.

## Resultado

Todos os fluxos foram executados com sucesso.

Foram validados:

- dashboard;
- listagem;
- filtros separados;
- filtros combinados;
- criação;
- detalhes;
- alteração de status;
- bloqueio da transição inválida para incidentes Critical;
- mensagem de erro compreensível;
- histórico;
- atualização das métricas do dashboard;
- persistência dos dados após reinicialização.

## Validação

A validação foi realizada diretamente pela interface da aplicação com frontend Angular e backend Django executando simultaneamente.

## Decisão

Considerar os principais requisitos funcionais concluídos e seguir para documentação e revisão final.

---

# 17. Redesign visual do frontend

## Ferramentas

- Lovable — acesso exclusivamente gratuito;
- Codex — acesso exclusivamente gratuito;
- ChatGPT Free para elaboração e refinamento das instruções.

## Objetivo

Melhorar significativamente a qualidade visual do frontend sem alterar regras de negócio, contratos da API, rotas ou comportamento funcional já validado.

## Contexto

Após concluir os requisitos funcionais e realizar a validação integrada da aplicação, avaliei criticamente o resultado visual do frontend.

A aplicação estava funcionando corretamente, porém a primeira interface produzida pela IA era visualmente muito simples.

Os principais problemas percebidos foram:

- aparência próxima de HTML básico;
- pouca hierarquia visual;
- navegação pouco trabalhada;
- métricas com pouco destaque;
- tabela visualmente simples;
- severidade e status apresentados com pouca diferenciação;
- formulário sem acabamento visual;
- tela de detalhes com informações pouco organizadas;
- baixa sensação de produto final.

Como os principais requisitos já estavam funcionando e validados, decidi utilizar parte do tempo restante para melhorar a experiência visual sem comprometer a estabilidade da aplicação.

## Instrução — Lovable

Utilizei o Lovable como ferramenta de exploração e referência visual.

Foram fornecidas como referência as quatro páginas existentes:

1. Dashboard;
2. Incidentes;
3. Novo incidente;
4. Detalhes do incidente.

Solicitei que o Lovable preservasse os fluxos e informações já existentes e trabalhasse especificamente em:

- layout;
- hierarquia;
- tipografia;
- espaçamento;
- navegação;
- cards;
- tabela;
- badges;
- formulário;
- histórico;
- cores semânticas;
- responsividade;
- apresentação de status e severidade.

Também deixei explícito que não deveriam ser inventadas novas regras de negócio ou funcionalidades.

## Resultado — Lovable

O Lovable produziu uma proposta visual mais próxima de uma ferramenta SaaS operacional.

A proposta incluiu:

- sidebar lateral;
- header superior;
- navegação com destaque para rota ativa;
- cards de métricas;
- badges de severidade;
- badges de status;
- tabela de incidentes mais organizada;
- área de filtros estruturada;
- formulário dentro de card;
- reorganização da tela de detalhes;
- histórico com apresentação semelhante a uma timeline;
- melhor hierarquia tipográfica;
- identidade visual consistente entre as páginas.

O projeto produzido pelo Lovable não substituiu a aplicação Angular existente.

O Lovable foi utilizado como referência visual.

## Decisão

Decidi preservar integralmente a aplicação Angular já funcional e utilizar a proposta do Lovable apenas como especificação visual.

Essa decisão evitou substituir uma implementação já testada por uma nova codebase.

A próxima etapa foi transportar a direção visual para o frontend Angular existente através do Codex.

## Instrução — Codex

Forneci ao Codex uma especificação detalhada baseada nas telas produzidas pelo Lovable.

A instrução descrevia página por página:

- Dashboard;
- Lista de incidentes;
- Novo incidente;
- Detalhes do incidente.

Também foram especificados:

- sidebar;
- header;
- cards;
- badges;
- tabela;
- inputs;
- selects;
- botões;
- formulário;
- histórico;
- espaçamentos;
- tipografia;
- cores;
- responsividade.

O Codex recebeu restrições explícitas para NÃO alterar:

- backend;
- Django;
- endpoints;
- contratos da API;
- `IncidentService`;
- models/interfaces;
- regras de negócio;
- chamadas HTTP;
- rotas existentes;
- comportamento funcional.

A tarefa deveria permanecer concentrada na camada visual, principalmente HTML e SCSS.

## Resultado — Codex

O redesign produzido a partir da referência visual do Lovable foi aplicado ao frontend Angular existente.

A implementação funcional anterior foi preservada, enquanto a apresentação visual passou por uma segunda etapa de evolução.

Essa abordagem permitiu separar:

1. exploração e definição da direção visual;
2. implementação dessa direção dentro da codebase Angular já existente.

## Validação

Após o redesign, foi realizada nova validação da aplicação.

Foram verificados:

- build do Angular;
- abertura da aplicação;
- Dashboard;
- Lista de incidentes;
- filtros;
- formulário de criação;
- detalhes;
- alteração de status;
- histórico;
- navegação.

Também foi verificado que o redesign não havia alterado regras ou contratos funcionais.

## Decisão

Manter o redesign como parte da entrega final.

Essa etapa também alterou minha avaliação inicial sobre o frontend: a primeira versão visual era uma limitação importante, mas decidi reabrir essa decisão após concluir os requisitos obrigatórios e utilizar o tempo restante para melhorar a qualidade percebida do produto.

---

# 18. Revisão da estratégia de uso de IA após o redesign

## Ferramentas

- ChatGPT Free;
- Lovable — acesso exclusivamente gratuito;
- Codex — acesso exclusivamente gratuito.

## Objetivo

Avaliar como diferentes ferramentas poderiam ser utilizadas de maneira complementar sem perder o controle sobre a aplicação existente.

## Contexto

Durante o desenvolvimento, percebi que ferramentas diferentes apresentavam vantagens diferentes.

O Codex foi muito eficiente na implementação e alteração da codebase existente, mas a primeira solução visual ficou abaixo do que eu esperava.

O Lovable, por outro lado, foi utilizado especificamente para exploração visual.

## Resultado

A combinação das ferramentas mostrou-se mais eficiente do que esperar que uma única IA fosse igualmente boa em todas as etapas.

O fluxo utilizado foi:

1. aplicação funcional criada e testada;
2. avaliação crítica do design;
3. Lovable utilizado para produzir uma referência visual;
4. referência analisada;
5. especificação detalhada criada;
6. Codex utilizado para aplicar o redesign no Angular existente;
7. aplicação novamente validada.

## Decisão

Utilizar cada ferramenta para uma função mais adequada ao seu perfil, mantendo sempre a decisão e a validação final sob minha responsabilidade.

---

# Estratégia geral de interação com IA

Durante o desafio, procurei evitar solicitações excessivamente amplas.

A maior parte do desenvolvimento foi dividida em etapas como:

1. definição do objetivo;
2. fornecimento de contexto;
3. instrução delimitada;
4. geração ou alteração pela IA;
5. execução;
6. teste;
7. análise do resultado;
8. correção quando necessário;
9. validação;
10. próxima decisão.

As principais formas de validação utilizadas foram:

- `python manage.py check`;
- `python manage.py test`;
- migrations do Django;
- execução de management commands;
- `npm run build`;
- execução simultânea de frontend e backend;
- validação manual dos fluxos pelo navegador.

Quando ocorreu um problema real no ambiente Python, não realizei uma correção manual no código ou na configuração da aplicação. O erro completo foi fornecido à IA para análise e orientação.

Quando os limites do acesso gratuito do Codex começaram a se tornar uma restrição, decidi agrupar algumas tarefas relacionadas de frontend em uma única interação. O escopo dessa solicitação permaneceu explicitamente delimitado.

Após a validação funcional da aplicação, também utilizei ferramentas diferentes para responsabilidades diferentes.

O Lovable foi utilizado para exploração e definição de uma direção visual mais madura.

O Codex foi utilizado posteriormente para transportar essa referência visual para a aplicação Angular existente.

Essa separação foi deliberada: preferi utilizar uma ferramenta mais orientada à exploração visual para definir a direção de design, preservando o Codex como ferramenta responsável pelas alterações na codebase já funcional.

A aplicação existente não foi substituída pelo projeto produzido pelo Lovable.

Também percebi ao longo do desafio que o uso de IA exige supervisão contínua.

Em alguns momentos, instruções explícitas de formatação de código ou texto não foram obedecidas exatamente como solicitado.

Também houve uma sugestão inicial de stack que não considerava minha experiência prévia.

Esses episódios reforçaram a necessidade de:

- revisar decisões sugeridas;
- fornecer contexto suficiente;
- limitar claramente o escopo;
- rejeitar abordagens inadequadas;
- validar o resultado produzido;
- não assumir que uma resposta da IA está correta apenas porque parece tecnicamente plausível.

---

# Principais aprendizados sobre interação com IA

## 1. A IA precisa receber contexto antes de sugerir decisões arquiteturais

No início, foi sugerido Node.js como abordagem possível antes que minha experiência tecnológica fosse considerada.

Eu rejeitei essa direção e optei por Angular + Django.

Essa experiência reforçou que uma decisão tecnicamente válida pode ser inadequada ao contexto real do desenvolvedor.

## 2. Instruções claras reduzem erros, mas não eliminam necessidade de revisão

Em alguns momentos, instruções específicas de formatação não foram seguidas exatamente.

Isso exigiu revisão e repetição de instruções.

## 3. Uma ferramenta não necessariamente é a melhor para todas as etapas

O Codex foi muito eficiente em implementação.

O Lovable apresentou uma contribuição mais forte na exploração visual.

O ChatGPT foi utilizado principalmente para:

- planejamento;
- acompanhamento;
- decomposição;
- investigação;
- revisão;
- criação e refinamento de prompts.

## 4. Funcionalidade e aparência devem ser tratadas em momentos diferentes quando o prazo é limitado

A primeira prioridade foi entregar a aplicação funcionando.

Somente depois que:

- backend estava pronto;
- frontend estava funcional;
- integração estava validada;
- testes principais estavam passando;

decidi reabrir o design e investir em acabamento visual.

## 5. O desenvolvedor continua responsável pelo resultado

As IAs geraram código, configurações, sugestões e referências visuais.

As decisões sobre:

- stack;
- escopo;
- prioridade;
- aceitação ou rejeição de sugestões;
- validação;
- redesign;
- momento de avançar;

continuaram sendo minhas.

---

# Conformidade com as regras de uso de IA

Todas as ferramentas de Inteligência Artificial efetivamente utilizadas durante o hackathon foram utilizadas exclusivamente em modalidades gratuitas disponíveis ao público.

Foram utilizados:

- ChatGPT Free;
- Codex com acesso exclusivamente gratuito;
- Lovable com acesso exclusivamente gratuito.

Não foram utilizados durante o desafio:

- ChatGPT Plus;
- ChatGPT Pro;
- Claude Pro;
- Gemini Advanced;
- Codex utilizando capacidade proveniente de plano pago;
- créditos adicionais comprados para Codex;
- créditos pagos de API;
- contas corporativas com capacidade superior ao plano gratuito;
- assinaturas premium de ferramentas de IA;
- qualquer outro recurso pago destinado a aumentar capacidade, limites ou disponibilidade de IA.

Nenhum crédito adicional foi comprado para ampliar o uso das ferramentas durante o desafio.

O Lovable foi utilizado exclusivamente em sua modalidade gratuita e somente como ferramenta de exploração e referência visual.

Nenhum crédito pago ou plano premium do Lovable foi utilizado.

A utilização do Lovable foi registrada neste `AI_LOG.md` por ter influenciado de forma relevante a etapa de redesign do frontend.

Os limites disponíveis nas modalidades gratuitas foram tratados como uma restrição real do desenvolvimento e influenciaram decisões como o agrupamento de algumas tarefas relacionadas.

As conversas e interações relevantes utilizadas durante o desenvolvimento foram preservadas para eventual auditoria.